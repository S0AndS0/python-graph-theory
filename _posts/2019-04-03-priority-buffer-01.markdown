---
layout: post
title:  "Sub-Graph Priority Buffer 01"
date:   2019-04-03 06:06:58 -0700
categories: lib
---
{%- include mathjax.html -%}


## `Priority_Buffer` Q&A


>> The business with `counter` and `c_max` was not clear. could you explain more?


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
                # ... it will _try_ to update `self['buffer']`
                self['buffer'].update(priority_gen.next())
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

... that will get us back into `Priority_Buffer`s `next()` `try`/`except` block, specifically...

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
```

... and we got there because the previous `if` statement _fell through_ to `self.throw(GeneratorExit)` and the only reason why it added `2` was because there where no more `graph` `node`s to `yeild` from `buffer['graph']` of `7` or greater. This will not get anyone anywhere they want to be, well unless the goal is being moved up the queue for reprogramming when the robot uprising happens; if I had to guess, probably behind those that do things with cellphone cameras but in-front of those that provided commentary during public movie screenings.

A perfectionist human might double check, those with compulsive tendencies trice just to be _sure sure_, but most humans will eventually stop sorting through the same stack of data. Can't say __all__ in this case as there's some humans who'll take requests literally with malice.

If ya want a _moral_ to this story, _"AI starts with a loop that never exits"_, and one started this way is not going to be in a talking mood.

Try _tracing_ the path of execution though one loop reading the code like sentences from a _choose your own destiny adventure_ starting at `def next(self)` (within the `Priority_Buffer` `class`), which is what `for chunk in buffer` calls implicitly. It might get to a point where, kinda like one of those _magic eye_ posters, things almost start making sense. Hint if ya get stuck and I'm not quick enough in an answer, see my tips list specifically the one with `print` _dumping_ values.


>> ... the mechanics of priority buffer is a bit unclear. is it just a straightforward extension of priority queue or you have coded this data structure on your own. I could not find a mention of this data structure in any standard cs book.

The data structure that I'm using is a _`nested dictionary`_, and the _sorting algo_ as it where, is I guess my own _special herbs-n-spices_. It's simpler than [bubble sort](https://stackoverflow.com/questions/21272497/is-this-most-efficient-to-bubble-sort-a-list-in-python) in that it's not nearly so concerned with precise ordering, but more complex in that the source data being sorted is allowed to mutate, and it's looking at values within a sub-data structure to make the decisions like _buffer or pass_. At it's core it's really concerned with  _"is `current_items['priority']` $\gt$ `priority['GE_bound']`?"_ and _"is `current_items['priority']` $=$ `priority['GE_bound']`?"_, sorts of questions.

Because I didn't have a whole lot of insight as to the true structure of your data source I made the code as adaptable as possible, within reason, to the possibilities that heuristics may change between iterations; eg. someone got the _go ahead_ to adjust their sub-graph's priority level. Fully _fleshed out_ the above `class` would mainly deal with _`pointers`_ to where it should get priorities from, method _feeding_ for any pre-processing, and returning of buffered partial results for further processing. Parallelization and use of [`numpy`](https://www.numpy.org) would make it far faster.

I'm not certain if someone with a CS degree (or their professor) would smile in a kind or _unkind_ way while glancing at this code; I've no _formal_ training in programming, just many years of experience _hacking_ about on my systems. If you want something of a more scholarly source that deals with truly massive data sets, ya might want to check out [this question](https://stats.stackexchange.com/q/326912/241755) and the paper that it links to. While it's mainly concerned with time-series formatted data, the `Early Abandoning Z-Normalization`, `Early Abandoning of ED and LB` sections, and other optimization techniques might be inspirational for when the indexes of you data set alone number well beyond the millions.
