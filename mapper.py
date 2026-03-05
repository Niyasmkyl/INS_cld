"""
NLP Text Mapper — Scientific Data-Tool GUI
Two text inputs → processed output via your backend function
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, font
import threading
import time


# ─────────────────────────────────────────────
#  BACKEND HOOK — replace this with your logic
# ─────────────────────────────────────────────
def process_inputs(input_a: str, input_b: str) -> str:
    """
    Plug your NLP backend here.
    Receives two strings, returns one output string.
    """
    # Example: simple concatenation + word stats
    time.sleep(0.6)  # simulate processing delay
    combined = f"{input_a.strip()} {input_b.strip()}"
    words = combined.split()
    unique = set(w.lower() for w in words)
    return (
        f"MERGED OUTPUT\n{'─'*40}\n{combined}\n\n"
        f"STATISTICS\n{'─'*40}\n"
        f"  Total words   : {len(words)}\n"
        f"  Unique words  : {len(unique)}\n"
        f"  Characters    : {len(combined)}\n"
        f"  Input A tokens: {len(input_a.split())}\n"
        f"  Input B tokens: {len(input_b.split())}\n"
    )
# ─────────────────────────────────────────────


# ── Colour palette ───────────────────────────
BG        = "#0d1117"
PANEL     = "#161b22"
BORDER    = "#21262d"
ACCENT    = "#58a6ff"
ACCENT2   = "#3fb950"
TEXT      = "#e6edf3"
TEXT_DIM  = "#8b949e"
TEXT_DARK = "#0d1117"
WARNING   = "#f78166"
MONO      = ("Courier New", 10)


class NLPMapperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NLP Text Mapper  v1.0")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(820, 640)

        self._build_ui()
        self.update_idletasks()
        # Centre window
        w, h = 920, 720
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ── UI Construction ───────────────────────
    def _build_ui(self):
        self._build_header()
        self._build_body()
        self._build_status_bar()

    def _build_header(self):
        hdr = tk.Frame(self, bg=PANEL, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(
            hdr, text="◈  INERTIAL NAVIGATION SYSTEM",
            bg=PANEL, fg=ACCENT,
            font=("Courier New", 15, "bold"),
            padx=20
        ).pack(side="left", pady=12)

        tk.Label(
            hdr, text="Frequency & Diameter → Navigation System",
            bg=PANEL, fg=TEXT_DIM,
            font=("Courier New", 9),
        ).pack(side="left", pady=18)

        # right-side badge
        badge = tk.Frame(hdr, bg=BORDER, padx=10, pady=4)
        badge.pack(side="right", padx=16, pady=12)
        tk.Label(badge, text="READY", bg=BORDER, fg=ACCENT2,
                 font=("Courier New", 8, "bold")).pack()

        # thin accent line at bottom
        tk.Frame(self, bg=ACCENT, height=1).pack(fill="x")

    def _build_body(self):
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=16)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(2, weight=1)
        body.rowconfigure(1, weight=1)
        body.rowconfigure(3, weight=2)

        # ── Input A ──────────────────────────
        self._section_label(body, "INPUT  A", ACCENT, row=0, col=0)
        self.box_a = self._text_box(body, row=1, col=0)

        # ── Arrow / Run button ────────────────
        mid = tk.Frame(body, bg=BG, width=80)
        mid.grid(row=0, column=1, rowspan=2, padx=8, sticky="ns")
        mid.pack_propagate(False)

        tk.Frame(mid, bg=BG).pack(expand=True)  # spacer

        self.run_btn = tk.Button(
            mid, text="▶\nRUN",
            bg=ACCENT, fg=TEXT_DARK,
            font=("Courier New", 9, "bold"),
            relief="flat", cursor="hand2",
            width=6, height=3,
            activebackground="#79c0ff",
            command=self._run
        )
        self.run_btn.pack(pady=4)

        tk.Label(mid, text="↕", bg=BG, fg=TEXT_DIM,
                 font=("Courier New", 18)).pack(pady=2)

        self.clear_btn = tk.Button(
            mid, text="CLR",
            bg=BORDER, fg=TEXT_DIM,
            font=("Courier New", 8),
            relief="flat", cursor="hand2",
            width=5,
            activebackground=PANEL,
            command=self._clear
        )
        self.clear_btn.pack(pady=4)

        tk.Frame(mid, bg=BG).pack(expand=True)

        # ── Input B ──────────────────────────
        self._section_label(body, "INPUT  B", ACCENT, row=0, col=2)
        self.box_b = self._text_box(body, row=1, col=2)

        # ── Separator ────────────────────────
        sep_frame = tk.Frame(body, bg=BG)
        sep_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(14, 10))
        tk.Frame(sep_frame, bg=BORDER, height=1).pack(fill="x")
        tk.Label(sep_frame, text="  OUTPUT  ", bg=BG, fg=TEXT_DIM,
                 font=("Courier New", 8)).place(relx=0.5, rely=0.5, anchor="center")

        # ── Output ────────────────────────────
        self._section_label(body, "Recommended Navigation System", ACCENT2, row=2, col=0, pady=(0,0))
        out_frame = tk.Frame(body, bg=BORDER, bd=0)
        out_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(2, 0))

        self.output_box = scrolledtext.ScrolledText(
            out_frame,
            bg=PANEL, fg=ACCENT2,
            font=MONO,
            relief="flat", bd=0,
            wrap="word",
            state="disabled",
            insertbackground=ACCENT2,
            padx=14, pady=14,
            selectbackground=BORDER
        )
        self.output_box.pack(fill="both", expand=True, padx=1, pady=1)

    def _section_label(self, parent, text, color, row, col, pady=(0, 4)):
        tk.Label(
            parent, text=text,
            bg=BG, fg=color,
            font=("Courier New", 8, "bold"),
            anchor="w"
        ).grid(row=row, column=col, sticky="sw", pady=pady)

    def _text_box(self, parent, row, col):
        frame = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
        frame.grid(row=row, column=col, sticky="nsew")
        box = tk.Text(
            frame,
            bg=PANEL, fg=TEXT,
            font=MONO,
            relief="flat", bd=0,
            wrap="word",
            insertbackground=ACCENT,
            selectbackground=BORDER,
            padx=12, pady=12,
            undo=True
        )
        box.pack(fill="both", expand=True)
        # placeholder behaviour
        box.bind("<FocusIn>",  lambda e, b=box: self._on_focus_in(b))
        box.bind("<FocusOut>", lambda e, b=box: self._on_focus_out(b))
        self._set_placeholder(box)
        return box

    # ── Placeholder helpers ───────────────────
    def _set_placeholder(self, box):
        box.insert("1.0", "Enter text here…")
        box.config(fg=TEXT_DIM)
        box._has_placeholder = True

    def _on_focus_in(self, box):
        if getattr(box, "_has_placeholder", False):
            box.delete("1.0", "end")
            box.config(fg=TEXT)
            box._has_placeholder = False

    def _on_focus_out(self, box):
        if not box.get("1.0", "end").strip():
            self._set_placeholder(box)

    def _get_text(self, box):
        if getattr(box, "_has_placeholder", False):
            return ""
        return box.get("1.0", "end-1c")

    # ── Status bar ────────────────────────────
    def _build_status_bar(self):
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")
        bar = tk.Frame(self, bg=PANEL, height=26)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(bar, textvariable=self.status_var,
                 bg=PANEL, fg=TEXT_DIM,
                 font=("Courier New", 8),
                 anchor="w", padx=16).pack(side="left", fill="y")

        self.progress_var = tk.StringVar(value="")
        tk.Label(bar, textvariable=self.progress_var,
                 bg=PANEL, fg=ACCENT,
                 font=("Courier New", 8),
                 anchor="e", padx=16).pack(side="right", fill="y")

    # ── Actions ───────────────────────────────
    def _run(self):
        a = self._get_text(self.box_a)
        b = self._get_text(self.box_b)

        if not a and not b:
            self._set_output("⚠  Both inputs are empty.", color=WARNING)
            self.status_var.set("Error: no input provided.")
            return
        if not a:
            self._set_output("⚠  Input A is empty.", color=WARNING)
            return
        if not b:
            self._set_output("⚠  Input B is empty.", color=WARNING)
            return

        self.run_btn.config(state="disabled", bg=BORDER, fg=TEXT_DIM, text="…\nWAIT")
        self.status_var.set("Processing…")
        self._animate_progress(True)

        def worker():
            try:
                result = process_inputs(a, b)
                self.after(0, lambda: self._set_output(result, color=ACCENT2))
                self.after(0, lambda: self.status_var.set(
                    f"Done. Output: {len(result)} chars"))
            except Exception as exc:
                self.after(0, lambda: self._set_output(
                    f"ERROR\n{'─'*40}\n{exc}", color=WARNING))
                self.after(0, lambda: self.status_var.set(f"Error: {exc}"))
            finally:
                self.after(0, self._reset_button)
                self.after(0, lambda: self._animate_progress(False))

        threading.Thread(target=worker, daemon=True).start()

    def _reset_button(self):
        self.run_btn.config(state="normal", bg=ACCENT, fg=TEXT_DARK, text="▶\nRUN")

    def _set_output(self, text, color=ACCENT2):
        self.output_box.config(state="normal", fg=color)
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        self.output_box.config(state="disabled")

    def _clear(self):
        for box in (self.box_a, self.box_b):
            box.delete("1.0", "end")
            self._set_placeholder(box)
        self._set_output("", color=ACCENT2)
        self.status_var.set("Cleared.")

    # ── Animated dots in status bar ───────────
    def _animate_progress(self, running):
        if running:
            self._animating = True
            self._anim_step(0)
        else:
            self._animating = False
            self.progress_var.set("")

    def _anim_step(self, n):
        if not self._animating:
            return
        dots = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        self.progress_var.set(dots[n % len(dots)] + "  processing")
        self.after(100, lambda: self._anim_step(n + 1))


if __name__ == "__main__":
    app = NLPMapperApp()
    app.mainloop()