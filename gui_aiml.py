import tkinter as tk
from tkinter import messagebox, filedialog
import json
import csv

# Fixed part of seat number
SEAT_NUMBER_PREFIX = "B1903103"

# Dictionary to store student data
students_data = {}

# Dictionary containing subject codes and corresponding subject names
subject_dict = {
    '418541': 'Information Retrieval in AI',
    '418542': 'Cloud Computing',
    '418543': 'Deep Learning for AI',
    '418544B': 'Block Chain',  # Optional
    '418545C': 'DevOps in Machine Learning',  # Optional
    '418546': 'Lab Practice III',
    '418547': 'Lab Practice IV',
    '418548': 'Project Stage I',
    '418549A': 'Copyrights and Patents'  # Optional
}


# Create main application window
root = tk.Tk()
root.title("Student Data Entry")
root.geometry("800x600")

# Scrollable Frame
canvas = tk.Canvas(root)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)

def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", update_scroll_region)
canvas_frame = canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

# Labels and Entry Fields
tk.Label(frame, text="Seat Number (Last 3 Digits):", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
seat_number_entry = tk.Entry(frame, width=10)
seat_number_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="SGPA:", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
sgpa_entry = tk.Entry(frame, width=10)
sgpa_entry.grid(row=1, column=1, padx=10, pady=5)

# Dictionary to store entry fields dynamically
marks_entries = {}
subject_fields = []  # To keep track of entry fields for navigation

# Create entry fields for subjects
row_counter = 2
tk.Label(frame, text="Enter Marks (e.g., 85)", font=("Arial", 12, "bold"), fg="blue").grid(row=row_counter, column=0, columnspan=2, pady=5)

row_counter += 1
for code, name in subject_dict.items():
    tk.Label(frame, text=f"{code} - {name}:", font=("Arial", 10), anchor="w", wraplength=400).grid(row=row_counter, column=0, padx=10, pady=2, sticky="w")
    entry = tk.Entry(frame, width=10)
    entry.grid(row=row_counter, column=1, padx=10, pady=2)
    
    # Bind Enter key to move to next field
    def focus_next(event, idx=len(subject_fields)):  
        if idx + 1 < len(subject_fields):
            subject_fields[idx + 1].focus_set()
    
    entry.bind("<Return>", focus_next)  # When Enter is pressed, move to next entry
    marks_entries[code] = entry
    subject_fields.append(entry)
    
    row_counter += 1

# Function to save student data
def save_student():
    last_three_digits = seat_number_entry.get().strip()
    sgpa = sgpa_entry.get().strip()

    if not last_three_digits.isdigit() or len(last_three_digits) != 3:
        messagebox.showwarning("Input Error", "Please enter the last 3 digits of the Seat Number!")
        return

    full_seat_number = SEAT_NUMBER_PREFIX + last_three_digits

    if not sgpa:
        messagebox.showwarning("Input Error", "Please enter SGPA!")
        return
    
    try:
        sgpa = float(sgpa)
    except ValueError:
        messagebox.showerror("Invalid Input", "SGPA must be a number!")
        return

    # Collect marks
    marks_data = {}
    for code, entry in marks_entries.items():
        marks = entry.get().strip()
        marks_data[code] = marks if marks else "NA"

    # Save to dictionary
    students_data[full_seat_number] = {
        "SGPA": sgpa,
        "Marks": marks_data
    }

    messagebox.showinfo("Success", f"Data saved for {full_seat_number}!")
    seat_number_entry.delete(0, tk.END)
    sgpa_entry.delete(0, tk.END)
    for entry in marks_entries.values():
        entry.delete(0, tk.END)

# Function to save students_data to JSON
def save_to_json():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if not file_path:
        return
    with open(file_path, "w") as json_file:
        json.dump(students_data, json_file, indent=4)
    messagebox.showinfo("Success", f"Data saved to {file_path}")

# Function to load student data from JSON
def load_from_json():
    global students_data
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if not file_path:
        return
    with open(file_path, "r") as json_file:
        students_data = json.load(json_file)
    messagebox.showinfo("Success", f"Data loaded from {file_path}")

# Function to export JSON data to CSV
def export_to_csv():
    if not students_data:
        messagebox.showwarning("No Data", "Load JSON data first before exporting to CSV!")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    with open(file_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Writing header
        header = ["Seat Number", "SGPA"] + list(subject_dict.values())
        csv_writer.writerow(header)
        
        # Writing student data
        for seat_no, data in students_data.items():
            row = [seat_no, data["SGPA"]]
            for subject_code in subject_dict.keys():
                row.append(data["Marks"].get(subject_code, "NA"))
            csv_writer.writerow(row)
    
    messagebox.showinfo("Success", f"Data exported to {file_path}")

# Buttons
tk.Button(frame, text="Save Student", command=save_student, font=("Arial", 12), bg="lightblue").grid(row=row_counter, column=0, pady=10, padx=5)
tk.Button(frame, text="Save to JSON", command=save_to_json, font=("Arial", 12), bg="orange").grid(row=row_counter+1, column=0, pady=10, padx=5)
tk.Button(frame, text="Load from JSON", command=load_from_json, font=("Arial", 12), bg="yellow").grid(row=row_counter+1, column=1, pady=10, padx=5)
tk.Button(frame, text="Export to CSV", command=export_to_csv, font=("Arial", 12), bg="pink").grid(row=row_counter+2, column=0, columnspan=2, pady=10, padx=5)

# Run the GUI application
root.mainloop()
