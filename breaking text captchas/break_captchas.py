



from tkinter import *
from PIL import Image, ImageTk



def makeform(root):
    entries = {}
    row = Frame(root)
    lab = Label(row, width=22, text="Enter text: ", anchor='w')
    ent = Entry(row)
    ent.insert(0,"0")
    row.pack(side=TOP, fill=X, padx=5 , pady=5)
    lab.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    entries["Enter text"] = ent
    return entries


def submit(entries):
    answer = str(entries["Enter text"].get())
    print(answer)
    print("Heyy")


#if __name__ == '__main__':
photo1 = "test_captchas/2A5Z.png"
photo2 = "test_captchas/2AD9.png"

root = Tk()
root.title("Are you a robot?")

root.photo1 = ImageTk.PhotoImage(Image.open(photo1))
root.photo2 = ImageTk.PhotoImage(Image.open(photo2))
vlabel = Label(root,image=root.photo1)
vlabel.pack()

#root.geometry("400x400")
ents = makeform(root)
#root.bind('<Return>', (lambda event, e = ents: fetch(e)))
b1 = Button(root, text = 'submit', command=(lambda e = ents: submit(e)))
b1.pack(side = LEFT, padx = 5, pady = 5)
b3 = Button(root, text = 'Quit', command = root.quit)
b3.pack(side = LEFT, padx = 5, pady = 5)
root.mainloop()



#
