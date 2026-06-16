import tkinter as tk
from tkinter import messagebox
import math
from datetime import datetime

root = tk.Tk()
root.title("Advanced Calculator")
root.geometry("650x550")
root.resizable(False, False)

dark_mode = True
history_data = []

def apply_theme():
    if dark_mode:
        root.configure(bg="#1E1E1E")

        display.configure(
            bg="#2D2D2D",
            fg="white",
            insertbackground="white"
        )

        history_box.configure(
            bg="#252525",
            fg="white"
        )

        clock_label.configure(
            bg="#1E1E1E",
            fg="white"
        )

        theme_button.configure(
            text="☀ Light Mode",
            bg="#444444",
            fg="white"
        )

    else:
        root.configure(bg="#F4F4F4")

        display.configure(
            bg="white",
            fg="black",
            insertbackground="black"
        )

        history_box.configure(
            bg="white",
            fg="black"
        )

        clock_label.configure(
            bg="#F4F4F4",
            fg="black"
        )

        theme_button.configure(
            text="🌙 Dark Mode",
            bg="#DDDDDD",
            fg="black"
        )


def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def update_clock():
    current_time = datetime.now().strftime("%I:%M:%S %p")
    clock_label.config(text=current_time)
    root.after(1000, update_clock)

def clear():
    display.delete(0, tk.END)


def backspace():
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current[:-1])


def copy_result():
    value = display.get()

    if value:
        root.clipboard_clear()
        root.clipboard_append(value)
        messagebox.showinfo("Copied", "Result copied to clipboard!")


def export_history():
    try:
        with open("history.txt", "w") as file:
            file.write("\n".join(history_data))

        messagebox.showinfo(
            "Success",
            "History exported to history.txt"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def add_to_history(entry):
    history_data.append(entry)

    history_box.insert(tk.END, entry + "\n")
    history_box.see(tk.END)


def calculate():
    expression = display.get().strip()

    try:
        expression = expression.replace("%", "/100")

        result = eval(expression)

        history_entry = f"{display.get()} = {result}"

        add_to_history(history_entry)

        display.delete(0, tk.END)
        display.insert(tk.END, result)

    except ZeroDivisionError:
        display.delete(0, tk.END)
        display.insert(tk.END, "Cannot Divide By Zero")

    except Exception:
        display.delete(0, tk.END)
        display.insert(tk.END, "Invalid Expression")


def square():
    try:
        value = float(display.get())

        result = value ** 2

        add_to_history(f"{value}² = {result}")

        display.delete(0, tk.END)
        display.insert(tk.END, result)

    except:
        display.delete(0, tk.END)
        display.insert(tk.END, "Invalid Input")


def square_root():
    try:
        value = float(display.get())

        if value < 0:
            raise ValueError

        result = math.sqrt(value)

        add_to_history(f"√{value} = {result}")

        display.delete(0, tk.END)
        display.insert(tk.END, result)

    except:
        display.delete(0, tk.END)
        display.insert(tk.END, "Invalid Input")


def click(value):
    if value == "=":
        calculate()
    else:
        display.insert(tk.END, value)

def key_press(event):

    key = event.keysym

    if key == "Return":
        calculate()

    elif key == "BackSpace":
        backspace()

    elif key == "Escape":
        clear()

root.bind("<Key>", key_press)

clock_label = tk.Label(
    root,
    font=("Arial", 12, "bold")
)
clock_label.pack(pady=5)

display = tk.Entry(
    root,
    font=("Arial", 28),
    justify="right",
    bd=0
)

display.pack(
    fill="x",
    padx=10,
    pady=10,
    ipady=15
)

top_frame = tk.Frame(root)
top_frame.pack(fill="x", padx=10)

theme_button = tk.Button(
    top_frame,
    text="☀ Light Mode",
    command=toggle_theme
)

theme_button.pack(side="left", padx=2)

tk.Button(
    top_frame,
    text="Copy",
    command=copy_result
).pack(side="left", padx=2)

tk.Button(
    top_frame,
    text="Export History",
    command=export_history
).pack(side="left", padx=2)

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

calc_frame = tk.Frame(main_frame)
calc_frame.pack(side="left", padx=10)

special_buttons = [
    ("C", clear),
    ("⌫", backspace),
    ("x²", square),
    ("√", square_root)
]

for i, (text, cmd) in enumerate(special_buttons):
    tk.Button(
        calc_frame,
        text=text,
        width=6,
        height=2,
        font=("Arial", 14, "bold"),
        command=cmd
    ).grid(row=0, column=i, padx=3, pady=3)

buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "%", "+",
    "="
]

row = 1
col = 0

for button in buttons:

    tk.Button(
        calc_frame,
        text=button,
        width=6,
        height=2,
        font=("Arial", 14, "bold"),
        command=lambda b=button: click(b)
    ).grid(
        row=row,
        column=col,
        padx=3,
        pady=3
    )

    col += 1

    if col > 3:
        col = 0
        row += 1

# History Panel

history_frame = tk.Frame(main_frame)
history_frame.pack(side="right", fill="both", expand=True, padx=10)

tk.Label(
    history_frame,
    text="Calculation History",
    font=("Arial", 14, "bold")
).pack()

history_box = tk.Text(
    history_frame,
    height=20,
    width=30
)

history_box.pack(fill="both", expand=True)

apply_theme()
update_clock()
display.focus_set()

root.mainloop()