---
layout: post
title:  "Points 01 Inheriting"
date:   2019-04-02 07:05:58 -0700
categories: graph
---
{% include mathjax.html %}


> If this is your first time here then it might be a good idea to review the [previous post][previous-post], and for everyone let the following _sketch_ be a quick refresher of the portion of the graph that is being modeled...


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


> And the _relationship_ that `Point` has with the `dict`ionary `class`


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

___


## Customizing `Point`s


>> If the cost of each edge depends on the number of agents using it, what `X` and `O` should I pass it to the 'neighbors' dictionary?


I believe that the total cost is a result of a function that takes `points['w']['population']`s travel plans for instance (a property that'll be updated iteratively) and `cost` (`X`, or `Y` depending upon `Point`). And not to get too lost in the details but both `X` and `O` could be functions.


Here's two quick examples of how that could look in Python using `lambda`s...


- _Masking_ saved `cost` states


```python
edge_cost = lambda base_cost, drivers: base_cost * drivers

travel_estimate = points['w']['neighbors']['u']
# ... > `O` ... > 0.7
edge_cost(base_cost = travel_estimate, drivers = 2)
# -> 1.4
```


> What I'm asking of `edge_cost` might also be able to be expressed as $ e{\left( c, d \right)} = d \times c $, though one _gotcha_ (if I remember correctly), is that $\text{`pythonLambda`} {\ne} {lambda}$, because a Python `lambda` can be asked to do things that don't quite translate cleanly the other-way-round.


- _Differing_ execution/calculations of `X` and `O`, or in this case `first` and `business` _class tickets_.


```python
first = lambda base_cost: base_cost + 0.5
business = lambda base_cost: base_cost + 0.2


customers = {
    'bob': {'name': 'Bob', 'ticket': business},
    'alice': {'name': 'Alice', 'ticket': first}}


for key, customer in customers.items():
    print("{name} ticket cost -> {cost}".format(**{
        'name': customer['name'],
        'cost': customer['ticket'](base_cost = 0.4)
    }))
# -> Bob ticket cost -> 0.6
# -> Alice ticket cost -> 0.9
```


These states a `Point` for the most part _totally doesn't care about_ from it's frame of reference as a destination that agents leave. At most in the second of the last to examples it would only _care_ about getting it's output by feeding a `first class function` call. One way to look at is maybe a `Point` could be like a dispatcher (a stationary agent) who keeps a roaster of other agents in town and maybe picks up calls (_if they _must_, and it's not a Monday_), from agents about recent traveling conditions after arriving at a neighbor. Defined this way a `Point` could intentionally give bad information to another agent.


> Maybe $v$ has never gotten along with $S_{1}$ and will happily _low-ball_ any travel cost estimates given to that agent, maybe $S_{1}$ doesn't figure this out till the end `n` of a _pay periods_ when their _gas_ cost vs. compensation are not as they expected. How $v$'s' and $S_{1}$'s _personalities_ cause them to _mess_ with one another I think are within the _scope_ of a `Point`.


If you wish to question an edge I think it maybe helpful to re-frame an edge (define a `class`) as the points that are populated on an edge, so that things can be asked about those on an edge. This isn't to say that an edge must contain every point between, computers and $\infty$ usually don't mix, but instead an edge could have a way of calculating things like distances between agents or their destination.


>> But it seems to me that the point class can only model edges with a constant cost?


Sorta; it depends upon how you use those values or choose to update them. I took some care trying to model only part of the problem because covering everything in one post can cause readers to feel a bit like [Joel Miller](https://www.youtube.com/watch?v=IueMdK9I4Qg); which is __not__ my intent, I'd rather hope code be seen as another way to break a problem down to the _atomic_ level if need be.


Think of `Point` as a starting point for organizing questions about it's state, the using of those states and final calculations are still a bit further _up the stack_ as far as code execution depth if you want fine-grain control. Suppose in the future you want to model the rising and falling travel of costs based on hour of day or number of iterations of a parent's loop. These and other things can be done within another class that either imports or inherits the `Point` class.


Inheriting a `Point` to model something based on construction hours for example could look something like...


$$
\color{#CD8C00}{\fbox{ dict }{
  \color{#00A}{\xleftarrow[]{
    \color{#000}{\text{super}_{\left(key\_word\_args\right)}}
  }}
  \over{
    \xrightarrow[\color{#000}{\text{returned value}}]{}
  }
}}
\color{#00A}{\fbox{ Point }{
  \color{#2E8B57}{\xleftarrow[]{
    \color{#000}{\text{super}_{\left(key\_word\_args\right)}}
  }}
  \over{\color{#00A}{
    \xrightarrow[\color{#000}{\text{returned value}}]{}
  }}
}}
\color{#2E8B57}{\fbox{ Construction }}
$$


> Above is just a _sketch_ to show an overview of the _relationships_ that are being built with the code bellow


```python
#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
# ... Above _unlocks_ some compatibility _magics_
#     for running within Python 2 or 3

import sys
sys.dont_write_bytecode = True

from __init__ import Point
# ... Import the `Point` class from the
#    `__init__.py` file within the same directory.


class Construction(Point):
    """
    Construction aids in modeling costs that rise and fall based on current hour

    ## Arguments

    - `hours` could be a dictionary, eg. `{12: 0.6, 14: 0.8, ...}`
    """

    def __init__(self, hours, current_hour, address, neighbors, **kwargs):
        super(Construction, self).__init__(address = address,
                                           neighbors = neighbors,
                                           **kwargs)
        self.update(hours = hours, current_hour = current_hour)

    def cost_modifier(self, cost):
        """
        Returns cost plus current hour's cost if available
        """
        if self['current_hour'] not in self['hours'].keys():
            return cost

        return cost + self['hours'][self['current_hour']]

    def how_much_to(self, address):
        """
        Returns adjusted cost for given `neighbors` `address` from `cost_modifier`
        """
        base = self['neighbors'][address]
        return self.cost_modifier(cost = base)

    def cheapest(self, routes = {}):
        """
        Returns `dict` of `{address: cost}` adjusted with `how_much_to`
        """
        headings = {}
        for address in super(Construction, self).cheapest(routes).keys():
            headings.update({address: self.how_much_to(address)})

        return headings


if __name__ == '__main__':
    raise Exception("No Construction points detected.")
```


Inheriting from `Point` we gain the `super` powers of pre-processing `cheapest` within the scope of `Construction.cheapest` method. Yes that also means there's now some `for` loop stacking, but the above is just an example of using the _scope_ stacking that Python almost expects of authors, while also addressing one way to have changing `cost` calculations done by a point.


> In other-words, to those yelling at their monitor, right now the focus is optimizing for developer's time and not code execution time; releasing [`pandas`](https://pandas.pydata.org) or other libraries and optimizing code can wait till the problem is _fleshed-out_ from components with well defined inputs and outputs.


Importing the `Construction` point if saved under `points/construction.py` could then look like...


```python
from points.construction import Construction
```


Adding a fourth point `c` to the `points` dictionary defined previously might then look like...


```python
points.update({
    'c': Construction(
        address = 'w',
        neighbors = {'v': O, 'w': X},
        current_hour = 6,
        hours = {9: 0.1, 10: 0.3,
                 11: 0.4, 13: 0.6,
                 14: 0.7, 15: 0.85,
                 16: 0.3, 17: 0.2}
        )})
```


> _City planners_ kinda _dropped the ball_ by having construction on both out-bound routs, but that kinda models life.


... and updating `points['c']`'s neighbors could look like...


```python
Z = 0.1
for address in points['c']['neighbors'].keys():
    points[address]['neighbors'].update({'c': Z})
```


Which then would require _some_ adjustments to the `for` loop that was being used to iterate over points such as...


```python
hours_start = 1
hours_end = 24
hours_step = 1
days = 2

day_count = 0
for i in range(hours_start, (hours_end * days) + 1, hours_step):
    for address, point in points.items():
        # ... This `try`/`except` syntax is known as
        #     "asking forgiveness" _dig_ into previous
        #     edits for a "asking permission" version ;-)
        try:
            current_hour = point['current_hour']
        except KeyError:
            current_hour = 'NaN'
        else:
            if current_hour >= hours_end:
                point['current_hour'] = hours_start
                day_count += 1
            else:
                point['current_hour'] += hours_step

        finally:
            cheapest_routs = point.cheapest()
            print("{d} {h} {p} cheapest routes -> {r}".format(
                d = day_count, h = current_hour,
                p = address, r = cheapest_routs))
```


Indeed I've just nested even more loops, I'll address one way of mitigating this overall problem in the future if asked; hint `Iterator`s are really swell. Right now what is important to grasp from the adjusted model is that we now have a way to consistently _mask_ the initialized `cost` values within a point based off some other state that is updated. And that regardless of if a `Point` is a normal point or special point like `Construction`, the `cheapest` of `routs` methods are what is called by what ever process asking the questions of `points`.


```
# ... Example _snippets_ of output
0 6 c cheapest routes -> {'w': 0.2}
0 NaN u cheapest routes -> {'w': 0.2, 'v': 0.2}
0 NaN w cheapest routes -> {'c': 0.1}
0 NaN v cheapest routes -> {'c': 0.1}
0 7 c cheapest routes -> {'w': 0.2}
# ...
1 12 c cheapest routes -> {'w': 0.2}
1 NaN u cheapest routes -> {'w': 0.2, 'v': 0.2}
1 NaN w cheapest routes -> {'c': 0.1}
1 NaN v cheapest routes -> {'c': 0.1}
1 13 c cheapest routes -> {'w': 0.8}
# ...
```


Okay I think it's time for another pause for digestion, hopefully these pointers have helped ya plan out a course.


{% capture previous_post %}{%- post_url 2019-04-02-points-00-preface -%}{% endcapture %}
[previous-post]: {{ previous_post | relative_url }}

{% comment %}
> After writing your own custom `Point` class that solves a small problem (tip; keeping things modular allows you to _steal_ code from your past self), consider checking the [next post][next-post], where I _zoom out_ to the _three thousand forty eight meter view_ of what a project like the could look like, and a little more Q&A for good measure.

> ... capture intentionally broken to nonexistent path to _future_; causality being what it may...

{% capture next_post %}{ post_url 2019-04-02-points-02-futures }{% endcapture %}
[next-post]: {{ next_post | relative_url }}
{% endcomment %}
