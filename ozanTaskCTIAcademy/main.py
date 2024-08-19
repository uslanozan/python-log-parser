import json
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
import os


selected_path = None
selected_directory_name = None


def filePath():
    global selected_path
    selected_path = filedialog.askdirectory(title="Choose Directory")
    global selected_directory_name
    selected_directory_name = os.path.basename(selected_path)

    if selected_path:
        selected_path_label.config(text=f"Selected Directory: {selected_directory_name}")
    else:
        selected_path_label.config(text="No directory selected.")


def get_relative_path(full_path, base_directory):
    # Get the directory path
    base_directory = os.path.abspath(base_directory)
    # To get the selected directory and subsequent paths within the full path
    relative_path = os.path.relpath(full_path, start=base_directory)
    return relative_path.replace("\\", "/")


# Enter the path
def saveDatas(txtPath, json_file_path):
    person = {}
    data_path = os.path.dirname(txtPath)
    people = []

    # Read and process the data
    with open(txtPath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            if line.startswith("URL:"):
                person['URL'] = line.split(":")[-1].strip()
            elif line.startswith("Username:"):
                person['Username'] = line.split(":")[1].strip()
            elif line.startswith("Password:"):
                person['Passw'] = line.split(":")[1].strip()
            elif line == "===============":
                if len(person) > 0:
                    file_name = get_relative_path(txtPath, selected_directory_name)
                    person = {'file_name': file_name, **person}
                    people.append(person)
                    person = {}

    # If there is just one person
    if len(person) > 0:
        person['file_name'] = data_path
        people.append(person)

    # Append to JSON file
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r+', encoding='utf-8') as json_file:
            try:
                # Read the existing data
                existing_data = json.load(json_file)
                if not isinstance(existing_data, list):
                    existing_data = []
            except json.JSONDecodeError:
                # If the JSON is invalid or empty, create new data
                existing_data = []
            existing_data.extend(people)
            json_file.seek(0)
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
            json_file.truncate()  # Truncate any excess data
    else:
        with open(json_file_path, 'a', encoding='utf-8') as json_file:
            json.dump(people, json_file, ensure_ascii=False, indent=4)


def parse(directory):
    if not directory:
        tkinter.messagebox.showwarning(title="Warning", message="Please select a directory")

    json_file_path = f"{selected_directory_name}.json"

    # Traverse all directories
    for root, dir, files in os.walk(directory, topdown=False):
        if 'Passwords.txt' in files:
            txtPath = os.path.join(root, 'Passwords.txt')
            saveDatas(txtPath, json_file_path)  # JSON file path

    # Complete message
    tkinter.messagebox.showinfo(title="Info", message=f"{json_file_path} saved.")


# Main window
window = tk.Tk()

# Window size
window.minsize(400, 150)
window.maxsize(400, 150)
window.title("Ozan Parser Script")

# Display selected file name
selected_path_label = tk.Label(text="Choose directory")
selected_path_label.place(x=200, y=50)

# Create start button
start = tk.Button(text="Start parsing", command=lambda: parse(selected_path))
start.place(x=50, y=12)

# Create directory selection button
choosePath = tk.Button(text="Choose directory", command=filePath)
choosePath.place(x=200, y=12)

window.mainloop()
