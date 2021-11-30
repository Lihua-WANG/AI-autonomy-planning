from template import Agent
import random
import copy
from Sequence.sequence_model import COORDS
import math


def heuristic(colour, coord, game_state):
    if colour == 'r':
        opponent = 'b'
    else:
        opponent = 'r'
    chips = game_state.board.chips
    occupation = 0
    special_case = False

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

    return 32-occupation


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)

    def SelectAction(self, actions, game_state):

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
                    h = min(heuristic(colour, draft_coord, game_state), h)
                action_temp['heuristic'] = h
                trade_actions.append(action_temp)
            else:
                if action['coords'] == latest_coord:
                    continue
                h = heuristic(colour, action['coords'], game_state)
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
                        h = min(heuristic(colour, dr_coord, game_state), h)
                    heur_draft[dr] = h
                act['draft_card'] = min(heur_draft, key=heur_draft.get)

        return act
