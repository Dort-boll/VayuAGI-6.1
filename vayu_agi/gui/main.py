"""Minimal GUI entrypoint built on the stable engine contract."""

from __future__ import annotations

import tkinter as tk
from tkinter import scrolledtext

from ..core.cognitive_engine import CognitiveEngine


def main() -> None:
    engine = CognitiveEngine()
    root = tk.Tk()
    root.title("VayuAGI 6.1")
    root.geometry("900x600")
    output = scrolledtext.ScrolledText(root, wrap=tk.WORD)
    output.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
    entry = tk.Entry(root)
    entry.pack(fill=tk.X, padx=12, pady=(0, 12))

    def submit() -> None:
        result = engine.think(entry.get())
        output.insert(tk.END, f"\n{result.synthesis}\nConfidence: {result.confidence:.1%}\n")
        entry.delete(0, tk.END)

    entry.bind("<Return>", lambda _event: submit())
    root.mainloop()


if __name__ == "__main__":
    main()