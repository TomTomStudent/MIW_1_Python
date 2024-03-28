import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, font
import random
import numpy as np

#Responsible for all simple formulas
class Model:
    #Creating the winning pairs
    WINNING_MOVES = {
        "Rock": "Scissors",
        "Paper": "Rock",
        "Scissors": "Paper"
    }

    #Decides winner based on WINNING_MOVES
    def determine_winner(self, user_choice, opponent_choice):
        if self.WINNING_MOVES[user_choice] == opponent_choice:
            return "Winner!"
        elif self.WINNING_MOVES[opponent_choice] == user_choice:
            return "Loser!"
        else:
            return "Draw!"

    def adjust_score(self, user_score, opponent_score, outcome):
        if outcome == "Winner!":
            user_score += 1
        elif outcome == "Loser!":
            opponent_score += 1
        return [user_score, opponent_score]

    def check_score(self, user_score, opponent_score):
        if user_score >= 10 or opponent_score >= 10:
            return 1
        return 0

    def declare_winner(self, user_score, opponent_score):
        if (user_score == 10 or user_score>opponent_score):
            return "USER WINS!!!"
        elif (opponent_score == 10 or opponent_score>user_score):
            return "OPPONENT WINS :("
        else:
            return "TIME'S UP, TIE!"

    def check_turn(self, turn):
        if turn >= 30:
            return 1
        return 0

    #Chooses random option as primary choice, since there were no prior user inputs
    def robot_choice(self):
        choices = ["Rock", "Paper", "Scissors"]
        return random.choice(choices)

    def end_of_round_check(self, turn_check, point_check):
        if turn_check == 1 or point_check == 1:
            return 1
        return 0
    
    def word_to_letter(self, move):
        if (move == "Rock"):
            return "T"
        elif (move == "Paper"):
            return "A"
        elif (move == "Scissors"):
            return "C"
        
    def letter_to_word(self, move):
        if (move == "T"):
            return "Rock"
        elif (move == "A"):
            return "Paper"
        elif (move == "C"):
            return "Scissors"

class MarkovModel:
    def __init__(self):
        #X-axis
        self.markov_states = ["VA", "VT", "VC", "LA", "LT", "LC"]
        #Y-axis
        self.TRANSITION_MATRIX = {
            "VA": [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],
            "VT": [0.1, 0.2, 0.2, 0.1, 0.1, 0.3],
            "VC": [0.4, 0.2, 0.1, 0.1, 0.1, 0.1],
            "LA": [0.1, 0.1, 0.3, 0.1, 0.2, 0.2],
            "LT": [0.3, 0.1, 0.3, 0.1, 0.1, 0.1],
            "LC": [0.1, 0.2, 0.2, 0.2, 0.2, 0.1]
        }
        #Filled with fill_final_matrix
        self.FINAL_MATRIX = {
            "A": [0, 0, 0],
            "T": [0, 0, 0],
            "C": [0, 0, 0]
        }

    #goes through each line and summs the probabilities
    def fill_final_matrix(self):
        for i, state in enumerate(self.markov_states):
            action = state[1] 
            choices = [row[i] for row in self.TRANSITION_MATRIX.values()] 
            self.FINAL_MATRIX[action] = [x + y for x, y in zip(self.FINAL_MATRIX[action], choices)] 

    #based on final matrix and opponents last move, guesses the most next move aka the one with the heighest probability
    def markov_choice(self, opponent_last_move):
        self.fill_final_matrix() 
        move_chosen = max(self.FINAL_MATRIX[opponent_last_move])
        choices = ["A", "T", "C"]
        move_chosen_index = self.FINAL_MATRIX[opponent_last_move].index(move_chosen)
        return choices[move_chosen_index]

class View:
    def __init__(self, root):
        self.root = root
        self.user_choice_label = None
        self.opponent_choice_label = None
        self.outcome_label = None
        self.user_score_label = None
        self.turn_label = None
        self.opponent_score_label = None
        self.controller = None
        self.create_widgets()

    def create_widgets(self):
        #General settings
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        arial_bold = font.Font(family="Arial", weight="bold")
        arial_regular = font.Font(family="Arial")


        #Top
        top_frame = ttk.Frame(self.root)
        top_frame.grid(row=0, column=0, sticky="nsew",  pady=5)
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(7, weight=1)

        ttk.Label(top_frame, text="Your score: ").grid(row=0, column=1, padx=0, pady=0)
        self.user_score_label = ttk.Label(top_frame, text="0", font=font.Font(weight="bold"))
        self.user_score_label.grid(row=0, column=2, padx=0, pady=0)

        ttk.Label(top_frame, text="Turn: ").grid(row=0, column=3, padx=0, pady=0)
        self.turn_label = ttk.Label(top_frame, text="0", font=font.Font(weight="bold"))
        self.turn_label.grid(row=0, column=4, padx=0, pady=0)

        ttk.Label(top_frame, text="Opponent score: ").grid(row=0, column=5, padx=0, pady=0)
        self.opponent_score_label = ttk.Label(top_frame, text="0", font=font.Font(weight="bold"))
        self.opponent_score_label.grid(row=0, column=6, padx=0, pady=0)

        #Middle
        middle_frame = ttk.Frame(self.root)
        middle_frame.grid(row=1, column=0, sticky="nsew", pady=5)

        middle_frame.columnconfigure(0, weight=1)
        middle_frame.columnconfigure(1, weight=1)
        middle_frame.columnconfigure(2, weight=1)

        ttk.Label(middle_frame, text="Your Choice: ").grid(row=0, column=0, padx=0, pady=0)
        self.user_choice_label = ttk.Label(middle_frame, text="Waiting...", font=font.Font(weight="bold"))
        self.user_choice_label.grid(row=1, column=0, padx=2, pady=5)

        ttk.Label(middle_frame, text="Outcome: ").grid(row=0, column=1, padx=0, pady=0)
        self.outcome_label = ttk.Label(middle_frame, text="", font=font.Font(weight="bold"))
        self.outcome_label.grid(row=1, column=1, padx=2, pady=5)

        ttk.Label(middle_frame, text="Opponent's Choice: ").grid(row=0, column=2, padx=0, pady=0)
        self.opponent_choice_label = ttk.Label(middle_frame, text="Waiting...", font=font.Font(weight="bold"))
        self.opponent_choice_label.grid(row=1, column=2, padx=2, pady=5)


        self.rock_image = PhotoImage(file="images/rock.png")
        self.paper_image = PhotoImage(file="images/paper.png")
        self.scissors_image = PhotoImage(file="images/scissors.png")

        #Bottom
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.grid(row=2, column=0, sticky="nsew")

        bottom_frame.rowconfigure(0, weight=1)
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.columnconfigure(2, weight=1)

        rock_button = ttk.Button(bottom_frame, image=self.rock_image, command=lambda: self.controller.round(0))
        rock_button.grid(row=0, column=0, padx=10, pady=5)

        paper_button = ttk.Button(bottom_frame, image=self.paper_image, command=lambda: self.controller.round(1))
        paper_button.grid(row=0, column=1, padx=10, pady=5)

        scissors_button = ttk.Button(bottom_frame, image=self.scissors_image, command=lambda: self.controller.round(2))
        scissors_button.grid(row=0, column=2, padx=10, pady=5)    

    def set_controller(self, controller):
        self.controller = controller


class Controller:
    def __init__(self, root):
        self.root = root
        self.model = Model()
        self.markov = MarkovModel()
        self.user_score = 0
        self.opponent_score = 0
        self.turn = 0
        self.view = View(root)
        self.view.set_controller(self)
        self.user_last_choice = ""

    #option is a parameter that passes which button is pressed, it corresponds to the index in user_choices
    def round(self, option):
        user_choices = ["Rock", "Paper", "Scissors"]
        user_choice = user_choices[option]

        #if it is turn 0, the oponent did not have a previous choice so the opponent choice is chosen randomly, otherwise the markov chains are used
        if (self.turn>0):
            opponent_choice = self.model.letter_to_word(self.markov.markov_choice(self.user_last_choice))
        else:
            opponent_choice = self.model.robot_choice()
        self.user_last_choice =  self.model.word_to_letter(user_choice)

        #result of the round is calculated
        result = self.model.determine_winner(user_choice, opponent_choice)

        #label strings are set
        self.view.user_choice_label.config(text=user_choice)
        self.view.opponent_choice_label.config(text=opponent_choice)
        self.view.outcome_label.config(text=result)
        
        #label for user and opponent score is updated
        self.update_score(result)
        #turn is increased and game checks for end of game
        self.update_turn()

    def update_score(self, result):
        self.user_score, self.opponent_score = self.model.adjust_score(self.user_score, self.opponent_score, result)
        self.view.user_score_label.config(text=str(self.user_score))
        self.view.opponent_score_label.config(text=str(self.opponent_score))

    #new window pops up which if closed, closes the entire app
    def update_turn(self):
        self.turn += 1
        self.view.turn_label.config(text=str(self.turn))
        if self.model.end_of_round_check(self.model.check_turn(self.turn), self.model.check_score(self.user_score, self.opponent_score)):
            result = self.model.declare_winner(self.user_score, self.opponent_score)
            messagebox.showinfo("Game Over", result)
            self.root.destroy()


def main():
    root = tk.Tk()
    root.title("Rock, Paper, Scissors")
    Controller(root)
    root.mainloop()


if __name__ == "__main__":
    main()
