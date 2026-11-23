import sys
import tkinter as tk
from grammar_checker.ui import GrammarCheckerUI


def main():
    try:
        root = tk.Tk()
        app = GrammarCheckerUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Error initializing application: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
