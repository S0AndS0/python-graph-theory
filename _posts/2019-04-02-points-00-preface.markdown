---
layout: post
title:  "Points 00 Preface"
date:   2019-04-02 06:05:58 -0700
categories: graph
---
{% include mathjax.html %}


Inspired by [modeling congestion games in Python without tons of for loop](https://math.stackexchange.com/questions/3130866/modelling-congestion-games-in-python-without-tons-of-for-loop)

{% comment %}
<img src="{ /assets/graph_images/Graph_UVW.png | relative_url }" alt="Please imagine a three pointed bidirectional graph with points labeled U V W" max-width="200" max-height="200">
{% endcomment %}

___

The following portions are what I'll attempt to aid with as I'm on a similar path...

>> I am trying to model this problem with a python script without any game theory library as a challenge.
>>
>> ...
>>
>> It would be difficult for me to try 10 agents in the future. Anyway to improve the algorithm?

... however, unfortunately helping with the `tons of for loop`s I cannot, __but__ I can help in spreading'em out such that `cyclomatic complexity` checker tools don't flag down what you're trying to accomplish, and code [`profilers`](https://docs.python.org/2/library/profile.html) can then give meaningful output for determining where libraries such as [`numpy`](https://stackoverflow.com/questions/tagged/numpy) are a good fit.

Looking through your code, I think you're on the right track with using dictionaries for some of this, well that is if you're dedicated to minimal library use; which I think is totally a legit way of learning.

The next step seems to be to use Python's OOP (Object Oriented Programing) tendencies, and `__doc__` strings to your advantage; first step you've already completed by getting some code that produces your desired output. Because you've stated this is __a challenge__ I'll not be posting a complete answer, but I'll provide some code to illustrate what I mean.

> Or in other words, maybe a good idea to get a snack and drink... this is about to get verbose,

## Nodes/`Point`s

The current graph looks sorta like the following when unwrapped, note I'm just _drawing a sketch_ to better frame what the code'll be covering.

$$
  \color{#000}{\fbox{ w }}{
  \color{#2E8B57}{ \xleftarrow[]{\color{#000}{X}} }}
  \color{#00A}{ \fbox{ u } }{
  \color{#2E8B57}{ \xrightarrow[]{\color{#000}{X}} }}
  \color{#000}{\fbox{ v }}
\\
  \color{#000}{\fbox{ u }}{
  \color{#FF0000}{ \xleftarrow[]{\color{#000}{O}} }}
  \color{#00A}{ \fbox{ v } }{
  \color{#2E8B57}{ \xrightarrow[]{\color{#000}{X}} }}
  \color{#000}{\fbox{ w }}
\\
  \color{#000}{\fbox{ v }}{
  \color{#2E8B57}{ \xleftarrow[]{\color{#000}{X}} }}
  \color{#00A}{ \fbox{ w } }{
  \color{#FF0000}{ \xrightarrow[]{\color{#000}{O}} }}
  \color{#000}{\fbox{ u }}
$$

`Point`s (the items from the middle column above and defined in the following `class`) are only concerned with where it is (`address`), and the `cost`s to each of it's `neighbors`'s `address`es. The `cheapest` (of `routes`) method (defined bellow) calculates the returned value at call time so that `neighbors` can be added, removed, or modified at any other time.

```python
#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
# ... Above _unlocks_ some compatibility _magics_
#     for running within Python 2 or 3

import sys
sys.dont_write_bytecode = True
# ... When in production remove or comment above
#     two lines to gain `pyc` _speed boost_. They're
#     there to mitigate thrashing SSD and similar
#     storage media during the development process.


class Point(dict):
    """
    Point is a custom dictionary to aid in modeling
    a graph point and base cost to get to neighbors.

    ## Arguments

    - `address` should be a unique identifier that can be used as a `key`
    - `neighbors` should be a `dict` with `{address: cost}` key value pares
      - `cost` should be a `float` or `int`

    > `address`es are the same regardless of scope
    """

    def __init__(self, address, neighbors = {}, **kwargs):
        super(Point, self).__init__(**kwargs)
        self.update({
            'address': address,
            'neighbors': neighbors,
            'population': []})

    def cheapest(self, routes = {}):
        """
        Returns `dict` with '{address: cost}' key pares

        > `routes` by default will read `self['neighbors']`
        """
        if not routes:
            routes = self['neighbors']

        headings = {}
        for address, cost in routes.items():
            destination = {address: cost}
            if not headings:
                headings = destination
                continue

            cheaper_mask = [cost < x for x in headings.values()]
            equal_mask = [cost == x for x in headings.values()]
            if False not in cheaper_mask:
                headings = destination
            elif True in equal_mask:
                headings.update(destination)

        return headings


if __name__ == '__main__':
    """
    Following are only execute if run as a script.
    - or in other-words importing ignores bellow
    - or in other-other-words a good place to put quick unit tests
    """
    raise Exception("No points have been made!")
```

___

> To the mathematically educated, I'd really like to see how to write a similar model through pure math, so feel free to edit this section here with something beautiful.

___

If ya saved the above to a file path such as `points/__init__.py`, importing could look like...

```python
from points import Point
```

Initializing a similarly shaped three pointed graph with bi-directional traveling costs between each point's neighbors could look like...

```python
X = 0.2
O = 0.7

points = {
    'u': Point(address = 'u', neighbors = {'v': X, 'w': X}),
    'v': Point(address = 'v', neighbors = {'u': O, 'w': X}),
    'w': Point(address = 'w', neighbors = {'u': O, 'v': X}),
}
```

Getting the information back out would then look like...

```python
help(points['w'])
# ... prints triple quoted block from class
#     AKA the `__doc__` string ;-)

points['w']['neighbors']
# -> {'u': 0.7, 'v': 0.2}

for name, point in points.items():
    neighbors = point['neighbors']
    print("{name} cheapest routes -> {route}".format(
        name = name,
        route = point.cheapest(neighbors)))
# -> u cheapest routes -> {'w': 0.2, 'v': 0.2}
# -> w cheapest routes -> {'v': 0.2}
# -> v cheapest routes -> {'w': 0.2}
```

The `cheapest` _of_ `routes` differ between points `u` and `v`, and so far the information of all possible routes are preserved, because this class inherits from the `dict` class, that's what the `class Point(dict)` did, it's possible to dump it's saved/current state via...

```python
print(points)
# -> {'u': {'address': 'u',...}, 'v': {'neighbors': {'u': 0.7, ...}, ...}, ...}
```

> Bellow is a _sketch_ of `Point`'s `super` _relationship_ with the `dict` `class`

$$
\color{#CD8C00}{\fbox{ dict }{
  \color{#00A}{\xleftarrow[]{
    \color{#000}{\text{super}_{\left(key\_word\_args\right)}}
  }}
  \over{
    \xrightarrow[\color{#000}{\text{returned value}}]{}
  }
}}
\color{#00A}{\fbox{ Point }}
$$

Essentially with one class we can model the graph, well minus the agents and something to coordinate iterating states through time, plus it abstracted three `for` loops and other logic to a _something_ that can be questioned reliably. Utilizing this methodology of splitting things into manageable chunks on the rest of the challenges will make adding more agents, changing algorithms, and even mutating the graph much simpler.

I probably should wrap it up here, so let me know if this was helpful or if ya'll want some more in this style once it's all been digested.

___

> After using `Point` and finding limitations you'll likely want to customize it's _behavior_ to suite the states that you wished modeled, when that happens consider checking out the [next post][next-post] where I get into some Q&A that leads to diving into building a simple `Construction` `Point`.

{% capture next_post %}{%- post_url 2019-04-02-points-01-inheriting -%}{% endcapture %}
[next-post]: {{ next_post | relative_url }}
