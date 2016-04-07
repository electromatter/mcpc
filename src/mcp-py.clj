; mcp-py.clj
;
; Copyright (c) 2016 Eric Chai <electromatter@gmail.com>
; All rights reserved.
;
; This software may be modified and distributed under the terms
; of the ISC license. See the LICENSE file for details.

;TODO: rewrite in better style (with macros and formatters)
;TODO: better value escaping
;TODO: nested arrays
;TODO: optimize: group fixed size fields together and use struct

(ns mcp-py
	(:use clojure.pprint)
	(:require mcp))

(def builtin-types {
	'bool :int 'byte :int 'short :int 'int :int 'long :int
	'varint :int 'varlong :int
	'float :simple 'double :simple 'uuid :simple 'angle :simple
	'position :simple 'slot :simple 'nbt :simple 'bytes_eof :simple
	'string :str 'string_utf16 :str 'bytes :str
	'array :array})

(def not-contains? (comp not contains?))

(defn non-const-fields
	[{orders :orders fields :fields}]
	(filter identity (map (fn [{action :action field :name}]
		(if (and (= action :field) (not-contains? (get fields field) :value))
			field)) orders)))

(declare gen-value)

(defn gen-init-field
	[source field]
	(if (.startsWith (str (:name field)) "_")
		nil
		(list
			(if (:value field)
				(str "_self.c_" (:name field) " = " (gen-value source field (:value field)))
				(str"_self." (:name field) " = " (:name field))))))

(defn gen-init
	[source typedef]
	(let [fields (non-const-fields typedef)]
	(list (str "def __init__(" (reduce #(str %1 ", " %2) "_self" fields) "):")
		(mapcat (fn [order] (cond
			(= (:action order) :field) (gen-init-field source (get (:fields typedef) (:name order)))
			(= (:action order) :emit) (list "return")
			:else (assert false (str "unknown action: " (:action order)))))
			(:orders typedef)))))

(defmulti gen-value (fn [source field value] (get builtin-types (-> field :type :name))))
(defmulti gen-encode-field (fn [source field] (get builtin-types (-> field :type :name))))
(defmulti gen-decode-field (fn [source field] (get builtin-types (-> field :type :name))))
(defmulti gen-encode-elem (fn [source elem] (get builtin-types (:name elem))))
(defmulti gen-decode-elem (fn [source elem] (get builtin-types (:name elem))))

;generate constant values
(defmethod gen-value :int
	[source field value]
	(assert (integer? value) (str (:name field) " of integer type must have integer value"))
	(str value))

(defmethod gen-value :str
	[source field value]
	(assert (string? value) (str (:name field) " of string type must have string value"))
	(str "\"" value "\""));FIXME ESCAPE STRING!!!!

(defmethod gen-value :default
	[source field value]
	(assert false (str (-> field :type :name) " cannot have a primitive value")))

(defn gen-value-vec
	[source field values]
	(str "[" (apply str (interpose "," (map (partial gen-value source field) values))) "]"))

(defn gen-size
	[template size]
	(if (not size)
		(template 'varint);default size type
		(if (integer? size)
			size;constant size
			(do
				(assert (= (get builtin-types (:name size)) :int) "size must be integer type")
				(template (:name size))))));integer type

;generate encode
(defmethod gen-encode-field :simple
	[source field]
	(assert (not (or (:value field) (:exclude field))) (str (-> field :type :name) " must be primitive"))
	(list (str "_raw += _mcp.encode_" (-> field :type :name) "(_self." (:name field) ")")))

(defmethod gen-encode-field :int
	[source field]
	(if (:value field)
		(list (str "_raw += _mcp.encode_" (-> field :type :name) "(" (gen-value source field (:value field)) ")"))
		(concat
			(if (:exclude field)
				(list (str "if " (:name field) " in " (gen-value-vec source field (:exclude field)) ":")
					(list "raise _mcp.NoMatchError()")))
			(list (str "_raw += _mcp.encode_" (-> field :type :name) "(_self." (:name field) ")")))))

(defmethod gen-encode-field :str
	[source field]
	(let [size (gen-size #(str "_mcp.encode_" %) (-> field :type :size))]
	(if (:value field)
		(list (str "_raw += _mcp.encode_" (-> field :type :name) "(" (gen-value source field (:value field)) ", " size ")"))
		(concat
			(if (:exclude field)
				(list (str "if _self." (:name field) " in " (gen-value-vec source field (:exclude field)) ":")
					(list "raise _mcp.NoMatchError()")))
			(list (str "_raw += _mcp.encode_" (-> field :type :name) "(_self." (:name field) ", " size ")"))))))

(defmethod gen-encode-field :array
	[source field]
	(assert (not (or (:value field) (:exclude field))) (str (-> field :type :name) " must be primitive"))
	(let [size (gen-size #(str "_mcp.encode_" %) (-> field :type :size))
		elem (gen-encode-elem source (-> field :type :elem))]
	(list (str "_raw += _mcp.encode_array(_self." (:name field) ", " size ", " elem ")"))))

;encode an element
(defmethod gen-encode-elem :int
	[source elem]
	(str "_mcp.encode_" (:name elem)))

(defmethod gen-encode-elem :simple
	[source elem]
	(str "_mcp.encode_" (:name elem)))

(defmethod gen-encode-elem :str
	[source elem]
	(let [size (gen-size #(str "_mcp.encode_" %) (:size elem))]
	(str "(lambda _val: _mcp.encode_" (:name elem) "(_val, " size "))")))

(defmethod gen-encode-elem :array
	[source elem]
	(assert false "nested arrays unsupported"))

(defmethod gen-encode-elem :default
	[source elem]
	(str "(lambda _val: _val.encode())"))

(defmethod gen-encode-field :default
	[source field]
	(assert (not (or (:value field) (:exclude field))) (str (-> field :type :name) " must be primitive"))
	(list (str "_raw += _self." (:name field) ".encode()")))

;generate decode
(defmethod gen-decode-field :simple
	[source field]
	(assert (not (or (:value field) (:exclude field))) (str (-> field :type :name) " must be primitive"))
	(list (str (:name field) ", _off = _mcp.decode_" (-> field :type :name) "(_raw, _off)")))

(defmethod gen-decode-field :int
	[source field]
	(concat
		(list (str (:name field) ", _off = _mcp.decode_" (-> field :type :name) "(_raw, _off)"))
		(if (:value field)
			(list (str "if " (:name field) " != " (gen-value source field (:value field)) ":")
				(list "raise _mcp.NoMatchError()"))
		(if (:exclude field)
			(list (str "if " (:name field) " in " (gen-value-vec source field (:exclude field)) ":")
				(list "raise _mcp.NoMatchError()"))))))

(defmethod gen-decode-field :str
	[source field]
	(let [size (gen-size #(str "_mcp.decode_" %) (-> field :type :size))]
	(concat
		(list (str (:name field) ", _off = _mcp.decode_" (-> field :type :name) "(_raw, _off, " size ")"))
		(if (:value field)
			(list (str "if " (:name field) " != " (gen-value source field (:value field)) ":")
				(list "raise _mcp.NoMatchError()")))
		(if (:exclude field)
			(list (str "if " (:name field) " in " (gen-value-vec source field (:exclude field)) ":")
				(list "raise _mcp.NoMatchError()"))))))

(defmethod gen-decode-field :array
	[source field]
	(assert (not (or (:value field) (:exclude field))) (str (-> field :type :name) " must be primitive"))
	(let [size (gen-size #(str "_mcp.decode_" %) (-> field :type :size))
		elem (gen-decode-elem source (-> field :type :elem))]
	(list (str (:name field) ", _off = _mcp.decode_array(_raw, _off, " size ", " elem ")"))))

;decode an element
(defmethod gen-decode-elem :int
	[source elem]
	(str "_mcp.decode_" (:name elem)))

(defmethod gen-decode-elem :simple
	[source elem]
	(str "_mcp.decode_" (:name elem)))

(defmethod gen-decode-elem :str
	[source elem]
	(let [size (gen-size #(str "_mcp.decode_" %) (:size elem))]
	(str "(lambda _raw, _off: _mcp.decode_" (:name elem) "(_raw, _off, " size "))")))

(defmethod gen-decode-elem :array
	[source elem]
	(assert false "nested arrays unsupported"))

(defmethod gen-decode-elem :default
	[source elem]
	(str (:name elem) ".decode"))

(defmethod gen-decode-field :default
	[source field]
	(assert (not (or (:value field) (:exclude field))) (str (-> field :type :name) " must be primitive"))
	(list (str (:name field) ", _off = " (-> field :type :name) ".decode(_raw, _off)")))

(defn gen-encode
	[source typedef]
	(list "def encode(_self):"
		(list "_raw = bytes()")
		(mapcat (fn [order] (cond
			(= (:action order) :field) (gen-encode-field source (get (:fields typedef) (:name order)))
			(= (:action order) :emit) (list "return _raw")
			:else (assert false (str "unknown action: " (:action order)))))
			(:orders typedef))))

(declare gen-decode-branch)

(defn gen-decode-match
	[source typedef match]
	(let [branches (dissoc (:branches match) 'default)
		default (-> match :branches (get 'default))
		field (get (:fields typedef) (:field match))]
	(assert (> (count branches) 0) "match with no branches?")
	(concat
		(list "if false:"	;so we can just use elif
			(list "pass"))
		(mapcat (fn [[value branch]]
			(list (str"elif " (:name field) " == " (gen-value source field value) ":")
				(gen-decode-branch source branch (:orders branch))))
		branches)
		(list "else:"
			(if default
				(gen-decode-branch source default (:orders default))
				(list "raise _mcp.NoMatchError()"))))))

(defn gen-decode-branch
	[source typedef branch]
	(let [fields (non-const-fields typedef)]
	(mapcat (fn [order] (cond
		(= (:action order) :field) (gen-decode-field source (get (:fields typedef) (:name order)))
		(= (:action order) :match) (gen-decode-match source typedef order)
		(= (:action order) :emit) (list (str "return " (:name order) "(" (reduce #(apply str (interpose ", " %&)) fields) ")"))
		:else (assert false (str "unknown action: " (:action order)))))
		branch)))

(defn gen-decode
	[source typedef]
	(list	"@staticmethod"
		"def decode(_raw, _off=0):"
		(gen-decode-branch source typedef (:orders typedef))))

(defn gen-code
	[source typename]
	(let [typedef (get source typename)]
	(assert typedef)
	(cond
	(:builtin typedef) (do
		(assert (contains? builtin-types typename))
		(list))
	(:union typedef) (do
		(list
			(str "class " typename "(_mcp.Base):")
			(gen-decode source typedef)
			""))
	:else (do
		(list
			(str "class " typename "(_mcp.Base):")
			(gen-init source typedef)
			(gen-encode source typedef)
			(gen-decode source typedef)
			"")))))

(assert (> (count *command-line-args*) 1) "usage: <source filename> <roots>...")

(def source (mcp/translate-file (first *command-line-args*)))
(def orders (apply mcp/order source (map symbol (rest *command-line-args*))))

; build source
(println "import mcp_base as _mcp")
(println)
(println (apply mcp/indent (mapcat (partial gen-code source) orders)))

