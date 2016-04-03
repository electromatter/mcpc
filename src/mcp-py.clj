; mcp-py.clj
;
; Copyright (c) 2016 Eric Chai <electromatter@gmail.com>
; All rights reserved.
;
; This software may be modified and distributed under the terms
; of the ISC license. See the LICENSE file for details.

(ns mcp-py
	(:use clojure.pprint)
	(:require mcp))

(def types #{'bool 'byte 'short 'int 'long 'varint 'varlong
		'float 'double 'uuid 'angle 'position
		'string 'string_utf16 'bytes 'bytes_eof
		'array 'slot 'nbt})

;### TEMPLATE ###
;class Variant(object):
;	#might also return a different variant
;	@classmethod
;	def decode(cls, ptr):	#throws SomeError
;		return cls(<fields>)
;
;	def __init__(self, fields...):
;		self.field = field
;
;	def encode(self):	#throws SomeError
;		return bytes(<some bytes>)
;### END TEMPLATE ###

(defn check-builtins
	[source]
	(let [builtins (filter #(:builtin (second %)) source)]
		(every? #(contains? types (first %)) builtins)))

(defn flatten-indent
	[& arg]
	(apply concat (map (fn [line]
			(if (or (string? line) (not (seq? line)))
				(list (str line))
				(map #(str "\t" %) (apply flatten-indent (seq line)))))
		 arg)))

(def indent (comp (partial reduce #(str %1 "\n" %2)) flatten-indent))

(defmulti gendecode
	(fn
		([source] :initial)
		([source expr] (:action expr))))

(defmethod gendecode :initial
	[source]
	(list "@staticmethod"
		"def decode(_ptr):"
		(apply concat (map (partial gendecode source) (:orders source)))
		""))

(defmethod gendecode :field
	[source expr]
	(let [fieldname (:name expr)
		field (get (:fields source) fieldname)
		postexpr (if (:value field) (list (str "if " fieldname " != " (:value field) ":") (list "raise _mcp.NoMatchError()")) ())]
		(concat (list (str (:name expr) " = _mcp." (:name (:type expr)) ".decode(_ptr)"))
			postexpr)))
(defmethod gendecode :literal
	[source expr]
	(list
		(str "_literal = _mcp." (:name (:type expr)) ".decode(_ptr)")
		(str "if _literal != " (:value expr) ":")
		(list "raise _mcp.NoMatchError()")))
(defmethod gendecode :match
	[source expr]
	(list "match"))
(defmethod gendecode :emit
	[source expr]
	(list "return"))

(defn geninit
	[source]
	(if (:union source)
		(list)
		(let [names (map :name (filter #(= (:action %) :field) (:orders source)))
			names (filter #(not (contains? (get (:fields source) %) :value)) names)]
		(list (str "def __init__(" (reduce #(str %1 ", " %2) "_self" names) "):")
			(map #(str "_self." % " = " %) names)
			(list "return")
			""))))

(defmulti genencode
	(fn
		([source] :initial)
		([source expr] (:action expr))))

(defmethod genencode :initial
	[source]
	(if (:union source)
		(list)
		(list "def encode(_self):"
			(list "_raw = bytes()")
			(map (partial genencode source) (:orders source))
			"")))

(defmethod genencode :field
	[source expr]
		(let [typename (:name (:type expr))
			fieldname (:name expr)
			value (if (contains? (get (:fields source) fieldname) :value)
				(:value (get (:fields source) fieldname))
				(str "_self." fieldname))]
			(str "_raw += _mcp." typename ".encode(" value ")")))

(defmethod genencode :literal
	[source expr]
		(str "_raw += _mcp." (:name (:type expr)) ".encode(" (:value expr) ")"))

(defmethod genencode :emit
	[source expr]
		"return _raw")

(defn genclass
	[source]
	(list (str "class " (:name source) "(_mcp._Base):")
		(gendecode source)
		(geninit source)
		(genencode source)))

(defn gencode
	[source]	; for each non builtin, gen class
	(apply indent (apply concat (list "import mcp_base as _mcp" "") (map #(genclass (second %)) (filter #(not (:builtin (second %))) source)))))

(def source (mcp/translate-file (first *command-line-args*)))

; verify that we support the builtin types
(assert (check-builtins source))

; TODO: validate expressions -> simple typechecking
(println (gencode source))

