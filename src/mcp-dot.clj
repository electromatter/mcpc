; mcp-dot.clj
;
; Copyright (c) 2016 Eric Chai <electromatter@gmail.com>
; All rights reserved.
;
; This software may be modified and distributed under the terms
; of the ISC license. See the LICENSE file for details.

(ns mcp-dot
	(:require mcp))

;shapes: elipse (default), box, diamond, ...
;
;nodes:
;{:name "nodea" :links ({:target "name" :label "derp"}...) :label "derp" :shape "box"}

(defmulti build-graph
	(fn
		([root] :initial)
		([root order nextid] ((first order) :action))))

(defmethod build-graph :initial
	[root]
	(let [idatom (atom 0)]
		(build-graph root (root :order) (fn [] (swap! idatom inc)))))

(defn format-type [typespec]
	(cond
	(= (typespec :name) 'array) (str "array" (format-type :elem-type))
	:else (str (typespec :name))))

; link to next
(defmethod build-graph :literal
	[root actions nextid]
	(let [id (nextid)
		action (first actions)
		rest_nodes (build-graph root (rest actions) nextid)]
	(cons {:name (str "literal" id)
		:label (str "literal\\n" (format-type (action :type)) "\\n" (action :value))
		:links (list {:target ((first rest_nodes) :name)})} rest_nodes)))

; link to next
(defmethod build-graph :field
	[root actions nextid]
	(let [id (nextid)
		action (first actions)
		rest_nodes (build-graph root (rest actions) nextid)]
	(cons {:name (str "field" id)
		:label (str (format-type (action :type)) "\\n" (action :name))
		:links (list {:target ((first rest_nodes) :name)})} rest_nodes)))

; link to branches
(defmethod build-graph :match
	[root actions nextid]
	(let [id (nextid)
		action (first actions)
		branches (root :branches)
		branch_rest (map #(build-graph % (% :order) nextid) (vals branches))]
	(cons {:name (str "match" id)
		:label (str "match\\n" (action :on))
		:shape "diamond"
		:links (doall (map #(do {:target ((first %) :name)
					:label %2}) branch_rest (keys branches)))}
		(reduce concat branch_rest))))

(defmethod build-graph :emit
	[root actions nextid]
	(let [id (nextid)
		action (first actions)]
	(list {:name (str "emit" id)
		:shape "box"
		:label (str "emit\\n" (action :name))})))

(defn format-options
	[options]
	(if (seq options)
		(str " [" (reduce  #(str %1 " " %2)
			(map (fn [[key value]] (str (name key) "=\"" value "\"")) options))
			"]")
		""))

; format graph
(defn build-dot
	[graph-name root]
	(let [nodes (build-graph root)]
	(str "digraph " graph-name " {\n"
	(apply str (map
			#(str "\t" (% :name) (format-options (dissoc % :links :name)) ";\n")
		 nodes))
	"\n"
	(apply str (map (fn [node] (apply str (map (fn [link]
				(str "\t" (node :name) "->" (link :target) (format-options (dissoc link :target)) ";\n"))
			(node :links))))
		nodes))
	"}\n")))

(use 'clojure.pprint)

(def numargs (count *command-line-args*))

(if (>= numargs 1) (do
	(def filename (first *command-line-args*))
	(def source (mcp/translate-file filename))))

(if (>= numargs 2) (do
	(def rootname (symbol (second *command-line-args*)))))

(cond
	(= numargs 1) (do (println "roots:") (pprint (source :roots)))
	(= numargs 2) (println (build-dot (str rootname) (source rootname)))
	:else (println "usage: <source filename> <rootname>"))


