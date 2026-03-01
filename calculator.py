import ast
import operator
import tkinter as tk
from tkinter import ttk


class SafeEvaluator:
    """Safely evaluate arithmetic expressions using ast."""

    ALLOWED_BINOPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
    }

    ALLOWED_UNARYOPS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def eval(self, expr: str):
        node = ast.parse(expr, mode="eval")
        return self._eval_node(node.body)

    def _eval_node(self, node):
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type in self.ALLOWED_BINOPS:
                return self.ALLOWED_BINOPS[op_type](left, right)
            raise ValueError(f"Operator {op_type} not allowed")

        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in self.ALLOWED_UNARYOPS:
                return self.ALLOWED_UNARYOPS[op_type](operand)
            raise ValueError(f"Unary operator {op_type} not allowed")

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only int/float constants allowed")

        if isinstance(node, ast.Expr):
            return self._eval_node(node.value)

        # For Python <3.8 compatibility (Num)
        if isinstance(node, ast.Num):
            return node.n

        raise ValueError(f"Unsupported expression: {ast.dump(node)}")


class CalculatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.eval = SafeEvaluator()

        self._create_widgets()

    def _create_widgets(self):
        mainframe = ttk.Frame(self, padding="8")
        mainframe.grid(row=0, column=0)

        self.display = tk.StringVar()
        entry = ttk.Entry(mainframe, textvariable=self.display, justify="right", font=(None, 18), width=20)
        entry.grid(row=0, column=0, columnspan=4, pady=(0, 8))
        entry.state(["readonly"])

        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        for (text, r, c) in buttons:
            action = (lambda t=text: self._on_button(t))
            ttk.Button(mainframe, text=text, command=action, width=5).grid(row=r, column=c, padx=4, pady=4)

        ttk.Button(mainframe, text="C", command=self._clear, width=5).grid(row=5, column=0, padx=4, pady=4)
        ttk.Button(mainframe, text="⌫", command=self._backspace, width=5).grid(row=5, column=1, padx=4, pady=4)
        ttk.Button(mainframe, text="(", command=lambda: self._on_button("("), width=5).grid(row=5, column=2, padx=4, pady=4)
        ttk.Button(mainframe, text=")", command=lambda: self._on_button(")"), width=5).grid(row=5, column=3, padx=4, pady=4)

        # Keyboard bindings
        self.bind("<Return>", lambda e: self._calculate())
        self.bind("<BackSpace>", lambda e: self._backspace())
        for key in "0123456789+-*/().":
            self.bind(key, lambda e, k=key: self._on_button(k))

    def _on_button(self, char: str):
        if char == "=":
            self._calculate()
            return
        # append char to display
        cur = self.display.get()
        self.display.set(cur + char)

    def _clear(self):
        self.display.set("")

    def _backspace(self):
        cur = self.display.get()
        self.display.set(cur[:-1])

    def _calculate(self):
        expr = self.display.get().strip()
        if not expr:
            return
        try:
            result = self.eval.eval(expr)
        except Exception as e:
            self.display.set("Error")
            return
        # trim trailing .0 for integers
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        self.display.set(str(result))


if __name__ == "__main__":
    app = CalculatorGUI()
    app.mainloop()
import ast
import operator
import tkinter as tk
from tkinter import ttk


class SafeEvaluator:
    """Safely evaluate arithmetic expressions using ast."""

    ALLOWED_BINOPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
    }

    ALLOWED_UNARYOPS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def eval(self, expr: str):
        node = ast.parse(expr, mode="eval")
        return self._eval_node(node.body)

    def _eval_node(self, node):
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type in self.ALLOWED_BINOPS:
                return self.ALLOWED_BINOPS[op_type](left, right)
            raise ValueError(f"Operator {op_type} not allowed")

        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in self.ALLOWED_UNARYOPS:
                return self.ALLOWED_UNARYOPS[op_type](operand)
            raise ValueError(f"Unary operator {op_type} not allowed")

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only int/float constants allowed")

        if isinstance(node, ast.Expr):
            return self._eval_node(node.value)

        # For Python <3.8 compatibility (Num)
        if isinstance(node, ast.Num):
            return node.n

        raise ValueError(f"Unsupported expression: {ast.dump(node)}")


class CalculatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.eval = SafeEvaluator()

        self._create_widgets()

    def _create_widgets(self):
        mainframe = ttk.Frame(self, padding="8")
        mainframe.grid(row=0, column=0)

        self.display = tk.StringVar()
        entry = ttk.Entry(mainframe, textvariable=self.display, justify="right", font=(None, 18), width=20)
        entry.grid(row=0, column=0, columnspan=4, pady=(0, 8))
        entry.state(["readonly"])

        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        for (text, r, c) in buttons:
            action = (lambda t=text: self._on_button(t))
            ttk.Button(mainframe, text=text, command=action, width=5).grid(row=r, column=c, padx=4, pady=4)

        ttk.Button(mainframe, text="C", command=self._clear, width=5).grid(row=5, column=0, padx=4, pady=4)
        ttk.Button(mainframe, text="⌫", command=self._backspace, width=5).grid(row=5, column=1, padx=4, pady=4)
        ttk.Button(mainframe, text="(", command=lambda: self._on_button("("), width=5).grid(row=5, column=2, padx=4, pady=4)
        ttk.Button(mainframe, text=")", command=lambda: self._on_button(")"), width=5).grid(row=5, column=3, padx=4, pady=4)

        # Keyboard bindings
        self.bind("<Return>", lambda e: self._calculate())
        self.bind("<BackSpace>", lambda e: self._backspace())
        for key in "0123456789+-*/().":
            self.bind(key, lambda e, k=key: self._on_button(k))

    def _on_button(self, char: str):
        if char == "=":
            self._calculate()
            return
        # append char to display
        cur = self.display.get()
        self.display.set(cur + char)

    def _clear(self):
        self.display.set("")

    def _backspace(self):
        cur = self.display.get()
        self.display.set(cur[:-1])

    def _calculate(self):
        expr = self.display.get().strip()
        if not expr:
            return
        try:
            result = self.eval.eval(expr)
        except Exception as e:
            self.display.set("Error")
            return
        # trim trailing .0 for integers
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        self.display.set(str(result))


if __name__ == "__main__":
    app = CalculatorGUI()
    app.mainloop()