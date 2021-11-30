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
            draft = [draft.pop(), '#']
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

        if action['type'] == 'trade':
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

        if game_state.agents[self.id].trade:
            for action in actions:
                if action['type'] == 'trade' and action['draft_card']:
                    return action

        chips = game_state.board.chips
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
                        myPriQue.push(newNode, 1 * new_cost + 3.5 * heur)  # weighted A*

        return path[0]


    def SelectAction(self, actions, game_state):
        """for action in actions:
            if action['coords'] == (4,4) or action['coords'] == (4,5) \
                or action['coords'] == (5,4) or action['coords'] == (5,5):
                return action"""
        action = self.refinedAstarSearch(actions, game_state)
        return action


    """def SelectAction(self,actions,game_state):


        return random.choice(actions)"""
