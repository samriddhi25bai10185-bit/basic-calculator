import tkinter as tk

root = tk.Tk()

root.title("Basic Calculator")
root.geometry("350x500")

display = tk.Entry(
    root,
    font=("Arial", 24),
    justify="right"
)

display.pack(fill="both", padx=10, pady=10)


def calculate():
    expression = display.get()

    try:
        result = eval(expression)

        display.delete(0, tk.END)
        display.insert(tk.END, result)

    except:
        display.delete(0, tk.END)
        display.insert(tk.END, "Error")


def click(value):

    if value == "=":
        calculate()
    else:
        display.insert(tk.END, value)


button_frame = tk.Frame(root)
button_frame.pack()

buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "=", "+"
]

row = 0
col = 0

for button in buttons:

    btn = tk.Button(
        button_frame,
        text=button,
        width=5,
        height=2,
        font=("Arial", 18),
        command=lambda b=button: click(b)
    )

    btn.grid(
        row=row,
        column=col,
        padx=5,
        pady=5
    )

    col += 1

    if col > 3:
        col = 0
        row += 1

root.mainloop()