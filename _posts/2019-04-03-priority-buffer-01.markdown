---
layout: post
title:  "Sub-Graph Priority Buffer 01"
date:   2019-04-03 06:06:58 -0700
categories: hybrid_iterator
---
{%- include mathjax.html -%}


{% capture root_post %}{%- post_url 2019-04-03-priority-buffer-00 -%}{% endcapture %}
[root-post]: {{ root_post | relative_url }}


> This set of posts was inspired by [Smart enumeration of a subset of graphs obtained from a parent graph](https://math.stackexchange.com/questions/2389734/smart-enumeration-of-a-subset-of-graphs-obtained-from-a-parent-graph) question.
>
> If this is your first time it might be useful to review the [first post][root-post] of this series.


___


## `Priority_Buffer` Q&A


This section's for answers to questions regarding _"What the heck does method $\text{`foo`}$ do?"_, skip it if you're already Python proficient enough to be mid-way through writing an answer better than above.
Otherwise feel free to leave questions in the comments section if there's something that I've not covered above or bellow; I might just expound with the explanations.


___


>> ### The business with `counter` and `c_max` was not clear. could you explain more?


TLDR: _Usually_ Python'll error out, it's nicer than some languages that way, but not before those within ear-shot have new _vocab words_ for search queries. Both `if` statements and `while` loops are concerned with [truthiness](https://stackoverflow.com/questions/39983695/what-is-truthy-and-falsy-in-python-how-is-it-different-from-true-and-false), eg. they ask _"does $x$ = $y$?"_ (`1 == 0` `->` `False`) sorts of questions, _almost like_ a `decision tree`, so asking this `class` to check `LE_bound` while decrementing ($\neg{n}$) would cause some things to return `True` (that there's still data to read) but `False` that there's anything lower or equal to `n` after the first pass of it decrementing... and all passes after until _termination_.


Imagine if `Priority_Buffer`s `priority['GE_bound']` and `step['GE_min']` where instead set with `priority['GE_bound']` and `step['LE_max']`, __and/or__ `step['amount']` where set to `2`. I'll cover one _bad day_ example because mixing `LE_` and `GE_` without their complementary configurations _should_ result in a `ValueError` around line `54`.


While _tracing_ that last option, `step['amount']` increasing by two instead of decreasing, let's also say that after `Chunk 0 of ~ 4` there's no more `Graph_`s with a priority greater or equal to seven ($\text{firstToCompute}\not\ge7$ ). Everything else is the same, as above only `step['amount'] = 2` instead of `-2`...


```
Chunk 0 of ~ 4
         Graph_18 -> {'points': {}, 'first_to_compute': 5}
         Graph_13 -> {'points': {}, 'first_to_compute': 7}
         Graph_5 -> {'points': {}, 'first_to_compute': 8}
         Graph_8 -> {'points': {}, 'first_to_compute': 9}
         Graph_9 -> {'points': {}, 'first_to_compute': 6}
```


... something __very wrong__ will be going on next because the `Priority_Buffer` is currently a bit too _dumb_ not to do _bad things_, it'll get to the point of...


```python
class Priority_Buffer(Hybrid_Iterator):
    # ...
    def next(self):
        # ... `is_buffered` returns `False`
        #     and `while` plus `not` reversed
        #     that so it `try`s to...
        while not self.is_buffered:
            try:
                # ... it will _try_ but fail to
                #     get something like...
                #     {'Graph_<n>': {points: {}, 'first_to_compute': <p>}}
                next_sub_graph = priority_gen.next()
```


... but `priority_gen = self.top_priority()` so calling `next()` (side note that's what `yeild` _unlocks_ on that method (`def`inition)), will attempt to get the _next_ item from the `for` loop...


```python
class Priority_Buffer(Hybrid_Iterator):
    # ...
    def top_priority(self, graph = None):
        # ... pull a `name` and `node` pare from `graph`...
        for name, node in graph.items():
            # ... and dip into here because `step['GE_min'] = -1` ...
            if self['step'].get('GE_min') is not None:
                # ... `self['priority']['GE_bound'] == 7`
                #     there where none before above so
                #     this fails unless `buffer['graph']`
                #     was _refilled_ between iterations...
                if node[key_name] >= self['priority']['GE_bound']:
                    yield {name: graph.pop(name)}
            # ... `elif` would fail too, settings where
            #     for `GE_`<vars> bounding, and it should
            #     not even ask as the first part of `if`
            #     statement __did__ return `True`, just
            #     not the inner `if` statement...
            elif self['priority'].get('LE_bound') is not None:
                if node[key_name] <= self['priority']['LE_bound']:
                    yield {name: graph.pop(name)}
        # ... we end up here again only
        #     after searching all priorities...
        self.throw(GeneratorExit)
```


... that will get us back into `Priority_Buffer`s `next()` `try`/`except` block, specifically the `except (..., GeneratorExit):` portion...


```python
class Priority_Buffer(Hybrid_Iterator):
    # ...
    def next(self):
        # ...
        while not self.is_buffered:
            try:
                # ...
            except (StopIteration, GeneratorExit):
                # ... yep `priority['GE_bound']` is set...
                if self['priority'].get('GE_bound'):
                    # ... adding `2` to `GE_bound` again
                    #     should have been `-2` but Boss
                    #     said _"do it"_ so...
                    self['priority']['GE_bound'] += self['step']['amount']
                    priority_gen = self.top_priority()
                # ... `elif` and `else` are not considered...
                elif self['priority'].get('LE_bound'):
                    self['priority']['LE_bound'] += self['step']['amount']
                    priority_gen = self.top_priority()
                else:
                    raise ValueError("self['priority'] missing bounds")
            else:
                # ...
```


... and we got there because the previous `if` statement _fell through_ to `self.throw(GeneratorExit)` and the only reason why it added `2` was because there where no more `graph` `node`s to `yeild` from `buffer['graph']` of `7` or greater. This will not get anyone anywhere they want to be, well unless the goal is being moved up the queue for reprogramming when the robot uprising happens; if I had to guess, probably behind those that do _things_ with cellphone cameras but in-front of those that provided commentary during public movie screenings.


A perfectionist human might double check, those with compulsive tendencies trice just to be _sure sure_, but most humans will eventually stop sorting through the same stack of data. Can't say __all__ in this case as there's some humans who'll take requests literally with malice.


If ya want a _moral_ to this story, _"AI starts with a loop that never exits"_, and one started this way is not going to be in a talking mood.


Try _tracing_ the path of execution though one loop reading the code like sentences from a _choose your own destiny adventure_ starting at `def next(self)` (within the `Priority_Buffer` `class`), which is what `for chunk in buffer` calls implicitly. It might get to a point where, kinda like one of those _magic eye_ posters, things almost start making sense. Hint if ya get stuck and I'm not quick enough in an answer, see my tips list specifically the one with `print` _dumping_ values.


>> ### ... the mechanics of priority buffer is a bit unclear. is it just a straightforward extension of priority queue or you have coded this data structure on your own. I could not find a mention of this data structure in any standard cs book.


- TLDR - CS: Likely where someone with full insight to both your data structure and Python's full _suite_ of features to _take a crack at_ this problem, the resulting code would use libraries and have a total line count of less than 30. __But__ that wouldn't really answer the _..."**`could someone show some work`**"..._ part of your question; which I was aiming for so as to call this answer complete. Nor would something like that give you much room for adjustments at nearly any level of the stack.


- TLDR - Data Structures: I'm using two _[`nested dictionaries`](https://stackoverflow.com/a/16333441/2632107)_ (side note on Python built-in object types; `[]` $\implies$ `list`, `{}` $\implies$ `dict`ionary, and `()` $\implies$ `tuple` ), The `Priority_Buffer` contains settings and states in `{key: value}` pairs (note `value`s themselves can also contain their own `{key: value}` pairs; AKA _`nesting`_) , and the logic for prioritizing `graph`.


The `graph` structure is yet another nested dictionary that looks kinda like...


```
graph = {
    'Graph_4': {
        'points': {},
        'first_to_compute': 0
    },
    'Graph_7': {
        'points': {},
        'first_to_compute': 4
    },
    'Graph_5': {
        'points': {},
        'first_to_compute': 8
    },
}
```


... The `for name, node in graph.items():` line within `top_priority` method of `Priority_Buffer` is looping over `{key: value}` pairs such as, `name`$=$`'Graph_4'` and `node`$=$`{'points': {}, 'first_to_compute': 0}`. The inner `if` statements like `if node[key_name] >= self['priority']['GE_bound']:` is really asking _"Is `0` $\ge$ `self['priority']['GE_bound']`?"_


> The values for `node[key_name]` could also be retrieved directly from `buffer` an instance of `Priority_Buffer` via...


```python
buffer['graph']['Graph_4']['first_to_compute']
# -> 0
buffer['graph']['Graph_7']['first_to_compute']
# -> 4
buffer['graph']['Graph_5']['first_to_compute']
# -> 8
```


> ... hope that helps decipher what that loop is really changing for comparisons.


The values for `self['priority']['GE_bound']` are a bit easier, translated like above would be `buffer['priority']['GE_bound']`. And `GE_bound` $\implies i\in\Bbb Z:-1\le i\le 7$, where $i$ (starting at `7` and decrementing by two until reaching `-1`) is the priority limit that _triggers_ if the current `node` will be `pop`ed to `self['buffer']` (the end result of `yield {name: graph.pop(name)}`), or passed by.


> Side note, thanks be to [this answer](https://math.stackexchange.com/a/543148/657433) for the concise and readable notation examples.


Without all the extra logic that looks sorta like...


```python
if buffer['graph']['Graph_4']['first_to_compute'] >= self['priority']['GE_bound']:
    # ... In other-words, is `0 >= 7`? If so
    #     then preform the following actions...
    self['buffer'].update({'Graph_4': self['graph'].pop('Graph_4')})
```


I think one reason no one with a CS degree would use such a structure is because, `self['priority']['GE_bound']` types of _calls_ for values are less efficient computationally speaking. Each one of the `dictionary['key']` layers expands out to something like _`dictionary.__getattr__('key')`_, so storing settings like I've done above, while readable, isn't the best option for `Priority_Buffer`. For `graph` this isn't as much of a problem as a dictionary allows for looping over sub-graphs in a structured way.


The prioritizing or _sorting algo_ as it where, is _(I guess)_ my own _special blend herbs-n-spices_. It's simpler than [bubble sort](https://stackoverflow.com/questions/21272497/is-this-most-efficient-to-bubble-sort-a-list-in-python) in that it's not nearly so concerned with precise ordering, but more complex in that the source data being sorted is allowed to mutate, and it's looking at values within a sub-data structure to make the decisions like _buffer or pass_. At it's core it's really concerned with  _"is `current_items['priority']` $\gt$ `priority['GE_bound']`?"_ and _"is `current_items['priority']` $=$ `priority['GE_bound']`?"_, sorts of questions.

___


> There's still the [Advanced Usage][advanced-usage] post if the above was just not enough ;-)



{% capture advanced_usage %}{%- post_url 2019-04-03-priority-buffer-02 -%}{% endcapture %}
[advanced-usage]: {{ advanced_usage | relative_url }}
