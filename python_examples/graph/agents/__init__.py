#!/usr/bin/env python
from __future__ import absolute_import

import sys
sys.dont_write_bytecode = True

from random import randint

from hybrid_iterator import Hybrid_Iterator


license = """
Python class for modeling agents of graphs.
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


class Agent(Hybrid_Iterator):
    """
    Let `point` be a `Point` instance of where this `Agent` is currently
    """

    def __init__(self, name, point, **kwargs):
        super(Agent, self).__init__(**kwargs)
        self.update(
            name = name,
            point = point,
            visited = [],
            heading = {})

    def next(self):
        """
        Sets `self['heading']` from unvisited `self['point'].cheapest()`

        If multiple choices are available a randome one is picked.

        `raises` an Exception if no where left to go.
        """
        self['heading'] = {}
        courses = {}
        cheapest_routes = self['point'].cheapest()
        visited_addresses = [x.keys()[0] for x in self['visited']]
        for address, cost in cheapest_routes.items():
            if address not in visited_addresses:
                courses.update({address: cheapest_routes.pop(address)})

        target_key = 0
        if len(courses.keys()) > 1:
            target_key = randint(0, int(len(courses.keys()) - 1))

        if courses:
            address = courses.keys()[target_key]
            self['heading'] = {address: courses.pop(address)}

        if not self['heading']:
            self.throw(GeneratorExit)

        return self


if __name__ == '__main__':
    raise Exception("This file must be used as a module!")
