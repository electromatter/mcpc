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

(defprotocol py-type
	; generates a field template
	(make-field [x])
	; generates definition
	(apply-class [x])
	; returns true if it is an integer type
	(integer-type? [x])
	(dependancies [x]))

(defprotocol py-field
	; generates code for parsing/generating
	(apply-parser [x])
	(apply-generator [x]))

;(def builtin-types {
;	'bool :int 'byte :int 'short :int 'int :int 'long :int
;	'varint :int 'varlong :int
;	'float :simple 'double :simple 'uuid :simple 'angle :simple
;	'position :simple 'slot :simple 'nbt :simple 'bytes_eof :simple
;	'string :str 'string_utf16 :str 'bytes :str
;	'array :array})

(def source (mcp/translate-file (first *command-line-args*)))
(def rootname (symbol (second *command-line-args*)))

; flatten dependency tree
(pprint (mcp/order source rootname))
; then build types in order

