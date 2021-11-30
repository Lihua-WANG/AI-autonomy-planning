from template import Agent
import random


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)

    def SelectAction(self, actions, game_state):
        # red team
        if self.id % 2 == 0:
            self_coords = game_state.board.plr_coords['r']
            opp_coords = game_state.board.plr_coords['b']
            opp_actions = [game_state.agents[1].last_action, game_state.agents[3].last_action]
        # blue team
        else:
            self_coords = game_state.board.plr_coords['b']
            opp_coords = game_state.board.plr_coords['r']
            opp_actions = [game_state.agents[0].last_action, game_state.agents[2].last_action]
        opp_attack_score = self.get_score(opp_actions[0], self_coords) + self.get_score(opp_actions[1], self_coords)
        opp_defense_score = self.get_score(opp_actions[0], opp_coords) + self.get_score(opp_actions[1], opp_coords)
        available_actions = self.available_actions(actions, game_state)

        # if the strategy of opponent is defense, i.e., they focuses on forming consecutive sequence
        if opp_defense_score > opp_attack_score:
            consecutive = []
            consecutive.extend(self.consecutive_sequence(opp_actions[0], opp_coords))
            consecutive.extend(self.consecutive_sequence(opp_actions[1], opp_coords))
            if consecutive:
                for action in available_actions:
                    # if the available actions have a way to prevent opponent from forming consecutive sequence
                    if action['coords'] in consecutive:
                        return action

        # the agent can focus on forming consecutive sequence for itself
        # choose the action that gets the highest score
        highest_score = 0
        highest_score_action = None
        for action in available_actions:
            score = self.get_score(action, self_coords)
            if score >= highest_score:
                highest_score = score
                highest_score_action = action
        if not highest_score_action:
            return random.choice(actions)
        return highest_score_action

    def available_actions(self, actions, game_state):
        """Find the available actions that the space is empty."""
        result = []
        for action in actions:
            if action['coords'] in game_state.board.empty_coords:
                result.append(action)
        return result

    def get_score(self, action, coords_distr):
        if not action:
            return 0
        score = 0
        (x, y) = action['coords']
        if (x + 1, y) in coords_distr and (x - 1, y) in coords_distr:
            score += 1
        if (x, y + 1) in coords_distr and (x, y - 1) in coords_distr:
            score += 1
        if (x + 1, y + 1) in coords_distr and (x - 1, y - 1) in coords_distr:
            score += 1
        if (x - 1, y + 1) in coords_distr and (x + 1, y - 1) in coords_distr:
            score += 1
        if (x + 1, y) in coords_distr and (x + 2, y) in coords_distr:
            score += 2
        if (x - 1, y) in coords_distr and (x - 2, y) in coords_distr:
            score += 2
        if (x, y + 1) in coords_distr and (x, y + 2) in coords_distr:
            score += 2
        if (x, y - 1) in coords_distr and (x, y - 2) in coords_distr:
            score += 2
        if (x + 1, y + 1) in coords_distr and (x + 2, y + 2) in coords_distr:
            score += 2
        if (x - 1, y - 1) in coords_distr and (x - 2, y - 2) in coords_distr:
            score += 2
        if (x - 1, y + 1) in coords_distr and (x - 2, y + 2) in coords_distr:
            score += 2
        if (x + 1, y - 1) in coords_distr and (x + 2, y - 2) in coords_distr:
            score += 2
        if (x + 1, y) in coords_distr and (x + 2, y) in coords_distr and (x + 3, y) in coords_distr:
            score += 3
        if (x - 1, y) in coords_distr and (x - 2, y) in coords_distr and (x - 3, y) in coords_distr:
            score += 3
        if (x, y + 1) in coords_distr and (x, y + 2) in coords_distr and (x, y + 3) in coords_distr:
            score += 3
        if (x, y - 1) in coords_distr and (x, y - 2) in coords_distr and (x, y - 3) in coords_distr:
            score += 3
        if (x + 1, y + 1) in coords_distr and (x + 2, y + 2) in coords_distr and (x + 3, y + 3) in coords_distr:
            score += 3
        if (x - 1, y - 1) in coords_distr and (x - 2, y - 2) in coords_distr and (x - 3, y - 3) in coords_distr:
            score += 3
        if (x - 1, y + 1) in coords_distr and (x - 2, y + 2) in coords_distr and (x - 3, y + 3) in coords_distr:
            score += 3
        if (x + 1, y - 1) in coords_distr and (x + 2, y - 2) in coords_distr and (x + 3, y - 3) in coords_distr:
            score += 3
        return score

    def consecutive_sequence(self, action, coords_distr):
        """Find the coordinates which prevent forming consecutive sequence of more than 3"""
        if not action:
            return []
        (x, y) = action['coords']
        if (x + 1, y) in coords_distr and (x + 2, y) in coords_distr:
            return [(x - 1, y), (x + 3, y)]
        if (x - 1, y) in coords_distr and (x - 2, y) in coords_distr:
            return [(x + 1, y), (x - 3, y)]
        if (x, y + 1) in coords_distr and (x, y + 2) in coords_distr:
            return [(x, y - 1), (x, y + 3)]
        if (x, y - 1) in coords_distr and (x, y - 2) in coords_distr:
            return [(x, y + 1), (x, y - 3)]
        if (x + 1, y + 1) in coords_distr and (x + 2, y + 2) in coords_distr:
            return [(x - 1, y - 1), (x + 3, y + 3)]
        if (x - 1, y - 1) in coords_distr and (x - 2, y - 2) in coords_distr:
            return [(x + 1, y + 1), (x - 3, y - 3)]
        if (x - 1, y + 1) in coords_distr and (x - 2, y + 2) in coords_distr and (x - 3, y + 3):
            return [(x + 1, y - 1), (x - 3, y + 3)]
        if (x + 1, y - 1) in coords_distr and (x + 2, y - 2) in coords_distr and (x + 3, y - 3):
            return [(x - 1, y + 1), (x + 3, y - 3)]
        else:
            return []
