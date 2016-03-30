(ns mcp-c)

(load "mcp")

;shapes: elipse (default), box, diamond, ...
;nodea [label="derp" shape=box];
;nodeb [label="face"];
;nodea->nodeb [label="0"];

(defn build-graph
	([machine] (let [x (atom 0)]
		(build-graph (rest machine) (fn [] (swap! x inc)))))
	([root nextid]
		(let [node (first root) cont (rest root)]
		(case (str (first node))
		"match" (let [typename (second node)
				label (str "match\\n" typename)
				node_name (str "match_" typename "_" (nextid))
				branches (nthrest node 2)
				branch_nodelinks (map #(build-graph (rest %) nextid) branches)
				next_nodes (map first branch_nodelinks)
				branch_nodes (reduce concat next_nodes)
				link_names (map #(str (first %)) branches)
				branch_links (map #(list node_name (first (first %1)) `{"label" ~%2}) next_nodes link_names)
				next_links (reduce concat (map last branch_nodelinks))]
			(list (cons (list node_name `{"label" ~label, "shape" "diamond"}) branch_nodes) (concat branch_links next_links)))
		"field"	(let [typename (last node)
				field_names (butlast (rest node))
				nodes (map #(list (str "field_" % "_" (nextid)) `{"label" ~(str typename "\\n" %)}) field_names)
				node_names (map first nodes)
				node_links (map list node_names (rest node_names) (repeat {}))
				next_nodelinks (build-graph cont nextid)
				next_nodes (first next_nodelinks)
				next_names (map first next_nodes)
				next_links (second next_nodelinks)]
			(list	(concat nodes next_nodes)
				(concat node_links `(~`(~(last node_names) ~(first next_names) {})) next_links)))
		"emit" (let [typename (second node)
				label (str "emit\\n" typename)
				node_name (str "emit_" typename "_" (nextid))]
			(list	`((~node_name {"label" ~label, "shape" "box"})) ()))))))

(defn format-attr [attr]
	(if (empty? attr)
		""
		(str " ["
			(reduce #(str %1 " " %2) (map #(str \" (first %) \"\=\" (second %) \") attr))
		"]")
	))

(defn format-graph [graph_name graph]
	(let [names (first graph) links (second graph)]
	(str "digraph " graph_name " {\n"
		(reduce #(str %1 "\t" (first %2) (format-attr (second %2)) ";\n") "" names) "\n"
		(reduce #(str %1 "\t" (first %2) "->" (second %2) (format-attr (nth %2 2)) ";\n") "" links)
	"}\n")))

(defn easy-graph [machine]
	(format-graph (first machine) (build-graph machine)))

(def source (mcp/read-file (first *command-line-args*)))
(def schema (map #(cons (first %) (mcp/fold-schema (rest %))) source))

(print (reduce str (map easy-graph source)))

