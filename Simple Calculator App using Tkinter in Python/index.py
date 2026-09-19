"""
MASA Modern Calculator Suite
Developer: MASA
"""

import math
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MasaCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MASA Calculator Pro")
        self.geometry("380x560")
        self.resizable(False, False)
        self.configure(fg_color="#12131A")

        self.history_expr = ""
        self.current_expr = "0"
        self._fresh_entry = True

        self._build_ui()
        self._bind_shortcuts()

    def _build_ui(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 0))

        title_label = ctk.CTkLabel(
            header_frame,
            text="MASA CALCULATOR",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#6366F1",
        )
        title_label.pack(side="left")

        brand_badge = ctk.CTkLabel(
            header_frame,
            text="PRO v2.0",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color="#94A3B8",
            fg_color="#1E2230",
            corner_radius=6,
            padx=8,
            pady=2,
        )
        brand_badge.pack(side="right")

        display_card = ctk.CTkFrame(
            self,
            fg_color="#181B26",
            corner_radius=16,
            border_width=1,
            border_color="#242938",
        )
        display_card.pack(fill="x", padx=20, pady=15)

        self.history_lbl = ctk.CTkLabel(
            display_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color="#64748B",
            anchor="e",
        )
        self.history_lbl.pack(fill="x", padx=16, pady=(14, 2))

        self.display_lbl = ctk.CTkLabel(
            display_card,
            text="0",
            font=ctk.CTkFont(family="Segoe UI", size=36, weight="bold"),
            text_color="#F8FAFC",
            anchor="e",
        )
        self.display_lbl.pack(fill="x", padx=16, pady=(0, 14))

        keypad_frame = ctk.CTkFrame(self, fg_color="transparent")
        keypad_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        for col in range(4):
            keypad_frame.grid_columnconfigure(col, weight=1, uniform="col")
        for row in range(5):
            keypad_frame.grid_rowconfigure(row, weight=1, uniform="row")

        buttons_layout = [
            ("C", self._on_clear, "#EF4444", "#DC2626", "#FFFFFF"),
            ("x²", self._on_square, "#1E2230", "#2D3446", "#E2E8F0"),
            ("√", self._on_sqrt, "#1E2230", "#2D3446", "#E2E8F0"),
            ("÷", lambda: self._on_operator("/"), "#4F46E5", "#4338CA", "#FFFFFF"),

            ("7", lambda: self._on_digit("7"), "#181B26", "#252B3B", "#F8FAFC"),
            ("8", lambda: self._on_digit("8"), "#181B26", "#252B3B", "#F8FAFC"),
            ("9", lambda: self._on_digit("9"), "#181B26", "#252B3B", "#F8FAFC"),
            ("×", lambda: self._on_operator("*"), "#4F46E5", "#4338CA", "#FFFFFF"),

            ("4", lambda: self._on_digit("4"), "#181B26", "#252B3B", "#F8FAFC"),
            ("5", lambda: self._on_digit("5"), "#181B26", "#252B3B", "#F8FAFC"),
            ("6", lambda: self._on_digit("6"), "#181B26", "#252B3B", "#F8FAFC"),
            ("-", lambda: self._on_operator("-"), "#4F46E5", "#4338CA", "#FFFFFF"),

            ("1", lambda: self._on_digit("1"), "#181B26", "#252B3B", "#F8FAFC"),
            ("2", lambda: self._on_digit("2"), "#181B26", "#252B3B", "#F8FAFC"),
            ("3", lambda: self._on_digit("3"), "#181B26", "#252B3B", "#F8FAFC"),
            ("+", lambda: self._on_operator("+"), "#4F46E5", "#4338CA", "#FFFFFF"),

            ("±", self._on_negate, "#181B26", "#252B3B", "#94A3B8"),
            ("0", lambda: self._on_digit("0"), "#181B26", "#252B3B", "#F8FAFC"),
            (".", self._on_decimal, "#181B26", "#252B3B", "#F8FAFC"),
            ("=", self._on_calculate, "#06B6D4", "#0891B2", "#0F172A"),
        ]

        idx = 0
        for r in range(5):
            for c in range(4):
                label, cmd, bg, hover, fg = buttons_layout[idx]
                btn = ctk.CTkButton(
                    keypad_frame,
                    text=label,
                    font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
                    fg_color=bg,
                    hover_color=hover,
                    text_color=fg,
                    corner_radius=12,
                    command=cmd,
                )
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
                idx += 1

    def _bind_shortcuts(self):
        self.bind("<Return>", lambda _: self._on_calculate())
        self.bind("<KP_Enter>", lambda _: self._on_calculate())
        self.bind("<Escape>", lambda _: self._on_clear())
        self.bind("<BackSpace>", lambda _: self._on_backspace())

        for num in range(10):
            self.bind(str(num), lambda _, n=str(num): self._on_digit(n))

        ops = {"+": "+", "-": "-", "*": "*", "/": "/"}
        for key, sym in ops.items():
            self.bind(key, lambda _, s=sym: self._on_operator(s))
        self.bind(".", lambda _: self._on_decimal())

    def _on_digit(self, digit: str):
        if self._fresh_entry or self.current_expr == "0":
            self.current_expr = digit
            self._fresh_entry = False
        else:
            self.current_expr += digit
        self.display_lbl.configure(text=self.current_expr)

    def _on_operator(self, op: str):
        if self.current_expr:
            self.history_expr = f"{self.current_expr} {op} "
            self.history_lbl.configure(text=self.history_expr)
            self._fresh_entry = True

    def _on_decimal(self):
        if self._fresh_entry:
            self.current_expr = "0."
            self._fresh_entry = False
        elif "." not in self.current_expr:
            self.current_expr += "."
        self.display_lbl.configure(text=self.current_expr)

    def _on_clear(self):
        self.current_expr = "0"
        self.history_expr = ""
        self._fresh_entry = True
        self.history_lbl.configure(text="")
        self.display_lbl.configure(text="0")

    def _on_backspace(self):
        if len(self.current_expr) > 1 and not self._fresh_entry:
            self.current_expr = self.current_expr[:-1]
        else:
            self.current_expr = "0"
            self._fresh_entry = True
        self.display_lbl.configure(text=self.current_expr)

    def _on_square(self):
        try:
            val = float(self.current_expr)
            res = val ** 2
            self._display_result(res, f"sqr({val})")
        except Exception:
            self.display_lbl.configure(text="Error")

    def _on_sqrt(self):
        try:
            val = float(self.current_expr)
            if val < 0:
                self.display_lbl.configure(text="Invalid Input")
                return
            res = math.sqrt(val)
            self._display_result(res, f"√({val})")
        except Exception:
            self.display_lbl.configure(text="Error")

    def _on_negate(self):
        try:
            val = float(self.current_expr)
            val = -val
            self.current_expr = f"{val:g}"
            self.display_lbl.configure(text=self.current_expr)
        except Exception:
            pass

    def _on_calculate(self):
        if not self.history_expr:
            return
        full_statement = f"{self.history_expr}{self.current_expr}"
        try:
            safe_statement = full_statement.replace("×", "*").replace("÷", "/")
            result = eval(safe_statement, {"__builtins__": None}, {})
            self._display_result(result, full_statement + " =")
        except ZeroDivisionError:
            self.display_lbl.configure(text="Cannot divide by 0")
            self.history_expr = ""
            self._fresh_entry = True
        except Exception:
            self.display_lbl.configure(text="Error")
            self.history_expr = ""
            self._fresh_entry = True

    def _display_result(self, val: float, history_text: str):
        if isinstance(val, float) and val.is_integer():
            formatted = str(int(val))
        else:
            formatted = f"{val:g}"
        self.history_lbl.configure(text=history_text)
        self.display_lbl.configure(text=formatted)
        self.current_expr = formatted
        self.history_expr = ""
        self._fresh_entry = True


if __name__ == "__main__":
    app = MasaCalculator()
    app.mainloop()
