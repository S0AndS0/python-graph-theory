---
layout: post
title:  "Sub-Graph Priority Buffer 02"
date:   2019-04-03 06:07:58 -0700
categories: hybrid_iterator
---
{%- include mathjax.html -%}


## Advanced Usage

I've updated the `try`/`else` block of code some to hopefully allow for an easier time of perhaps applying $R$ as a `modifier`, hint `self['buffer'].update(buffer['modifier'](next_sub_graph))`, here's a quick example...

```python
def populate(sub_graph):
    """
    Expects `{'hash': {'key': None}}` structure where `key` needs a population
    """
    key = 'points'
    hash = sub_graph.keys()[0]
    for x in range(randint(2, 5)):
        sub_graph[hash][key].update(
            {
                "point_{0}".format(x): randint(200, 500),
            }
        )

    return sub_graph

buffer['modifier'] = point_populate
```
> Note assigning to `modifier` may also be done at initialization too.

... so doing the same loop over `buffer` (once `buffer['graph']` has been refilled and `buffer['priority']['GE_bound']` reset) should now produce results similar to...

```
Chunk 0 of ~ 4
    sub_graph_11 -> {
        'points': {
            'point_0': 379,
            'point_1': 478},
        'first_to_compute': 7}

    sub_graph_10 -> {
        'points': {
            'point_0': 433,
            'point_1': 377,
            'point_2': 462},
        'first_to_compute': 8}
    # ...
#...
```

... the `populate` function is being called only on those who are within the priority range!

> As there maybe some following along with an empty `buffer['graph']`, here's how to repopulate and re-set bits within `buffer` for re-looping...

```
buffer['modifier'] = populate
buffer['priority']['GE_bound'] = 7

for i in range(0, 21, 1):
    buffer['graph'].update({
        "sub_graph_{0}".format(i): {
            'points': {},
            'first_to_compute': randint(0, 9),
        }
    })
```
