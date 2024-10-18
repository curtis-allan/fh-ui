# Exploring Client-Side scripting options for Hypermedia driven systems

Specifically, exploring the use case of
popular scripting frameworks within FastHTML, HTMX

## References

* [https://htmx.org/essays/hypermedia-friendly-scripting/]
* [https://hypermedia.systems/book/contents/]

### Objective

The primary objective of this investigation is to explore the
relevance and potential integration of scripting frameworks/
languages within the FastHTML/ HTMX ecosystem. As a rule, the
scripting libraries must adhere to a set of pre-defined constraints
to be considered as viable options:

* They **must** compliment the pre-existing stack

* They should **not** introduce complexities (follow progressive enhancement principles)

* They **must** be able to respect HATEOAS
(small client state is fine, but use of fetch() and data
rendering should not be an integral feature):

* Should be minimal by default

* No build steps

* Small package size

* No substantial load times

Brainstorming:

* Primary reason for wanting to use react - largest ecosystem
most likely.

* Exploring these options so far:

Apline.js
React
Preact
Vue
Petite-vue
Web Components (Lit, Fast, Spectrum, UIKit)
Solidjs
Sveltekit
Signals API in vanilla JS

* Pushing the boundaries/ adding to/ optimizing the current
stack (htmx + surreal)
