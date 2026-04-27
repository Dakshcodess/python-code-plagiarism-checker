import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

from compare import compare_python_files, get_risk_level, get_matched_lines
from database import connect_db, save_result, fetch_history


# ---------------- APP SETUP ----------------
root = tk.Tk()
root.title("Python Code Plagiarism Checker")
root.geometry("980x760")
root.minsize(900, 700)
root.configure(bg="#121212")

connect_db()

# ---------------- VARIABLES ----------------
file1 = ""
file2 = ""
last_score = None
last_risk = None


# ---------------- COLORS ----------------
BG = "#121212"
CARD = "#1e1e1e"
TEXT = "#ffffff"
SUB = "#bdbdbd"

BTN1 = "#2563eb"
BTN2 = "#16a34a"
BTN3 = "#9333ea"
BTN4 = "#f59e0b"

LOW = "#00e5ff"       # cyan
MEDIUM = "#ffd54f"    # gold
HIGH = "#dc143c"      # crimson


# ---------------- FUNCTIONS ----------------
def shorten_path(path, max_len=70):
    if len(path) <= max_len:
        return path
    return "..." + path[-max_len:]


def select_file1():
    global file1
    file1 = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])

    if file1:
        label_file1.config(text=shorten_path(file1))


def select_file2():
    global file2
    file2 = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])

    if file2:
        label_file2.config(text=shorten_path(file2))


def compare_files():
    global last_score, last_risk

    if file1 == "" or file2 == "":
        messagebox.showwarning("Warning", "Please select both files first.")
        return

    score = compare_python_files(file1, file2)
    risk = get_risk_level(score)

    last_score = score
    last_risk = risk

    save_result(file1, file2, score, risk)

    color = LOW

    if risk == "Medium Risk":
        color = MEDIUM
    elif risk == "High Risk":
        color = HIGH

    result_label.config(
        text=f"Similarity: {score}%\nRisk Level: {risk}",
        fg=color
    )


def show_history():
    rows = fetch_history()

    win = tk.Toplevel(root)
    win.title("Comparison History")
    win.geometry("900x500")
    win.configure(bg=BG)

    tk.Label(
        win,
        text="Comparison History",
        font=("Segoe UI", 20, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=15)

    box = tk.Text(
        win,
        bg=CARD,
        fg="#90ee90",
        font=("Consolas", 10),
        wrap="word"
    )
    box.pack(fill="both", expand=True, padx=20, pady=10)

    for row in rows:
        f1, f2, score, risk = row

        box.insert(
            tk.END,
            f"File 1 : {f1}\n"
            f"File 2 : {f2}\n"
            f"Score  : {score}%\n"
            f"Risk   : {risk}\n"
            + "-" * 100 + "\n"
        )

    box.config(state="disabled")


def export_report():
    global last_score, last_risk

    if last_score is None:
        messagebox.showwarning("Warning", "Please compare files first.")
        return

    filename = "report_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("PYTHON CODE PLAGIARISM REPORT\n")
        file.write("=" * 50 + "\n")
        file.write(f"File 1: {file1}\n")
        file.write(f"File 2: {file2}\n")
        file.write(f"Similarity Score: {last_score}%\n")
        file.write(f"Risk Level: {last_risk}\n")
        file.write("=" * 50 + "\n")

    messagebox.showinfo("Saved", f"Report exported as {filename}")


def show_matched_lines():
    if file1 == "" or file2 == "":
        messagebox.showwarning("Warning", "Please select both files first.")
        return

    matched = get_matched_lines(file1, file2)

    win = tk.Toplevel(root)
    win.title("Matched Lines")
    win.geometry("950x550")
    win.configure(bg=BG)

    tk.Label(
        win,
        text="Matched / Suspicious Lines",
        font=("Segoe UI", 18, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(pady=15)

    box = tk.Text(
        win,
        bg=CARD,
        fg="#ffd54f",
        font=("Consolas", 10),
        wrap="word"
    )
    box.pack(fill="both", expand=True, padx=20, pady=10)

    if matched:
        for a, b in matched:
            box.insert(tk.END, f"File1: {a}\n")
            box.insert(tk.END, f"File2: {b}\n")
            box.insert(tk.END, "-" * 100 + "\n")
    else:
        box.insert(tk.END, "No suspicious lines found.")

    box.config(state="disabled")


# ---------------- UI ----------------
main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True, padx=30, pady=25)

title = tk.Label(
    main_frame,
    text="Python Code Plagiarism Checker",
    font=("Segoe UI", 28, "bold"),
    bg=BG,
    fg=TEXT
)
title.pack(pady=(10, 5))

subtitle = tk.Label(
    main_frame,
    text="Hybrid Similarity Detection for Python Source Files",
    font=("Segoe UI", 11),
    bg=BG,
    fg=SUB
)
subtitle.pack(pady=(0, 25))


# Upload Card
card = tk.Frame(main_frame, bg=CARD, bd=0)
card.pack(fill="x", padx=80, pady=10)

tk.Button(
    card,
    text="Upload File 1",
    command=select_file1,
    font=("Segoe UI", 11, "bold"),
    bg=BTN1,
    fg="white",
    width=22,
    relief="flat"
).pack(pady=(25, 8))

label_file1 = tk.Label(
    card,
    text="No file selected",
    bg=CARD,
    fg="#8bc34a",
    font=("Segoe UI", 10)
)
label_file1.pack()

tk.Button(
    card,
    text="Upload File 2",
    command=select_file2,
    font=("Segoe UI", 11, "bold"),
    bg=BTN1,
    fg="white",
    width=22,
    relief="flat"
).pack(pady=(20, 8))

label_file2 = tk.Label(
    card,
    text="No file selected",
    bg=CARD,
    fg="#8bc34a",
    font=("Segoe UI", 10)
)
label_file2.pack(pady=(0, 25))


# Buttons Row
btn_frame = tk.Frame(main_frame, bg=BG)
btn_frame.pack(pady=20)

tk.Button(
    btn_frame,
    text="Compare Files",
    command=compare_files,
    bg=BTN4,
    fg="black",
    font=("Segoe UI", 10, "bold"),
    width=18
).grid(row=0, column=0, padx=8, pady=8)

tk.Button(
    btn_frame,
    text="View History",
    command=show_history,
    bg=BTN2,
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=18
).grid(row=0, column=1, padx=8, pady=8)

tk.Button(
    btn_frame,
    text="Export Report",
    command=export_report,
    bg=BTN1,
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=18
).grid(row=1, column=0, padx=8, pady=8)

tk.Button(
    btn_frame,
    text="Matched Lines",
    command=show_matched_lines,
    bg=BTN3,
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=18
).grid(row=1, column=1, padx=8, pady=8)


# Result Card
result_card = tk.Frame(main_frame, bg=CARD)
result_card.pack(fill="x", padx=120, pady=25)

result_label = tk.Label(
    result_card,
    text="Upload two files and click Compare Files",
    font=("Segoe UI", 20, "bold"),
    bg=CARD,
    fg=LOW,
    pady=25
)
result_label.pack()


# Footer
footer = tk.Label(
    main_frame,
    text="BTech CSE Mini Project | Python + Tkinter + SQLite",
    font=("Segoe UI", 9),
    bg=BG,
    fg="#757575"
)
footer.pack(side="bottom", pady=10)

root.mainloop()