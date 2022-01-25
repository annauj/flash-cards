from tkinter import *
import pandas
import random
import csv
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ---------------------------- GENERATE WORD ------------------------------- #
def next_card():
    global current_card, flip_timer, to_learn
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(image, image=card_front)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text =current_card["French"], fill="black")
    flip_timer = window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(image, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")

def remove():
    global current_card, to_learn
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index= False)
    next_card()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")

image = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 30, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

yes_image = PhotoImage(file="images/right.png")
no_image = PhotoImage(file="images/wrong.png")

yes_button = Button(image=yes_image, bd=0, compound="center", highlightthickness=0, command=remove)
yes_button.grid(column=0, row=1)

no_button = Button(image=no_image, bd=0, compound="center", highlightthickness=0, command=next_card)
no_button.grid(column=1, row=1)

next_card()


window.mainloop()