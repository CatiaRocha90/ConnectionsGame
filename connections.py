import tkinter as tk
from tkinter import messagebox
import random

# Define the groups and words with colors
GROUPS = {
    "Best": (["Selling", "Kown", "Ever", "Fit"], "#FFFACD"),  # Light Yellow
    "Newbie": (["Rookie", "Starter", "Novice", "A Baby"], "#98FB98"),  # Light Green
    "Gym": (["Gossip", "Lifestyle", "Be strong", "Good time"], "#ADD8E6"),  # Light Blue
    "Buddy": (["Friend", "Partner", "Pal", "Teammate"], "#D8BFD8"),  # Light Purple
}

# "Best": (["Champion", "Top-notch", "Gold", "Excellent"], "#FFFACD"),  # Light Yellow
# "Newbie": (["Rookie", "Starter", "Novice", "A Baby"], "#98FB98"),  # Light Green
# "Gym": (["Weights", "Treadmill", "Squat", "Bench"], "#ADD8E6"),  # Light Blue
# "Buddy": (["Friend", "Partner", "Pal", "Teammate"], "#D8BFD8"),  # Light Purple

# Flatten the groups into a single list of words and shuffle them
WORDS = [(word, group, color) for group, (words, color) in GROUPS.items() for word in words]
random.shuffle(WORDS)

class ConnectionsGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connections Game")
        self.geometry("600x600")
        self.configure(bg="white")
        
        self.selected_words = []  # Stores currently selected words
        self.correct_groups = []  # Tracks completed groups

        # Instructions
        self.instructions = tk.Label(
            self, text="Select 4 words that belong to the same group.", 
            font=("Helvetica", 14), bg="white"
        )
        self.instructions.pack(pady=10)

        # Words Grid
        self.words_frame = tk.Frame(self, bg="white")
        self.words_frame.pack(pady=10)

        self.word_buttons = []  # Stores buttons with their word/group info
        for i, (word, group, color) in enumerate(WORDS):
            btn = tk.Button(
                self.words_frame, text=word, font=("Helvetica", 12), width=15, height=2,
                command=lambda w=word: self.select_word(w), bg="gray", state=tk.NORMAL
            )
            btn.grid(row=i // 4, column=i % 4, padx=10, pady=10)
            self.word_buttons.append((btn, word, group, color))

        # Selected words display
        self.selected_label = tk.Label(self, text="Selected: None", font=("Helvetica", 12), bg="white")
        self.selected_label.pack(pady=10)

        # Check Group Button
        self.check_button = tk.Button(
            self, text="Check Group", font=("Helvetica", 14), 
            command=self.check_group
        )
        self.check_button.pack(pady=10)

    def select_word(self, word):
        if word in self.selected_words:
            messagebox.showwarning("Already Selected", f"{word} is already in your selection.")
            return
        
        self.selected_words.append(word)
        self.update_selected_label()

    def update_selected_label(self):
        if not self.selected_words:
            self.selected_label.config(text="Selected: None")
        else:
            self.selected_label.config(text=f"Selected: {', '.join(self.selected_words)}")
    
    def check_group(self):
        if len(self.selected_words) != 4:
            messagebox.showwarning("Invalid Selection", "You must select exactly 4 words!")
            return

        # Check if all selected words belong to the same group
        groups = set()
        for word in self.selected_words:
            for btn, w, g, color in self.word_buttons:
                if w == word:
                    groups.add(g)
        
        if len(groups) == 1:  # All words belong to the same group
            group = groups.pop()
            if group in self.correct_groups:
                messagebox.showwarning("Already Found", f"You already found the {group} group.")
            else:
                self.correct_groups.append(group)

                # Change button color to indicate completion
                for btn, w, g, color in self.word_buttons:
                    if g == group:
                        btn.config(state=tk.DISABLED, bg="white")

            # Check for game completion
            if len(self.correct_groups) == 4:
                self.show_congratulations()
        else:
            messagebox.showerror("Incorrect Group", "The selected words don't belong to the same group.")
        
        # Reset the selection
        self.reset_selection()

    def reset_selection(self):
        self.selected_words = []
        self.update_selected_label()

    def show_congratulations(self):
        # Arrange the words by group color at the end in specific order
        self.correct_groups.sort()  # Sort groups alphabetically
        group_order = ["Best", "Newbie", "Gym", "Buddy"]  # Desired order

        # Create a frame for the group display
        congrats_frame = tk.Frame(self, bg="white")
        congrats_frame.pack(pady=20)

        # Display each group with its corresponding color and group title in specific order
        for i, group in enumerate(group_order):
            group_words = [word for word, g, color in WORDS if g == group]

            # Create the group title on top with stronger color
            title_label = tk.Label(
                congrats_frame, text=group, font=("Helvetica", 16, "bold"), bg=self.get_group_color(group),
                padx=10, pady=5, width=15, fg="black"  # Stronger title color
            )
            title_label.grid(row=i, column=0, padx=10, pady=5)

            # Display the words in the corresponding color row
            for j, word in enumerate(group_words):
                btn = tk.Button(
                    congrats_frame, text=word, font=("Helvetica", 12), width=15, height=2,
                    state=tk.DISABLED, bg=self.get_group_color(group)
                )
                btn.grid(row=i, column=j + 1, padx=10, pady=5)

        # Display the congratulatory message
        congrats_label = tk.Label(
            self, text="Best Newbie Gym Buddy!", 
            font=("Helvetica", 32, "bold"), fg="green", bg="white"
        )
        congrats_label.pack(expand=True)

        # Optionally, display a restart or exit button
        exit_button = tk.Button(
            self, text="Exit", font=("Helvetica", 14), command=self.destroy
        )
        exit_button.pack(pady=20)

    def get_group_color(self, group):
        # Get color for each group
        for g, (words, color) in GROUPS.items():
            if g == group:
                return color

# Run the game
if __name__ == "__main__":
    app = ConnectionsGame()
    app.mainloop()
