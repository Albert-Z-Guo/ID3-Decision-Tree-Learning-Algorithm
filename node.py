class Node:
  def __init__(self, label):
    self.label = label
    self.children = {}
    self.attribute = None
    self.attribute_values = []

    # useful for pruning
    self.pruned = False
    self.examples_labeled = []

    # useful for debugging
    self.parent_attribute = None
    self.parent_attribute_value = None
