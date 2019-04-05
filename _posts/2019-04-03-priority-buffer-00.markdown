---
layout: post
title:  "Sub-Graph Priority Buffer 00"
date:   2019-04-03 06:05:58 -0700
categories: hybrid_iterator
---
{%- include mathjax.html -%}

> This set of posts was inspired by [Smart enumeration of a subset of graphs obtained from a parent graph](https://math.stackexchange.com/questions/2389734/smart-enumeration-of-a-subset-of-graphs-obtained-from-a-parent-graph) question.


I'll attempt to assist with the following bits...


>> One idea I could think was that we define biases based on user/operator input. Thus some graphs are more relevant/important than others. Using this as a guiding heuristic we can do some kind of pruning to avoid enumerating all possible graphs.


... but first it's probably a good idea to get comfortable (snack and/or drink in other-words), it's going to be one of those posts ;-D


Your idea sounds smart for prioritizing computation of unordered (and possibly mutating) structured data sets, keeping humans _in the loop_ allows for the _illusion_ of control and given the strides being made in machine learning... enough _hand-waving_ though time to focus on a portion of this problem; a prioritizing iterator.


The best way that I know how to express this is in Python, I'll try to keep it to a minimum as far as script size while also only using/inheriting built-ins so that the _technical-debt_ (a measure of having to understand sets of $library_{dependency}$ before even beginning to code), for readers is kept to a minimum too. A balancing act but at least what I share is very generalizable.


## `hybrid_iterator/__init__.py`


Scroll past this code block and on to the next one, it's just a dependency to keep code clean and _mostly_ reliable.


```python
#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True
# ... When in production remove or comment above
#     two lines to gain `pyc` _speed boost_.
#     They're there to mitigate thrashing
#     SSD or similar during development process.

from collections import Iterator


class Hybrid_Iterator(dict, Iterator):
    """
    Contains _boilerplate_ and Python 2/3 compatibility for
    making a looping dictionary. Not intended to be used
    directly but instead to reduce redundant repetition.
    """

    def __init__(self, **kwargs):
        super(Hybrid_Iterator, self).__init__(**kwargs)

    def __iter__(self):
        return self

    def throw(self, type = None, traceback = None):
        raise StopIteration

    def next(self):
        """
        Inheriting classes __must__ override this method to activate.

        - Called implicitly via `for` loops but maybe called explicitly.
        - `GeneratorExit`/`StopIteration` are an exit signal for loops.
        """
        self.throw(GeneratorExit)

    __next__ = next


if __name__ == '__main__':
    raise Exception("Hybrid_Iterator import and modify it to iterate dictionaries!")
```


> Bellow's a _sketch_ of `Hybrid_Iterator`'s `super` relationships with `dict` and `Iterator` `class`es


$$
\color{#CD8C00}{\fbox{ dict }{
  \color{#2E8B57}{\xleftarrow[]{
    \color{#000}{\text{super}_{\left(key\_word\_args\right)}}
  }}
  \over{\color{#CD8C00}{
    \xrightarrow[\color{#000}{\text{returned value}}]{}
  }}
}}
\color{#2E8B57}{\fbox{ Hybrid~Iterator }{
  \color{#2E8B57}{\xrightarrow[]{
    \color{#000}{\text{super}_{\left(key\_word\_args\right)}}
  }}
  \over{\color{#00A}{
    \xleftarrow[\color{#000}{\text{returned value}}]{}
  }}
}}
\color{#00A}{\fbox{ Iterator }}
$$


Above is nothing overly _special_ on it's own, in fact without modification it's in someways a worse dictionary than it was before. Hint, compare the lists of methods available for each via `dir()`, eg `dir(Hybrid_Iterator)` to see it's _inner bits_ that can be called upon... But let's not get lost in the details, instead get past the prereqs, and on to the proof of concept code and it's usage.


## `priority_buffer.py`


$$
\color{#2E8B57}{\fbox{ Hybrid~Iterator }{
  \color{#8C0073}{\xleftarrow[]{
    \color{#000}{\text{super}_{\left(key\_word\_args\right)}}
  }}
  \over{\color{#2E8B57}{
    \xrightarrow[\color{#000}{\text{returned value}}]{}
  }}
}}
\color{#8C0073}{\fbox{ Priority~Buffer }}
$$


> Above is a _sketch_ of the _relationships_ being built between above and bellow `code` blocks.


```python
#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

import sys
sys.dont_write_bytecode = True

from hybrid_iterator import Hybrid_Iterator


class Priority_Buffer(Hybrid_Iterator):
    """
    Priority_Buffer

    ## Arguments

    - `graph`, with `{name: sub_graph}` and `sub_graph[key_name]` to compare
    - `buffer_size`, `int` of desired `{name: sub_graph}` pairs to buffer
    - `priority`, dictionary containing the following data structure
        - `key_name`, withing `graph` to compare with `_bound`s bellow
        - `GE_bound`, buffers those greater than or equal to `graph[key_name]`
        - `LE_bound`, buffers those less than or equal to `graph[key_name]`
    - `step`, dictionary containing the following `{key: value}` pairs
        - `amount`, to increment or decrement `_bound`s to ensure full buffer
        - `GE_min`/`LE_max`, bounds the related `_bounds` above
    - `modifier` if set __must__ accept `{key: value}` pairs from `graph`
    """

    def __init__(self, graph, priority, buffer_size, step, modifier = None, **kwargs):
        super(Priority_Buffer, self).__init__(**kwargs)
        self.update(
            graph = graph,
            priority = priority,
            buffer_size = buffer_size,
            step = step,
            modifier = modifier,
            buffer = {})

    @property
    def is_buffered(self):
        """
        Returns `True` if buffer is satisfied or graph is empty, `False`
        otherwise. Used by `next()` to detect conditions to `return` on.
        """
        if len(self['buffer'].keys()) >= self['buffer_size']:
            return True

        if len(self['graph'].keys()) <= 0:
            return True

        # ... Note `\` ignores new-lines so that
        #     the following compound checks do not
        #     require excessive side-scrolling...
        if self['step'].get('GE_min') is not None:
            if self['priority']['GE_bound'] < self['step']['GE_min']:
                return True
        elif self['step'].get('LE_max') is not None:
            if self['priority']['LE_bound'] > self['step']['LE_max']:
                return True
        else:
            raise ValueError("self['priority'] missing step missing min/max")

        return False

    def top_priority(self, graph = None):
        """
        Yields `dict`s from `graph` where value of `graph[key_name]`,
        as set by `self['priority']['key_name']`, is within range of
        `self['GE_bound']` or `self['LE_bound']`

        - `graph`, dictionary that is __destructively__ read (`pop`ed) from

        > if `graph` is `None` then `top_priority` reads from `self['graph']`
        """
        if graph is None:
            graph = self['graph']

        key_name = self['priority']['key_name']
        for name, node in graph.items():
            # ... Priorities greater or equal to some bound
            if self['priority'].get('GE_bound') is not None:
                if node[key_name] >= self['priority']['GE_bound']:
                    yield {name: graph.pop(name)}
              # ... Priorities less or equal to some bound
            elif self['priority'].get('LE_bound') is not None:
                if node[key_name] <= self['priority']['LE_bound']:
                    yield {name: graph.pop(name)}
            else:
                raise ValueError('Misconfiguration, either `GE_`/`LE_bound`s ')

        self.throw(GeneratorExit)

    def next(self):
        """
        Sets `self['buffer']` from `self.top_priority()` and returns `self`
        """
        if not self['graph']:
            self.throw(GeneratorExit)

        self['buffer'] = {}
        priority_gen = self.top_priority()
        while not self.is_buffered:
            try:
                # ... to get next priority
                next_sub_graph = priority_gen.next()
            except (StopIteration, GeneratorExit):
                # ... that we have run out items within
                #     the current bounds, so _step_ in prep
                #     for next iteration of `while` loop
                if self['priority'].get('GE_bound'):
                    self['priority']['GE_bound'] += self['step']['amount']
                    priority_gen = self.top_priority()
                    # ... Note `priority_gen` re-assignments are
                    #     a good place for future optimization.
                elif self['priority'].get('LE_bound'):
                    self['priority']['LE_bound'] += self['step']['amount']
                    priority_gen = self.top_priority()
                else:
                    raise ValueError("self['priority'] missing bounds")
            else:
                # ... got `next_sub_graph` successfully! So
                try:
                    self['buffer'].update(self['modifier'](next_sub_graph))
                except TypeError:
                    self['buffer'].update(next_sub_graph)
                #     though this is a good spot
                #     for pre-processing too...
            finally:
                # ... check for other ways out of `while`
                #     loop before doing it all again...
                pass

        return self


if __name__ == '__main__':
    """
    A good place to put unit-tests bellow
    because following lines are executed when
    this file is run as a script but ignored
    when imported as a module.
    """
    raise Exception("No priorities?")
```


Indeed that was _some_ code so to cover the _what's_, _hows_, and _whys_ I'll try to put it into some context with usage examples.


___


## Usage Examples


Provided that the first code block was saved to `lib/hybrid_iterator.py` and the second to `priority_buffer.py` (within what-ever sub-directory you've made and changed working directories to), it should be possible to run the following within a Python shell...


```python
from priority_buffer import Priority_Buffer
```

... which should produce __no__ output just a new line; _thrilling_ for sure.


I'm going to ask Python to generate some _toy_ data to play with, _priorities_ will be randomly set within upper and lower bounds between `0` and `9` respectively...


```python
from random import randint


graph = {}
for i in range(0, 21, 1):
    graph.update({
        "sub_graph_{0}".format(i): {
            'points': {},
            'first_to_compute': randint(0, 9),
        }
    })
```


Above should generate a `graph` dictionary that'll look _sorta_ like the following...


```python
for k, v in graph.items():
    print("{0} -> {1}".format(k, v))
# ...
# Graph_4 -> {'points': {}, 'first_to_compute': 0}
# Graph_7 -> {'points': {}, 'first_to_compute': 4}
# Graph_5 -> {'points': {}, 'first_to_compute': 8}
# ...
```

The `first_to_compute` keys are what are going to be used soon and I hope readers like it, doesn't really matter what you call this key so long as you're consistent between above and bellow `code` blocks. The `sub_graph`s `key` names are unimportant for these examples as dictionaries are unordered, only serving as a _hash_ for look-ups. The `points` are just place-holders to show that more than one key value pair are allowed in a dictionary; well so long as the keys are unique. Note nesting `dict`s is often easer than getting data back out without forethought though so this should not be used in production without significant modifications.


> Readers who really want _something_ more substantial in complexity to substitute in for `points` empty dictionary can find a link within the comments of this OP's question to another `class` written for a different graph related question. However, for the following set of examples it'll not be important.


With all that set-up out of the way it is time to initialize the `Priority_Buffer` `class`!...


```python
buffer = Priority_Buffer(
    graph = graph,
    priority = {'key_name': 'first_to_compute',
                'GE_bound': 7},
    step = {'amount': -2,
            'GE_min': -1},
    buffer_size = 5,
)
```


... then to loop it, safely...


```python
counter = 0
c_max = int(len(graph.keys()) / buffer['buffer_size'] + 1)
# ... (21 / 5) + 1 -> int -> 5


for chunk in buffer:
    print("Chunk {count} of ~ {max}".format(
        count = counter, max = c_max - 1))

    for key, val in chunk['buffer'].items():
        print("\t{k} -> {v}".format(**{
            'k': key, 'v': val}))

    counter += 1

    if counter > c_max:
        raise Exception("Hunt for bugs!")
```


> That business above with `counter` and `c_max` is to ensure an initialized `Priority_Buffer` with inputs that result in contemplating $\infty$ the wrong way are not disastrous.


... which should output something that looks like...


```
Chunk 0 of ~ 4
         Graph_18 -> {'points': {}, 'first_to_compute': 5}
         Graph_13 -> {'points': {}, 'first_to_compute': 7}
         Graph_5 -> {'points': {}, 'first_to_compute': 8}
         Graph_8 -> {'points': {}, 'first_to_compute': 9}
         Graph_9 -> {'points': {}, 'first_to_compute': 6}
# ... Trimmed for brevity...
Chunk 3 of ~ 4
         Graph_6 -> {'points': {}, 'first_to_compute': 0}
         Graph_4 -> {'points': {}, 'first_to_compute': 0}
         Graph_3 -> {'points': {}, 'first_to_compute': 0}
         Graph_16 -> {'points': {}, 'first_to_compute': 3}
         Graph_1 -> {'points': {}, 'first_to_compute': 2}
Chunk 4 of ~ 4
         Graph_0 -> {'points': {}, 'first_to_compute': 0}
```


The original `graph` dictionary should now be _empty_, destructive reads with `pop()` are a memory vs computation optimization _feature_ as well as an attempt to mitigate _looking over_ the same priorities ranges' worth of data too redundantly before expanding the _search space_.


If _consuming_ the `graph` is not a desired behavior I believe `Priority_Buffer(graph = dict(graph),...)` _copies_ the source data during initialization, this means you'd have two copies of the same data, however, `Priority_Buffer`'s will on average always be decreasing... well that is unless you _refill_ `buffer['graph']` with an `update({'sub_graph_<n>': ...})` before the main loop exits, which hint hint, allowing for such _shenanigans_ on a loop is kinda why it's written the way it is ;-) though you'll want to _refresh_ the `buffer['GE_bound']` (or `LE_bound`) to ensure things are bubbling up again like they should.


Using the currently scripted methods you'll always get `chunk`s size of `buffer['buffer_size']` or less. The first found that are greater or equal to `buffer['priority']['GE_bound']` (inverse for `LE_bound`) are returned as a `chunk`. If for example it didn't have enough on a given call of `buffer.next()` (implicitly called by loops), the _search space_ would expand by `buffer['step']['amount']` till either it reaches (or crosses) `buffer['step']['GE_min']` or the buffer size is satisfied. There's a few other _bits-n-bobs_ for exiting when `graph` is empty but that's the _gist_ of it.


While it'll happily make mistakes on your behalf at the speed of _ohh sh_... I think it's a __fair start__ (in that those within a range are prioritized, _first-found $=$ first-`pop`ed_), and close enough to what you're asking for that it _hacking_ into something better is totally likely. This is probably a good point to pause and allow things to _steep_. When you're ready, the following are a few extra tips;


- be __careful__ with `step['amount']`'s _direction_; decrement (use negative numbers) when using `GE_` related configurations, and increment when using `LE_`,
-- `_bounds` should be `-+1` (less or more by `1`) than the total target `priority['key_name']` priority value max/min to avoid having a _bad time_.
- the `priority['GE_bound']`, `buffer_size`, and other values should be _played with_ because ideal settings will depend upon system resources available.
- for applying $R$ at some level in the execution stack check the other answer I linked in your question's comments for hints on adding `first class function` calls, I used Python `lambda`s there (_quick-n-dirty_), but `function`s and `method`s work similarly.
- try removing the `raise Exception("No priorities?")` line within the `priority_buffer.py` file, then placing the above usage examples under the `if __name__ == '__main__':` line (tabbed in one level; Python is _sensitive_ in that way), and then try running the file as a script, eg. `python priority_buffer.py`, a few times to observe the _behavior_ of the current sorting methods.
- If new to Python try, adding `print("something -> {0}".format('value'))` (replacing `'value'` with _something_), lines anywhere that you want to _dump_ some info during execution, or use a _fancy_ [IDE](https://en.wikipedia.org/wiki/Integrated_development_environment) such as [Atom](https://flight-manual.atom.io/getting-started/sections/installing-atom/) (with a few plugins) to enable setting `break points` and `step` through parts that don't quite make sense.


Hope this was somewhat helpful in getting ya up-to speed with how one can develop an approach for solving such problems.


___


> When ready, further reading can be found at the [Q&A post][q-and-a], and [Advanced Usage][advanced-usage] posts.


{% capture q_and_a %}{%- post_url 2019-04-03-priority-buffer-01 -%}{% endcapture %}
[q-and-a]: {{ q_and_a | relative_url }}

{% capture advanced_usage %}{%- post_url 2019-04-03-priority-buffer-02 -%}{% endcapture %}
[advanced-usage]: {{ advanced_usage | relative_url }}
