import argparse
import os
import shutil
from random import sample
import tkinter as tk
from tkinter import filedialog, messagebox

# Tambahkan Parser
parser = argparse.ArgumentParser()

parser.add_argument("--train", type=int, default=80,
                    help="Percentage of train set")
parser.add_argument("--val", type=int, default=20,
                    help="Percentage of val set")
parser.add_argument("--folder", type=str, default="img",
                    help="Folder that contains images")
parser.add_argument("--dest", type=str, default="img-dest",
                    help="Destination folder")

args = parser.parse_args()

count = 0
list_id = []


def get_difference_from_2_list(list1, list2):
    set_list1 = set(list1)
    set_list2 = set(list2)

    diff = list(set_list1.difference(set_list2))

    return diff


def get_split_data(list_id_param):
    # Set Data Pelatihan
    # Hitung jumlah data pelatihan
    n_train = (count * args.train) // 100
    # Acak
    train = sample(list_id_param, int(n_train))

    list_id_param = get_difference_from_2_list(list_id_param, train)

    # Set Data Val
    # Hitung jumlah data validasi
    val = get_difference_from_2_list(list_id_param, [])

    return train, val


def make_folder():
    folders = ["images", "labels"]
    inner_folders = ["train", "val"]

    if not os.path.isdir(args.dest):
        os.mkdir(args.dest)

    for folder in folders:
        path = os.path.join(args.dest, folder)
        # Periksa folder yang sudah ada
        if not os.path.isdir(path):
            os.mkdir(path)

        for in_folder in inner_folders:
            inner_path = os.path.join(path, in_folder)
            # Periksa folder dalam folder
            if not os.path.isdir(inner_path):
                os.mkdir(inner_path)


def copy_image(file, id_folder):
    inner_folders = ["train", "val"]

    # Image
    source = os.path.join(args.folder, file)
    out_dest = os.path.join(args.dest, 'images')
    destination = os.path.join(out_dest, inner_folders[id_folder])

    try:
        shutil.copy(source, destination)

        # Labels
        separator = file.find(".")
        filename = file[0:separator] + ".txt"

        source = os.path.join(args.folder, filename)
        out_dest = os.path.join(args.dest, 'labels')
        destination = os.path.join(out_dest, inner_folders[id_folder])

        shutil.copy(source, destination)

    except shutil.SameFileError:
        print("Sumber dan tujuan mewakili file yang sama.")

    if id_folder == 1:
        return True

    return False


def browse_source():
    folder_path = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(tk.END, folder_path)


def browse_destination():
    folder_path = filedialog.askdirectory()
    dest_entry.delete(0, tk.END)
    dest_entry.insert(tk.END, folder_path)


def clear_text():
    source_entry.delete(0, tk.END)
    dest_entry.delete(0, tk.END)


def process_split():
    global count
    global list_id

    args.folder = source_entry.get()
    args.dest = dest_entry.get()

    # Validasi folder sumber
    if not args.folder:
        messagebox.showerror('Error', 'Folder sumber tidak boleh kosong.')
        return

    # Validasi folder tujuan
    if not args.dest:
        messagebox.showerror('Error', 'Folder tujuan tidak boleh kosong.')
        return

    # Check train set
    if args.train < args.val:
        messagebox.showerror(
            'Error', 'Set pelatihan harus memiliki persentase yang lebih besar daripada set validasi.')
        return

    # Count number of data
    count = 0
    list_id = []
    for file in os.listdir(args.folder):
        if file.endswith((".jpg", ".png")):
            list_id.append(count)
            count += 1

    train, val = get_split_data(list_id)
    make_folder()

    count = 0
    success_message_shown = False
    for file in os.listdir(args.folder):
        if file.endswith((".jpg", ".png")):
            if count in train:
                copy_success = copy_image(file, 0)
            else:
                copy_success = copy_image(file, 1)

            if copy_success and not success_message_shown:
                messagebox.showinfo('Split Dataset',
                                    'Dataset berhasil dibagi dengan sukses.')
                success_message_shown = True

            count += 1


# Create the main window
window = tk.Tk()
window.title('Split Dataset')
window.geometry('780x200')
window.configure(bg='#4c1d95')  # Set the background color

# Foder sumber
source_label = tk.Label(window, text='Source Folder:',
                        bg='#4c1d95', fg='#FFF', anchor='w')
source_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
source_entry = tk.Entry(window, width=50)
source_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
source_button = tk.Button(window, text='Browse', command=browse_source, highlightbackground="#4c1d95")
source_button.grid(row=1, column=3, padx=10, pady=10)

# Folder tujuan
dest_label = tk.Label(
    window, text='Destination Folder:', bg='#4c1d95', fg='#FFF', anchor='w')
dest_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
dest_entry = tk.Entry(window, width=50)
dest_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
dest_button = tk.Button(window, text='Browse', command=browse_destination, highlightbackground="#4c1d95")
dest_button.grid(row=2, column=3, padx=10, pady=10)

# Split button
process_button = tk.Button(window, text='Split Dataset', command=process_split, highlightbackground="#4c1d95")
process_button.grid(row=3, column=1, columnspan=2,
                    padx=10, pady=10, sticky='w')

# Clear button
clear_button = tk.Button(window, text='Clear', command=clear_text, highlightbackground="#4c1d95")
clear_button.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

window.resizable(False, False)
window.mainloop()
