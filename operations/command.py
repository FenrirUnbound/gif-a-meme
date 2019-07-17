import os

class Command(object):
    def __init__(self):
        pass

    def run(self, cmd, args=[]):
        command_parts = [cmd]
        command_parts.extend(args)
        command = ' '.join(str(input) for input in command_parts)

        exit_code = os.system(command=command)
        return exit_code