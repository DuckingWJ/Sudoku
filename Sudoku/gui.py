import copy
import tkinter as tk
from tkinter import messagebox

import main


def has_conflict(board, r, c, val):
    for j in range(9):
        if j != c and board[r][j] == val:
            return True
    for i in range(9):
        if i != r and board[i][c] == val:
            return True

    block = main.GRID[r][c]
    for i in range(9):
        for j in range(9):
            if (i != r or j != c) and main.GRID[i][j] == block and board[i][j] == val:
                return True
    return False


def can_place(board, r, c, val):
    for j in range(9):
        if board[r][j] == val:
            return False
    for i in range(9):
        if board[i][c] == val:
            return False
    block = main.GRID[r][c]
    for i in range(9):
        for j in range(9):
            if main.GRID[i][j] == block and board[i][j] == val:
                return False
    return True


def solve_board(board):
    best = None
    best_candidates = None

    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                continue
            candidates = []
            for v in range(1, 10):
                if can_place(board, r, c, v):
                    candidates.append(v)
            if not candidates:
                return None
            if best_candidates is None or len(candidates) < len(best_candidates):
                best = (r, c)
                best_candidates = candidates

    if best is None:
        return [row[:] for row in board]

    r, c = best
    for v in best_candidates:
        board[r][c] = v
        solved = solve_board(board)
        if solved is not None:
            return solved
        board[r][c] = 0

    return None


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.fixed_cells = set()

        self.status_var = tk.StringVar(value="Fill cells with 1-9. Leave blank for unknown.")

        self._build_ui()

    def _build_ui(self):
        board_frame = tk.Frame(self.root, padx=12, pady=12)
        board_frame.pack()

        for r in range(9):
            for c in range(9):
                frame = tk.Frame(
                    board_frame,
                    highlightbackground="#333333",
                    highlightthickness=2 if (r % 3 == 0 or c % 3 == 0) else 1,
                )
                frame.grid(row=r, column=c, padx=(0 if c % 3 else 1), pady=(0 if r % 3 else 1))

                e = tk.Entry(frame, width=2, font=("Consolas", 18), justify="center")
                e.pack(ipadx=5, ipady=5)
                e.bind("<KeyRelease>", self._validate_cell)
                self.entries[r][c] = e

        control = tk.Frame(self.root, pady=8)
        control.pack(fill="x")

        tk.Button(control, text="Process", command=self.process_board, width=12).pack(side="left", padx=6)
        tk.Button(control, text="Clear", command=self.clear_board, width=12).pack(side="left", padx=6)

        tk.Label(self.root, textvariable=self.status_var, anchor="w", padx=12).pack(fill="x")

    def _validate_cell(self, event):
        widget = event.widget
        value = widget.get().strip()
        if value == "":
            widget.config(bg="white")
            return
        if len(value) == 1 and value.isdigit() and "1" <= value <= "9":
            widget.config(bg="white")
            return
        widget.delete(0, tk.END)
        widget.config(bg="#ffd6d6")

    def read_board(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        for r in range(9):
            for c in range(9):
                text = self.entries[r][c].get().strip()
                if text == "":
                    board[r][c] = 0
                else:
                    if not (len(text) == 1 and text.isdigit() and "1" <= text <= "9"):
                        raise ValueError(f"Invalid value at row {r + 1}, col {c + 1}")
                    board[r][c] = int(text)
        return board

    def mark_conflicts(self, board):
        has_any_conflict = False
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val == 0:
                    self.entries[r][c].config(bg="white")
                    continue
                if has_conflict(board, r, c, val):
                    self.entries[r][c].config(bg="#ffcccc")
                    has_any_conflict = True
                else:
                    self.entries[r][c].config(bg="white")
        return has_any_conflict

    def write_board(self, board, highlight_new=False):
        for r in range(9):
            for c in range(9):
                old_val = self.entries[r][c].get().strip()
                old_num = int(old_val) if old_val.isdigit() else 0

                self.entries[r][c].delete(0, tk.END)
                if board[r][c] != 0:
                    self.entries[r][c].insert(0, str(board[r][c]))

                if highlight_new and old_num == 0 and board[r][c] != 0:
                    self.entries[r][c].config(fg="#0a66c2")
                else:
                    self.entries[r][c].config(fg="black")

    def process_board(self):
        try:
            board = self.read_board()
        except ValueError as ex:
            self.status_var.set(str(ex))
            messagebox.showerror("Input Error", str(ex))
            return

        if self.mark_conflicts(board):
            self.status_var.set("Current board has conflicts. Please fix highlighted cells.")
            messagebox.showwarning("Conflict", "Board has conflicts. Red cells violate Sudoku rules.")
            return

        is_complete = all(board[r][c] != 0 for r in range(9) for c in range(9))

        if is_complete:
            ok = main.checkSudoku(board)
            if ok:
                self.status_var.set("Completed board is legal.")
                messagebox.showinfo("Result", "Sudoku is complete and legal.")
            else:
                self.status_var.set("Completed board is illegal.")
                messagebox.showerror("Result", "Sudoku is complete but illegal.")
            return

        # Keep using main as the rule engine state carrier.
        for r in range(9):
            for c in range(9):
                main.mp[r][c] = board[r][c]

        solved = solve_board(copy.deepcopy(board))
        if solved is None:
            self.status_var.set("No solution found for current board.")
            messagebox.showerror("Result", "No valid solution exists for this board.")
            return

        self.write_board(solved, highlight_new=True)
        self.status_var.set("Board was incomplete. A solved result has been filled in blue.")
        messagebox.showinfo("Solved", "Incomplete board solved. Newly filled cells are blue.")

    def clear_board(self):
        for r in range(9):
            for c in range(9):
                e = self.entries[r][c]
                e.delete(0, tk.END)
                e.config(bg="white", fg="black")
        self.status_var.set("Board cleared.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.resizable(False, False)
    root.mainloop()
