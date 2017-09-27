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
    # testing
    counter = 0
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        print '\t STARTING STATE IS : ', [state]
        # queue initialised with base state
        queue = [state]
        bfs_traversal = []
        node_child_mapping = {}
        node_status_mapping = {}


        while(queue):
            # testing
            if self.counter > 3:
                print '\n\n FINAL DATA IS \n\n'
                print '_'*10, ' queue ', '_'*10
                print queue, '\n'

                print '_'*10, ' bfs traversal ', '_'*10
                print  bfs_traversal, '\n'

                print '_'*10, ' node child mapping ', '_'*10
                print node_child_mapping, '\n'

                print '_'*10, ' node_status mapping ', '_'*10
                print node_status_mapping, '\n'

                print '_'*10, ' queue ', '_'*10
                print queue

                exit()
            print self.counter, '<<<<< counter'
            self.counter += 1
            current_state = queue.pop(0)
            print '\t CURRENT STATE IS : ', [current_state]
            bfs_traversal.append(current_state)

            if current_state.isLose():
                node_status_mapping[current_state] = 'lose'
            elif current_state.isWin():
                node_status_mapping[current_state] = 'win'
            else:
                node_status_mapping[current_state] = None

            node_child_mapping[current_state] = {}

            # get all legal actions for pacman
            legal = current_state.getLegalPacmanActions()

            # get successor states for each action
            for action in legal:
                successor = current_state.generatePacmanSuccessor(action)


                if successor == None:
                    break
                queue.append(successor)
                score = scoreEvaluation(successor)
                node_child_mapping[current_state][successor] = (action, score)


            print '_'*10, ' queue ', '_'*10
            print queue, '\n'

            print '_'*10, ' bfs traversal ', '_'*10
            print  bfs_traversal, '\n'

            print '_'*10, ' node child mapping ', '_'*10
            print node_child_mapping, '\n'

            print '_'*10, ' node_status mapping ', '_'*10
            print node_status_mapping, '\n'

            print '_'*10, ' queue ', '_'*10
            print queue


        exit()
        print 'shayad kuch thukaaa'



        # SHRADHA RECENT CODE ABOVE THIS - 5 pm

        # TODO: write BFS Algorithm instead of returning Directions.STOP
        return Directions.STOP


    def getCustomSuccessors(self, state, action):
        return state.generatePacmanSuccessor(action)

class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP
        return Directions.STOP

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        return Directions.STOP
