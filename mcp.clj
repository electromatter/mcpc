(ns mcp)

;machines here are defined as trees of expressions
; match = branch
; field = output
; emit = leaf
;
; field is non-terminal
; match is terminal
; emit is terminal
;
; (match <type> <&matches>)
; (field <&names> <type>)
; (emit <name>)
;
; machines are:
; (<name> <root>)

(defn read-file [filename]
	(read-string (str \( (slurp filename) \))))

(defn build-fields [arg]
	(let [names (butlast arg) typename (last arg)]
		(assert (not-empty names))
		(map #(list % typename) names)))

(defn fold-schema
	([root] (fold-schema root '()))
	([root fields]
		(let [node (first root) cont (rest root)]
		(case (str (first node))
		"match" (let [arg (second node) branches (nthrest node 2)]
			(assert (empty? cont) (not-empty branches))
			(assert (distinct? (map #(first %) branches)))
			(let [records (map #(fold-schema (rest %) fields) branches)]
				(assert (distinct? (map #(first %) records)))
				(reduce concat records)
			))
		"field" (let []
			(assert (not-empty cont))
			(fold-schema cont (concat fields (build-fields (rest node)))))
		"emit" (let [name (second node)]
			(assert (= (count node) 2))
			(assert (distinct? (map #(first %) fields)))
			(list (cons name fields)))))))

; (println (map #(cons (first %) (fold-schema (rest %))) (read-file "server.mc107")))

