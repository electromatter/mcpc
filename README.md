basic syntax:
compound defines a new union type
emit defines a new exact type

built-in types: varint, varlong, int, ...

(compound <name> <fields>)
(enum <name> <basetype>
	<key> <value>...)

fields:
(field <names> <type>)
(match <type>
	(<case> <fields>)...)
(emit <name>)

