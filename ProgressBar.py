#!/usr/bin/env python
#coding: utf-8

import sys

class ProgressBar(object):
    def __init__(self, bar_length=50, progress_symbol='#', space_symbol='-'):
        self.length = bar_length
        self.symbol = progress_symbol
        self.space = space_symbol
        self.text = '\rProgress [{:s}] {:4.1f}%'

    def start(self):
        sys.stdout.write(self.text.format(self.space * self.length , 0.0))
        sys.stdout.flush()

    def finish(self):
        sys.stdout.write(self.text.format(self.symbol * self.length , 100.0) + '\n')
        sys.stdout.flush()

    def update(self, percent):
        """
        changes the progress bar to reflect the value in percent, percent must
        be a value between 0 and 1, a cast to float will be be done regardless
        of its value.
        """
        percent = float(percent)
        if percent < 0:
            percent = 0.0
        elif percent > 1:
            percent = 1.0
        symbols = self.symbol * int(round(percent * self.length))
        spaces = self.space * (self.length - len(symbols))

        sys.stdout.write(self.text.format(symbols + spaces, percent*100.0))
        sys.stdout.flush()

if __name__ == '__main__':
    pass
