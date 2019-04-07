#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True


from graph.points import Point
from graph.agents import Agent


f_line = "".join(['_' for x in range(9)])


print("{0}\nInitializing points of graph".format(f_line))
X, Y = (0.2, 0.7)
points = {
    'u': Point(address = 'u', neighbors = {'v': X, 'w': X}),
    'v': Point(address = 'v', neighbors = {'u': Y, 'w': X}),
    'w': Point(address = 'w', neighbors = {'u': Y, 'v': X}),
}
print("{0}\n{1}".format(points, f_line))

agents = {
    'Bill': Agent(name = 'Bill', point = points['u']),
    'Alice': Agent(name = 'Alice', point = points['u']),
    'Tom': Agent(name = 'Tom', point = points['v']),
    'Jain': Agent(name = 'Jain', point = points['w']),
}


for agent in agents.values():
    agent['point']['population'].append(agent['name'])


count = 0
agent_key = 'Bill'

for step in agents[agent_key]:
    name = step['name']
    here = step['point']['address']
    there = step['heading'].keys()[0]
    cost = step['heading'][there]

    print("{name} paid {cost} to get from {here} to {there}".format(
        name = name,
        cost = cost,
        here = here,
        there = there))

    points[here]['population'].remove(name)
    points[there]['population'].append(name)
    step['visited'].append({there: cost})
    step['point'] = points[there]

    count += 1
    if count > 4:
        raise Exception("Hunt for bugs!")


print("Places that {0} has been -> {1}\n\tcurrently -> at {2}".format(
    agents[agent_key]['name'],
    agents[agent_key]['visited'],
    agents[agent_key]['point']['address']))
