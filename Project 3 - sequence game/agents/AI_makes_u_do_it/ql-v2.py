from template import Agent
import random
import sys

# record the board
my_board = []
for i in range(10):
    my_board.append([])
    for j in range(10):
        my_board[i].append(0)

# dictionary sequence of board
chess_location = {'jk': (9, 9, 0, 0), '2s': (8, 6, 0, 1), '3s': (8, 5, 0, 2), '4s': (8, 4, 0, 3), '5s': (8, 3, 0, 4), '6s': (8, 2, 0, 5), '7s': (8, 1, 0, 6), '8s': (7, 1, 0, 7), '9s': (6, 1, 0, 8), '6c': (3, 2, 1, 0), '5c': (3, 3, 1, 1), '4c': (3, 4, 1, 2), '3c': (3, 5, 1, 3), '2c': (3, 6, 1, 4), 'ah': (4, 6, 1, 5), 'kh': (5, 6, 1, 6), 'qh': (1, 7, 6, 6), 'th': (6, 5, 1, 8), 'ts': (5, 1, 1, 9), '7c': (4, 2, 2, 0), 'as': (4, 9, 2, 1), '2d': (5, 9, 2, 2), '3d': (6, 9, 2, 3), '4d': (7, 9, 2, 4), '5d': (8, 9, 2, 5), '6d': (9, 8, 2, 6), '7d': (9, 7, 2, 7), '9h': (6, 4, 2, 8), 'qs': (4, 1, 2, 9), '8c': (5, 2, 3, 0), 'ks': (3, 1, 3, 9), '8d': (9, 6, 3, 7), '8h': (6, 3, 3, 8), '9c': (6, 2, 4, 0), '6h': (5, 8, 4, 3), '5h': (6, 8, 4, 4), '4h': (7, 8, 4, 5), '9d': (9, 5, 4, 7), '7h': (5, 3, 4, 8), 'tc': (7, 2, 5, 0), '2h': (8, 7, 5, 4), '3h': (8, 8, 5, 5), 'td': (9, 4, 5, 7), 'qc': (7, 3, 6, 0), 'qd': (9, 3, 6, 7), 'kc': (7, 4, 7, 0), 'ac': (8, 0, 7, 5), 'ad': (9, 1, 7, 6), 'kd': (9, 2, 7, 7)}

rotation = {'up': (-1,0), 'up_right': (-1, 1), 'right': (0, 1), 'right_down': (1, 1), 'down': (1, 0), 'down_left': (1, -1), 'left': (0, -1), 'left_up': (-1, -1)}


class Logger(object):
    def __init__(self, filename="print.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

vr = [(-4,0),(-3,0),(-2,0),(-1,0),(0,0),(1,0),(2,0),(3,0),(4,0)]
hz = [(0,-4),(0,-3),(0,-2),(0,-1),(0,0),(0,1),(0,2),(0,3),(0,4)]
d1 = [(-4,-4),(-3,-3),(-2,-2),(-1,-1),(0,0),(1,1),(2,2),(3,3),(4,4)]
d2 = [(-4,4),(-3,3),(-2,2),(-1,1),(0,0),(1,-1),(2,-2),(3,-3),(4,-4)]

class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.id = _id
        sys.stdout = Logger('print.txt')
        self.yes = _id % 2 + 1
        self.no = 3 - self.yes

    # obtain the board and output
    def get_board(self, plr):
        l_r = plr['r']
        l_b = plr['b']

        # clear
        for i in range(10):
            for j in range(10):
                my_board[i][j] = 0
        my_board[0][0] = self.yes
        my_board[0][9] = self.yes
        my_board[9][0] = self.yes
        my_board[9][9] = self.yes

        # record board for red and blue teams
        for i in range(len(l_r)):
            x, y = l_r[i]
            my_board[x][y] = self.yes
        for i in range(len(l_b)):
            x, y = l_b[i]
            my_board[x][y] = self.no

    # get actions based on the card name
    def get_action(self, char):
        actions = []
        Action = {}
        Action['play_card'] = char
        Action['draft_card'] = None
        if char == 'jh' or char == 'js':
            Action['type'] = 'remove'
            for i in range(10):
                for j in range(10): # remove cards on the opponents positions
                    if my_board[i][j] == self.no:
                        Action['coords'] = (i, j)
                        actions.append(Action)
        elif char == 'jd' or char == 'jc':
            Action['type'] = 'place'
            for i in range(10):
                for j in range(10):  # alternative positions to place cards
                    if my_board[i][j] == 0:
                        Action['coords'] = (i, j)
                        actions.append(Action)
        else:
            x1, y1, x2, y2 = chess_location[char]
            if my_board[x1][y1] == 0:
                Action['type'] = 'place'
                Action['coords'] = (x1, y1)
                actions.append(Action)
            if my_board[x2][y2] == 0:
                Action['type'] = 'place'
                Action['coords'] = (x2, y2)
                actions.append(Action)

        # 一个动作都没加上，是死牌，这张牌就没必要取了，即返回None牌，注意，自定的action集合中类型添加了None
        if len(actions) == 0:
            Action['type'] = None
            Action['coords'] = None
            actions.append(Action)

        return actions

    # place card
    def cal_value(self, x, y, gama):
        value = -1
        # calculate the density, start at the corner
        for seq, seq_name in [(vr, 'vr'), (hz, 'hz'), (d1, 'd1'), (d2, 'd2')]:
            coord_list = [(r + x, c + y) for r, c in seq]
            coord_list = [i for i in coord_list if 0 <= min(i) and 9 >= max(i)]
            for add_x, add_y in coord_list:
                if my_board[add_x][add_y] == self.yes:
                    value += 1

        # calculate center positions
        if (x, y) == (4, 4) or (x, y) == (4, 5) or (x, y) == (5, 4) or (x, y) == (5, 5):
            value += 3.5  # choose center
        value = value * gama
        return value

    # remove
    def delete_value(self, x, y, gama):
        value = 0
        # calclate the around players cards
        sx = int(x / 2)
        sy = int(y / 2)
        for i in range(sx, sx + 5):
            for j in range(sy, sy + 5):
                if my_board[i][j] == self.no:
                    value += 0.5

        value = value * gama
        return value

    def recursive(self, Action, gama):
        value = 0
        x = -1
        y = -1
        if Action['type'] == 'place':
            x, y = Action['coords']
            value = self.cal_value(x, y, gama)

        if Action['type'] == 'remove':
            x, y = Action['coords']
            if my_board[x][y] == self.no:
                value = self.delete_value(x, y, gama)

        # avoid to take dead card
        if Action['type'] == None:
            return -1

        # recursive
        if x == -1 or Action['draft_card'] == None:
            return value
        actions = self.get_action(Action['draft_card'])
        my_board[x][y] = self.yes
        for Action in actions:
            value += self.recursive(Action, 0.95)

        my_board[x][y] = 0

        return value

    def SelectAction(self, actions, game_state):

        board = game_state.board
        self.get_board(board.plr_coords)

        value = []
        record_i = []
        num = 2
        for k in range(num):  # two episodes
            value.append(-1)
            record_i.append(0)
        # calculate valuses for the first q table， calculate each values
            for i in range(len(actions)):
                Action = actions[i]
                #  the gamma in the first time is 1
                new_value = self.recursive(Action, 1) # discount factory
                if new_value > value[k]:
                    value[k] = new_value
                    record_i[k] = i

        for k in range(1, num):
            if value[k] > value[k-1]:
                return actions[record_i[k]]

        return actions[record_i[0]]

