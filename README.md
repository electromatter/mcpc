# MCP Compiler
A language to concisely represent regular network
protocols. This language can be thought of as a 
specification of an automata that translates input
stream into a sequence of typed values. This work was
motivated by the need to interface with Minecraft.

**NOTE: this is currently a work-in-progress.**

## License and Acknowledgements
I would like to thank [Mojang][2] and Notch for making
such an interesting game.

I would also like to thank the [Minecraft Coalition][3]
for providing the documentation making this project possible.

The compiler itself is licensed under the ISC license, see
the LICENSE file for more details.

## Built-in types

| Integer | Non-integer | Parameterized | Non-trivial |
|---------|-------------|---------------|-------------|
| bool    | float       | string        | slot        |
| byte    | double      | string_utf16  | nbt_tag     |
| int     | uuid        | bytes         | bytes_eof   |
| long    | angle       | array         |             |
| varint  | position    |               |             |
| varlong |             |               |             |

`bytes_eof` is like bytes, but takes all input up to
the `EOF`.

### Parameterized Types

#### string
```
(string <size>)
```
A UTF-8 encoded string.

`<size>` - the size of the string in bytes.
May be a constant, a reference to a previously
read field, or an anonomous field (see match)
that prefixes the string.

#### string_utf16
```
(string_utf16 <size>)
```
A UTF-16 encoded string.

`<size>` - the number of UTF-16 characters in the string.

See string's parameterization.

#### bytes
```
(bytes <size>)
```
A raw byte array.

`<size>` - the size of the payload in bytes.

See string's parameterization.

#### array
```
(array <size> <type>)
```
`<size>` - See string's parameterization.

`<type>` - The type of all the elements in the array, see type below for more information

## Grammar
Below is a modified [Backus-Naur][1] form grammar of the 
language. This language is represented in lisp S-expressions.
The lower level details syntax is defined to be the same
as clojure.

#### compose
```
( compose <name> <body> )
```
A composite type is a named type composed of zero or more
fields.

#### field
```
( field <names>... <type> )
```
The field command causes the generated automata to
consume some data to construct a value of the specified
type. Multiple definitions of fields of the same type
may be combined into one for brevity. The fields are read
from the datastream in order of definition.

#### match
```
( match <name> <branch>... )
       OR
( match <type> <branch>... )
```
The match rule is used to create union types.
If the first form is matched, the value of the previously
defined named field is used to find a branch to follow.
The second form creates an unnamed field to match on.
The first form takes precedence in conflict.
If no branch is matched, the generated automata raises 
an error condition.
There can be a maximum of one default branch.
See the definition of branch for more details.

#### literal
```
( literal <value>... <type> )
```
This is an alias for a match with a single branch that 
matches value.

Value may be a list of literal values to match.

None of the literals are represented in the output of
the generated automata.

#### emit
```
( emit <name> )
   OR
( emit )
```
The emit rule specifies a variant of the composite type. 
It terminates the definition of the body of a composite
type. And when reached by the generated automata, it
emits a value of the type named by this rule.

The second form is only valid in the context of a
composite type that has no brances and therefore no 
variants. It is an alias for writing emit to specify a
variant of the same name as the composite type.

#### body
```
<field or literal>... <emit OR match>
```
The body of a composite type is composed of zero or more
fields and is terminated by exactly one of either an
emit rule or a match rule.

#### branch
```
( <value> <body> )
      OR
(default <body> )
```
A branch is a variant of a composite type. Composite 
types are always terminated by emit.

The rule for value is dependant on the type being 
matched.
For integer types, it is an integer value.
For strings, it is a string value.
etc.

#### type
```
<name>
  OR
( <name> <parameters>... )
  OR
<compose>
```
The type rule specifies the type of a field to be read
from the input stream.
The name above referes to a built-in named type or a
previously defined type in the translation unit.

The second rule is used to create arrays and specify
parameterized types.

The third rule allows the definition of arrays of
composite types.

[1]: http://en.wikipedia.org/wiki/Backus-Naur_Form
[2]: http://mojang.com
[3]: http://wiki.vg/

