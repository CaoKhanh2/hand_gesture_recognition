import tkinter as tk
from tkinter import filedialog
import subprocess
from tkinter import messagebox
import train_model

def save_file():
    
    file_name = entry.get()
    
    if(file_name == ""):
        messagebox.showwarning("Warning", "Please enter file name!")
    else:
        file_name = file_name + ".hdf5"
        subprocess.run(["python", "train_model.py", str(file_name)])
        train_model.main()
    

def main():
    root = tk.Tk()
    root.title("Save File")

    root.minsize(height=100,width=500)

    global entry
    default_text = "cnn_model_VGG16_"

    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Tạo label và entry để nhập tên file
    label = tk.Label(frame, text="Enter file name:", font=("Arial Bold", 14))
    label.grid(column=0, row=1)

    entry = tk.Entry(frame, width=24, font=("Arial Bold", 12), textvariable="cnn_model_VGG16")
    entry.grid(column=1, row=1)

    entry.insert(0, default_text)

    # Tạo nút để lưu file
    save_button = tk.Button(root, text="Save File", command=save_file, font=("Arial Bold", 14))
    save_button.pack(pady=20)


    # Khởi chạy giao diện
    root.mainloop()