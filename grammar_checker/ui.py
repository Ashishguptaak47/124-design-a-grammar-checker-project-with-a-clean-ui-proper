import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from .engine import GrammarEngine, Issue, IssueType


class GrammarCheckerUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Grammar & Style Studio")
        self.root.geometry("950x650")
        self.root.minsize(800, 500)

        self.engine = GrammarEngine()
        self.issues: List[Issue] = []

        self._setup_styles()
        self._build_layout()
        self._bind_events()
        self._load_sample_text()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Palette
        self.BG_COLOR = "#1e1e2e"
        self.PANEL_BG = "#252538"
        self.TEXT_FG = "#cdd6f4"
        self.ACCENT = "#89b4fa"

        self.root.configure(bg=self.BG_COLOR)

        self.style.configure("TFrame", background=self.BG_COLOR)
        self.style.configure("Panel.TFrame", background=self.PANEL_BG)
        self.style.configure("TLabel", background=self.BG_COLOR, foreground=self.TEXT_FG, font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground=self.ACCENT)
        self.style.configure("Stat.TLabel", font=("Segoe UI", 9), foreground="#a6adc8")

        self.style.configure("TButton", font=("Segoe UI", 9.5, "bold"), padding=6)
        self.style.map("TButton",
                       background=[("active", "#74c7ec"), ("!disabled", self.ACCENT)],
                       foreground=[("!disabled", "#11111b")])

    def _build_layout(self):
        # Header Frame
        header_frame = ttk.Frame(self.root, padding=(15, 10))
        header_frame.pack(fill=tk.X)

        title_lbl = ttk.Label(header_frame, text="Grammar & Style Studio", style="Header.TLabel")
        title_lbl.pack(side=tk.LEFT)

        btn_check = ttk.Button(header_frame, text="Check Text", command=self.run_check)
        btn_check.pack(side=tk.RIGHT, padx=5)

        btn_clear = ttk.Button(header_frame, text="Clear", command=self.clear_text)
        btn_clear.pack(side=tk.RIGHT, padx=5)

        # Main Content Split
        main_split = ttk.Frame(self.root, padding=10)
        main_split.pack(fill=tk.BOTH, expand=True)

        # Left Text Editor Frame
        editor_frame = ttk.Frame(main_split)
        editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        editor_lbl = ttk.Label(editor_frame, text="Input Document", font=("Segoe UI", 10, "bold"))
        editor_lbl.pack(anchor=tk.W, pady=(0, 5))

        self.text_editor = tk.Text(
            editor_frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#181825",
            fg="#cdd6f4",
            insertbackground="#f5e0dc",
            selectbackground="#45475a",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.text_editor.pack(fill=tk.BOTH, expand=True)

        # Right Sidebar Issues Panel
        sidebar_frame = ttk.Frame(main_split, width=320, style="Panel.TFrame", padding=10)
        sidebar_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(5, 0))
        sidebar_frame.pack_propagate(False)

        sidebar_lbl = ttk.Label(sidebar_frame, text="Issues & Suggestions", style="Header.TLabel", background=self.PANEL_BG)
        sidebar_lbl.pack(anchor=tk.W, pady=(0, 10))

        # Scrollable Issues List
        self.issues_listbox = tk.Listbox(
            sidebar_frame,
            bg="#1e1e2e",
            fg="#cdd6f4",
            selectbackground="#45475a",
            selectforeground="#f5e0dc",
            font=("Segoe UI", 9.5),
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#313244"
        )
        self.issues_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.issues_listbox.bind("<<ListboxSelect>>", self.on_issue_select)

        # Fix Panel
        self.fix_frame = ttk.Frame(sidebar_frame, style="Panel.TFrame")
        self.fix_frame.pack(fill=tk.X)

        self.issue_detail_lbl = ttk.Label(self.fix_frame, text="Select an issue to view suggestions.",
                                          wraplength=280, justify=tk.LEFT, background=self.PANEL_BG)
        self.issue_detail_lbl.pack(fill=tk.X, pady=(0, 8))

        self.btn_apply_fix = ttk.Button(self.fix_frame, text="Apply Fix", command=self.apply_fix, state=tk.DISABLED)
        self.btn_apply_fix.pack(fill=tk.X)

        # Footer Status Bar
        self.status_bar = ttk.Frame(self.root, padding=(15, 5))
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.stats_lbl = ttk.Label(self.status_bar, text="Words: 0 | Chars: 0 | Sentences: 0 | Readability Score: 100", style="Stat.TLabel")
        self.stats_lbl.pack(side=tk.LEFT)

        # Text Tags Configuration for Highlights
        self.text_editor.tag_config(IssueType.SPELLING.value, underline=True, underlinefg="#f38ba8")
        self.text_editor.tag_config(IssueType.GRAMMAR.value, underline=True, underlinefg="#fab387")
        self.text_editor.tag_config(IssueType.PUNCTUATION.value, underline=True, underlinefg="#f9e2af")
        self.text_editor.tag_config(IssueType.STYLE.value, underline=True, underlinefg="#89b4fa")

    def _bind_events(self):
        self.text_editor.bind("<KeyRelease>", self._on_key_release)

    def _on_key_release(self, event=None):
        text = self.text_editor.get("1.0", tk.END)
        stats = self.engine.calculate_stats(text)
        self.stats_lbl.config(
            text=f"Words: {stats['words']} | Chars: {stats['chars']} | Sentences: {stats['sentences']} | Readability Score: {stats['readability']}/100"
        )

    def _load_sample_text(self):
        sample = "i think that the the checker is working. He could of done better when he wrote a apple phrase. irregardless, your welcome!"
        self.text_editor.delete("1.0", tk.END)
        self.text_editor.insert("1.0", sample)
        self.run_check()

    def clear_text(self):
        self.text_editor.delete("1.0", tk.END)
        self.issues_listbox.delete(0, tk.END)
        self.issues.clear()
        self.issue_detail_lbl.config(text="Select an issue to view suggestions.")
        self.btn_apply_fix.config(state=tk.DISABLED)
        self._on_key_release()

    def run_check(self):
        # Clear tag highlights
        for tag in [t.value for t in IssueType]:
            self.text_editor.tag_remove(tag, "1.0", tk.END)

        self.issues_listbox.delete(0, tk.END)
        text = self.text_editor.get("1.0", tk.END)
        self.issues = self.engine.check(text)

        if not self.issues:
            self.issues_listbox.insert(tk.END, "No issues found! Great job.")
            self.issue_detail_lbl.config(text="Text looks clean.")
            self.btn_apply_fix.config(state=tk.DISABLED)
            return

        for idx, issue in enumerate(self.issues):
            label = f"[{issue.issue_type.value}] {issue.original} -> {issue.message}"
            self.issues_listbox.insert(tk.END, label)

            # Apply highlight tag
            start_idx = f"1.0 + {issue.start} chars"
            end_idx = f"1.0 + {issue.end} chars"
            self.text_editor.tag_add(issue.issue_type.value, start_idx, end_idx)

        self._on_key_release()

    def on_issue_select(self, event):
        selection = self.issues_listbox.curselection()
        if not selection or not self.issues:
            return
        index = selection[0]
        if index >= len(self.issues):
            return

        issue = self.issues[index]
        msg = f"Type: {issue.issue_type.value}\nDetail: {issue.message}"
        if issue.suggestions:
            msg += f"\nSuggestion: '{issue.suggestions[0]}'"
            self.btn_apply_fix.config(state=tk.NORMAL)
        else:
            self.btn_apply_fix.config(state=tk.DISABLED)

        self.issue_detail_lbl.config(text=msg)

        # Highlight & scroll to issue in text widget
        start_idx = f"1.0 + {issue.start} chars"
        end_idx = f"1.0 + {issue.end} chars"
        self.text_editor.see(start_idx)
        self.text_editor.tag_add(tk.SEL, start_idx, end_idx)
        self.text_editor.focus_set()

    def apply_fix(self):
        selection = self.issues_listbox.curselection()
        if not selection or not self.issues:
            return
        index = selection[0]
        if index >= len(self.issues):
            return

        issue = self.issues[index]
        if not issue.suggestions:
            return

        replacement = issue.suggestions[0]
        start_idx = f"1.0 + {issue.start} chars"
        end_idx = f"1.0 + {issue.end} chars"

        self.text_editor.delete(start_idx, end_idx)
        self.text_editor.insert(start_idx, replacement)

        # Re-check text to refresh coordinates
        self.run_check()
