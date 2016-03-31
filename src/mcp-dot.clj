; mcp-dot.clj
;
; Copyright (c) 2016 Eric Chai <electromatter@gmail.com>
; All rights reserved.
;
; This software may be modified and distributed under the terms
; of the ISC license. See the LICENSE file for details.

(ns mcp-dot
	(:require mcp))

; WARNING: does not support non-trivial types

;shapes: elipse (default), box, diamond, ...
;nodea [label="derp" shape=box];
;nodeb [label="face"];
;nodea->nodeb [label="0"];

; returns (nodes, links)
(defn build-graph
	[root]
	(println (root :order)))

(defn build-dot
	[root]
	(build-graph root))

(build-dot ((mcp/translate-file (first *command-line-args*)) 'status))

