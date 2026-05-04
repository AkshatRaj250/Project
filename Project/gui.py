import tkinter as tk
from tkinter import ttk, messagebox
from db import insert_entry, fetch_all_entries, delete_entry
from analysis import analyze_data
import matplotlib.pyplot as plt
import pandas as pd


def create_gui():
    root = tk.Tk()
    root.title("Gym Progress Tracker")
    root.geometry("750x520")
    root.configure(bg="#020617")

    # Centering
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Title
    tk.Label(root,
             text="GYM PROGRESS TRACKER",
             bg="#020617",
             fg="white",
             font=("Segoe UI", 16, "bold")
             ).grid(row=0, column=0, columnspan=2, pady=20)

    # Input 
    labels = ["Name", "Date (YYYY-MM-DD)", "Exercise", "Sets", "Reps", "Weight"]
    entries = []

    for i, text in enumerate(labels):
        tk.Label(root,
                 text=text,
                 bg="#020617",
                 fg="white",
                 font=("Segoe UI", 10)
                 ).grid(row=i+1, column=0, padx=(0,2), pady=8, sticky="e")

        entry = tk.Entry(root,
                         bg="#292B36",
                         fg="white",
                         insertbackground="white",  # cursor fix
                         relief="solid",
                         bd=1)
        entry.grid(row=i+1, column=1, padx=(2,0), pady=8, ipadx=5, ipady=5, sticky="w")

        entries.append(entry)

        root.grid_columnconfigure(0, minsize=80)  # label column width
        root.grid_columnconfigure(1, minsize=150) # entry column width

    # Functions
    def add_entry():
        try:
            data = {
                "name": entries[0].get(),
                "date": entries[1].get(),
                "exercise": entries[2].get(),
                "sets": int(entries[3].get()),
                "reps": int(entries[4].get()),
                "weight": float(entries[5].get())
            }

            if "" in [str(v).strip() for v in data.values()]:
                messagebox.showerror("Error", "All fields required")
                return

            insert_entry(data)
            messagebox.showinfo("Success", "Entry Added")

            for e in entries:
                e.delete(0, tk.END)

        except:
            messagebox.showerror("Error", "Invalid Input")

    def view_records():
        records = fetch_all_entries()

        win = tk.Toplevel(root)
        win.title("Records")
        win.geometry("700x400")
        win.configure(bg="#020617")

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="#020617",
                        foreground="white",
                        fieldbackground="#020617")

        style.configure("Treeview.Heading",
                        background="#1e293b",
                        foreground="white")

        tree = ttk.Treeview(win,
                            columns=("ExNo", "Name", "Date", "Exercise", "Sets", "Reps", "Weight"),
                            show="headings")

        tree.heading("ExNo", text="Exercise No.")
        tree.column("ExNo", width=100, anchor="center") 

        for col in tree["columns"][1:]:  
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        for i, r in enumerate(records, start=1):
            tree.insert("",tk.END, iid=str(r["_id"]), values=(
                i,
                r["name"], 
                r["date"], 
                r["exercise"],
                r["sets"], 
                r["reps"], 
                r["weight"]
            ))

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Delete
        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Select a row")
                return

            entry_id_to_delete = selected[0]

            delete_entry(entry_id_to_delete) 

            
            tree.delete(selected[0])
            messagebox.showinfo("Deleted", "Entry removed")

        tk.Button(win, text="Delete Selected",
                  command=delete_selected,
                  bg="#dc2626", fg="white"
                  ).pack(pady=5)

    def show_analysis():
        data = fetch_all_entries()
        result = analyze_data(data)
        messagebox.showinfo("Analysis", result)

    def show_graph():
        data = fetch_all_entries()

        if not data:
            messagebox.showerror("Error", "No data to plot")
            return

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        plt.plot(df["date"], df["weight"])
        plt.xlabel("Date")
        plt.ylabel("Weight")
        plt.title("Workout Progress")
        plt.show()

    # Buttons
    btn_style = {
        "bg": "#1e293b",
        "fg": "white",
        "font": ("Segoe UI", 10, "bold"),
        "relief": "flat",
        "padx": 10,
        "pady": 5
    }

    tk.Button(root, text="Add Entry", command=add_entry, **btn_style)\
        .grid(row=8, column=0, pady=10, sticky="ew")

    tk.Button(root, text="View Records", command=view_records, **btn_style)\
        .grid(row=8, column=1, sticky="ew")

    tk.Button(root, text="Analyze", command=show_analysis, **btn_style)\
        .grid(row=9, column=0, sticky="ew")

    tk.Button(root, text="Show Graph", command=show_graph, **btn_style)\
        .grid(row=9, column=1, sticky="ew")

    # Display
    root.mainloop()