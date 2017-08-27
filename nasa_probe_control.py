import sys
from itertools import islice


def execute():
    map_size = sys.argv[1:3]
    commands = sys.argv[3:]
    controller = Controller(map_size[0], map_size[1])
    splited_params = split_every(4, commands)
    for parameter in splited_params:

        probe = Probe(parameter[0], parameter[1], parameter[2])
        commands = parameter[3]

        for command in list(commands):
            if command.upper() == 'M':
                next_moviment = controller.get_next_moviment(probe)
                probe.move(next_moviment)
            else:
                probe.set_direction(command)

        print(probe.position, probe.direction)


class Direction(object):
    """
      N
    W   E
      S
    """
    
    west = {'x': -1, 'y': 0}
    north = {'x': 0, 'y': 1}
    east = {'x': 1, 'y': 0}
    south = {'x': 0, 'y': -1}

    get_pos = {'W': west, 'N': north, 'E': east, 'S': south}

    @staticmethod
    def get_next_direction(command, current_position):
        command_reference = {"L": -1, "R": 1}
        position_order = ['W', 'N', 'E', 'S']
        it = command_reference[command]

        index = position_order.index(current_position)
        next_index = index+it
        if next_index == len(position_order):
            next_index = 0

        return position_order[next_index]


class Probe(object):
    position = (0, 0)
    direction = 'N'

    def __init__(self, x, y, d):
        self.position = (int(x), int(y))
        self.direction = d.upper()
        print("Starting probe in {} in direction {}".format(self.position,
                                                            self.direction))

    def move(self, moviment):
        self.position = (self.position[0] + moviment['x'],
                         self.position[1] + moviment['y'])

    def calcule_next_position(self, moviment):
        return (self.position[0] + moviment['x'],
                self.position[1] + moviment['y'])

    def set_direction(self, command):
        self.direction = Direction.get_next_direction(command, self.direction)


class Controller(object):
    map_size = (5,5)
       
    def __init__(self, x, y):
        self.map_size = (int(x), int(y))

    def get_next_moviment(self, probe):
        move = Direction.get_pos[probe.direction]
        next_position = probe.calcule_next_position(move)

        if next_position[0] not in range(0, self.map_size[0]+1) or \
           next_position[1] not in range(0, self.map_size[1]+1):
            return {"x": 0, "y": 0}
        return move


def split_every(n, iterable):
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))

if __name__ == '__main__':
    """Usage exemple: python3 nasa_probe_control.py 5 5 1 2 N LMLMLMLMM 3 3 E MMRMMRMRRM """
    execute()

