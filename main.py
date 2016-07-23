#!/usr/bin/env python
#coding: utf-8

from NPuzzle import NPuzzle
from misc import print_analysis
from misc import read_input
from misc import solve
from misc import write_heuristics_data
from search import a_star
from search import a_star_tree
from search import ida_star
import argparse

def create_parser():
    d = 'Solver for the NPuzzle problem.'
    op_h = 'Select what to do: *solve : solve from file or random state if none given ; * write : write data on all heuristics to a file ; *analyse : analyses the data from a file'
    h_h = 'Select the heuristic used, default is manhattan ; *hamming ; *manhattan ; *linear_conflict'
    m_h = 'Select the search method used, default is a_star ; *a_star ; *ida_star'
    f_h = 'Path to a file depending on the func maybe input or output'
    da_h = 'Amount of states for the write data functionality'

    parser = argparse.ArgumentParser(description=d)

    parser.add_argument('func', help=op_h)
    parser.add_argument('-he', '--heuristic', dest='heuristic',
            help=h_h, default='manhattan')
    parser.add_argument('-m', '--search_method', dest='method',
            help=m_h, default='a_star')
    parser.add_argument('-f', '--file', dest='fname',
            help=f_h)
    parser.add_argument('-amt', '--amount', dest='amount',
            help=da_h, type=int)
    parser.add_argument('-s', '--start', dest='start',
            help=da_h, type=int, default=0)

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.method == 'ida_star':
        method = ida_star
    elif args.method == 'a_star':
        method = a_star
    elif args.method == 'a_star_tree':
        method = a_star_tree
    else:
        parser.print_help()
        exit()
    method_text = 'Selected method: {}'

    if args.heuristic == 'manhattan':
        heuristic = NPuzzle.manhattan_distance
    elif args.heuristic == 'linear_conflict':
        heuristic = NPuzzle.linear_conflict
    elif args.heuristic == 'hamming':
        heuristic = NPuzzle.hamming_distance
    elif args.heuristic == 'gaschnig':
        heuristic = NPuzzle.gaschnig
    elif args.heuristic == 'tiles_out':
        heuristic = NPuzzle.tiles_out
    else:
        parser.print_help()
        exit()
    heuristic_text = 'Selected heuristic: {}'

    if 'solve' == args.func:
        print heuristic_text.format(args.heuristic)
        print method_text.format(args.method)
        if args.fname:
            f = open(args.fname)
            initial = read_input(f)
        else:
            initial = NPuzzle(3)
        solve(initial, search=method, heuristic=heuristic)

    elif args.func == 'write':
        print heuristic_text.format(args.heuristic)
        fname = args.fname
        amount = args.amount
        if fname is None or amount is None:
            print 'Output file and amount os states required. Ex: write -f data.csv -amt 15'
            exit()

        print method_text.format(args.method)
        write_heuristics_data(start=args.start, n=amount, search=method, res_fname=fname, h_name=args.heuristic, heuristic=heuristic)
        print_analysis(fname)

    elif args.func == 'analyse':
        fname = args.fname
        if fname is None:
            print 'Input file required. Ex: analyse -f data.csv'
            exit()
        print_analysis(fname)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
