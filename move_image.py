import os
import shutil
import tkinter as tk
from tkinter import filedialog


def copy_images(source_var, destination_var):
    try:
        source_directory = source_var.get()
        destination_directory = destination_var.get()  # Get the string value from StringVar
        source_files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

        for source_path in source_files:
            filename = os.path.basename(source_path)
            destination_path = os.path.join(destination_directory, filename)
            shutil.copy2(source_path, destination_path)
        result_label.config(text="Successfully!")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

def main(destination_var):

    global source_var, destination_entry, source_entry, result_label
    source_var = tk.StringVar()
    source_files = []

    # Create tkinter window
    root = tk.Tk()
    root.title("Add Images")
    root.minsize(height=100,width=450)

    # Variables to store source and destination paths
    source_var = tk.StringVar()
    destination_var = tk.StringVar(value=destination_var)

    # Frame for source
    source_frame = tk.Frame(root)
    source_frame.pack(pady=10)

    source_label = tk.Label(source_frame, text="Source folder:")
    source_label.grid(row=0, column=0)

    source_var.set("Source")
    source_entry = tk.Entry(source_frame, textvariable=source_var, width=40)
    source_entry.grid(row=0, column=1)

    # Copy button
    copy_button = tk.Button(root, text="Add", command=lambda: copy_images(source_var, destination_var))
    copy_button.pack(pady=10, padx=20)

    # Display result
    result_label = tk.Label(root, text="")
    result_label.pack()


    root.mainloop()

