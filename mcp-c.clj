(ns mcp-c)

(load "mcp")

(def source (mcp/read-file (first *command-line-args*)))
(def schema (map #(cons (first %) (mcp/fold-schema (rest %))) source))

(println schema)

