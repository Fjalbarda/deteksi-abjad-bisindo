import tkinter as tk
from pathlib import Path
import webbrowser
import os
from PIL import Image, ImageTk


ASSETS_PATH = Path(__file__).resolve().parent / "assets/images"


def make_label(master, x, y, h, w, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0)  # type: ignore # don't shrink
    f.place(x=x, y=y)

    label = tk.Label(f, *args, **kwargs)
    label.pack(fill=tk.BOTH, expand=1)

    return label


def button_info_app():
    os.system("python about_page.py")


def button_preprocessing():
    os.system("python preprocessing.py")


def button_split():
    os.system("python split_dataset.py")


def button_train():
    webbrowser.open_new(
        r"https://colab.research.google.com/drive/1LBH08j0GWnwNAhiw0vLtdkbQ8CGTs1eX#scrollTo=I5VchEykJXxq")


def button_identify():
    os.system("python identifying.py")


window = tk.Tk()
window.title("Identifikasi Abjad BISINDO")

window.geometry("862x519")
window.configure(bg="#4C1D95")

background_image = Image.open("assets/images/bahasa.png")
resized_image = background_image.resize((400, 300))
width, height = resized_image.size

canvas = tk.Canvas(
    window, bg="#4C1D95", height=519, width=862,
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#EDE9FE", outline="")

canvas.create_text(
    610.0, 80.0, text="#InklusivitasMulaiDariKita.",
    fill="#4C1D95", font=("Inter", 16, "bold"))

canvas.create_text(
    645.0, 430.0, text="Memperluas Akses Bahasa Isyarat Bisindo untuk Semua",
    fill="#4C1D95", font=("Inter", 10, "bold", "italic"))

btn_info = tk.PhotoImage(file=ASSETS_PATH / "about.png")
generate_info = tk.Button(
    image=btn_info, borderwidth=0, highlightbackground="#FCFCFC", highlightthickness=30,
    command=button_info_app, relief="flat")
generate_info.place(x=480, y=120, width=332, height=39)

btn_preprocessing = tk.PhotoImage(file=ASSETS_PATH / "preprocessing.png")
generate_preprocessing = tk.Button(
    image=btn_preprocessing, borderwidth=0, highlightbackground="#FCFCFC", highlightthickness=30,
    command=button_preprocessing, relief="flat")
generate_preprocessing.place(x=480, y=180, width=332, height=39)

btn_split = tk.PhotoImage(file=ASSETS_PATH / "split.png")
generate_split = tk.Button(
    image=btn_split, borderwidth=0, highlightbackground="#FCFCFC", highlightthickness=30,
    command=button_split, relief="flat")
generate_split.place(x=480, y=240, width=332, height=39)

btn_train = tk.PhotoImage(file=ASSETS_PATH / "yolo.png")
generate_train = tk.Button(
    image=btn_train, borderwidth=0, highlightbackground="#FCFCFC", highlightthickness=30,
    command=button_train, relief="flat")
generate_train.place(x=480, y=300, width=332, height=39)

btn_identify = tk.PhotoImage(file=ASSETS_PATH / "identifying.png")
generate_identify = tk.Button(
    image=btn_identify, borderwidth=0, highlightbackground="#FCFCFC", highlightthickness=30,
    command=button_identify, relief="flat")
generate_identify.place(x=480, y=360, width=332, height=39)

title = tk.Label(
    text="Tugas Akhir", bg="#4C1D95",
    fg="white", justify="left", font=("Inter", 18, "bold"))
title.place(x=20.0, y=45.0)
canvas.create_rectangle(25, 80, 33 + 60, 80 + 5, fill="#FCFCFC", outline="")

background_photo = ImageTk.PhotoImage(resized_image)
background_label = canvas.create_image(
    0, 180, anchor=tk.NW, image=background_photo
)

info_text = tk.Label(
    text="Identifikasi Abjad Bahasa Isyarat\n"
    "Dengan Metode You Only Look Once (YOLO)\n"
    "Pada Bahasa Isyarat Indonesia (BISINDO).",
    bg="#4C1D95", fg="white", justify="left",
    font=("Inter", 14, "italic"))
info_text.place(x=20.0, y=90.0)

copyright_text = tk.Label(
    text="© 2023 Fajri J. Albarda • 2011501588",
    bg="#4C1D95", fg="white", justify="left",
    font=("Open Sans", 10, "italic"))
copyright_text.place(x=130.0, y=485.0)


window.resizable(False, False)
window.mainloop()
