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

license = """
Python class for modeling Points of simple graphs.
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
    Following block of code is only execute if run as a script.
    - or in other-words importing ignores bellow
    - or in other-other-words a good place to put quick unit tests
    """
    print("Initalizing unit test.\n{0}".format("".join(['_' for x in range(9)])))
    X = 0.2
    O = 0.7

    points = {
        'u': Point(address = 'u', neighbors = {'v': X, 'w': X}),
        'v': Point(address = 'v', neighbors = {'u': O, 'w': X}),
        'w': Point(address = 'w', neighbors = {'u': O, 'v': X}),
    }

    print("Dumping named points.\n{0}".format("".join(['_' for x in range(9)])))
    for name, point in points.items():
        print("{name} -> {point}".format(name = name, point = point))

    print("Finished unit tests.\n{0}".format("".join(['_' for x in range(9)])))
