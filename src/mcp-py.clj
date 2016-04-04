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

;(def types {
;	'bool inttype
;	'byte inttype
;	'short inttype
;	'int inttype
;	'long inttype
;	'varint inttype
;	'varlong inttype
;	'float simpletype
;	'double simpletype
;	'uuid simpletype
;	'angle simpletype
;	'position simpletype
;	'slot simpletype
;	'nbt simpletype
;	'string strtype
;	'string_utf16 strtype
;	'bytes strtype
;	'bytes_eof eoftype
;	'array arraytype})

(def source (mcp/translate-file (first *command-line-args*)))

(def source nil)

; 1) augment types with generators
; 2) use augmented types to generate code

