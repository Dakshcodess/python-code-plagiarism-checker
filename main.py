import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

from compare import compare_python_files, get_risk_level, get_matched_lines
from database import connect_db, save_result, fetch_history


# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Python Code Plagiarism Checker")
root.geometry("750x650")
root.config(bg="#1e1e1e")

# Initialize database
connect_db()

# ---------------- VARIABLES ----------------
file1 = ""
file2 = ""

last_score = None
last_risk = None


# ---------------- FILE SELECT FUNCTIONS ----------------
def select_file1():
    global file1

    file1 = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py")]
    )

    if file1:
        label_file1.config(text=file1)


def select_file2():
    global file2

    file2 = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py")]
    )

    if file2:
        label_file2.config(text=file2)


# ---------------- COMPARE FUNCTION ----------------
def compare_files():
    global last_score, last_risk

    if file1 == "" or file2 == "":
        messagebox.showwarning(
            "Warning",
            "Please select both files first."
        )
        return

    score = compare_python_files(file1, file2)
    risk = get_risk_level(score)

    last_score = score
    last_risk = risk

    save_result(file1, file2, score, risk)

    color = "lightgreen"

    if risk == "Medium Risk":
        color = "orange"

    elif risk == "High Risk":
        color = "red"

    result_label.config(
        text=f"Similarity: {score}%\nRisk Level: {risk}",
        fg=color
    )


# ---------------- HISTORY WINDOW ----------------
def show_history():
    records = fetch_history()

    history_window = tk.Toplevel(root)
    history_window.title("Comparison History")
    history_window.geometry("780x420")
    history_window.config(bg="#1e1e1e")

    title = tk.Label(
        history_window,
        text="Previous Comparisons",
        font=("Arial", 16, "bold"),
        bg="#1e1e1e",
        fg="white"
    )
    title.pack(pady=10)

    text_box = tk.Text(
        history_window,
        width=95,
        height=20,
        bg="#2b2b2b",
        fg="lightgreen",
        font=("Consolas", 10)
    )
    text_box.pack(pady=10)

    for row in records:
        f1, f2, score, risk = row

        line = (
            f"File1: {f1}\n"
            f"File2: {f2}\n"
            f"Score: {score}% | Risk: {risk}\n"
            + "-" * 90 + "\n"
        )

        text_box.insert(tk.END, line)

    text_box.config(state="disabled")


# ---------------- EXPORT REPORT ----------------
def export_report():
    global last_score, last_risk

    if last_score is None:
        messagebox.showwarning(
            "Warning",
            "Please compare files first."
        )
        return

    filename = (
        "report_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".txt"
    )

    with open(filename, "w", encoding="utf-8") as file:
        file.write("PYTHON CODE PLAGIARISM REPORT\n")
        file.write("=" * 45 + "\n")
        file.write(f"File 1: {file1}\n")
        file.write(f"File 2: {file2}\n")
        file.write(f"Similarity Score: {last_score}%\n")
        file.write(f"Risk Level: {last_risk}\n")
        file.write("=" * 45 + "\n")

    messagebox.showinfo(
        "Success",
        f"Report saved as {filename}"
    )

def show_matched_lines():
    if file1 == "" or file2 == "":
        messagebox.showwarning("Warning", "Please select both files first.")
        return

    matched = get_matched_lines(file1, file2)

    match_window = tk.Toplevel(root)
    match_window.title("Matched Lines")
    match_window.geometry("850x450")
    match_window.config(bg="#1e1e1e")

    title = tk.Label(
        match_window,
        text="Matched / Suspicious Lines",
        font=("Arial", 16, "bold"),
        bg="#1e1e1e",
        fg="white"
    )
    title.pack(pady=10)

    text_box = tk.Text(
        match_window,
        width=105,
        height=22,
        bg="#2b2b2b",
        fg="yellow",
        font=("Consolas", 10)
    )
    text_box.pack(pady=10)

    if matched:
        for line1, line2 in matched:
            text_box.insert(tk.END, f"File1: {line1}\n")
            text_box.insert(tk.END, f"File2: {line2}\n")
            text_box.insert(tk.END, "-" * 95 + "\n")
    else:
        text_box.insert(tk.END, "No matched lines found.")

    text_box.config(state="disabled")

# ---------------- TITLE ----------------
title = tk.Label(
    root,
    text="Python Code Plagiarism Checker",
    font=("Arial", 24, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title.pack(pady=20)


# ---------------- FILE 1 ----------------
btn1 = tk.Button(
    root,
    text="Upload File 1",
    command=select_file1,
    width=22
)
btn1.pack(pady=10)

label_file1 = tk.Label(
    root,
    text="No file selected",
    bg="#1e1e1e",
    fg="lightgreen"
)
label_file1.pack()


# ---------------- FILE 2 ----------------
btn2 = tk.Button(
    root,
    text="Upload File 2",
    command=select_file2,
    width=22
)
btn2.pack(pady=10)

label_file2 = tk.Label(
    root,
    text="No file selected",
    bg="#1e1e1e",
    fg="lightgreen"
)
label_file2.pack()


# ---------------- BUTTONS ----------------
compare_btn = tk.Button(
    root,
    text="Compare Files",
    command=compare_files,
    width=22,
    bg="orange"
)
compare_btn.pack(pady=20)

history_btn = tk.Button(
    root,
    text="View History",
    command=show_history,
    width=22,
    bg="#4CAF50"
)
history_btn.pack(pady=5)

export_btn = tk.Button(
    root,
    text="Export Report",
    command=export_report,
    width=22,
    bg="#2196F3"
)
export_btn.pack(pady=5)

match_btn = tk.Button(
    root,
    text="View Matched Lines",
    command=show_matched_lines,
    width=22,
    bg="#9C27B0"
)
match_btn.pack(pady=5)

# ---------------- RESULT LABEL ----------------
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 18, "bold"),
    bg="#1e1e1e",
    fg="cyan"
)
result_label.pack(pady=25)


# ---------------- START APP ----------------
root.mainloop()