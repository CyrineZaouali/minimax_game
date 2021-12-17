from tree import Tree
from anytree import Node
from random import random


class Game:
    def __init__(self):
        self.number_of_tokens: int = None
        self.isMaxFirst: bool = None
        self.tree: Tree = None
        self.isCurrentPlayer: bool = None
        self.isAlgoMinMax: bool = None
        self.play()

    def play(self):
        self.show_title()
        self.show_insert_number_of_tokens()
        self.show_algorithm_choice()
        # self.show_turn_choice()
        self.isMaxFirst = True
        self.creating_tree()
        current_node = self.tree.rootNode
        while  self.available_moving_point(current_node):
            if self.isCurrentPlayer:
                current_node = self.get_max_moving_choice(current_node)
            else:
                current_node = self.get_min_moving_choice(current_node)
            self.isCurrentPlayer = not self.isCurrentPlayer
        self.show_winner()
        self.show_rendered_tree()

    @staticmethod
    def show_title():
        print("\t **********************************************")
        print("\t *           TP AI -  MINIMAX GAME            *")
        print("\t **********************************************\n\n")

    def show_insert_number_of_tokens(self):
        while True:
            self.number_of_tokens = int(input("Inserez le nombre de tokens\t: "))
            if self.number_of_tokens > 0:
                break
            print("Le nombre doit etre positif!\n")

    def show_algorithm_choice(self):
        print("Les algorithmes disponibles:")
        print("1. Algorithme Min Max")
        print("2. Algorithme Alpha Beta\n")
        while True:
            choice = int(input("Choisissez un algorithme\t: "))
            if choice in range(1, 3):
                self.isAlgoMinMax = (choice == 1)
                break
            print("Choix invalide.\n")

    def show_turn_choice(self):
        self.isMaxFirst = True if random() >= 0.5 else False
        print("Tirage au sort...")
        print(("Vous êtes" if self.isMaxFirst else "MIN est ") + " le premier joueur")
        print("-----------------------------------------------------------------------------\n")

    def creating_tree(self):
        print("Arbre en construction....")
        self.tree = Tree(self.number_of_tokens, self.isMaxFirst, self.isAlgoMinMax)
        print("Arbre créé.")
        print("-----------------------------------------------------------------------------\n\n")
        self.isCurrentPlayer = self.isMaxFirst

    def available_moving_point(self, current_node):
        print("\n-------"+("VOTRE TOUR" if self.isCurrentPlayer else "LE TOUR DE MIN") + "------")
        print("Les actions possibles")
        if current_node.is_leaf:
            print("\nPas d'actions possibles :(", end="")
            return False
        for index, child in enumerate(current_node.children):
            print(str(index + 1) + ". [" + ("-".join(map(str, child.node_value))) + "]")
        print("")
        return True

    def get_min_moving_choice(self, current_node):
        choice_child = self.check_min_moving_choice(current_node)
        print("Action de MIN\t: [" + ("-".join(map(str, choice_child.node_value))) + "]")
        return choice_child

    @staticmethod
    def check_min_moving_choice(current_node) -> Node:
        child_choice = current_node.children[0]
        for child in current_node.children:
            if child.utility:
                if child.utility < child_choice.utility:
                    child_choice = child
        return child_choice

    @staticmethod
    def get_max_moving_choice(current_node):
        while True:
            moving_choice = int(input("Choisissez votre action\t: "))
            if moving_choice - 1 in range(0, len(current_node.children)):
                child = current_node.children[moving_choice - 1]
                print("Votre action\t\t: [" + ("-".join(map(str, child.node_value))) + "]")
                return child
            print("Action invalide\n")

    def show_rendered_tree(self):
        print("-----------------------------------------------------------------------------")
        print("Les noeuds visités: " + str(self.tree.nodesVisited))
        is_show_tree = input("Voir l'arbre de jeu  [o/n]? ")
        if is_show_tree.capitalize() == "O":
            print(str(self.tree))

    def show_winner(self):
        print("\n\n\t ***********************")
        print("\t"+(" *   VOUS AVEZ GAGNE   *" if not self.isCurrentPlayer else " *   MIN A GAGNE       * "))
        self.isCurrentPlayer = not self.isCurrentPlayer
        print("\t"+(" *   VOUS AVEZ " if not self.isCurrentPlayer else " *   MIN A ") + "PERDU !     *")
        print("\t ***********************\n\n")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Game()

