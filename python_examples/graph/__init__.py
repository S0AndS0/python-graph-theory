#!/usr/bin/env python
from __future__ import absolute_import

from hybrid_iterator import Hybrid_Iterator
from graph.points import Point
from graph.agents import Agent


license = """
Python class for simulating moving agents to points on a graph.
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


class Graph(Hybrid_Iterator):
    """
    Let `agents` be a `dict` with `{'agent_name': 'address'}` key pares
    Let `points` be a `dict` with `{'address': {'neighbors': {'addr': 'cost'}}}`
    """

    def __init__(self, agents, points, **kwargs):
        super(Graph, self).__init__(**kwargs)
        self.update(agents = {}, points = {}, off_duty = {})
        for point, neighbors in points.items():
            self.add_point(point, neighbors)
            # print(self)

        for name, address in agents.items():
            self.add_agent(name, address)

    def add_agent(self, name, address):
        if isinstance(address, str):
            address = self['points'][address]

        self['agents'].update({name: Agent(name, address)})
        address['population'].append(name)

    def add_point(self, address, neighbors):
        self['points'].update({address: Point(address, neighbors)})

    def next(self):
        """
        This is what is called by `for` loops implicitly but maybe called explicitly
        """
        # if self.is_finished is True:
        #     self.throw(GeneratorExit)

        ## ... Get travel plans from agents
        travel_plans = {}
        for name, agent in self['agents'].items():
            try:
                travel_plans.update({name: agent.next()})
            except (StopIteration, GeneratorExit):
                # Pop agents that will not move anymore
                print("Moved {name} to off_duty".format(name = name))
                self['off_duty'].update({name: self['agents'].pop(name)})
            else:
                # Let them pass by updating their location
                here = agent['point']['address']
                heading = agent['heading']
                there = heading.keys()[0]

                print("{name} traveling from {here} to {there} paying {cost}".format(
                    name = name,
                    here = here,
                    there = there,
                    cost = heading[there]))

                agent['point']['population'].remove(name)
                agent['visited'].append(heading)

                agent['point'] = self['points'][there]
                agent['point']['population'].append(name)

        if not self['agents']:
            self.throw(GeneratorExit)

        return self


if __name__ == '__main__':
    raise Exception("This file must be used as a module!")
