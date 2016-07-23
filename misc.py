#!/usr/bin/env python
#coding: utf-8

from NPuzzle import NPuzzle
from search import a_star
from search import a_star_tree
from search import ida_star

def print_solution(expanded_nodes, steps, path):
    print '{} nodes expanded.'.format(expanded_nodes)
    print '{} steps to solution.'.format(steps)

    for move, state in path:
        if state is not None:
            print move
            state.show()

def read_input(f):
    """
    Returns the initial state (NPuzzle object) the file f contains.

    The file should contain in the first line the dimension of the puzzle,
    i.e., in the case its an 8 puzzle it should be 3.
    The following lines should be the state of the board, one number per line,
    the blank should be the number 0.
    """
    K = int(f.readline())

    block = []
    for k in range(K*K):
        e = f.readline()
        block.append(int(e))

    initial = NPuzzle(K, block)
    return initial

def solve(initial, search=a_star, heuristic=NPuzzle.manhattan_distance):
    """
    Solve if solvable and print the results, given an initial state, search
    method and heuristic.
    """
    print 'Initial state'
    initial.show()
    solvable = initial.is_solvable()
    print 'Is this puzzle solvable? {}\n'.format(solvable)

    if solvable:
        goal = NPuzzle(initial.K, range(initial.K**2))

        expanded, steps, path = search(initial, goal, heuristic)
        print_solution(expanded, steps, path)

def generate_random_states(fname, amount, K = 3):
    with open(fname, 'w') as f:
        d = {}
        for i in range(amount):
            state = NPuzzle(K)
            while not state.is_solvable() and state not in d:
                state = NPuzzle(K)
            d[state] = 1
            f.write('{}\n'.format(state))

def write_heuristics_data(start, n, res_fname, states_fname='data/states.txt', search=a_star, h_name='linear_conflict', heuristic=NPuzzle.linear_conflict):
    """
    Write a file with information on states, depths, expanded nodes, and
    running time for the 3 heuristics implemented on a specific search method.
    """
    from ProgressBar import ProgressBar
    import time
    import re

    with open(res_fname, 'a') as res_f, open(states_fname, 'r') as s_f:
        K = 3
        goal = NPuzzle(K, range(K*K))

        for i in range(start):
            s_f.readline()

        print 'Reading states from file {:s}'.format(states_fname)
        print 'Writing {} states data to file {:s}'.format(n, res_fname)

        pb = ProgressBar() # a simple pogressbar
        pb.start()

        f_format = '{};{};{};{}\n'
        if start == 0:
            columns = ['state', 'steps', h_name + '_nodes', h_name + '_time']
            res_f.write(f_format.format(*columns))

        for i in range(n - start):
            state_str = s_f.readline().strip()
            state = [int (b) for b in re.findall('[0-9]+', state_str)]
            initial = NPuzzle(3, state)

            percent = float(i+start)/(n)
            pb.update(percent)

            try:
                init_time1 = time.time()
                n1, s1, path1 = search(initial, goal, heuristic)
                end_time1 = time.time()
                t1 = end_time1 - init_time1
            except KeyboardInterrupt:
                break
            except:
                t1 = 'NaN'
                n1 = 'NaN'
                s1 = 'NaN'

            res_f.write(f_format.format(initial, s1, n1, t1))
            res_f.flush()
        pb.finish()

def print_analysis(fname='heuristics_data.csv'):
    """
    Print statistical analysis of the file created by the write_heuristics_data
    function.
    """
    import pandas as pd
    data = pd.read_csv(fname, sep=';')
    #print data
    #print data['state']
    print data.describe()

if __name__ == '__main__':
    pass

