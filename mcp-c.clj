(ns mcp-c)

(load "mcp")

(def source (mcp/read-file (first *command-line-args*)))
(def schema (map #(cons (second %) (mcp/fold-schema (nthrest % 2))) source))

(println schema)

