#!/usr/bin/env python
#coding: utf-8

from copy import copy
from random import shuffle

class NPuzzle(object):
    _coordinates = None

    def __init__(self, K, state=None):
        self.K = K
        if state is None:
            self.state = self.random_state()
        elif len(state) == K**2:
            self.state = state
        else:
            raise ValueError('Board must be square')

        if self._coordinates is None:
            self._initialize_coordinates()
        self.hash_value = None

    def __hash__(self):
        if self.hash_value is None:
            self.hash_value = hash(tuple(self.state))
        return self.hash_value

    def __eq__(self, other):
        return self.state == other.state

    def __repr__(self):
        return '{}'.format(self.state)

    def show(self):
        for i in range(self.K):
            for e in self.state[i*self.K:(i+1)*self.K]:
                print '{:2d}'.format(e),
            print ''
        print ''

    @property
    def coordinates(self):
        return self._coordinates
    @coordinates.setter
    def coordinates(self, value):
        self._coordinates = value

    def _initialize_coordinates(self):
        #print 'I ran'
        if NPuzzle._coordinates is None:
            d = {}
            for i in range (self.K):
                for j in range(self.K):
                    index = i*self.K + j
                    d[index] = (i, j)
                    d[(i, j)] = index
            NPuzzle._coordinates = d

    def random_state(self):
        state = range(self.K**2)
        shuffle(state)
        return state

    def __get_successor(self, action, blank, swap):
        state = copy(self.state)
        state[blank], state[swap] = state[swap], state[blank]
        return action, NPuzzle(self.K, state)

    def get_successors(self, random_shuffle=False):
        K = self.K
        successors = []
        blank = self.state.index(0)

        # if the 0 is not on the top line move up
        if blank >= K:
            up = blank - K
            successors.append(self.__get_successor('UP', blank, up))

        # if the blank is not on the bottom line move down
        if blank < len(self.state) - K:
            down = blank + K
            successors.append(self.__get_successor('DOWN', blank, down))

        # if the blank is not on the leftmost column move left
        if blank % K > 0:
            left = blank - 1
            successors.append(self.__get_successor('LEFT', blank, left))

        # if the blank is not on the rightmost column move right
        if blank % K < K - 1:
            right = blank + 1
            successors.append(self.__get_successor('RIGHT', blank, right))

        if random_shuffle:
            shuffle(successors)

        return successors

    def hamming_distance(self, goal):
        distance = 0
        for i, e in enumerate(goal.state):
            if e == 0: continue
            if e != self.state[i]:
                distance += 1
        return distance

    def manhattan_distance(self, goal):
        distance = 0
        for i, e in enumerate(goal.state):
            if e == 0: continue
            goal_l, goal_c = NPuzzle._coordinates[i]
            index = self.state.index(e)
            cur_l, cur_c = NPuzzle._coordinates[index]
            distance += abs(goal_l - cur_l) + abs(goal_c - cur_c)
        return distance

    def _check_conflicts(self, conflicts, goal, lower_bound, upper_bound, step):
        for i in range(lower_bound, upper_bound, step):
            value_i = self.state[i]
            if i not in conflicts and value_i != 0 and value_i in goal:
                for j in range(i + step, upper_bound, step):
                    value_j = self.state[j]
                    if value_j != 0 and value_i > value_j and value_j in goal:
                        conflicts[j] = 1

    def linear_conflict(self, goal):
        conflicts = {}
        K = self.K
        max_K = K*K

        for i in range(K):
            # check row conflicts
            lower_bound = i*K
            upper_bound = K*(i+1)
            step = 1
            goal_row = goal.state[lower_bound:upper_bound]

            self._check_conflicts(conflicts, goal_row, lower_bound, upper_bound, step)

            # check column conflicts
            lower_bound = i
            upper_bound = max_K
            step = K
            goal_column = goal.state[lower_bound::K]

            self._check_conflicts(conflicts, goal_column, lower_bound, upper_bound, step)

        distance = self.manhattan_distance(goal)
        distance += 2*len(conflicts)
        return distance

    def gaschnig(self, goal):
        """
        AKA n-max swap heuristic. Assumes the goal is range(K*K). this
        heuristic dominates the hamming distance heuristic.
        """
        cur_state = copy(self.state)
        g_state = goal.state
        blank = 0

        moves = 0
        while cur_state != g_state:
            #print cur_state, moves
            blank_index = cur_state.index(blank)
            if blank_index == 0:
                for i, e in enumerate(cur_state):
                    if i != e:
                        swap = i
            else:
                swap = cur_state.index(blank_index)

            moves += 1
            #print 'swap {} e {}'.format(cur_state[swap], cur_state[blank_index])
            cur_state[swap], cur_state[blank_index] = cur_state[blank_index], cur_state[swap]
        #print cur_state, moves
        return moves

    def tiles_out(self, goal):
        K = self.K
        value = 0
        for i, e in enumerate(self.state):
            if e == 0: continue

            c_line, c_col = self._coordinates[i]
            g_line, g_col = self._coordinates[e]

            if c_line != g_line:
                #print '{} is out of line'.format(e)
                value += 1
            if c_col != g_col:
                #print '{} is out of column'.format(e)
                value += 1
        return value

    def is_solvable(self):
        """
        Checks if the state of the puzzle is solvable. For boards of even width,
        the goal state must be of the kind [0, 1, ..., (K*K-1)], otherwise if the
        blank is the last block then the result is the oposite of this functions
        result.
        """
        inversions = 0
        state = self.state
        size = self.K**2
        for i in range(size):
            if not state[i]: continue # ignores blank
            for j in range(i+1, size):
                if not state[j]: continue # ignores blank
                if state[i] > state[j]:
                    inversions += 1

        # a puzzle is solvable:
        # if the board width is odd and the inversions number is even
        #   then the puzzle is solvable
        # if the board width is even then
        #   if the blank is in an even row with an even number of inversions, or
        #   if the blank is in an odd row with an odd number of inversions
        #       then the puzzle is solvable.
        # it is unsolvable otherwise
        if self.K % 2 == 0: # width is even
            blank = self.state.index(0)
            i, j = NPuzzle._coordinates[blank]

            if (i % 2 == 0) == (inversions % 2 == 0):
                return True
            else:
                return False
        else: # width is odd
            if inversions % 2 == 0:
                return True
            else:
                return False

if __name__ == '__main__':
    import timeit
    print timeit.timeit('state=NPuzzle(3); d = state.hamming_distance(goal)', setup='from NPuzzle import NPuzzle; goal = NPuzzle(3, range(3**2))', number=100000)
    print timeit.timeit('state=NPuzzle(3); d = state.manhattan_distance(goal)', setup='from NPuzzle import NPuzzle; goal = NPuzzle(3, range(3**2))', number=100000)
    print timeit.timeit('state=NPuzzle(3); d = state.linear_confict(goal)', setup='from NPuzzle import NPuzzle; goal = NPuzzle(3, range(3**2))', number=100000)
