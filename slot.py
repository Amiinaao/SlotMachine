import random
import tkinter as tk
from tkinter import messagebox

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 4,
    "B": 5,
    "C": 2,
    "D": 3
}


class SlotMachineGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Slot Machine")

        self.balance = tk.IntVar()
        self.lines = tk.IntVar()
        self.bet = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Current Balance:").grid(row=0, column=0, sticky='w')
        tk.Label(self.master, textvariable=self.balance).grid(row=0, column=1, sticky='w')

        tk.Label(self.master, text="Number of Lines:").grid(row=1, column=0, sticky='w')
        tk.Entry(self.master, textvariable=self.lines).grid(row=1, column=1, sticky='w')

        tk.Label(self.master, text="Bet Amount:").grid(row=2, column=0, sticky='w')
        tk.Entry(self.master, textvariable=self.bet).grid(row=2, column=1, sticky='w')

        tk.Button(self.master, text="Spin", command=self.spin).grid(row=3, columnspan=2)

        self.result_labels = [[None for _ in range(COLS)] for _ in range(ROWS)]

    def spin(self):
        lines = self.lines.get()
        bet = self.bet.get()
        total_bet = bet * lines

        if total_bet <= 0:
            messagebox.showerror("Error", "Invalid bet amount.")
            return

        if total_bet > self.balance.get():
            messagebox.showerror("Error", "Not enough balance.")
            return

        slots = self.get_slot_machine_spin(ROWS, COLS)
        self.display_slots(slots)

        winnings, _ = self.check_winnings(slots, lines, bet)

        if winnings > 0:
            self.balance.set(self.balance.get() + winnings)
            messagebox.showinfo("Congratulations", f"You won ${winnings}!")
        else:
            self.balance.set(self.balance.get() - total_bet)
            messagebox.showinfo("No Luck", "Sorry, you didn't win anything.")

    def get_slot_machine_spin(self, rows, cols):
        all_symbols = []
        for symbol, count in symbol_count.items():  # Rename symbol_count to count
            for _ in range(count):
                all_symbols.append(symbol)

        columns = []
        for _ in range(cols):
            column = random.sample(all_symbols, rows)
            columns.append(column)
        return columns

    def display_slots(self, slots):
        for i in range(ROWS):
            for j in range(COLS):
                if self.result_labels[i][j] is not None:
                    self.result_labels[i][j].destroy()
                self.result_labels[i][j] = tk.Label(self.master, text=slots[j][i], borderwidth=1, relief="solid", width=5, height=2)
                self.result_labels[i][j].grid(row=i+4, column=j)

    def check_winnings(self, columns, lines, bet):
        winnings = 0
        for line in range(lines):
            symbol = columns[line][0]
            for column in columns:
                symbol_to_check = column[line]
                if symbol != symbol_to_check:
                    break
            else:
                winnings += symbol_value[symbol] * bet

        return winnings, lines


def main():
 
    root = tk.Tk()
    app = SlotMachineGUI(root)
    app.balance.set()

    # Center  GUI window on the screen
    window_width = 300  
    window_height = 300  
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    root.mainloop()


if __name__ == "__main__":
    main()
