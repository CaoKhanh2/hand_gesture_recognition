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
# import os
# import shutil
# import tkinter as tk
# from tkinter import filedialog

# def browse_source_directory():
#     source_files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
#     if source_files:
#         source_directory = os.path.dirname(source_files[0])
#         source_var.set(source_directory)
#         source_entry.delete(0, tk.END)

# def copy_images(source_var, destination_var):
#     try:
#         source_directory = source_var.get()
#         destination_directory = destination_var.get()  # Get the string value from StringVar
#         source_files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

#         for source_path in source_files:
#             filename = os.path.basename(source_path)
#             destination_path = os.path.join(destination_directory, filename)
#             shutil.copy2(source_path, destination_path)
#         result_label.config(text="Successfully!")
#     except Exception as e:
#         result_label.config(text=f"Error: {str(e)}")

# global source_var, destination_entry, source_entry, result_label

# root = tk.Tk()
# root.title("Add Images")

# root.minsize(height=100,width=450)

# source_var = tk.StringVar()
# destination_var = tk.StringVar()

# source_frame = tk.Frame(root)
# source_frame.pack(pady=10)

# source_label = tk.Label(source_frame, text="Source folder:")
# source_label.grid(row=0, column=0)

# # source_var.set("Source")
# source_entry = tk.Entry(source_frame, textvariable=source_var, width=35)
# source_entry.grid(row=0, column=1)

# # Copy button
# copy_button = tk.Button(root, text="Add", command=lambda: copy_images(source_var, destination_var))
# copy_button.pack(pady=10, padx=20)

# # Display result
# result_label = tk.Label(root, text="")
# result_label.pack()

# # Run tkinter window
# root.mainloop()


# import tkinter as tk
# from tkinter import ttk

# def on_combobox_select(event):
#     selected_value = combobox.get()
#     label.config(text=f"You selected: {selected_value}")

# # Tạo cửa sổ chính
# root = tk.Tk()
# root.title("Combobox Example")

# # Tạo một Combobox
# options = ["Option 1", "Option 2", "Option 3"]
# combobox = ttk.Combobox(root, values=options)
# combobox.pack(pady=10)
# combobox.set("Select an option")  # Giá trị mặc định hiển thị trong combobox

# # Label để hiển thị thông tin khi chọn một tùy chọn
# label = tk.Label(root, text="")
# label.pack(pady=10)

# # Gán hàm xử lý sự kiện khi chọn một tùy chọn
# combobox.bind("<<ComboboxSelected>>", on_combobox_select)

# # Hiển thị cửa sổ
# root.mainloop()


# import tkinter as tk
# from tkinter import filedialog

# def save_file():
#     file_name = entry.get()
#     if file_name:
#         file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=file_name, filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
#         if file_path:
#             with open(file_path, 'w') as file:
#                 # Ghi nội dung file ở đây (đây là ví dụ)
#                 file.write("Hello, this is some content.")

# # Tạo cửa sổ chính
# root = tk.Tk()
# root.title("Save File")

# # Tạo label và entry để nhập tên file
# label = tk.Label(root, text="Enter file name:")
# label.pack(pady=10)

# entry = tk.Entry(root)
# entry.pack(pady=10)

# # Tạo nút để lưu file
# save_button = tk.Button(root, text="Save File", command=save_file)
# save_button.pack(pady=20)

# # Khởi chạy giao diện
# root.mainloop()

import tkinter as tk
from tkinter import filedialog

def save_file():
    file_name = entry.get()
    if file_name:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=file_name, filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                # Ghi nội dung file ở đây (đây là ví dụ)
                file.write("Hello, this is some content.")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Save File")
root.minsize(height=100, width=400)

# Tạo label và entry để nhập tên file
label = tk.Label(root, text="Enter file name:", font=("Arial Bold", 14))
label.pack(pady=10)

entry = tk.Entry(root, width=25)
entry.pack(pady=10)

# Tạo nút để lưu file
save_button = tk.Button(root, text="Save File", command=save_file, font=("Arial Bold", 14))

# Sử dụng pack để đặt nút ở giữa cửa sổ và cùng hàng với label và entry
save_button.pack(side=tk.BOTTOM, pady=20)

# Khởi chạy giao diện
root.mainloop()



