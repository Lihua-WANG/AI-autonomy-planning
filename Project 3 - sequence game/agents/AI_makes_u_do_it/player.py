from template import Agent
import random
import copy
from Sequence.sequence_model import COORDS
import math
import heapq
from Sequence.sequence_model import SequenceGameRule as GameRule


class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


def inadmissibleHeuristic(colour, coord, game_state):
    if colour == 'r':
        opponent = 'b'
    else:
        opponent = 'r'
    chips = game_state.board.chips
    occupation = 0
    special_case = False

    # center_distance
    r, c = coord
    center_distance = abs(r - 4.5) + abs(c - 4.5)

    # special case
    if coord == (4,4) or coord == (4,5) or coord == (5,4) or coord == (5,5):
        if chips[4][4] != opponent and chips[4][5] != opponent and chips[5][4] != opponent and chips[5][5] != opponent:
            special_case = True
    if special_case:
        if chips[4][4] == colour:
            occupation += 1
        if chips[4][5] == colour:
            occupation += 1
        if chips[5][4] == colour:
            occupation += 1
        if chips[5][5] == colour:
            occupation += 1
        return 3-occupation

    # horizontal
    row_p = coord[0]
    column_p = coord[1]
    while column_p > coord[1]-4 and column_p >= 1:
        column_p -= 1
        if chips[row_p][column_p] == opponent:
            break
        if chips[row_p][column_p] == colour or chips[row_p][column_p] == '#':
            occupation += 1
    row_p = coord[0]
    column_p = coord[1]
    while column_p < coord[1]+4 and column_p <= 8:
        column_p += 1
        if chips[row_p][column_p] == opponent:
            break
        if chips[row_p][column_p] == colour or chips[row_p][column_p] == '#':
            occupation += 1

    # vertical
    row_p = coord[0]
    column_p = coord[1]
    while row_p > coord[0]-4 and row_p >= 1:
        row_p -= 1
        if chips[row_p][column_p] == opponent:
            break
        if chips[row_p][column_p] == colour or chips[row_p][column_p] == '#':
            occupation += 1
    row_p = coord[0]
    column_p = coord[1]
    while row_p < coord[0]+4 and row_p <= 8:
        row_p += 1
        if chips[row_p][column_p] == opponent:
            break
        if chips[row_p][column_p] == colour or chips[row_p][column_p] == '#':
            occupation += 1

    # upleft-downright
    row_p = coord[0]
    column_p = coord[1]
    while column_p > coord[1]-4 and column_p >= 1 and row_p > coord[0]-4 and row_p >= 1:
        column_p -= 1
        row_p -= 1
        if chips[row_p][column_p] == opponent:
            break
        if chips[row_p][column_p] == colour or chips[row_p][column_p] == '#':
            occupation += 1
    row_p = coord[0]
    column_p = coord[1]
    while column_p < coord[1]+4 and column_p <= 8 and row_p < coord[0]+4 and row_p <= 8:
        column_p += 1
        row_p += 1
        if chips[row_p][column_p] == opponent:
            break
        if chips[row_p][column_p] == colour or chips[row_p][column_p] == '#':
            occupation += 1

    # downleft-upright
    row_p = coord[0]
    column_p = coord[1]
    while column_p > coord[1]-4 and column_p >= 1 and row_p < coord[0]+4 and row_p <= 8:
        column_p -= 1
        row_p += 1
        if chips[row_p][column_p] == opponent:
            break
        if chips[row_p][column_p] == colour or chips[row_p][column_p] == '#':
            occupation += 1
    row_p = coord[0]
    column_p = coord[1]
    while column_p < coord[1]+4 and column_p <= 8 and row_p > coord[0]-4 and row_p >= 1:
        column_p += 1
        row_p -= 1
        if chips[row_p][column_p] == opponent:
            break
        if chips[row_p][column_p] == colour or chips[row_p][column_p] == '#':
            occupation += 1

    return 32-occupation + 0.1 * center_distance


def seq_evaluation(colour, coord, chips):
    if colour == 'r':
        opp_colour = 'b'
        seq = 'X'
        opp_seq = 'O'
    else:
        opp_colour = 'r'
        seq = 'O'
        opp_seq = 'X'
    center = [(4,4),(4,5),(5,4),(5,5)]

    # center_distance
    r, c = coord
    center_distance = abs(r - 4.5) + abs(c - 4.5)

    # center
    center_count = 0
    center_opp_count = 0
    if coord in center:
        center.remove(coord)
        for center_coord in center:
            if center_coord == colour or center_coord == seq:
                center_count += 1
            if center_coord == opp_colour or center_coord == opp_seq:
                center_opp_count += 1
        if center_count == 3:
            return 0 + 0.1 * center_distance
        if center_opp_count == 3:
            return 2 + 0.1 * center_distance
        """if center_count == 2:
            return 4 + 0.1 * center_distance
        if center_opp_count == 2:
            return 6 + 0.1 * center_distance"""

    # sequence
    up_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r - i < 0:
            break
        elif chips[r - i][c] == colour or chips[r - i][c] == '#':
            up_count += 1
        elif chips[r - i][c] == seq and not completed_use:
            up_count += 1
            completed_use = True
        else:
            break

    down_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r + i > 9:
            break
        elif chips[r + i][c] == colour or chips[r + i][c] == '#':
            down_count += 1
        elif chips[r + i][c] == seq and not completed_use:
            down_count += 1
            completed_use = True
        else:
            break

    left_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if c - i < 0:
            break
        elif chips[r][c - i] == colour or chips[r][c - i] == '#':
            left_count += 1
        elif chips[r][c - i] == seq and not completed_use:
            left_count += 1
            completed_use = True
        else:
            break

    right_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if c + i > 9:
            break
        elif chips[r][c + i] == colour or chips[r][c + i] == '#':
            right_count += 1
        elif chips[r][c + i] == seq and not completed_use:
            right_count += 1
            completed_use = True
        else:
            break

    upleft_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r - i < 0 or c - i < 0:
            break
        elif chips[r - i][c - i] == colour or chips[r - i][c - i] == '#':
            upleft_count += 1
        elif chips[r - i][c - i] == seq and not completed_use:
            upleft_count += 1
            completed_use = True
        else:
            break

    downright_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r + i > 9 or c + i > 9:
            break
        elif chips[r + i][c + i] == colour or chips[r + i][c + i] == '#':
            downright_count += 1
        elif chips[r + i][c + i] == seq and not completed_use:
            downright_count += 1
            completed_use = True
        else:
            break

    upright_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r - i < 0 or c + i > 9:
            break
        elif chips[r - i][c + i] == colour or chips[r - i][c + i] == '#':
            upright_count += 1
        elif chips[r - i][c + i] == seq and not completed_use:
            upright_count += 1
            completed_use = True
        else:
            break

    downleft_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r + i > 9 or c - i < 0:
            break
        elif chips[r + i][c - i] == colour or chips[r + i][c - i] == '#':
            downleft_count += 1
        elif chips[r + i][c - i] == seq and not completed_use:
            downleft_count += 1
            completed_use = True
        else:
            break

    ver_seq = up_count + down_count + 1
    if ver_seq > 5: ver_seq = 5
    hor_seq = left_count + right_count + 1
    if hor_seq > 5: hor_seq = 5
    dia1_seq = upleft_count + downright_count + 1
    if dia1_seq > 5: dia1_seq = 5
    dia2_seq = upright_count + downleft_count + 1
    if dia2_seq > 5: dia2_seq = 5

    seq_list = [ver_seq, hor_seq, dia1_seq, dia2_seq]
    for seq_value in seq_list:
        if seq_value == 5:
            return 1 + 0.1 * center_distance

    # opp_sequence
    up_opp_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r - i < 0:
            break
        elif chips[r - i][c] == opp_colour or chips[r - i][c] == '#':
            up_opp_count += 1
        elif chips[r - i][c] == opp_seq and not completed_use:
            up_opp_count += 1
            completed_use = True
        else:
            break

    down_opp_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r + i > 9:
            break
        elif chips[r + i][c] == opp_colour or chips[r + i][c] == '#':
            down_opp_count += 1
        elif chips[r + i][c] == opp_seq and not completed_use:
            down_opp_count += 1
            completed_use = True
        else:
            break

    left_opp_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if c - i < 0:
            break
        elif chips[r][c - i] == opp_colour or chips[r][c - i] == '#':
            left_opp_count += 1
        elif chips[r][c - i] == opp_seq and not completed_use:
            left_opp_count += 1
            completed_use = True
        else:
            break

    right_opp_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if c + i > 9:
            break
        elif chips[r][c + i] == opp_colour or chips[r][c + i] == '#':
            right_opp_count += 1
        elif chips[r][c + i] == opp_seq and not completed_use:
            right_opp_count += 1
            completed_use = True
        else:
            break

    upleft_opp_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r - i < 0 or c - i < 0:
            break
        elif chips[r - i][c - i] == opp_colour or chips[r - i][c - i] == '#':
            upleft_opp_count += 1
        elif chips[r - i][c - i] == opp_seq and not completed_use:
            upleft_opp_count += 1
            completed_use = True
        else:
            break

    downright_opp_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r + i > 9 or c + i > 9:
            break
        elif chips[r + i][c + i] == opp_colour or chips[r + i][c + i] == '#':
            downright_opp_count += 1
        elif chips[r + i][c + i] == opp_seq and not completed_use:
            downright_opp_count += 1
            completed_use = True
        else:
            break

    upright_opp_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r - i < 0 or c + i > 9:
            break
        elif chips[r - i][c + i] == opp_colour or chips[r - i][c + i] == '#':
            upright_opp_count += 1
        elif chips[r - i][c + i] == opp_seq and not completed_use:
            upright_opp_count += 1
            completed_use = True
        else:
            break

    downleft_opp_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r + i > 9 or c - i < 0:
            break
        elif chips[r + i][c - i] == opp_colour or chips[r + i][c - i] == '#':
            downleft_opp_count += 1
        elif chips[r + i][c - i] == opp_seq and not completed_use:
            downleft_opp_count += 1
            completed_use = True
        else:
            break

    ver_opp_seq = up_opp_count + down_opp_count + 1
    if ver_opp_seq > 5: ver_opp_seq = 5
    hor_opp_seq = left_opp_count + right_opp_count + 1
    if hor_opp_seq > 5: hor_opp_seq = 5
    dia1_opp_seq = upleft_opp_count + downright_opp_count + 1
    if dia1_opp_seq > 5: dia1_opp_seq = 5
    dia2_opp_seq = upright_opp_count + downleft_opp_count + 1
    if dia2_opp_seq > 5: dia2_opp_seq = 5

    seq_opp_list = [ver_opp_seq, hor_opp_seq, dia1_opp_seq, dia2_opp_seq]
    for seq_opp_value in seq_opp_list:
        if seq_opp_value == 5:
            return 3 + 0.1 * center_distance

    return 8 + 0.1 * center_distance


def remove_evaluation(colour, coord, chips):
    if colour == 'r':
        opp_colour = 'b'
        seq = 'X'
        opp_seq = 'O'
    else:
        opp_colour = 'r'
        seq = 'O'
        opp_seq = 'X'
    center = [(4,4),(4,5),(5,4),(5,5)]

    # center_distance
    r, c = coord
    center_distance = abs(r - 4.5) + abs(c - 4.5)

    # center
    center_count = 0
    center_opp_count = 0
    if coord in center:
        center.remove(coord)
        for center_coord in center:
            if center_coord == colour or center_coord == seq:
                center_count += 1
            if center_coord == opp_colour or center_coord == opp_seq:
                center_opp_count += 1
        if center_count == 2 and center_opp_count == 0:
            return 0 + 0.1 * center_distance

    # sequence
    up_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r - i < 0:
            break
        elif chips[r - i][c] == colour or chips[r - i][c] == '#':
            up_count += 1
        elif chips[r - i][c] == seq and not completed_use:
            up_count += 1
            completed_use = True
        else:
            break

    down_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r + i > 9:
            break
        elif chips[r + i][c] == colour or chips[r + i][c] == '#':
            down_count += 1
        elif chips[r + i][c] == seq and not completed_use:
            down_count += 1
            completed_use = True
        else:
            break

    left_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if c - i < 0:
            break
        elif chips[r][c - i] == colour or chips[r][c - i] == '#':
            left_count += 1
        elif chips[r][c - i] == seq and not completed_use:
            left_count += 1
            completed_use = True
        else:
            break

    right_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if c + i > 9:
            break
        elif chips[r][c + i] == colour or chips[r][c + i] == '#':
            right_count += 1
        elif chips[r][c + i] == seq and not completed_use:
            right_count += 1
            completed_use = True
        else:
            break

    upleft_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r - i < 0 or c - i < 0:
            break
        elif chips[r - i][c - i] == colour or chips[r - i][c - i] == '#':
            upleft_count += 1
        elif chips[r - i][c - i] == seq and not completed_use:
            upleft_count += 1
            completed_use = True
        else:
            break

    downright_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r + i > 9 or c + i > 9:
            break
        elif chips[r + i][c + i] == colour or chips[r + i][c + i] == '#':
            downright_count += 1
        elif chips[r + i][c + i] == seq and not completed_use:
            downright_count += 1
            completed_use = True
        else:
            break

    upright_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r - i < 0 or c + i > 9:
            break
        elif chips[r - i][c + i] == colour or chips[r - i][c + i] == '#':
            upright_count += 1
        elif chips[r - i][c + i] == seq and not completed_use:
            upright_count += 1
            completed_use = True
        else:
            break

    downleft_count = 0
    completed_use = False
    for i in range(5)[1:]:
        if r + i > 9 or c - i < 0:
            break
        elif chips[r + i][c - i] == colour or chips[r + i][c - i] == '#':
            downleft_count += 1
        elif chips[r + i][c - i] == seq and not completed_use:
            downleft_count += 1
            completed_use = True
        else:
            break

    ver_seq = up_count + down_count + 1
    if ver_seq > 5: ver_seq = 5
    hor_seq = left_count + right_count + 1
    if hor_seq > 5: hor_seq = 5
    dia1_seq = upleft_count + downright_count + 1
    if dia1_seq > 5: dia1_seq = 5
    dia2_seq = upright_count + downleft_count + 1
    if dia2_seq > 5: dia2_seq = 5

    seq_list = [ver_seq, hor_seq, dia1_seq, dia2_seq]
    for seq_value in seq_list:
        if seq_value == 4:
            return 1 + 0.1 * center_distance

    return 2 + 0.1 * center_distance


def heuristic(game_state,agent_id):
    if agent_id == 0 or agent_id == 2:
        colour = 'r'
        my_seq = 'X'
        opponent = 'b'
        opp_seq = 'O'
        completed_seq = game_state.agents[0].completed_seqs + game_state.agents[2].completed_seqs
    else:
        colour = 'b'
        my_seq = 'O'
        opponent = 'r'
        opp_seq = 'X'
        completed_seq = game_state.agents[1].completed_seqs + game_state.agents[3].completed_seqs

    if completed_seq == 2:
        return 0

    chips = game_state.board.chips
    max_sequence = 0

    # Special case
    center_chips = [chips[4][4],chips[4][5],chips[5][4],chips[5][5]]
    center_remain = 0
    center = False
    for center_chip in center_chips:
        if center_chip == colour or center_chip == my_seq:
            center = True
            break
        if center_chip == '_':
            center_remain += 1
        if center_chip == opponent:
            center_remain += 2

    # Normal case
    coords = []
    for i in range(10):
        for j in range(10):
            coords.append((i,j))
    # if we have no chip identified:
    if max_sequence == 0:
        for line in chips:
            for chip in line:
                if chip == colour or chip == my_seq:
                    max_sequence = 1
                    break
            if max_sequence == 1: break

    # if we have find a chip
    if max_sequence == 1:
        hor = [(0,0),(0,1)]
        ver = [(0,0),(1,0)]
        dia1 = [(0,0),(1,1)]
        dia2 = [(0,1),(1,0)]
        for coord in coords:
            hor_coords = [(r+coord[0], c+coord[1]) for r,c in hor]
            hor_coords = [i for i in hor_coords if 0<=min(i) and 9>=max(i)]
            if len(hor_coords) == 2:
                if (chips[hor_coords[0][0]][hor_coords[0][1]] == colour
                    or chips[hor_coords[0][0]][hor_coords[0][1]] == '#') \
                        and (chips[hor_coords[1][0]][hor_coords[1][1]] == colour
                            or chips[hor_coords[1][0]][hor_coords[1][1]] == '#'):
                    max_sequence = 2
                    break
            ver_coords = [(r + coord[0], c + coord[1]) for r, c in ver]
            ver_coords = [i for i in ver_coords if 0 <= min(i) and 9 >= max(i)]
            if len(ver_coords) == 2:
                if (chips[ver_coords[0][0]][ver_coords[0][1]] == colour
                    or chips[ver_coords[0][0]][ver_coords[0][1]] == '#') \
                        and (chips[ver_coords[1][0]][ver_coords[1][1]] == colour
                             or chips[ver_coords[1][0]][ver_coords[1][1]] == '#'):
                    max_sequence = 2
                    break
            dia1_coords = [(r + coord[0], c + coord[1]) for r, c in dia1]
            dia1_coords = [i for i in dia1_coords if 0 <= min(i) and 9 >= max(i)]
            if len(dia1_coords) == 2:
                if (chips[dia1_coords[0][0]][dia1_coords[0][1]] == colour
                    or chips[dia1_coords[0][0]][dia1_coords[0][1]] == '#') \
                        and (chips[dia1_coords[1][0]][dia1_coords[1][1]] == colour
                             or chips[dia1_coords[1][0]][dia1_coords[1][1]] == '#'):
                    max_sequence = 2
                    break
            dia2_coords = [(r + coord[0], c + coord[1]) for r, c in dia2]
            dia2_coords = [i for i in dia2_coords if 0 <= min(i) and 9 >= max(i)]
            if len(dia2_coords) == 2:
                if (chips[dia2_coords[0][0]][dia2_coords[0][1]] == colour
                    or chips[dia2_coords[0][0]][dia2_coords[0][1]] == '#') \
                        and (chips[dia2_coords[1][0]][dia2_coords[1][1]] == colour
                             or chips[dia2_coords[1][0]][dia2_coords[1][1]] == '#'):
                    max_sequence = 2
                    break

    # if we have found a sequence with 2 chips
    if max_sequence == 2:
        hor = [(0, -1), (0, 0), (0, 1)]
        ver = [(-1, 0), (0, 0), (1, 0)]
        dia1 = [(-1, -1), (0, 0), (1, 1)]
        dia2 = [(-1, 1), (0, 0), (1, -1)]
        for coord in coords:
            hor_coords = [(r + coord[0], c + coord[1]) for r, c in hor]
            hor_coords = [i for i in hor_coords if 0 <= min(i) and 9 >= max(i)]
            if len(hor_coords) == 3:
                if (chips[hor_coords[0][0]][hor_coords[0][1]] == colour
                    or chips[hor_coords[0][0]][hor_coords[0][1]] == '#') \
                        and (chips[hor_coords[1][0]][hor_coords[1][1]] == colour
                             or chips[hor_coords[1][0]][hor_coords[1][1]] == '#') \
                        and (chips[hor_coords[2][0]][hor_coords[2][1]] == colour
                             or chips[hor_coords[2][0]][hor_coords[2][1]] == '#'):
                    max_sequence = 3
                    break
            ver_coords = [(r + coord[0], c + coord[1]) for r, c in ver]
            ver_coords = [i for i in ver_coords if 0 <= min(i) and 9 >= max(i)]
            if len(ver_coords) == 3:
                if (chips[ver_coords[0][0]][ver_coords[0][1]] == colour
                    or chips[ver_coords[0][0]][ver_coords[0][1]] == '#') \
                        and (chips[ver_coords[1][0]][ver_coords[1][1]] == colour
                             or chips[ver_coords[1][0]][ver_coords[1][1]] == '#') \
                        and (chips[ver_coords[2][0]][ver_coords[2][1]] == colour
                             or chips[ver_coords[2][0]][ver_coords[2][1]] == '#'):
                    max_sequence = 3
                    break
            dia1_coords = [(r + coord[0], c + coord[1]) for r, c in dia1]
            dia1_coords = [i for i in dia1_coords if 0 <= min(i) and 9 >= max(i)]
            if len(dia1_coords) == 3:
                if (chips[dia1_coords[0][0]][dia1_coords[0][1]] == colour
                    or chips[dia1_coords[0][0]][dia1_coords[0][1]] == '#') \
                        and (chips[dia1_coords[1][0]][dia1_coords[1][1]] == colour
                             or chips[dia1_coords[1][0]][dia1_coords[1][1]] == '#') \
                        and (chips[dia1_coords[2][0]][dia1_coords[2][1]] == colour
                             or chips[dia1_coords[2][0]][dia1_coords[2][1]] == '#'):
                    max_sequence = 3
                    break
            dia2_coords = [(r + coord[0], c + coord[1]) for r, c in dia2]
            dia2_coords = [i for i in dia2_coords if 0 <= min(i) and 9 >= max(i)]
            if len(dia2_coords) == 3:
                if (chips[dia2_coords[0][0]][dia2_coords[0][1]] == colour
                    or chips[dia2_coords[0][0]][dia2_coords[0][1]] == '#') \
                        and (chips[dia2_coords[1][0]][dia2_coords[1][1]] == colour
                             or chips[dia2_coords[1][0]][dia2_coords[1][1]] == '#') \
                        and (chips[dia2_coords[2][0]][dia2_coords[2][1]] == colour
                             or chips[dia2_coords[2][0]][dia2_coords[2][1]] == '#'):
                    max_sequence = 3
                    break

    # if we have found a sequence with 3 chips
    if max_sequence == 3:
        hor = [(0, -1), (0, 0), (0, 1), (0, 2)]
        ver = [(-1, 0), (0, 0), (1, 0), (2, 0)]
        dia1 = [(-1, -1), (0, 0), (1, 1), (2, 2)]
        dia2 = [(-1, 1), (0, 0), (1, -1), (2, -2)]
        for coord in coords:
            hor_coords = [(r + coord[0], c + coord[1]) for r, c in hor]
            hor_coords = [i for i in hor_coords if 0 <= min(i) and 9 >= max(i)]
            if len(hor_coords) == 4:
                if (chips[hor_coords[0][0]][hor_coords[0][1]] == colour
                    or chips[hor_coords[0][0]][hor_coords[0][1]] == '#') \
                        and (chips[hor_coords[1][0]][hor_coords[1][1]] == colour
                             or chips[hor_coords[1][0]][hor_coords[1][1]] == '#') \
                        and (chips[hor_coords[2][0]][hor_coords[2][1]] == colour
                             or chips[hor_coords[2][0]][hor_coords[2][1]] == '#') \
                        and (chips[hor_coords[3][0]][hor_coords[3][1]] == colour
                             or chips[hor_coords[3][0]][hor_coords[3][1]] == '#'):
                    max_sequence = 4
                    break
            ver_coords = [(r + coord[0], c + coord[1]) for r, c in ver]
            ver_coords = [i for i in ver_coords if 0 <= min(i) and 9 >= max(i)]
            if len(ver_coords) == 4:
                if (chips[ver_coords[0][0]][ver_coords[0][1]] == colour
                    or chips[ver_coords[0][0]][ver_coords[0][1]] == '#') \
                        and (chips[ver_coords[1][0]][ver_coords[1][1]] == colour
                             or chips[ver_coords[1][0]][ver_coords[1][1]] == '#') \
                        and (chips[ver_coords[2][0]][ver_coords[2][1]] == colour
                             or chips[ver_coords[2][0]][ver_coords[2][1]] == '#') \
                        and (chips[ver_coords[3][0]][ver_coords[3][1]] == colour
                             or chips[ver_coords[3][0]][ver_coords[3][1]] == '#'):
                    max_sequence = 4
                    break
            dia1_coords = [(r + coord[0], c + coord[1]) for r, c in dia1]
            dia1_coords = [i for i in dia1_coords if 0 <= min(i) and 9 >= max(i)]
            if len(dia1_coords) == 4:
                if (chips[dia1_coords[0][0]][dia1_coords[0][1]] == colour
                    or chips[dia1_coords[0][0]][dia1_coords[0][1]] == '#') \
                        and (chips[dia1_coords[1][0]][dia1_coords[1][1]] == colour
                             or chips[dia1_coords[1][0]][dia1_coords[1][1]] == '#') \
                        and (chips[dia1_coords[2][0]][dia1_coords[2][1]] == colour
                             or chips[dia1_coords[2][0]][dia1_coords[2][1]] == '#') \
                        and (chips[dia1_coords[3][0]][dia1_coords[3][1]] == colour
                             or chips[dia1_coords[3][0]][dia1_coords[3][1]] == '#'):
                    max_sequence = 4
                    break
            dia2_coords = [(r + coord[0], c + coord[1]) for r, c in dia2]
            dia2_coords = [i for i in dia2_coords if 0 <= min(i) and 9 >= max(i)]
            if len(dia2_coords) == 4:
                if (chips[dia2_coords[0][0]][dia2_coords[0][1]] == colour
                    or chips[dia2_coords[0][0]][dia2_coords[0][1]] == '#') \
                        and (chips[dia2_coords[1][0]][dia2_coords[1][1]] == colour
                             or chips[dia2_coords[1][0]][dia2_coords[1][1]] == '#') \
                        and (chips[dia2_coords[2][0]][dia2_coords[2][1]] == colour
                             or chips[dia2_coords[2][0]][dia2_coords[2][1]] == '#') \
                        and (chips[dia2_coords[3][0]][dia2_coords[3][1]] == colour
                             or chips[dia2_coords[3][0]][dia2_coords[3][1]] == '#'):
                    max_sequence = 4
                    break

    h_normal = 10
    if completed_seq == 1:
        h_normal = 5 - max_sequence
    else:
        h_normal = 10 - max_sequence

    return min(h_normal,center_remain)


def null_heuristic(game_state, agent_id):
    return 0


def evalHeuristic(game_state, agent_id):
    if agent_id == 0 or agent_id == 2:
        colour = 'r'
    else:
        colour = 'b'

    action = game_state.agents[agent_id].last_action

    h = 32
    if action['type'] == 'trade':
        draft_coords = COORDS[action['draft_card']]
        for draft_coord in draft_coords:
            if game_state.board.chips[draft_coord[0]][draft_coord[1]] != '_':
                h = min(32, h)
            h = min(inadmissibleHeuristic(colour, draft_coord, game_state), h)
    else:
        eval = seq_evaluation(colour, action['coords'], game_state.board.chips)
        if eval < 8:
            h = 0.1 * eval
        else:
            h = inadmissibleHeuristic(colour, action['coords'], game_state)

    return h


class SimuBoard:
    def __init__(self):
        self.chips = [['#','_','_','_','_','_','_','_','_','#'],
                      ['_','_','_','_','_','_','_','_','_','_'],
                      ['_','_','_','_','_','_','_','_','_','_'],
                      ['_','_','_','_','_','_','_','_','_','_'],
                      ['_','_','_','_','_','_','_','_','_','_'],
                      ['_','_','_','_','_','_','_','_','_','_'],
                      ['_','_','_','_','_','_','_','_','_','_'],
                      ['_','_','_','_','_','_','_','_','_','_'],
                      ['_','_','_','_','_','_','_','_','_','_'],
                      ['#','_','_','_','_','_','_','_','_','#']]


class SimuAgent:
    def __init__(self):
        self.completed_seqs = 0
        self.last_action = None


class SimuState:
    def __init__(self):
        self.hand = []
        self.draft = []
        self.counter = 0
        self.board = SimuBoard()
        self.agents = []
        for i in range(4):
            agent = SimuAgent()
            self.agents.append(agent)


class Simulator:
    def __init__(self):
        self.id = 0

    def getActions(self, state, agent_id):
        if agent_id == 0 or agent_id == 2:
            opponent = 'b'
        else:
            opponent = 'r'

        chips = state.board.chips
        hand = state.hand
        draft = state.draft
        counter = state.counter

        if counter == 0:
            print("[Warning] Please use given actions!")
            actions = None
        elif counter == 1:
            draft = [c for c in draft if c != '#']
            random.shuffle(draft)
            if len(draft) != 0:
                draft = [draft.pop(), '#']
            else:
                draft = ['#']
        else:
            draft = ['#']

        actions = []
        random_case = False
        for card in hand:

            if card in ['jd', 'jc']:  # two-eyed jacks
                for r in range(10):
                    for c in range(10):
                        if chips[r][c] == '_':
                            for draft_card in draft:
                                actions.append(
                                    {'play_card': card, 'draft_card': draft_card,
                                     'type': 'place', 'coords': (r, c)})

            elif card in ['jh', 'js']:  # one-eyed jacks
                for r in range(10):
                    for c in range(10):
                        if chips[r][c] == opponent:
                            for draft_card in draft:
                                actions.append(
                                    {'play_card': card, 'draft_card': draft_card, 'type': 'remove', 'coords': (r, c)})

            elif card == '#':
                if random_case:
                    continue
                random_case = True
                options = []
                for r in range(10):
                    for c in range(10):
                        if chips[r][c] == '_':
                            options.append((r,c))
                random.shuffle(options)
                coord = options.pop()
                actions.append(
                    {'play_card': card, 'draft_card': '#', 'type': 'place', 'coords': coord})

            else:  # regular cards
                for r, c in COORDS[card]:
                    if chips[r][c] == '_':
                        for draft_card in draft:
                            actions.append(
                                {'play_card': card, 'draft_card': draft_card, 'type': 'place', 'coords': (r, c)})

        return actions

    def getSuccessor(self, state, action, agent_id):
        new_state = copy.deepcopy(state)
        chips = new_state.board.chips
        hand = new_state.hand
        draft = new_state.draft
        counter = new_state.counter
        if agent_id == 0 or agent_id == 2:
            colour = 'r'
        else:
            colour = 'b'

        if action['type'] == 'trade' and action['play_card']:
            hand.remove(action['play_card'])
            hand.append(action['draft_card'])
            draft.remove(action['draft_card'])
            draft.append('#')
            counter += 1
        if action['type'] == 'place':
            (r, c) = action['coords']
            chips[r][c] = colour
            hand.remove(action['play_card'])
            hand.append(action['draft_card'])
            draft.remove(action['draft_card'])
            draft.append('#')
            counter += 1
        if action['type'] == 'remove':
            (r, c) = action['coords']
            chips[r][c] = '_'
            hand.remove(action['play_card'])
            hand.append(action['draft_card'])
            draft.remove(action['draft_card'])
            draft.append('#')
            counter += 1

        new_state.board.chips = chips
        new_state.hand = hand
        new_state.draft = draft
        new_state.counter = counter
        new_state.agents[agent_id].last_action = action
        return new_state


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)

    def evalSelectAction(self, actions, game_state):

        if self.id == 0 or self.id == 2:
            colour = 'r'
        else:
            colour = 'b'

        if len(actions) == 0:
            return random.choice(actions)

        trade = False
        trade_actions = []
        nontrade_actions = []
        latest_coord = (-1, -1)

        for action in actions:
            h = math.inf
            if action['type'] == 'trade':
                trade = True
                action_temp = copy.deepcopy(action)
                draft_coords= COORDS[action['draft_card']]
                for draft_coord in draft_coords:
                    if game_state.board.chips[draft_coord[0]][draft_coord[1]] != '_':
                        h = min(math.inf, h)
                    h = min(inadmissibleHeuristic(colour, draft_coord, game_state), h)
                action_temp['heuristic'] = h
                trade_actions.append(action_temp)
            else:
                if action['coords'] == latest_coord:
                    continue
                h = inadmissibleHeuristic(colour, action['coords'], game_state)
                action_temp = copy.deepcopy(action)
                action_temp['heuristic'] = h
                nontrade_actions.append(action_temp)
                latest_coord = action['coords']

        # if trade is true
        if trade:
            act = min(trade_actions, key=lambda d: d['heuristic'])
            del act['heuristic']
        else:
            act = min(nontrade_actions, key=lambda d: d['heuristic'])
            del act['heuristic']
            # Choose draft card
            drafts = game_state.board.draft
            if len(drafts) != 0:
                heur_draft = {}
                h = math.inf
                for dr in drafts:
                    dr_coords = COORDS[dr]
                    for dr_coord in dr_coords:
                        if game_state.board.chips[dr_coord[0]][dr_coord[1]] != '_':
                            h = min(math.inf, h)
                        h = min(inadmissibleHeuristic(colour, dr_coord, game_state), h)
                    heur_draft[dr] = h
                act['draft_card'] = min(heur_draft, key=heur_draft.get)

        return act


    def astarSearch(self,actions,game_state):
        # COMP90054 Task 1, Implement your A Star search algorithm here
        """Search the node that has the lowest combined cost and heuristic first."""
        cards = [(r + s) for r in ['2', '3', '4', '5', '6', '7', '8', '9', 't', 'j', 'q', 'k', 'a'] for s in
                 ['d', 'c', 'h', 's']]
        cards = cards * 2  # Sequence uses 2 decks.
        random.shuffle(cards)
        discards = copy.deepcopy(game_state.deck.discards)
        hand = copy.deepcopy(game_state.agents[self.id].hand)
        draft = copy.deepcopy(game_state.board.draft)
        for discard in discards:
            cards.remove(discard)
        for handcard in hand:
            cards.remove(handcard)
        for draftcard in draft:
            cards.remove(draftcard)

        plr1_hand = cards[0:6]
        plr2_hand = cards[6:12]
        plr3_hand = cards[12:18]
        cards = cards[18:]

        simulator = GameRule(4)
        simulator.current_game_state = copy.deepcopy(game_state)
        simulator.current_agent_index = self.id

        simulator.current_game_state.deck.cards = cards
        simulator.current_game_state.deck.discards = discards
        simulator.current_game_state.agents[self.id].hand = hand
        simulator.current_game_state.board.draft = draft
        simulator.current_game_state.agents[(self.id + 1) % 4].hand = plr1_hand
        simulator.current_game_state.agents[(self.id + 2) % 4].hand = plr2_hand
        simulator.current_game_state.agents[(self.id + 3) % 4].hand = plr3_hand

        myPriQue = PriorityQueue()
        startNode = (simulator.current_game_state, '', 0, [])
        h = heuristic(simulator.current_game_state,self.id)
        myPriQue.push(startNode, 0 + h)
        visited = set()
        bestCost = dict()
        search_control = 0
        while myPriQue.isEmpty() == 0:
            search_control += 1
            node = myPriQue.pop()
            state, action, cost, path = node

            if (state not in visited) or (cost < bestCost[state]):
                visited.add(state)
                bestCost.update({state: cost})
                simulator.current_game_state = copy.deepcopy(state)
                if simulator.gameEnds() or search_control > 2:
                    path = path + [action]
                    break
                if search_control != 1:
                    actions = simulator.getLegalActions(simulator.current_game_state, self.id)
                for action in actions:
                    simulator.current_game_state = copy.deepcopy(state)
                    temp_state = simulator.generateSuccessor(simulator.current_game_state, action, self.id)
                    temp_actions = simulator.getLegalActions(temp_state, (self.id+1)%4)
                    opp_action1 = self.evalSelectAction(temp_actions, temp_state)
                    temp_state = simulator.generateSuccessor(temp_state, opp_action1, (self.id+1)%4)
                    temp_actions = simulator.getLegalActions(temp_state, (self.id + 2) % 4)
                    partner_action = self.evalSelectAction(temp_actions, temp_state)
                    temp_state = simulator.generateSuccessor(temp_state, partner_action, (self.id + 2) % 4)
                    temp_actions = simulator.getLegalActions(temp_state, (self.id + 3) % 4)
                    opp_action2 = self.evalSelectAction(temp_actions, temp_state)
                    new_state = simulator.generateSuccessor(temp_state, opp_action2, (self.id + 3) % 4)

                    new_cost = cost + 1
                    newNode = (new_state, action, new_cost, path + [action])
                    heur = heuristic(new_state,self.id)
                    if heur != None:
                        myPriQue.push(newNode, new_cost + 1.3 * heur)  # weighted A*

        return path[0]


    def refinedAstarSearch(self,actions,game_state):
        if self.id == 0 or self.id == 2:
            colour = 'r'
            opp_colour = 'b'
        else:
            colour = 'b'
            opp_colour = 'r'

        chips = game_state.board.chips

        my_trade_queue = PriorityQueue()
        for action in actions:
            if action['type'] == 'trade' and action['draft_card']:
                h_draft = 8
                for draft_coord in COORDS[action['draft_card']]:
                    min(h_draft, seq_evaluation(colour, draft_coord, chips))
                my_trade_queue.push(action, h_draft)
        if not my_trade_queue.isEmpty():
            return my_trade_queue.pop()

        hand = game_state.agents[self.id].hand
        draft = game_state.board.draft
        agents = []
        for i in range(4):
            agent = SimuAgent()
            agent.completed_seqs = game_state.agents[i].completed_seqs
            agents.append(agent)


        for card in hand:
            if card in ['jd','jc']:
                my_j_queue = PriorityQueue()
                for action in actions:
                    if action['play_card'] == 'jd' or action['play_card'] == 'jc':
                        if action['coords'] and action['draft_card']:
                            h_coords = seq_evaluation(colour, action['coords'], chips)
                            h_draft = 8
                            for draft_coord in COORDS[action['draft_card']]:
                                min(h_draft,seq_evaluation(colour, draft_coord, chips))
                            h_eval = h_coords + h_draft
                            if h_coords < 8:
                                my_j_queue.push(action, h_eval)
                        actions.remove(action)
                if not my_j_queue.isEmpty():
                    return my_j_queue.pop()

            if card in ['jh','js']:
                my_1j_queue = PriorityQueue()
                for action in actions:
                    if action['play_card'] == 'jh' or action['play_card'] == 'js':
                        if action['coords'] and action['draft_card']:
                            h_coords = remove_evaluation(opp_colour, action['coords'], chips)
                            h_draft = 8
                            for draft_coord in COORDS[action['draft_card']]:
                                min(h_draft,seq_evaluation(colour, draft_coord, chips))
                            h_eval = h_coords + h_draft
                            if h_coords < 2:
                                my_1j_queue.push(action, h_eval)
                        actions.remove(action)
                if not my_1j_queue.isEmpty():
                    return my_1j_queue.pop()

        initial_state = SimuState()
        initial_state.board.chips = chips
        initial_state.hand = hand
        initial_state.draft = draft
        initial_state.agents = agents

        simulator = Simulator()

        myPriQue = PriorityQueue()
        startNode = (initial_state, '', 0, [])

        h = 32
        myPriQue.push(startNode, 0 + h)
        visited = set()
        bestCost = dict()
        search_control = 0
        while myPriQue.isEmpty() == 0:
            search_control += 1
            node = myPriQue.pop()
            state, action, cost, path = node

            if (state not in visited) or (cost < bestCost[state]):
                visited.add(state)
                bestCost.update({state: cost})

                if search_control > 5:
                    path = path + [action]
                    break
                if search_control != 1:
                    actions = simulator.getActions(state, self.id)
                for action in actions:
                    new_state = simulator.getSuccessor(state, action, self.id)
                    new_cost = cost + 1
                    newNode = (new_state, action, new_cost, path + [action])
                    heur = evalHeuristic(new_state,self.id)
                    if heur != None:
                        myPriQue.push(newNode, 1 * new_cost + 4 * heur)  # weighted A*

        return path[0]


    def noJRefinedAstarSearch(self,actions,game_state):
        if self.id == 0 or self.id == 2:
            colour = 'r'
            opp_colour = 'b'
        else:
            colour = 'b'
            opp_colour = 'r'

        chips = game_state.board.chips

        my_trade_queue = PriorityQueue()
        for action in actions:
            if action['type'] == 'trade' and action['draft_card']:
                h_draft = 8
                for draft_coord in COORDS[action['draft_card']]:
                    min(h_draft, seq_evaluation(colour, draft_coord, chips))
                my_trade_queue.push(action, h_draft)
        if not my_trade_queue.isEmpty():
            return my_trade_queue.pop()

        hand = game_state.agents[self.id].hand
        draft = game_state.board.draft
        agents = []
        for i in range(4):
            agent = SimuAgent()
            agent.completed_seqs = game_state.agents[i].completed_seqs
            agents.append(agent)

        initial_state = SimuState()
        initial_state.board.chips = chips
        initial_state.hand = hand
        initial_state.draft = draft
        initial_state.agents = agents

        simulator = Simulator()

        myPriQue = PriorityQueue()
        startNode = (initial_state, '', 0, [])

        h = heuristic(initial_state, self.id)
        myPriQue.push(startNode, 0 + h)
        visited = set()
        bestCost = dict()
        search_control = 0
        while myPriQue.isEmpty() == 0:
            search_control += 1
            node = myPriQue.pop()
            state, action, cost, path = node

            if (state not in visited) or (cost < bestCost[state]):
                visited.add(state)
                bestCost.update({state: cost})

                if search_control > 5:
                    path = path + [action]
                    break
                if search_control != 1:
                    actions = simulator.getActions(state, self.id)
                for action in actions:
                    new_state = simulator.getSuccessor(state, action, self.id)
                    new_cost = cost + 1
                    newNode = (new_state, action, new_cost, path + [action])
                    heur = evalHeuristic(new_state,self.id)
                    if heur != None:
                        myPriQue.push(newNode, 1 * new_cost + 4 * heur)  # weighted A*

        return path[0]



    def SelectAction(self, ori_actions, ori_game_state):
        """for action in actions:
            if action['coords'] == (4,4) or action['coords'] == (4,5) \
                or action['coords'] == (5,4) or action['coords'] == (5,5):
                return action"""
        actions = copy.deepcopy(ori_actions)
        game_state = copy.deepcopy(ori_game_state)
        action = self.refinedAstarSearch(actions, game_state)
        return action


    """def SelectAction(self,actions,game_state):


        return random.choice(actions)"""
