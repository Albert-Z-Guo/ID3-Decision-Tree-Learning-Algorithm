from node import Node
from math import log
from collections import Counter


def ID3(examples, default):
    '''
    Takes in an array of examples, and returns a tree (an instance of Node)
    trained on the examples.  Each example is a dictionary of attribute:value pairs,
    and the target class variable is a special attribute with the name "Class".
    Any missing attributes are denoted with a value of "?"
    '''
    # if there is no example, return a tree with default class label
    if len(examples) == 0:
        return Node(default)

    # if all examples are classified to the same class
    # or if no non-trivial splits are possible (i.e. no split on single example)
    classes = []
    for example in examples:
        classes.append(example['Class'])
    if len(Counter(classes)) == 1 or len(classes) == 1:
        tree = Node(mode_label(examples))
        return tree

    else:
        best_attribute = choose_attribute(examples)
        tree = Node(mode_label(examples))
        tree.attribute = best_attribute

        # find best_attribute_values
        best_attribute_values = []
        for example in examples:
            best_attribute_values.append(example[best_attribute])
        tree.attribute_values = list(set(best_attribute_values))

        for value_i in tree.attribute_values:
            # find examples with best_attribute = value_i
            examples_i = []
            for example in examples:
                if example[best_attribute] == value_i:
                    examples_i.append(example)

            # generate subtree
            subtree = ID3(examples_i, mode_label(examples))
            subtree.examples_labeled = examples_i
            subtree.parent_attribute = best_attribute
            subtree.parent_attribute_value = value_i

            # attach subtree to t
            tree.children[value_i] = subtree
        return tree


TREE = None
def prune(node, examples):
    '''
    Takes in a trained tree and a validation set of examples. Recusively (Postorder)
    prune nodes to improve accuracy on the validation data.
    '''
    global TREE
    TREE = node

    def prune_node(node, examples):
        if len(node.children) == 0:
            accuracy_before_pruning = test(TREE, examples)
            node.pruned = True
            if accuracy_before_pruning >= test(TREE, examples):
                node.pruned = False
            return

        for value, child in node.children.items():
            prune_node(child, examples)

        accuracy_before_pruning = test(TREE, examples)
        node.pruned = True
        if accuracy_before_pruning >= test(TREE, examples):
            node.pruned = False
    prune_node(TREE, examples)


def test(node, examples):
    '''
    Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
    of examples the tree classifies correctly).
    '''
    num_correct_label = 0
    for example in examples:
        if evaluate(node, example) == example['Class']:
            num_correct_label += 1

    return num_correct_label / len(examples)


def evaluate(node, example):
    '''
    Takes in a tree and one example.  Returns the Class value that the tree
    assigns to the example.
    '''
    if len(node.children) == 0:
        return node.label
    else:
        attribute_value = example[node.attribute]
        if attribute_value in node.children and node.children[attribute_value].pruned == False:
            return evaluate(node.children[attribute_value], example)

        # in case the attribute value was pruned or not belong to any existing branch
        # return the mode label of examples with other attribute values for the current attribute
        else:
            examples = []
            for value in node.attribute_values:
                examples += node.children[value].examples_labeled
            return mode_label(examples)


# method to return the most frequent value of an attribute
def mode_attribute_value(examples, attribute):
    values = []
    for example in examples:
        values.append(example[attribute])
    return Counter(values).most_common(1)[0][0]


# method to return most frequent class label in examples
def mode_label(examples):
    classes = []
    for example in examples:
        classes.append(example['Class'])
    return Counter(classes).most_common(1)[0][0]


# method to calculate events probability
def p(num_event, num_possible_outcomes):
    return num_event / num_possible_outcomes


# method to calculate entropy
def H(examples, attribute, attribute_value):
    classes = []
    for example in examples:
        if example[attribute] == attribute_value:
            classes.append(example['Class'])
    counter = Counter(classes)

    # if all examples are classified to the same class, entropy = 0
    if len(counter) == 1:
        return 0
    else:
        entropy = 0
        for c, num_c in counter.items():
            prob = p(num_c, len(classes))
            entropy += prob * (log(prob) / log(2))
        return -entropy


# method to calculate entropy gain
def entropy_gain(examples, attribute):
    values = []
    for example in examples:
        # if value is missing for an attribute, replace '?' with the mode value
        if example[attribute] == '?':
            values.append(mode_attribute_value(examples, attribute))
        else:
            values.append(example[attribute])
    counter = Counter(values)

    entropy = 0
    for attribute_value, num_attribute_value in counter.items():
        entropy += p(num_attribute_value, len(values)) * H(examples, attribute, attribute_value)

    return entropy


# method to choose the best atrribute with maximum information gain
# since the prior entropy is constant with respect to each attribute value,
# we choose attribute based on minimum entropy gain
def choose_attribute(examples):
    chosen_attribute = None
    min_entropy = 10000

    # find all attributes
    attributes = [key for key, value in examples[0].items()]
    attributes.remove('Class')

    for attribute in attributes:
        entropy = entropy_gain(examples, attribute)
        if entropy < min_entropy:
            min_entropy = entropy
            chosen_attribute = attribute

    return chosen_attribute
