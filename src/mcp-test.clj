(ns mcp-test
	(:use clojure.pprint)
	(:require mcp))

(pprint (mcp/translate-file (first *command-line-args*)))

