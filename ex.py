# # # # Đọc nội dung từ file txt
# # with open('a1.txt', 'r') as file:
# #     lines = file.readlines()
# # new_lines = [f"{line.strip()} {index}" if any(char.isdigit() for char in line) else line.strip() for index, line in enumerate(lines, 1)]


# # # # # Thêm số đằng sau mỗi chuỗi ký tự
# # # # new_lines = [f"{line.strip()} {index}" for index, line in enumerate(lines)]

# # # # # In ra kết quả hoặc ghi vào file mới
# # # # for new_line in new_lines:
# # # #     print(new_line)

# # # # # Hoặc ghi vào file mới
# # with open('a1.txt', 'w') as output_file:
# #     for new_line in new_lines:
# #         output_file.write(f"{new_line}\n")


# # def add_number_to_lines(filename):
# #     try:
# #         with open(filename, 'r') as file:
# #             lines = file.readlines()
# #             updated_lines = [f"{line.strip()} {index}" if any(char.isdigit() for char in line) else line for index, line in enumerate(lines, start=1)]

# #         # In ra màn hình danh sách các dòng đã được cập nhật
# #         for updated_line in updated_lines:
# #             print(updated_line)

# #         # Ghi danh sách đã được cập nhật vào file
# #         with open(filename, 'w') as file:
# #             file.writelines(updated_lines)

# #     except FileNotFoundError:
# #         print(f"File '{filename}' does not exist.")

# # # Example usage with a txt file
# # filename = 'a1.txt'
# # add_number_to_lines(filename)

# # with open('a1.txt', 'r') as file:
# #     lines = file.readlines()

# # # new_lines = [f"{line.strip()} {index}" if not any(char.isdigit() for char in line) else line.strip() for index, line in enumerate(lines)]

# # new_lines = []

# # for index, line in enumerate(lines):
# #     if not any(char.isdigit() for char in line):
# #         new_line = f"{line.strip()} {index}"
# #     else:
# #         new_line = line.strip()
# #     new_lines.append(new_line)

# # with open('a1.txt', 'w') as output_file:
# #     for new_line in new_lines:
# #         output_file.write(f"{new_line}\n")

# with open('a1.txt', 'r') as file:
#     lines = file.readlines()

# new_lines = new_lines = [line.strip() for line in lines]

# print(new_lines)
import os
import shutil
import tkinter as tk
from tkinter import filedialog

def browse_source_directory():
    source_files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if source_files:
        source_directory = os.path.dirname(source_files[0])
        source_var.set(source_directory)
        source_entry.delete(0, tk.END)

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

global source_var, destination_entry, source_entry, result_label

root = tk.Tk()
root.title("Add Images")

root.minsize(height=100,width=450)

source_var = tk.StringVar()
destination_var = tk.StringVar()

source_frame = tk.Frame(root)
source_frame.pack(pady=10)

source_label = tk.Label(source_frame, text="Source folder:")
source_label.grid(row=0, column=0)

# source_var.set("Source")
source_entry = tk.Entry(source_frame, textvariable=source_var, width=35)
source_entry.grid(row=0, column=1)

# Copy button
copy_button = tk.Button(root, text="Add", command=lambda: copy_images(source_var, destination_var))
copy_button.pack(pady=10, padx=20)

# Display result
result_label = tk.Label(root, text="")
result_label.pack()

# Run tkinter window
root.mainloop()