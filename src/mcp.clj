; mcp.clj
;
; Copyright (c) 2016 Eric Chai <electromatter@gmail.com>
; All rights reserved.
;
; This software may be modified and distributed under the terms
; of the ISC license. See the LICENSE file for details.

;TODO: sanitize names

(ns mcp)

(defn flatten-indent
        [& arg]
        (apply concat (map (fn [line]
                        (if (or (string? line) (not (seq? line)))
                                (list (str line))
                                (map #(str "\t" %) (apply flatten-indent (seq line)))))
                 arg)))

(def indent (comp (partial reduce #(str %1 "\n" %2)) flatten-indent))

(defn read-file [filename]
	(read-string (str \( (slurp filename) \))))

(defn newcounter
	[]
	(let [x (atom 0)]
		(fn
			([] (swap! x inc))
			([text] (str text (swap! x inc))))))

(defn disjoint?
	[& maps]
	(apply distinct? (mapcat keys maps)))

(defn sorted-map-invert
	[coll]
		(reduce (fn [c [k v]] (assoc c v k)) (sorted-map) coll))

; flattnes the depenancy tree and gives an arbitrary order
; to the sequence of definitions
(defn order
	([source & names] (-> (reduce (partial order source) {} names) sorted-map-invert vals))
	([source counter deps typename]
		(let [cont (partial order source counter)
			typedef (get source typename)
			deps (reduce cont deps (:depends typedef))
			deps (reduce cont deps (:variants typedef))]
			(if (contains? deps typename)
				deps
				(assoc deps typename (counter))))))

; augments the ast and flattens types
(defmulti translate
	(fn
		([expr] :initial)
		([state expr] (first expr))))

(def translate-file (comp translate read-file))

(defrecord State [cur done fields orders types counter])

(declare buildtype)

(defn buildarraytype
	([state typename elem]
		(let [[state elem] (buildtype state elem)]
		`(~state ~{:name 'array :elem elem})))
	([state typename size elem]
		(let [[state size] (if (integer? size) (list state size) (buildtype state size))
			[state elem] (buildtype state elem)]
		`(~state ~{:name 'array :size size :elem elem}))))

(defn buildstrtype
	([state typename]
		`(~state ~{:name typename}))
	([state typename size]
		(let [[state size] (if (integer? size) (list state size) (buildtype state size))]
		`(~state ~{:name 'array :size size}))))

(def basetypes {'array {:name 'array :builtin true :build buildarraytype}
		'string {:name 'string :builtin true :build buildstrtype}
		'string_utf16 {:name 'string_utf16 :builtin true :build buildstrtype}
		'bytes {:name 'bytes :builtin true :build buildstrtype}})

;;;;; ADD DEPS

; this sets up the state of the translator
(defmethod translate :initial
	[expr]	; translate each expression with a new state
	(:types (reduce translate (->State nil nil nil nil basetypes (newcounter)) expr)))

; Begin
(defmethod translate 'compose
	[state [_ cname & fields]]
	(assert (not (:cur state)))	; ensure we are in the correct state
	(assert (not (:done state)))
	(assert (not (contains? (:types state) cname)))
	(let [state (reduce translate (assoc state	; translate each field
				:cur {:name cname}	; reserve the name and create a stub
				:types (assoc (:types state) cname :cur))
			fields)]
		(assert (:done state))	; ensure we completed the composite
		(assoc state		; clean up the state
			:cur nil
			:done nil
			:fields nil
			:depends #{}
			:variants nil
			:orders nil)))

(defn buildtype
	[state typespec]
	(let [types (:types state)
		[typename & args] (if (= (type typespec) (type 'symbol))
					(list typespec)
					typespec)
		state (assoc state
			:depends (conj (get state :depends #{}) typename))]
		(if (contains? types typename)
			(let [typerec (get types typename)]
				(if (contains? typerec :build)
					(apply (:build typerec) (cons state (cons typename args)))
					(list state (if (seq args)
						{:name typename :args args}
						{:name typename}))))
			(buildtype (assoc state :types (assoc types typename
				{:name typename :builtin true})) typespec))))

; Body
(defmethod translate 'literal
	[state [_ & values]]
	(let [typespec (last values)
		values (butlast values)
		fields (reduce #(assoc %1 ((:counter state) "_literal") {:value %2}) nil values)
		state (translate state (concat '(field) (keys fields) `(~typespec)))]
		(assert (>= (count values) 1))
		(assoc state	; set the value of literals
			:fields (merge-with merge (:fields state) fields))))

(defmethod translate 'field
	[state [_ & names]]
	(let [typespec (last names)
		names (butlast names)
		[state typespec] (buildtype state typespec)
		orders (map #(do {:action :field :name %}) names)
		fields (reduce #(assoc %1 %2 {:name %2 :type typespec}) nil names)
		cur (:cur state)]
		(assert cur)		; ensure we are in the correct state
		(assert (not (:done state)))
		(assert (>= (count fields) 1))
		(assert (disjoint? (:fields state) fields) (str "ensure: unique field names" (keys (:fields state)) (keys fields)))
		(assoc state	; add orders for parsing the field
			:cur (assoc cur :orders (concat (:orders cur) orders))
			:orders (concat (:orders state) orders)
			:fields (merge (:fields state) fields))))

; Terminals
(defmethod translate 'match
	[state [_ field & branches]]
	(assert (:cur state))
	(assert not (:done state))
	(assert (>= (count branches) 1))
	(if (contains? (:fields state) field)
		(let [oldfields (:fields state)
			values (map first branches)
			[state branches] (reduce (fn [[state branches] [value & fields]]	; translate each branch
					(let [newstate (reduce translate (assoc state
							:cur {}	; enter a new context for the branch
							:fields (if (= value 'default)
								(assoc oldfields	; default match is not a constant value
									field (assoc (get oldfields field) :exclude (filter (partial not= 'default) values)))
								(assoc oldfields	; add value to field that was matched on
									field (assoc (get oldfields field) :value value))))
						fields)]
					(assert (:done newstate))
					(assert (not (contains? branches value)))
					`(~(merge state (select-keys newstate [:types :depends :variants]))
						~(assoc branches value (assoc (:cur newstate) :fields (:fields newstate))))))
				`(~state ~{}) branches)
			; this hack preserves order, this could be improved
			branches (apply array-map (interleave values (map (partial get branches) values)))
			cur (:cur state)
			orders `({:action :match :field ~field :branches ~branches})]
			(assert not (and (contains? branches 'default) (.startsWith field "_")))
			(assoc state	; we reached the end of the current type
				:cur (assoc cur :orders (concat (:orders cur) orders))
				:done true
				:variants (if (:name cur)
					#{}
					(:variants state))
				:types (if (:name cur)	; if we were a root, finalize type
					(assoc (:types state) (:name cur)
						{:name (:name cur)
						:depends (:depends state)
						:variants (:variants state)
						:fields (:fields state)
						:union true
						:orders (concat (:orders state) orders)})
					(:types state))))
		; matching on an anon field; create the anon field.
		(let [fieldname (symbol ((:counter state) "_match"))]
			(assert (every? #(not (= (first %) 'default)) branches))
			(translate (translate state (list 'field fieldname field))
				(cons 'match (cons fieldname branches))))))

(defmethod translate 'emit
	[state [_ newname]]
	(assert (:cur state))
	(assert not (:done state))
	(let [oldname (:name (:cur state))
		cname (or oldname newname)
		orders `({:action :emit :name ~cname})]
		(assert (not (and oldname newname)))
		(assoc state
			:cur (assoc (:cur state)
				:orders (concat (:orders (:cur state)) orders))
			:done true
			:variants
				(if (not= cname oldname)
					(conj (get state :variants #{}) cname)
					(:variants state))
			:types (assoc (:types state)
				cname {:name cname
					:depends (:depends state)
					:fields (:fields state)
					:orders (concat (:orders state) orders)}))))

