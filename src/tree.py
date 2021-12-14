from anytree import Node
from anytree import RenderTree


class Tree:
    def __init__(self, rootValue: int, isMaxFirst: bool, isAlgoMinMax: bool):
        self.rootNode = Node(str(rootValue), node_value=[rootValue], isRoot=True, utility=None)
        self.nodesVisited: int = 0
        self.isMaxFirst = isMaxFirst
        self.generate_tree(self.rootNode)
        if isAlgoMinMax:
            self.evaluate_tree_min_max(self.rootNode)
        else:
            self.evaluate_tree_alpha_beta(self.rootNode)

    def generate_tree(self, currentNode) -> None:
        max_value = max(currentNode.node_value)
        if max_value <= 2:
            return
        else:
            current_node_values = currentNode.node_value.copy()
            for index, value in enumerate(current_node_values): # enumerate() : return an enumerate object
                total_children = (int(value / 2) - 1) if value % 2 == 0 else int(value / 2)
                for i in range(1, total_children + 1):
                    child_value = current_node_values.copy()
                    child_value[index] -= i
                    child_value.insert(index + 1, i)
                    child = Node(currentNode.name + "-" + str(i), parent=currentNode, node_value=child_value,
                                 utility=None)
                    self.generate_tree(child)

    def evaluate_tree_min_max(self, currentNode: Node) -> None:
        if currentNode.is_leaf:
            currentNode.utility = 1 if self.isMaxFirst == (currentNode.depth % 2 == 1) else -1
        else:
            child_evaluate_values = []
            for child in currentNode.children:
                self.evaluate_tree_min_max(child)
                child_evaluate_values.append(child.utility)
            evaluate = max(child_evaluate_values) if (currentNode.depth % 2 == 0) else min(child_evaluate_values)
            currentNode.utility = evaluate
        self.nodesVisited += 1

    def evaluate_tree_alpha_beta(self, currentNode: Node, parentEvaluator: int = None) -> None:
        if currentNode.is_leaf:
            currentNode.utility = 1 if self.isMaxFirst == (currentNode.depth % 2 == 1) else -1
        else:
            child_evaluate_values = []
            current_evaluation: int = None
            is_current_max = currentNode.depth % 2 == 0
            for child in currentNode.children:
                self.evaluate_tree_alpha_beta(child, current_evaluation)
                if child.utility:
                    if parentEvaluator:
                        skipped: bool = (child.utility >= parentEvaluator) if is_current_max else (
                                parentEvaluator <= child.utility)
                        if skipped:
                            return
                    if not current_evaluation or (
                            is_current_max == child.utility > current_evaluation): current_evaluation = child.utility
                    child_evaluate_values.append(child.utility)
            evaluate = max(child_evaluate_values) if is_current_max else min(child_evaluate_values)
            currentNode.utility = evaluate
        self.nodesVisited += 1

    def __str__(self) -> str:
        return RenderTree(self.rootNode).by_attr(lambda n: ("-".join(map(str, n.node_value)) +
                                                            "  [" + str(n.utility) + "]"))
