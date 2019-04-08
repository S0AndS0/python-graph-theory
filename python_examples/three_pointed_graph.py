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


def key_dump(dictionary, key):
    for k, v in dictionary[key].items():
        print("{0} -> {1}".format(k, v))


"""
Initializing `graph` and state inspection
"""


X, O = (0.2, 0.7)
graph = Graph(
    agents = {
        'Bill': 'u',
        'Alice': 'u',
        'Ted': 'v',
        'Jain': 'w'
    },
    points = {
        'u': {'v': X, 'w': X},
        'v': {'u': O, 'w': X},
        'w': {'u': O, 'v': X},
    })


key_dump(graph, 'points')
key_dump(graph, 'agents')


"""
Observe the _little computer people_ move about the `graph`
"""


print("## 0 {0}".format(f_line))
key_dump(graph, 'points')
for i, _ in enumerate(graph):
    if i > 5:
        raise Exception("Hunt for bugs!")

    print("## {0} {1}".format(i, f_line))
    key_dump(graph, 'points')

print("## {0} {1}".format(i, f_line))
key_dump(graph, 'off_duty')
key_dump(graph, 'points')
