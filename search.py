#!/usr/bin/env python
#coding: utf-8

import heapq

def build_path_to_goal(initial, goal, parents):
    current_state = parents[goal][1]
    path = [('END', goal), parents[goal]]

    while current_state is not None:
        path.append(parents[current_state])
        current_state = parents[current_state][1]
    path.reverse()

    return path

def a_star(initial, goal, heuristic):
    distances = {} # the count of state transitions to reach the key
    heuristics = {} # heuristc values tables to avoid having to compute repeatedly
    parents = {} # a link table so we can find the solution
    fringe = [] # binary heap to keep the states

    parents[initial] = (None, None)
    distances[initial] = 0
    heuristics[initial] = heuristic(initial, goal)
    heapq.heappush(fringe, (distances[initial] + heuristics[initial], initial))

    expanded = 0
    while True:
        if not fringe:
            raise Exception('Could not find a solution.')
        expanded += 1

        f, current_state = heapq.heappop(fringe)

        if current_state == goal:
            return expanded, distances[current_state], build_path_to_goal(initial, goal, parents)

        for action, successor in current_state.get_successors():
            if successor not in distances or distances[successor] > distances[current_state] + 1:
                distances[successor] = distances[current_state] + 1
                if successor not in heuristics:
                    heuristics[successor] = heuristic(successor, goal)
                parents[successor] = (action, current_state)
                heapq.heappush(fringe, (distances[successor] + heuristics[successor], successor))

def build_path_to_goal_tree(initial, goal, f, parents):
    f, action, current_state = parents[(f, goal)]
    path = [('END', goal)]

    while current_state is not None:
        path.append((action, current_state))
        f, action, current_state = parents[(f, current_state)]
    path.reverse()

    return path

def a_star_tree(initial, goal, heuristic, max_iter=1e6):
    distances = {} # the count of state transitions to reach the key
    heuristics = {} # heuristc values tables to avoid having to compute repeatedly
    parents = {} # a link table so we can find the solution
    fringe = [] # binary heap to keep the states

    heuristics[initial] = heuristic(initial, goal)
    f = heuristics[initial]
    parents[(f, initial)] = (None, None, None)
    heapq.heappush(fringe, (f, 0, initial))

    expanded = 0
    i = 0
    while i < max_iter:
        if not fringe:
            break
        expanded += 1

        f, distance, current_state = heapq.heappop(fringe)

        if current_state == goal:
            return expanded, distance, build_path_to_goal_tree(initial, goal, f, parents)

        for action, successor in current_state.get_successors():
            if successor not in heuristics:
                heuristics[successor] = heuristic(successor, goal)
            successor_dist = distance + 1
            successor_f = successor_dist + heuristics[successor]
            parents[(successor_f, successor)] = (f, action, current_state)
            heapq.heappush(fringe, (successor_f, successor_dist, successor))
        i += 1
    else:
        raise Exception('Could not find a solution.')

def ida_star(initial, goal, heuristic):
    f_limit = heuristic(initial, goal)
    heuristics = {} # table to avoid recomputing heuristic function
    heuristics[initial] = f_limit
    cost = 0
    expanded = 0
    while True:
        result = dfs_countour(initial, goal, 0, f_limit, heuristic, heuristics)
        solution, n_cost, f_limit, nodes_expanded = result
        expanded += nodes_expanded
        if solution is not None:
            solution[initial] = (None, None)
            return expanded, n_cost, build_path_to_goal(initial, goal, solution)
        if f_limit == float('inf') or expanded > 1e6:
            raise Exception('Could not find a solution.')

def dfs_countour(state, goal, cost, f_limit, heuristic, heuristics):
    next_f = float('inf')
    if state not in heuristics:
        heuristics[state] = heuristic(state, goal)

    f_cost = heuristics[state] + cost

    expanded = 0
    if f_cost > f_limit:
        return None, cost, f_cost, expanded
    if state == goal:
        return {}, cost, f_cost, expanded + 1

    expanded += 1
    for action, successor in state.get_successors(random_shuffle=False):
        result = dfs_countour(successor, goal, cost + 1, f_limit, heuristic, heuristics)
        solution, n_cost, new_f, n_expanded = result
        expanded += n_expanded
        if expanded > 1e6:
            return None, cost, float('inf'), expanded
        if solution is not None:
            solution[successor] = (action, state)
            return solution, n_cost, f_limit, expanded
        next_f = min(new_f, next_f)
    return None, cost, next_f, expanded

if __name__ == '__main__':
    from NPuzzle import *
    from misc import *
    g = NPuzzle(3, range(9))
    s = NPuzzle(3)
    while not s.is_solvable():
        s = NPuzzle(3)
    print 'initial state'
    s.show()
    expanded, steps, path = a_star_tree(s, g, NPuzzle.manhattan_distance)
    print_solution(expanded, steps, path)

    expanded, steps, path = ida_star(s, g, NPuzzle.linear_conflict)
    print_solution(expanded, steps, path)

