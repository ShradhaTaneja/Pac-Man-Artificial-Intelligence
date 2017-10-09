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

        # stores the first action for all the nodes, each instance is the key, and the very first action to be taken from the given state is the value for each key
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

        # stores the main action for all the nodes
        base_action = {}
        max_score = 0
        max_state = ''

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
#        sorted_items = sorted(self.items, key = lambda x:x[1], reverse = True)
#        return self.get_max(sorted_items)

        min_value = sorted_items.pop(0)
        self.items = sorted_items
        return min_value

    def get_max(self, sorted_array):
        max_data = sorted_array[0]
        max_score = max_data[1]
        max_len_path = 0
        count = {}

        for path in sorted_array:
            print path, '??????????????'
        for path, value in sorted_array:
            print path, value, '?????'
            try:
                count[value] += 1
            except:
                count[value] = 0
        print count, '>>>>>>'
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
    count = 0
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    def getTotalScore(self, depth, state):
        return 0

    # GetAction Function: Called with every frame
    def getAction(self, state):
        s = 0
        # stores the main action for all the nodes
        base_action = {}
        max_score = 0
        max_state = ''

#        if self.count > 3:
#            print 'frame calls finished'
#            print base_action[max_state]
#            exit()

        self.count += 1
        print '-- call ', self.count

        open_list = priorityQueue()
        closed_list = priorityQueue()
#        print open_list, closed_list, '>>>>>>>>>>'

        open_list.insert(([state], scoreEvaluation(state)))

        while (not open_list.isEmpty()):
            current_value = open_list.pop()
            current_path = current_value[0]
            last_visited_state = current_path[-1]

#            print current_value, current_path, '<<<<<<<<<<<<<<<<<<<<'

            # g(x) = depth, root node is depth 0, depth for each successor will be length of it's parent path
            g_cost = len(current_path)
#            print g_cost, '______ g cost = depth '

            if last_visited_state.isWin():
                print 'win state mil gyi'
                return Directions.STOP

            # get all legal actions for pacman
            legal = last_visited_state.getLegalPacmanActions()

            print 'successor call ', s
#            if s > 5:
#                print 'successor calls finish'
#                break
            # get successor states for each action
            for action in legal:
#                print action
                successor = last_visited_state.generatePacmanSuccessor(action)
#                print [successor], (' -- successor')
                if successor == None:
                    break
                if successor.isLose():
                    print 'lose state mil gyi'
                    continue
                s += 1
#                print current_path, ' -- current path', type(current_path)
                new_path = current_path + [successor]
#                print new_path, ' -- new path'

                new_score = scoreEvaluation(successor)

                h_cost = - (scoreEvaluation(successor) - scoreEvaluation(state))
#                print 'h_cost %d, scoreeval(succ) %d, scoreeval(root) %d' % (h_cost, scoreEvaluation(successor), scoreEvaluation(state))
#                print h_cost, scoreEvaluation(successor), scoreEvaluation(state)

                total_cost = g_cost + h_cost
#                print total_cost, '---- total cost'
                new_data = (new_path, total_cost)

#                print new_data, ' -- new data'
                open_list.insert(new_data)

                try:
                    base_action[successor] = base_action[last_visited_state]
                except:
                    base_action[successor] = action
#                print '\t max score : ', max_score
#                print '\t new score : ', new_score
                if new_score > max_score:
                    max_score = new_score
                    print 'max state set krdi'
                    max_state = successor


        print '\t max score : ', max_score
        print ' _____returning _____', base_action[max_state], '\n\n'
#        exit()
        return base_action[max_state]

        # TODO: write A* Algorithm instead of returning Directions.STOP
        return Directions.STOP
