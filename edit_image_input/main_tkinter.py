import tkinter as tk
from tkinter import font

root = tk.Tk()

root.geometry("700x250")
bg_color = '#f0f0f0'

tk_font = font.Font(family='DejaVu Sans Mono', size=12)


def update_hit_box(_, self):
    width = tk_font.measure(text_test.get()) + 10
    self.grid_forget()
    self.place(x=10, y=10, width=width)


text_test = tk.StringVar(root, 'show')
entry = tk.Entry(root, bg=bg_color, borderwidth=0, highlightthickness=0, textvariable=text_test, font=tk_font)
entry.place(x=10, y=10)
entry.bind('<KeyPress>', lambda event: update_hit_box(event, entry))
entry.bind('<KeyRelease>', lambda event: update_hit_box(event, entry))
entry.bind('<Return>', lambda _: root.focus())

root.mainloop()
