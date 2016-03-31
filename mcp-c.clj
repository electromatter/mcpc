; mcp-c.clj
;
; Copyright (c) 2016 Eric Chai <electromatter@gmail.com>
; All rights reserved.
;
; This software may be modified and distributed under the terms
; of the ISC license. See the LICENSE file for details.

(ns mcp-c)

(load "mcp")

(def source (mcp/read-file (first *command-line-args*)))
(def schema (map #(cons (second %) (mcp/fold-schema (nthrest % 2))) source))

(println schema)

