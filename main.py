from tkinter import *
from customtkinter import *
import PIL
from PIL import ImageTk, Image, ImageDraw, ImageFont
from tkinter import messagebox, filedialog, ttk, colorchooser, font
from ttkbootstrap.dialogs.dialogs import FontDialog

import fontstest

window = CTk()
# window.resizable(False, False)
window.geometry("1050x625")
window.title("Water-Mark")
set_appearance_mode("dark")  # Modes: system (default), light, dark
# set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

global thing

def choose_font():
    # font chooser
    fc = Listbox(window)
    fc.grid(row=0, column=1, sticky='nswe')

    # insert all the fonts
    for f in font.families():
        fc.insert('end', f)


def open_font():
    global fd
    # Define Font Dialog
    fd = FontDialog("danger")
    # Show the box
    fd.show()

    # Capture The Reult fd.result and update label
    print(fd.realfamily.lower())
    print(fd.realsize)
    image_label.config(font=fd.result)


def display_image():
    file_path = filedialog.askopenfilename(title="Open Image File",
                                           filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
    print(file_path)
    if file_path:
        global image
        try:
            global pic
            pic = Image.open(file_path)
            re_pic = pic.resize((image_label.winfo_width(), image_label.winfo_height()))

            image = ImageTk.PhotoImage(re_pic)

        except PIL.UnidentifiedImageError:
            messagebox.showerror(title="Invalid image", message=f"{file_path} is not a valid image file.")
        image_label.config(image=image)




def save():

    global image
    """Combines the watermark text with the full-size image and saves file"""
    position = my_combo.get()
    print(position)
    image_width = pic.width
    image_height = pic.height
    x = None
    y = None
    # choose position to place text
    if position == "Top left":
        x = 20
        y = 20
    elif position == "Top center":
        x = image_width // 2
        y = 20
    elif position == "Top right":
        x = image_width - 20
        y = 20
    elif position == "Center":
        x = image_width // 2
        y = image_height // 2
    elif position == "Bottom right":
        x = image_width - 20
        y = image_height - 20
    elif position == "Bottom left":
        x = 20
        y = image_height
    elif position == "bottom_center":
        x = image_width // 2
        y = image_height - 20

    # create the transparent watermark
    v_font = ImageFont.truetype(font="arial.ttf", size=int(font_size))
    # watermark_font = ImageFont.load_default()

    # txt = Image.new('RGBA', pic.size)
    edit_image = ImageDraw.Draw(pic)

    edit_image.text((x, y), text=thing, fill=hex_code, font=v_font, anchor="ms")

    file_path = filedialog.asksaveasfilename(confirmoverwrite=True,
                                     defaultextension="png",
                                     filetypes=[("jpeg", ".jpg"),
                                                ("png", ".png"),
                                                ("bitmap", "bmp"),
                                                ("gif", ".gif")])
    if file_path is not None:  # if dialog not closed with "cancel".
        pic.save(fp=file_path)
        messagebox.showinfo(message="Your images have been saved!\nThank you for using this tool.",
                            title="Saving Successful")
    else:
        messagebox.showinfo(message="You haven't uploaded a watermark and/or an image.",
                            title="Can Not Save")


def font_color():
    global hex_code
    hex_code = colorchooser.askcolor()[1]
    image_label.config(foreground=hex_code)

def add_text():
    global thing
    dialog = CTkInputDialog(text="What is your Name?", title="Hello There!",
                                          fg_color="white",
                                          button_fg_color="red",
                                          button_hover_color="pink",
                                          button_text_color="black",
                                          entry_fg_color="green",
                                          entry_border_color="red",
                                          entry_text_color="black")
    thing = dialog.get_input()
    if thing:
        label_text.set(thing)
        image_label.config(text=thing, compound="center")
    else:
        image_label.config(text=f"You Forgot To Type Anything!", compound="center")


def delete():
    # text = label_text.get()
    # print(text)
    # print(type(text))
    image_label.config(text="")

def sliding(value):
    global font_size
    font_size = value



frame = CTkFrame(window, height=625, width=1000, border_width=5)
frame.grid(row=0, column=0)

im = Image.new(size=(620, 650), mode="RGBA", color="gray")
photo = ImageTk.PhotoImage(im)

label_text = StringVar()
image_label = Label(frame, image=photo, text="Hi", textvariable=label_text, font="courier 14 bold", compound="center", width=650, height=650)
image_label.grid(row=0, column=0, padx=10, pady=5, rowspan=6, columnspan=3, sticky="nw")





# Create a label and button
font_button = CTkButton(frame, text="Text Font", command=open_font)
font_button.grid(row=1, column=1)

font_color_button = CTkButton(frame, text="Font Color", command=font_color)
font_color_button.grid(row=1, column=2)


print(font_button.cget("bg_color"))

save_button = CTkButton(frame, text="Save", command=save )
save_button.grid(row=6, column=0, padx=250, pady=10, sticky="sw")

remove_button = CTkButton(frame, text="Delete", width=80, command=delete)
remove_button.grid(row=5, column=1, columnspan=1)

watermark_button = CTkButton(frame, text="Add Watermark", width=80)
watermark_button.grid(row=0, column=1, pady=20, ipadx=20,)

text_button = CTkButton(frame, text="Add Text", width=80, command=add_text)
text_button.grid(row=0, column=2, pady=10, padx=10, ipadx=35)


size_slider = CTkSlider(frame,
                        from_=0,
                        to=150,
                        command=sliding,
                        orientation="horizontal",
                        number_of_steps=10,
                        width=200,
                        # height=50,
                        fg_color="white",
                        progress_color="blue",
                        button_color="#2d74b5",
                        button_hover_color="",
                        state="normal",
                        hover=False)

size_slider.grid(row=2, column=2, columnspan=2, padx=20, sticky="w")
size_slider.set(0)

size_label = CTkLabel(frame, text="Text size:", font=("Helvetica", 16), bg_color='#2d74b5', width=80,
                      height=25)
size_label.grid(row=2, column=1)



my_label = CTkLabel(frame, text="Text Position", font=("Helvetica", 18))
my_label.grid(row=3, column=1, columnspan=2)

# Set the options for our combobox
positions = ["Top left", "Top center", "Top right", "Center", "Bottom left", "Bottom center", "Bottom right"]
# Create combobox
my_combo = CTkComboBox(frame, values=positions,
	height=40,
	width=300,
	font=("Helvetica", 18),
	dropdown_font=("Helvetica", 18),
	corner_radius=30,
	border_width=2,
	#border_color="red",
	#button_color="red",
	#dropdown_fg_color = "black",
	dropdown_text_color="white",
	text_color="white",
	hover=True,
	justify="center",
	state="normal")
my_combo.set("Center")
my_combo.grid(row=4, column=1, columnspan=2, sticky=N)



open_button = CTkButton(frame, text="Select Image", command=display_image)
open_button.grid(row=6, column=0, padx=100, pady=10, sticky="sw")




window.mainloop()
