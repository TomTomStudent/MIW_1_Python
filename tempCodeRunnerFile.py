import tkinter as tk
from tkinter import ttk, messagebox
import random

class Model:
    WINNING_MOVES = {
        "Rock": "Scissors",
        "Paper": "Rock",
        "Scissors": "Paper"
    }

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
        if user_score == 10:
            return "USER WINS!!!"
        return "OPPONENT WINS :("

    def check_turn(self, turn):
        if turn > 30:
            return 1
        return 0

    def robot_choice(self):
        choices = ["Rock", "Paper", "Scissors"]
        return random.choice(choices)

    def end_of_round_check(self, turn_check, point_check):
        if turn_check == 1 or point_check == 1:
            return 1
        return 0


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
        # Creating Labels
        ttk.Label(self.root, text="Your score: ").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.root, text="Opponent score: ").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(self.root, text="Turn: ").grid(row=1, column=0, padx=5, pady=5)
        self.user_score_label = ttk.Label(self.root, text="0")
        self.user_score_label.grid(row=0, column=1, padx=5, pady=5)
        self.opponent_score_label = ttk.Label(self.root, text="0")
        self.opponent_score_label.grid(row=0, column=3, padx=5, pady=5)
        self.turn_label = ttk.Label(self.root, text="0")
        self.turn_label.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Your Choice: ").grid(row=2, column=0, padx=5, pady=5)
        self.user_choice_label = ttk.Label(self.root, text="Waiting...")
        self.user_choice_label.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(self.root, text="Outcome: ").grid(row=2, column=2, padx=5, pady=5)
        self.outcome_label = ttk.Label(self.root, text="DRAW!")
        self.outcome_label.grid(row=2, column=3, padx=5, pady=5)
        ttk.Label(self.root, text="Opponent's Choice: ").grid(row=3, column=0, padx=5, pady=5)
        self.opponent_choice_label = ttk.Label(self.root, text="Waiting...")
        self.opponent_choice_label.grid(row=3, column=1, padx=5, pady=5)

        # Creating Buttons
        ttk.Button(self.root, text="Rock", command=lambda: self.controller.round(0)).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(self.root, text="Paper", command=lambda: self.controller.round(1)).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Scissors", command=lambda: self.controller.round(2)).grid(row=4, column=2, padx=5, pady=5)

    def set_controller(self, controller):
        self.controller = controller


class Controller:
    def __init__(self, root):
        self.root = root
        self.model = Model()
        self.user_score = 0
        self.opponent_score = 0
        self.turn = 0
        self.view = View(root)
        self.view.set_controller(self)

    def round(self, option):
        user_choices = ["Rock", "Paper", "Scissors"]
        user_choice = user_choices[option]
        opponent_choice = self.model.robot_choice()
        self.view.opponent_choice_label.config(text="Chosen")
        result = self.model.determine_winner(user_choice, opponent_choice)
        self.view.opponent_choice_label.config(text=opponent_choice)
        self.view.outcome_label.config(text=result)
        self.update_score(result)
        self.update_turn()

    def update_score(self, result):
        self.user_score, self.opponent_score = self.model.adjust_score(self.user_score, self.opponent_score, result)
        self.view.user_score_label.config(text=str(self.user_score))
        self.view.opponent_score_label.config(text=str(self.opponent_score))

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
