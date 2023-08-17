import cv2
import imgaug.augmenters as iaa
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import glob
import os

# Path to asset files for this GUI window.
ASSETS_PATH = Path(__file__).resolve().parent / "assets/images"

# Windows control
window = tk.Tk()
window.title('Augmentasi dan Preprocessing')
window.geometry('850x200')
window.config(bg='#4c1d95')

# Label = judul skripsi
labelJudul = tk.Label(window,  fg='#FFF', width=540, font=(
    "Open Sans", 14, "bold"), text="Augmentasi dan Preprocessing", bg='#4c1d95')
labelJudul.pack(ipadx=5, ipady=5, pady=10)

# Fungsi flip lr image


def btn_fliplr_image():
    currdir = os.getcwd()
    file_path_variable1 = filedialog.askdirectory(
        parent=window, initialdir=currdir, title='Pilih direktori')
    file_path_variable2 = filedialog.askdirectory(
        parent=window, initialdir=currdir, title='Silakan pilih direktori untuk disimpan')

    if os.path.exists(file_path_variable1) and os.path.exists(file_path_variable2):
        images = []
        images_path = glob.glob(file_path_variable1 + "/*.*")
        for img_path in images_path:
            img = cv2.imread(img_path)
            images.append(img)

        augmentation = iaa.Sequential([
            iaa.Fliplr(1.0)  # type: ignore
        ])

        augmented_images = augmentation(images=images)

        i = 0
        sum_img = len(augmented_images)  # type: ignore
        for img in augmented_images:  # type: ignore
            cv2.imshow("Flipped Image", img)
            cv2.imwrite(file_path_variable2 + "/flip%03i.jpg" % i, img)
            i += 1
            cv2.waitKey(5)

        messagebox.showinfo(
            "Show Info", "Jumlah gambar setelah flip horizontal: " + str(sum_img))
        cv2.destroyAllWindows()
    else:
        messagebox.showinfo("Show Info", "Path File Atau Folder Harus Ada!")

# Fungsi rotasi image


def btn_rotate_image():
    currdir = os.getcwd()
    file_path_variable1 = filedialog.askdirectory(
        parent=window, initialdir=currdir, title='Pilih direktori')
    file_path_variable2 = filedialog.askdirectory(
        parent=window, initialdir=currdir, title='Silakan pilih direktori untuk disimpan')

    if os.path.exists(file_path_variable1) and os.path.exists(file_path_variable2):
        images = []
        images_path = glob.glob(file_path_variable1 + "/*.*")
        for img_path in images_path:
            img = cv2.imread(img_path)
            if img is not None:
                images.append(img)

        if len(images) > 0:
            augmentation = iaa.Sequential([
                iaa.Affine(translate_px={"x": (-20, 20),
                           "y": (-20, 20)}, rotate=(-18, 18))
            ])

            augmented_images = augmentation(images=images)

            i = 0
            sum_img = len(augmented_images)  # type: ignore
            for img in augmented_images:  # type: ignore
                cv2.imshow("Rotated Image", img)
                cv2.imwrite(file_path_variable2 + "/rotate%03i.jpg" % i, img)
                i += 1
                cv2.waitKey(5)

            messagebox.showinfo(
                "Show Info", "Jumlah gambar setelah rotasi: " + str(sum_img))
            cv2.destroyAllWindows()
        else:
            messagebox.showinfo(
                "Show Info", "Tidak ada gambar yang valid di direktori!")
    else:
        messagebox.showinfo("Show Info", "Path File Atau Folder Harus Ada!")

# Fungsi resize image


def btn_resize_image():
    currdir = os.getcwd()
    file_path_variable = filedialog.askdirectory(
        parent=window, initialdir=currdir, title='Pilih direktori')

    if os.path.exists(file_path_variable):
        images = []
        images_path = glob.glob(file_path_variable + "/*.*")
        for img_path in images_path:
            img = cv2.imread(img_path)
            images.append(img)

        augmentation = iaa.Sequential([
            iaa.Resize({"height": 640, "width": 640})
        ])

        augmented_images = augmentation(images=images)

        i = 0
        sum_img = len(augmented_images)  # type: ignore
        for img in augmented_images:  # type: ignore
            cv2.imshow("Resize Image", img)
            # Menyimpan gambar yang diubah ke gambar awalnya
            cv2.imwrite(images_path[i], img)
            i += 1
            cv2.waitKey(5)

        messagebox.showinfo(
            "Show Info", "Jumlah gambar setelah mengubah ukuran gambar: " + str(sum_img))
        cv2.destroyAllWindows()
    else:
        messagebox.showinfo("Show Info", "Path File Atau Folder Harus Ada!")


# Button control
frame = tk.Frame(window, bg='#F2B33D')

btn_resize = tk.PhotoImage(file=ASSETS_PATH / "resize.png")
generate_resize = tk.Button(
    image=btn_resize, borderwidth=0, highlightbackground="#4c1d95", highlightthickness=30,
    command=btn_resize_image, relief="flat")
generate_resize.place(x=100, y=100, width=174, height=39)

btn_flip = tk.PhotoImage(file=ASSETS_PATH / "flip.png")
generate_flip = tk.Button(
    image=btn_flip, borderwidth=0, highlightbackground="#4c1d95", highlightthickness=30,
    command=btn_fliplr_image, relief="flat")
generate_flip.place(x=340, y=100, width=174, height=39)

btn_rotate = tk.PhotoImage(file=ASSETS_PATH / "rotate.png")
generate_rotate = tk.Button(
    image=btn_rotate, borderwidth=0, highlightbackground="#4c1d95", highlightthickness=30,
    command=btn_rotate_image, relief="flat")
generate_rotate.place(x=570, y=100, width=174, height=39)

window.resizable(False, False)
frame.pack(expand=True)
window.mainloop()
