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

; this sets up the state of the translator
(defmethod translate :initial
	[expr]
	(reduce translate {} expr))			; visit each expr

; the following take state and expr and return the new state

; creates a new composite type
(defmethod translate 'compose
	[state expr]
	(let [[_ typename & fields] expr]
	(assert (not (contains? state typename)))	; ensure distinct name
	(assert (not (state :cur)))			; ensure we are root
	(let [state (assoc state typename :cur)		; reserve the name and visit fields
		state (reduce translate
			(assoc state :cur {:name typename})
			fields)]
	(dissoc (assoc state
			:roots (cons typename (state :roots))
			typename (state :cur))		; name the type
		:cur :done :fields :order))))		; cleanup

(defn buildsize
	[state typename]
	(cond
	(= (type typename) (type 'symbol))
		(list state typename)
	(integer? typename)
		(list state typename)
	))

(defn buildtype
	[state typename]
	(if (= (type typename) (type 'symbol))
		(list state {:name typename})
		(let [[kw & args] typename]
		(cond
;		(= kw 'compose) TODO: non-trivial types
		(= kw 'array)
			(let [[size elem] args
				[state size] (buildsize state size)
				[state elem] (buildtype state elem)]
			(list state {:name kw :size-type size :elem-type elem}))
		(= kw 'bytes)
			(let [[size] args
				[state size] (buildsize state size)]
			(list state {:name kw :size-type size}))
		(= kw 'string)
			(let [[size] args
				[state size] (buildsize state size)]
			(list state {:name kw :size-type size}))
		:else
			(list state {:name kw :args args})))))

; adds a field to the current type
(defmethod translate 'field
	[state expr]
	(let [[_ & names] expr
		typename (last names)
		names (butlast names)
		[state typename] (buildtype state typename); construct type
		cur (state :cur)
		fields (interleave names (repeat typename)); build fields
		order (map #(do {:action :field :name % :type typename}) (take-nth 2 fields))
		fields (apply hash-map fields)]
		(assert cur)				; field without context?
		(assert (not (state :done)))		; field after terminal!
		(assert (disjoint? (state :fields) fields))
		(assoc state
			:cur (assoc cur
				:fields (merge (cur :fields) fields)
				:order (concat (cur :order) order))
			:fields (merge (state :fields) fields))))

; adds a literal to the type
(defmethod translate 'literal
	[state expr]
	(let [[_ & values] expr
		typename (last values)
		[state typename] (buildtype state typename)
		values (butlast values)
		cur (state :cur)
		literals (map #(do {:action :literal :value % :type typename}) values)]
		(assert cur)				; literal without context?
		(assert (not (state :done)))		; literal after end?
		(assoc state
			:cur (assoc cur
				:order (concat (cur :order) literals)))))

; builds a branch into the current type
(defmethod translate 'match
	[state expr]
	(let [[_ condition & branches] expr
		cur (state :cur)]
	(assert cur)					; make sure we are in a composite
	(assert (not (state :done)))			; match after terminal symbol!
	(assert (distinct? (map first branches)))	; ensure distinct branches
	(assoc state
		; append match
		:cur (assoc cur
			:order (concat (cur :order)	; add the condition marker and reduce branches
				`(~{:action :match :on condition}))
			:branches (apply sorted-map (interleave
				(map first branches)
				(map #(get (reduce translate (assoc state :cur {}) (rest %)) :cur) branches))))
		:done true)))

; names a new terminal type
(defmethod translate 'emit
	[state expr]
	(let [[_ newname] expr
		cur (state :cur)]
	(assert cur)					; make sure we are in a composite
	(assert (not (state :done)))			; emit after terminal!
	(assert (or
		(and (not newname) (cur :name))
		(and newname (not (cur :name)))))	; check if we need a name
	(assert (not (contains? state newname)))	; ensure distinct name
	(if newname
		(assoc state
			:cur (assoc cur
				:order (concat (cur :order)
					`(~{:action :emit :name newname})))
			newname {:name newname :fields (state :fields) :order (state :order)}
			:done true)
		(assoc state
			:cur (assoc cur
				:order (concat (cur :order)
					`(~{:action :emit :name (cur :name)})))
			:done true))))

