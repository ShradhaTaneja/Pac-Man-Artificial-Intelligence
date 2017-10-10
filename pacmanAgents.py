# pacmanAgents.py
# ---------------
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


from pacman import Directions
from game import Agent
from heuristics import scoreEvaluation
import random

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        print actions
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class GreedyAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # queue initialised with base state
        queue = [state]

        # stores the first action to reach specific nodes, ex: {<gameStateInstance> : <action>}
        base_action = {}

        max_score = 0
        max_state = state

        while(queue):
            current_state = queue.pop(0)
            if current_state.isWin():
                return Directions.STOP

            # get all legal actions for pacman
            legal = current_state.getLegalPacmanActions()

            # get successor states for each action
            for action in legal:
                successor = current_state.generatePacmanSuccessor(action)
                if successor == None:
                    break
                if successor.isLose():
                    continue

                # append successor state in queue
                queue.append(successor)
                score = scoreEvaluation(successor)

                # base action for current state is same as the base action for parent state
                try:
                    base_action[successor] = base_action[current_state]
                except:
                    base_action[successor] = action

                if score > max_score:
                    max_score = score
                    max_state = successor

        return base_action[max_state]

class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # stack initialised with base state
        stack = [state]

        # stores the first action to reach specific nodes, ex: {<gameStateInstance> : <action>}
        base_action = {}
        max_score = 0
        max_state = state

        while(stack):
            current_state = stack.pop()
            if current_state.isWin():
                return Directions.STOP

            # get all legal actions for pacman
            legal = current_state.getLegalPacmanActions()

            # get successor states for each action
            for action in legal:
                successor = current_state.generatePacmanSuccessor(action)
                if successor == None:
                    break

                if successor.isLose():
                    continue

                # append successor state in stack
                stack.append(successor)
                score = scoreEvaluation(successor)

                # base action for current state is same as the base action for parent state
                try:
                    base_action[successor] = base_action[current_state]
                except:
                    base_action[successor] = action

                if score > max_score:
                    max_score = score
                    max_state = successor

        return base_action[max_state]

class priorityQueue():
    def __init__(self):
        self.items = []

    def pop(self):
        sorted_items = sorted(self.items, key = lambda x:x[1])
        min_value = sorted_items.pop(0)
        self.items = sorted_items
        return min_value

    def get_max(self, sorted_array):
        max_data = sorted_array[0]
        max_score = max_data[1]
        max_len_path = 0
        count = {}

        for path, value in sorted_array:
            try:
                count[value] += 1
            except:
                count[value] = 0
        if count[max_score] > 1:
            for path, value in sorted_array:
                if value == max_score and len(path) > max_len_path:
                    final_max = (path, value)
        else:
            final_max = max_data

        return final_max

    def insert(self, value):
        self.items.append(value)
        return self.items

    def get(self):
        return self.items

    def isEmpty(self):
        return len(self.items) == 0

    def len(self):
        return len(self.items)

    def getSorted(self):
        return sorted(self.items, key = lambda x:x[1])

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # stores the first action for all the nodes, ex: {<gameStateInstance> : <action>}
        base_action = {}
        max_score = 0
        max_state = state

        open_list = priorityQueue()
        closed_list = priorityQueue()

        open_list.insert(([state], 0))

        while (not open_list.isEmpty()):
            current_value = open_list.pop()
            current_path = current_value[0]
            last_visited_state = current_path[-1]

            # g(x) = depth, root node is depth 0, depth for each successor will be length of it's parent path
            g_cost = len(current_path)

            if last_visited_state.isWin():
                return Directions.STOP

            # get all legal actions for pacman
            legal = last_visited_state.getLegalPacmanActions()

            # get successor states for each action
            for action in legal:
                successor = last_visited_state.generatePacmanSuccessor(action)
                if successor == None:
                    break
                if successor.isLose():
                    continue
                new_path = current_path + [successor]

                new_score = scoreEvaluation(successor)

                h_cost = - (scoreEvaluation(successor) - scoreEvaluation(state))

                total_cost = g_cost + h_cost
                new_data = (new_path, total_cost)

                open_list.insert(new_data)

                # base action for current state is same as the base action for parent state
                try:
                    base_action[successor] = base_action[last_visited_state]
                except:
                    base_action[successor] = action

                if new_score > max_score:
                    max_score = new_score
                    max_state = successor

        return base_action[max_state]

