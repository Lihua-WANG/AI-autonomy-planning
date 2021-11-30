# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import sys

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    mystack = util.Stack()
    startNode = (problem.getStartState(), '', 0, [])
    mystack.push(startNode)
    visited = set()
    while mystack:
        node = mystack.pop()
        state, action, cost, path = node
        if state not in visited:
            visited.add(state)
            if problem.isGoalState(state):
                path = path + [(state, action)]
                break;
            succNodes = problem.expand(state)
            for succNode in succNodes:
                succState, succAction, succCost = succNode
                newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                mystack.push(newNode)
    actions = [action[1] for action in path]
    del actions[0]
    return actions


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(state, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = state
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def aStarSearch(problem, heuristic=nullHeuristic):
    # COMP90054 Task 1, Implement your A Star search algorithm here
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startNode = ('', 0, [], 0)
    open_set = {problem.getStartState(): startNode}
    close_set = set()
    myqueue = util.PriorityQueue()
    myqueue.push(problem.getStartState(), 0)
    while myqueue:
        state = myqueue.pop()
        action, gcost, path, _ = open_set[state]
        if problem.isGoalState(state):
            path = path + [(state, action)]
            break

        close_set.add(state)
        succNodes = problem.expand(state)
        for succNode in succNodes:
            succState, succAction, succCost = succNode
            if succState in close_set:
                continue

            hcost = heuristic(succState, problem)
            totalCost = gcost + succCost + hcost
            newNode = (succAction, gcost + succCost, path + [(state, action)], totalCost)
            myqueue.update(succState, totalCost)
            if succState in open_set:
                _, _, _, oldTotalCost = open_set[succState]
                if oldTotalCost > totalCost:
                    open_set[succState] = newNode
            else:
                open_set[succState] = newNode

    actions = [action[1] for action in path]
    del actions[0]
    return actions


def manhattanHeuristic1(position1, position2):
    """The Manhattan distance heuristic between two points"""
    xy1 = position1
    xy2 = position2
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def aStarSearch_task4_1(problem, startState, goalState, heuristic=manhattanHeuristic1):
    startNode = ('', 0, [], 0)
    open_set = {startState: startNode}
    close_set = set()
    myqueue = util.PriorityQueue()
    myqueue.push(startState, 0)
    outNode = (startState, '', 0, [])
    while myqueue:
        state = myqueue.pop()
        action, gcost, path, _ = open_set[state]
        if state == goalState:
            path = path + [(state, action)]
            outNode = (state,action,gcost,path)
            break

        close_set.add(state)
        succNodes = problem.expand(state)
        for succNode in succNodes:
            succState, succAction, succCost = succNode
            if succState in close_set:
                continue

            hcost = heuristic(succState, goalState)
            totalCost = gcost + succCost + hcost
            newNode = (succAction, gcost + succCost, path + [(state, action)], totalCost)
            myqueue.update(succState, totalCost)
            if succState in open_set:
                _, _, _, oldTotalCost = open_set[succState]
                if oldTotalCost > totalCost:
                    open_set[succState] = newNode
            else:
                open_set[succState] = newNode

    actions = [action[1] for action in path]
    del actions[0]
    return outNode, actions


def aStarSearch_task4_2(problem, startStae, target, goalReal, goalFalse, alpha, heuristic=manhattanHeuristic1):
    startNode = ('', 0, [], 0)
    open_set = {startStae: startNode}
    close_set = set()
    myqueue = util.PriorityQueue()
    myqueue.push(startStae, 0)
    outNode = (startStae, '', 0, [])
    while myqueue:
        state = myqueue.pop()
        action, gcost, path, _ = open_set[state]
        if state == target:
            path = path + [(state, action)]
            outNode = (state, action, gcost, path)
            break

        close_set.add(state)
        succNodes = problem.expand(state)
        for succNode in succNodes:
            succState, succAction, succCost = succNode
            if succState in close_set:
                continue
            h_gr = heuristic(succState, goalReal)
            h_gf = heuristic(succState, goalFalse)
            hcost = heuristic(succState, target)
            if h_gr < h_gf:
                hcost = alpha * hcost
            totalCost = gcost + succCost + hcost
            newNode = (succAction, gcost + succCost, path + [(state, action)], totalCost)
            myqueue.update(succState, totalCost)
            if succState in open_set:
                _, _, _, oldTotalCost = open_set[succState]
                if oldTotalCost > totalCost:
                    open_set[succState] = newNode
            else:
                open_set[succState] = newNode

    actions = [action[1] for action in path]
    del actions[0]
    return outNode, actions


# get fifth element
def takeFifth(elem):
    return elem[4]


def RBFS(problem, node, f_limit, heuristic):
    # print(node)
    state, action, gcost, path, fcost = node
    if problem.isGoalState(state):
        path = path + [(state, action)]
        return path, fcost

    succNodes = problem.expand(state)
    if 0 == len(succNodes):
        return [], sys.maxsize

    successors = []
    for succNode in succNodes:
        succState, succAction, succCost = succNode
        node_gcost = gcost + succCost
        node_hcost = heuristic(succState, problem)
        node_fcost = max(node_gcost + node_hcost, fcost)
        node = (succState, succAction, node_gcost, path + [(state, action)], node_fcost)
        successors.append(node)

    while True:
        successors.sort(key=takeFifth)
        best = successors[0]
        if best[4] > f_limit:
            return [], best[4]
        if len(successors) > 1:
            alternative = successors[1][4]
        else:
            alternative = successors[0][4]
        result, best_fcost = RBFS(problem, best, min(f_limit, alternative), heuristic)
        if len(result) > 0:
            return result, best_fcost
        else:
            new_best = (best[0], best[1], best[2], best[3], best_fcost)
            del successors[0]
            successors.append(new_best)


def recursivebfs(problem, heuristic=nullHeuristic):
    # COMP90054 Task 2, Implement your Recursive Best First Search algorithm here
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    fcost = heuristic(problem.getStartState(), problem)
    startNode = (problem.getStartState(), '', 0, [], fcost)

    f_limit = sys.maxsize
    path, _ = RBFS(problem, startNode, f_limit, heuristic)
    # print(path)
    if 0 == len(path):
        return []

    actions = [action[1] for action in path]
    del actions[0]
    # print(actions)
    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
rebfs = recursivebfs
