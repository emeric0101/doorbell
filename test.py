from tkinter import *

class Timer:
    def __init__(self, parent, canvas, image):
        # variable storing time
        self.seconds = 0
        # label displaying time
        # start the timer
        self.parent = parent
        self.canvas = canvas
        self.image = image
        self.serverimage = None
        self.image1 = PhotoImage(file="blue_pops.png")
        self.image2 = PhotoImage(file="green_pops.png")
        self.render1 = self.canvas.create_image(0, 0, anchor=NW, image=self.image1)
        self.render2 = self.canvas.create_image(0, 0, anchor=NW, image=self.image2)
        self.number_image = 0
        self.img = PhotoImage(file="test.png")
        self.render3 = self.canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.parent.after(1000, self.refresh_label)

    def refresh_label(self):
        if self.number_image == 0:
            self.canvas.create_image(0, 0, anchor=NW, image=self.image1)
            self.number_image = 1
        elif self.number_image == 1:
            self.canvas.create_image(0, 0, anchor=NW, image=self.image2)
            self.number_image = 2
        elif self.number_image == 2:
            self.canvas.create_image(0, 0, anchor=NW, image=self.img)
            self.number_image = 0
        self.parent.after(200, self.refresh_label)


root = Tk()
canvas = Canvas(root, width=628, height=628)
canvas.pack()
root.resizable(0, 0)
img = PhotoImage(file="test.png")
render = canvas.create_image(0, 0, anchor=NW, image=img)
timer = Timer(root, canvas, render)
root.wm_title("Miel Pops")
root.mainloop()

