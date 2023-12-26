from tkinter import *
from tkinter import Canvas
from tkinter import ttk
from tkinter import messagebox
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
from cnn_sift import _model

import read_file_txt
import move_image
import save

import shutil
import send2trash
import imutils
import cv2
import os
import re


root=Tk()
root.iconphoto(False, PhotoImage(file='./icon/icon.png'))

root.title("Hand Gesture Recognition")
root.resizable(height=False,width=False)
root.minsize(height=400,width=400)

global result, image
current_index = 0
index = 1
k = 0
result = []
file_path_label = './data/storage/gesture_hand.txt'
file_path_model = './data/storage/model.txt'

################################################# show_function1 ########################################################

def input():
    input_path = filedialog.askopenfilenames()
    input_entry.delete(0, END)
    input_entry.insert(0, input_path)

def show_img(path):
    img = Image.open(path)
    img = img.resize((448,448), Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(img)
    image_label.configure(image=image)
    image_label.image = image

def output():
    
    filename = []
    filename = input_entry.get().split()


    if(len(filename) != 0):
        
        for i in range (len(filename)):
            if(current_index == 0 and k == 0):

                cnn_sift = _model()
                result.append(cnn_sift.main_image(filename[i]))
                show_img(filename[current_index])
                lbl.configure(text="Prediction: "+result[current_index],font=("Arial Bold", 25))
                lbl.pack() 

                lbl_index.configure(text=str(index)+"/"+str(len(filename)),font=("Arial Bold", 14))
                lbl_index.pack(side=RIGHT, pady=10, padx=3, fill=X)
            elif(0 <= current_index < len(filename)):
                show_img(filename[current_index])
                lbl.configure(text="Prediction: "+result[current_index],font=("Arial Bold", 25))
                lbl.pack()

                lbl_index.configure(text=str(index)+"/"+str(len(filename)), font=("Arial Bold", 14))
                lbl_index.pack(side=RIGHT, pady=10, padx=3, fill=X)
            else:
                print("Index out of range")
                break

    return result


def show():

    filename = []
    filename = input_entry.get().split()

    if(len(filename) != 0):
        
        for i in range (len(filename)):
            if(0 <= current_index < len(filename)):
                show_img(filename[current_index])
                lbl.configure(text="Dự đoán: "+result[current_index],font=("Arial Bold", 25))
                lbl.pack()

def show_next_image():
    global current_index, index
    current_index = current_index + 1
    index = index + 1
    output()

def show_pre_image():
    global current_index, index, k
    k = 1
    current_index = current_index - 1
    index = index - 1
    output()

def new():
    global current_index, index, k
    k = 0
    current_index = 0
    index = 1
    result.clear()

    input_entry.delete(0, END)
    image_label.config(image=None)
    image_label.image = None
    lbl.configure(text="")
    lbl_index.config(text="")
    lbl.pack()

#########################################################################################################################


################################################# show_function3 ########################################################

def auto_index():
    #file_path = "./data/storage/gesture_hand.txt"
    with open(file_path_label, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for index, line in enumerate(lines):
        if not any(char.isdigit() for char in line):
            new_line = f"{line.strip()} {index}"
        else:
            new_line = line.strip()
        new_lines.append(new_line)

    with open(file_path_label, 'w') as output_file:
        for new_line in new_lines:
            output_file.write(f"{new_line}\n")

def check_string_in_file(input_string, file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                non_numeric_matches = re.findall(r'[^\d\s]+', line)
                if input_string in non_numeric_matches:
                    return True
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def add_data_to_file(data):

    global lines
    #file_path = "./gesture_hand.txt"

    selected_item = tree.selection()

    if data == "" and not selected_item:
        messagebox.showwarning("Warning", "Empty!")
    elif check_string_in_file(data,file_path_label) == True:
        messagebox.showerror("Error", "The directory already exists !")
    elif selected_item:
        confirmed = messagebox.askyesno("Confirm Deletion", "Are you sure you want to edit the data?")
        if confirmed:
            pth = tree.item(selected_item, 'values')[0]
            path = './data/train/' + str(pth)
            #print(path)
            move_image.main(path)
    else:
        with open(file_path_label, "a") as file:
            file.write(data + "\n")
        entry_data.delete(0, END)

        auto_index()

        label2id = read_file_txt.read_file(file_path_label)
        for key in label2id:
            if not os.path.exists('./data/train/' + str(key)):
                    os.mkdir('./data/train/' + str(key))
        
        display_file_content()

        path = './data/train/' + str(data)
        print(path)
        move_image.main(path)
    
def new_training ():
    # label2id = read_file_txt.read_file(file_path_label)
    # for key in label2id:
    #     if not os.path.exists('./data/train/' + str(key)):
    #             os.mkdir('./data/train/' + str(key))
    # train_model.main()
    save.main()

def display_file_content():
    #file_path = "./gesture_hand.txt"
    try:
        with open(file_path_label, "r") as file:
            content = file.readlines()
            new_lines = [re.sub(r'\d', '', line) for line in content]
            update_table(new_lines)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")

def update_table(content):
    # Clear existing rows in the table
    for row in tree.get_children():
        tree.delete(row)
    # Insert new rows based on file content
    for line in content:
        tree.insert("", "end", values=(line.strip(),))

def delete_selected_row():
    selected_item = tree.selection()
    if selected_item:
        confirmed = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected row?")
        if confirmed:
            pth = tree.item(selected_item, 'values')[0]
            # cleaned_value = pth.strip("()").strip("'")
            # result = re.sub(r'\d+', '', cleaned_value)
            tree.delete(selected_item)
            #shutil.rmtree("./data/train/"+str(cleaned_value))
            send2trash.send2trash("./data/train/"+str(pth))
            save_table_to_file()
    else:
        messagebox.showwarning("Warning", "Please select a row to delete.")

def save_table_to_file():
    #file_path = "./gesture_hand.txt"
    with open(file_path_label, "w") as file:
        for item in tree.get_children():
            content = tree.item(item, 'values')[0]
            file.write(content + "\n")
    auto_index()

#########################################################################################################################

def hide():
    open_button1.pack_forget()
    open_button2.pack_forget()
    open_button3.pack_forget()
    label_main1.pack_forget()
    combobox.pack_forget()

def get_file_names_in_directory(directory_path):
    file_names = []
    
    # Kiểm tra xem đường dẫn thư mục có tồn tại không
    if os.path.exists(directory_path):
        # Lấy danh sách tất cả các tên trong thư mục
        all_names = os.listdir(directory_path)
        
        # Tách tên file và tên thư mục bằng cấu trúc if-else
        for name in all_names:
            full_path = os.path.join(directory_path, name)
            if os.path.isfile(full_path):
                file_names.append(name)
    
    return file_names

def on_combobox_select(event):
    selected_value = combobox.get()
    # subprocess.run(["python", "cnn_sift.py", str(selected_value)])
    with open(file_path_model, 'w') as file:
    # Ghi dữ liệu vào file
        file.write(selected_value)
    print(selected_value)


#########################################################################################################################

def show_function1():
    global sel
    sel = 1
    global input_entry, image_label, lbl, lbl_index, button_excu, button_del, button_next, button_back, browse1, input_path, line, top_frame, bottom_frame

    root.minsize(height=800,width=800)

    top_frame = Frame(root)
    bottom_frame = Frame(root)

    bottom_frame.pack(side=BOTTOM)
    top_frame.pack(side=TOP)

    line = Frame(root, height=1, width=400, bg="grey80", relief='groove')
    line.pack(pady=10)
    
    input_path = Label(top_frame, text="Image path:", font=("Arial Bold", 12))
    input_entry = Entry(top_frame, text="", width=40)

    browse1 = Button(top_frame, text="Choose image", command=input, font=("Arial Bold", 12))
    input_path.pack(pady=5)
    input_entry.pack(pady=5)
    browse1.pack(pady=5)

    button_excu = Button(bottom_frame, text='Identification',command=output, font=("Arial Bold", 12))
    button_excu.pack(side=BOTTOM,pady=10 , fill=X)
    button_del = Button(bottom_frame, text='Clear',command=new, font=("Arial Bold", 12))
    button_del.pack(side=BOTTOM,pady=10 , fill=X)

    button_next = Button(bottom_frame, text=' >> ',command=show_next_image, font=("Arial Bold", 12))
    button_next.pack(side=RIGHT,pady=20, padx=20)

    lbl_index = Label(bottom_frame)
    lbl_index.pack(side=RIGHT, padx=3, fill=X)

    button_back = Button(bottom_frame, text=' << ',command=show_pre_image, font=("Arial Bold", 12))
    button_back.pack(side=RIGHT, pady=20, padx= 20)

    image_label = Label(root)
    image_label.pack(pady=10)

    lbl = Label(root)
    lbl.pack(pady=15, fill=X)

    hide()

def show_function2():

    cnn_sift = _model()
    cnn_sift.main_cam()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

def show_function3():

    global sel
    sel = 2
    global top_frame, bottom_frame, entry_data, label_data, button_training, button_display_file, button_add_data, label_file_content, tree, delete_button

    root.minsize(height=500,width=500)
    top_frame = Frame(root)
    bottom_frame = Frame(root)

    bottom_frame.pack(side=BOTTOM)
    top_frame.pack(side=TOP)
    
    label_data = Label(top_frame, text="Add new gestures:", font=("Arial Bold", 12))
    label_data.pack()

    entry_data = Entry(top_frame, width=30, font=("Arial Bold", 14))
    entry_data.pack(pady=5)

    tree = ttk.Treeview(top_frame, columns=("Column1",), show="headings", selectmode="browse")
    tree.column("#1", width=200)
    tree.heading("#1", text="Label_id")
    tree.pack(pady=5)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=(None, 12))  # Điều chỉnh kích cỡ chữ của tiêu đề cột
    style.configure("Treeview", font=(None, 12))  # Điều chỉnh kích cỡ chữ của nội dung cột


    button_training = Button(bottom_frame, text="Training", command=new_training, font=("Arial Bold", 12))
    button_training.pack(side=BOTTOM,pady=15 , fill=X)

    delete_button = Button(bottom_frame, text="Delete Selected Row", command=delete_selected_row, font=("Arial Bold", 12))
    delete_button.pack(side=BOTTOM,pady=15, fill=X)

    button_add_data = Button(bottom_frame, text="Add label2id", command=lambda: add_data_to_file(entry_data.get()), font=("Arial Bold", 12))
    button_add_data.pack(side=BOTTOM,pady=15, fill=X)

    button_display_file = Button(bottom_frame, text="Show label2id", command=display_file_content, font=("Arial Bold", 12))
    button_display_file.pack(side=BOTTOM,pady=15 , fill=X)


    hide()


def back():

    global current_index, index

    ############################
    current_index = 0
    index = 1
    result.clear()

    root.minsize(height=400,width=400)
    if(sel == 1):
        line.destroy()

        input_entry.delete(0, END)
        input_entry.destroy()

        button_excu.destroy()
        browse1.destroy()
        button_del.destroy() 
        button_next.destroy()
        button_back.destroy()

        input_path.destroy()
        lbl.destroy()
        lbl_index.destroy()
        image_label.destroy()

        top_frame.destroy()
        bottom_frame.destroy()

    #############################
    else:
        label_data.destroy()

        tree.destroy()

        entry_data.delete(0, END)
        entry_data.destroy()

        button_add_data.destroy()
        button_training.destroy()
        button_display_file.destroy()
        delete_button.destroy()

        top_frame.destroy()
        bottom_frame.destroy()
    
    label_main1.pack(anchor="n")
    combobox.pack(pady=10)
    open_button1.pack(pady=20, side="top")
    open_button2.pack(pady=20, side="top")
    open_button3.pack(pady=20, side="top")
    
    

bt_back = Button(root, text="<-", command=back, font=("Arial Bold", 12))
bt_back.pack(anchor="nw")

label_main1 = Label(root, text="Model", font=("Arial Bold", 14))
label_main1.pack(anchor="n")

directory_path = './model'
options = get_file_names_in_directory(directory_path)

combobox = ttk.Combobox(root, values=options, width=25, font=("Arial Bold", 14))
combobox.pack(pady=10)
combobox.set("Select an option")

combobox.bind("<<ComboboxSelected>>", on_combobox_select)

open_button1 = Button(root, text="Recognition through Image",command=show_function1, width=25, height=3, font=("Arial Bold", 14))
open_button1.pack(pady=20, side=TOP)

open_button2 = Button(root, text="Recognition through Camera",command=show_function2, width=25, height=3, font=("Arial Bold", 14))
open_button2.pack(pady=20, side=TOP)

open_button3 = Button(root, text="Add hand gestures",command=show_function3, width=25, height=3, font=("Arial Bold", 14))
open_button3.pack(pady=20, side=TOP)


root.mainloop()


