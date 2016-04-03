; mcp.clj
;
; Copyright (c) 2016 Eric Chai <electromatter@gmail.com>
; All rights reserved.
;
; This software may be modified and distributed under the terms
; of the ISC license. See the LICENSE file for details.

(ns mcp)

(defn read-file [filename]
	(read-string (str \( (slurp filename) \))))

; returns true if a set of maps are disjoint i.e. have no keys in common
(defn disjoint?
	[& col]
	(distinct? (apply concat (map keys col))))

; augments the ast and flattens types
(defmulti translate
	(fn
		([expr] :initial)
		([state expr] (first expr))))

(def translate-file (comp translate read-file))

(defrecord State [cur done fields orders types])

; this sets up the state of the translator
(defmethod translate :initial
	[expr]	; translate each expression with a new state
	(:types (reduce translate {} expr)))

; Begin
(defmethod translate 'compose
	[state [_ cname & fields]]
	(assert (not (:cur state)))	; ensure we are in the correct state
	(assert (not (contains? (:types state) cname)))
	(let [state (reduce translate (assoc state	; translate each field
				:cur {:name cname}	; reserve the name and create a stub
				:types (assoc (:types state) cname :cur))
			fields)]
		(assert (not (:cur state)))	; ensure we hit and emit
		(assert (not (:fields state)))
		(assert (not (:orders state)))
		state))

(defn buildtype
	[state typespec]
	(list state {:name typespec}))

; Body
(defmethod translate 'literal
	[state [_ & values]]
	(let [typespec (last values)
		values (butlast values)
		[state typespec] (buildtype state typespec)
		orders (map #(do {:action :literal :value % :type typespec}) values)
		cur (:cur state)]
		(assert cur)
		(assoc state	; add orders for parsing the literal
			:cur (assoc cur :orders (concat (:orders cur) orders))
			:orders (concat (:orders state) orders))))

(defmethod translate 'field
	[state [_ & names]]
	(let [typespec (last names)
		names (butlast names)
		[state typespec] (buildtype state typespec)
		orders (map #(do {:action :field :name % :type typespec}) names)
		fields (apply hash-map (interleave names (repeat typespec)))
		cur (:cur state)]
		(assert cur)
		(assoc state	; add orders for parsing the field
			:cur (assoc cur :orders (concat (:orders cur) orders))
			:orders (concat (:orders state) orders)
			:fields (merge (:fields state) fields))))

(use 'clojure.pprint)

(defn build-branch
	[[state branches] [value & expr] field]
	(let [fields (:fields :state)
		newstate (reduce translate (assoc state
				:cur {}	; enter branch and add value to field
				:fields (assoc fields field (assoc (get fields field) :value value)))
			expr)]
		(println (:final newstate))
	)
	; take defined types
	; assoc branch
	(list state branches))

; Terminals
(defmethod translate 'match
	[state [_ field & branches]]
	(assert (:cur state))
	(if (contains? (:fields state) field)
		(let [cur (:cur state)	; build branches
			[state branches] (reduce #(build-branch %1 %2 field) (list state nil) branches)
			orders `({:action :match :field ~field :branches ~branches})
			final (assoc cur :orders (concat (:orders cur) orders))]
		(println cur)
			(assoc state	; terminate cur
				:cur nil
				:fields nil
				:orders nil
				:final final
				:types (if (:name cur)	; if it was a root, we need to update the type
						(assoc (:types state) (:name cur) final)
						(:types state))))
		; matching on an anon field; create the anon field.
		(let [fieldname (symbol ((:newname state) "_match"))]
			(translate (translate state (list 'field fieldname field))
				(cons 'match (cons fieldname branches))))))

(defmethod translate 'emit
	[state [_ newname]]
	(let [oldname (:name (:cur state))
		cname (or newname oldname)
		cur (:cur state)
		orders `({:action :emit :name ~cname})]
		(assert (not (and newname oldname)))
		(assert cname)	; check name is valid and that we are in a valid state
		(assert (= (get (:types state) cname :cur) :cur))
		(assert cur)
		(assoc state	; clean up state and emit a type
			:cur nil
			:fields nil
			:orders nil
			:final (assoc cur :orders (concat (:orders cur) orders))
			:types (assoc (:types state)
				cname {
					:name cname
					:fields (:fields state)
					:orders (concat (:orders state) orders)}))))

