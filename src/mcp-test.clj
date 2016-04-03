; mcp-test.clj
;
; Copyright (c) 2016 Eric Chai <electromatter@gmail.com>
; All rights reserved.
;
; This software may be modified and distributed under the terms
; of the ISC license. See the LICENSE file for details.

(ns mcp-test
	(:use clojure.pprint)
	(:require mcp))

(pprint (mcp/translate-file (first *command-line-args*)))

