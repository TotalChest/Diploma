import zss
from zss import Node
from enum import Enum


class QLearningStrategy(Enum):
    POSSIBLE_EVENTS = 'possible_events'
    DQN = 'dqn'
    EVENTS_COUNT = 'events_count'
    EPSILON_GREEDY = 'epsilon_greedy'
    TREE_EDIT_DISTANCE = 'tree_edit_distance'
    TRAIN = 'train'
    ABSTRACT_STATES = 'abstract_states'
    REVERSE_POSSIBLE_EVENTS = 'reverse_possible_events'

    def __str__(self):
        return self.value


def AVT2zss(root):
    queue = []
    curr_number = 0
    nodes_dict = {0: Node('0')}
    if root:
        # (Node, parent_number, children view_tree)
        queue.extend([
            (Node('0'), 0, child)
            for child in root.to_dict().get('children', [])
        ])
    while queue:
        curr_number += 1
        curr_node = queue.pop()
        nodes_dict[curr_node[1]].addkid(curr_node[0])
        nodes_dict[curr_number] = curr_node[0]
        if curr_node[0]:
            children = [
                (Node('0'), curr_number, child) 
                for child in curr_node[2].to_dict().get('children', [])
            ]
            queue.extend(children)
    return nodes_dict[0], curr_number


def zss_dist(A, B):
    return zss.distance(A, B,
                        get_children=zss.Node.get_children,
                        insert_cost=lambda x: 1,
                        remove_cost=lambda x: 1,
                        update_cost=lambda x, y: 0)


def AVTdiff(curr_AVT, prev_AVT):
    # |s(t+1)\s(t)| / |s(t+1)|
    curr_zss_tree, curr_nodes_number = AVT2zss(curr_AVT)
    prev_zss_tree, prev_nodes_number = AVT2zss(prev_AVT)
    return max(0, zss_dist(prev_zss_tree, curr_zss_tree))
