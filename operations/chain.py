import sys

from abc import abstractmethod
from operations.command import Command

class Chain(object):
    def __init__(self, nextOp=None):
        self.next = nextOp

        self.command = Command()
    
    def exec(self, config={}):
        exit_code = 0

        try:
            exit_code = self._exec(config=config)
        except Exception as e:
            print('[error] Received error from executing: {}'.format(e), file=sys.stderr)

            return 1

        if exit_code > 0:
            print('[error] Exit code is non-zero: {}'.format(exit_code), file=sys.stderr)

            return exit_code

        if  self.next != None:
            exit_code = self.next.exec(config=config)

        return exit_code
    
    @abstractmethod
    def _exec(self, config={}):
        pass