; mcp.clj
;
; Copyright (c) 2016 Eric Chai <electromatter@gmail.com>
; All rights reserved.
;
; This software may be modified and distributed under the terms
; of the ISC license. See the LICENSE file for details.

(ns mcp)

(require '[clojure.set])

;machines here are defined as trees of expressions
; match = branch
; field = output
; emit = leaf
;
; field is non-terminal
; match is terminal
; emit is terminal
;
; (match <type> <&matches>)
; (field <&names> <type>)
; (emit <name>)
;
; machines are:
; (<name> <root>)

(def integer_types
	#{"varint" "varlong" "bool" "byte" "short" "int" "long"})

(defn integer_type? [typename]
	(contains? integer_types (str typename)))

(def parameterized_types
	#{"array" "bytes"})

(declare valid_type?)

(defn valid_size? [size fields]
	(or (integer? size)
		(integer_type? size)
		(integer_type? (get (reduce concat fields) size))))

(def parameter_checkers {
	"array" (fn [fields size elmtype]
		(and	(valid_size? size fields)
			(valid_type? elmtype fields)))
	"bytes" (fn [fields size]
		(or (= (str size) "eof")
			(valid_size? fields size)))
	})

(def types (clojure.set/union integer_types parameterized_types
	#{"float" "double" "string" "slot" "position" "angle" "uuid"}))

(defn valid_type? [typename fields]
	(or (contains? types (str typename))
		(let [parameters (rest typename) typename (str (first typename))]
		(and (contains? parameterized_types typename)
			(apply (get parameter_checkers typename) (cons fields parameters))))))

(defn build-fields [arg]
	(let [names (butlast arg) typename (last arg)]
		(assert (seq names))
		(map #(list % typename) names)))

(defn fold-schema
	([root] (fold-schema root '()))
	([root fields]
		(let [node (first root) cont (rest root)]
		(case (str (first node))
		"match" (let [arg (second node) branches (nthrest node 2)]
			(assert (empty? cont) (seq branches))
			(assert (distinct? (map #(first %) branches)))
			(assert (integer_type? arg))
			(let [records (map #(fold-schema (rest %) fields) branches)]
				(assert (distinct? (map #(first %) records)))
				(reduce concat records)
			))
		"field" (do
			(assert (seq cont))
			(assert (valid_type? (last node) fields))
			(fold-schema cont (concat fields (build-fields (rest node)))))
		"emit" (let [name (second node)]
			(assert (= (count node) 2))
			(assert (distinct? (map #(first %) fields)))
			(list (cons name fields)))))))

(defn read-file [filename]
	(read-string (str \( (slurp filename) \))))

