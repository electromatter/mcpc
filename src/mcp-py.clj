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

;BASIC PROTOCOL
; check use
; generate class
; generate parser
; generate generator
; dependancies (including variants, including builtins, only first order)
; variants

(def inttype {:integer true
	:checkuse (fn [field] true)
	:makeclass (fn [field] (list))
	:makeparse (fn [field] (list))
	:makegen (fn [field] (list))
	:depends (list)
	:variants (list)
	})
(def simpletype {})
(def strtype {:string true})
(def arraytype {})

(def builtin-types {
	'bool inttype 'byte inttype 'short inttype 'int inttype 'long inttype
	'varint inttype 'varlong inttype
	'float simpletype 'double simpletype 'uuid simpletype 'angle simpletype
	'position simpletype 'slot simpletype 'nbt simpletype
	'bytes_eof simpletype
	'string strtype 'string_utf16 strtype 'bytes strtype
	'array arraytype})

(defn build-type
	[typedef]
	(merge typedef (cond
		; augment a builtin type
		(:builtin typedef) (do
			(assert (contains? builtin-types (:name typedef)))
			(get builtin-types (:name typedef)))
		; augment a union type
		(:union typedef) (do
			{:potato true})
		; augment a terminal type
		:else (do
			{:not-potato true}))))

; augment the source
(pprint (mcp/augment-file build-type (first *command-line-args*)))

; invoke the type checker
; invoke the code generators

