#!/usr/bin/env python
from __future__ import absolute_import

import sys
sys.dont_write_bytecode = True

from graph import Graph


license = """
Python script for simulating a populated bi-directional three pointed graph.
Copyright (C) 2019  S0AndS0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


f_line = "".join(['_' for x in range(9)])


"""
Convenience functions
"""


def dump_points(graph):
    for addr, point in graph['points'].items():
        print("{0} -> {1}".format(addr, point))


def dump_agents(graph):
    for name, agent in graph['agents'].items():
        print("{0} -> {1}".format(name, agent))


def dump_off_duty(graph):
    for name, agent in graph['off_duty'].items():
        print("{0} -> {1}".format(name, agent))


"""
Initializing `graph` and state inspection
"""


X, O = (0.2, 0.7)
graph = Graph(
    agents = {
        'Bob': 'u',
        'Alice': 'u',
        'Ted': 'v',
        'Jain': 'w'
    },
    points = {
        'u': {'v': X, 'w': X},
        'v': {'u': O, 'w': X},
        'w': {'u': O, 'v': X},
    })


dump_points(graph)
dump_agents(graph)


"""
Observe the _little computer people_ move about the `graph`
"""


count = 0
print("## {0} {1}".format(count, f_line))
dump_points(graph)
for travel_plans in graph:
    count += 1
    if count > 5:
        raise Exception("Hunt for bugs!")

    print("## {0} {1}".format(count, f_line))
    dump_points(travel_plans)

print("## {0} {1}".format(count, f_line))
dump_off_duty(graph)
dump_points(graph)
