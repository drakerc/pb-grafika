from tkinter import *

canvas_width = 500
canvas_height = 150


class Menu():
    def __init__(self):
        maincolor = '#0288d1'
        global root
        root = Tk()
        root.configure(bg=maincolor)
        root.title('Krzysztof Kosinski - program grafika komputerowa')
        root.minsize(width=800, height=600)

        line = Button(root, width=15, command=1, text='Linia', height=2)
        line.grid(row=0, column=1, sticky='N', padx=10, pady=10)

        rectangle = Button(root, width=15, command=1, text='Prostokąt', height=2)
        rectangle.grid(row=1, column=1, sticky='N', padx=10, pady=10)

        circle = Button(root, width=15, command=1, text='Okrąg', height=2)
        circle.grid(row=2, column=1, sticky='N', padx=10, pady=10)

        w = Canvas(root,
                   width=700,
                   height=600,
                   background='#ffffff')

        w.grid(row=0, column=2, columnspan=2, rowspan=3, sticky=W+E+N+S)

        # w.pack(expand=YES, fill=BOTH)
        # w.bind("<B1-Motion>", paint)

        root.mainloop()


Menu()

# def paint(event):
#     python_green = "#476042"
#     x1, y1 = (event.x - 1), (event.y - 1)
#     x2, y2 = (event.x + 1), (event.y + 1)
#     w.create_oval(x1, y1, x2, y2, fill=python_green)
#
#
# master = Tk()
# master.title("Painting using Ovals")
# w = Canvas(master,
#            width=canvas_width,
#            height=canvas_height)
# w.pack(expand=YES, fill=BOTH)
# w.bind("<B1-Motion>", paint)
#
# message = Label(master, text="Press and Drag the mouse to draw")
# message.pack(side=BOTTOM)
#
# mainloop()
#
# print('x')