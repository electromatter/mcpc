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
;class Variant(Union):
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

(defmulti gentypecode
	[state]
	)

(defn gencode
	([source]
		(str "import mcp_base\n\n"
			(reduce #(str %1 "\n" %2) (map gencode source roots)))
	([source [_ root]]
		(gentypecode {:source source
			:name (root :name)
			:stack nil
			:branches (root :branches)
			:order (root :order)})))

(print (gencode (mcp/translate-file (first *command-line-args*))))

