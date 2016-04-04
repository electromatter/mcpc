; mcp.clj
;
; Copyright (c) 2016 Eric Chai <electromatter@gmail.com>
; All rights reserved.
;
; This software may be modified and distributed under the terms
; of the ISC license. See the LICENSE file for details.

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

; augments the ast and flattens types
(defmulti translate
	(fn
		([expr] :initial)
		([state expr] (first expr))))

(def translate-file (comp translate read-file))

(defn augment-file
	[with filename]
	(reduce #(assoc %1 (first %2) (with (second %2)))
		nil (translate-file filename)))

(defn newcounter
	[]
	(let [x (atom 0)]
		(fn [text] (str text (swap! x inc)))))

(defrecord State [cur done fields orders types counter])

(declare buildtype)

(defn buildarraytype
	([state elem]
		(let [[state elem] (buildtype state elem)]
		`(~state ~{:name 'array :elem elem})))
	([state size elem]
		(let [[state size] (if (integer? size) (list state size) (buildtype state size))
			[state elem] (buildtype state elem)]
		`(~state ~{:name 'array :size size :elem elem}))))

(def basetypes {'array {:name 'array :builtin true :build buildarraytype}})

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
			:orders nil)))

(defn buildtype
	[state typespec]
	(let [types (:types state)
		[typename & args] (if (= (type typespec) (type 'symbol))
					(list typespec)
					typespec)]
		(if (contains? types typename)
			(let [typerec (get types typename)]
				(if (contains? typerec :build)
					(apply (:build typerec) (cons state args))
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
		(assoc state	; set the value of literals
			:fields (merge-with merge (:fields state) fields))))

(defmethod translate 'field
	[state [_ & names]]
	(let [typespec (last names)
		names (butlast names)
		[state typespec] (buildtype state typespec)
		orders (map #(do {:action :field :field %}) names)
		fields (apply hash-map (interleave names (repeat typespec)))
		cur (:cur state)]
		(assert cur)		; ensure we are in the correct state
		(assert (not (:done state)))
		(assoc state	; add orders for parsing the field
			:cur (assoc cur :orders (concat (:orders cur) orders))
			:orders (concat (:orders state) orders)
			:fields (merge (:fields state) fields))))

; Terminals
(defmethod translate 'match
	[state [_ field & branches]]
	(assert (:cur state))
	(assert not (:done state))
	(if (contains? (:fields state) field)
		(let [oldfields (:fields state)
			[state branches] (reduce (fn [[state branches] [value & fields]]	; translate each branch
					(let [newstate (reduce translate (assoc state
							:cur {}	; enter a new context for the branch
							:fields (if (= value 'default)
								oldfields		; default match is not a constant value
								(assoc oldfields	; add value to field that was matched on
									field (assoc (get oldfields field) :value value))))
						fields)]
					(assert (:done newstate))
					(assert (not (contains? branches value)))
					`(~(assoc state :types (:types newstate))
						~(assoc branches value (:cur newstate)))))
				`(~state ~{}) branches)
			cur (:cur state)
			orders `({:action :match :field ~field :branches ~branches})]
			(assoc state	; we reached the end of the current type
				:cur (assoc cur :orders (concat (:orders cur) orders))
				:done true
				:types (if (:name cur)	; if we were a root, finalize type
					(assoc (:types state) (:name cur)
						{:name (:name cur)
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
			:types (assoc (:types state)
				cname {:name cname
					:fields (:fields state)
					:orders (concat (:orders state) orders)}))))

