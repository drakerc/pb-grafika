from functools import partial
from tkinter import *

class Menu():
    root = Tk()
    w = Canvas(root,
               width=700,
               height=600,
               background='#ffffff')

    mode = 'none'
    mouse_line_start = None
    mouse_line_end = None

    mouse_rectangle_a = None
    mouse_rectangle_d = None

    def __init__(self):
        maincolor = '#0288d1'

        self.root.configure(bg=maincolor)
        self.root.title('Krzysztof Kosinski - program grafika komputerowa')
        self.root.minsize(width=800, height=600)

        line_prompted = Button(self.root, width=15, command=self.line_prompt, text='Linia - tekstowe', height=2)
        line_prompted.grid(row=0, column=1, sticky='N')

        rectangle_prompted = Button(self.root, width=15, command=self.rectangle_prompt, text='Prostokąt - tekstowe', height=2)
        rectangle_prompted.grid(row=1, column=1, sticky='N')

        circle_prompted = Button(self.root, width=15, command=1, text='Okrąg - tekstowe', height=2)
        circle_prompted.grid(row=2, column=1, sticky='N')

        line_mouse = Button(self.root, width=15, command=self.line_mouse, text='Linia - mysz', height=2)
        line_mouse.grid(row=3, column=1, sticky='N', padx=10, pady=10)

        rectangle_mouse = Button(self.root, width=15, command=self.rectangle_mouse, text='Prostokąt - mysz', height=2)
        rectangle_mouse.grid(row=4, column=1, sticky='N', padx=10, pady=10)

        circle_mouse = Button(self.root, width=15, command=1, text='Okrąg - mysz', height=2)
        circle_mouse.grid(row=5, column=1, sticky='N', padx=10, pady=10)


        # paint = Button(self.root, width=15, command=self.paint, text='Rysowanko', height=2)
        # paint.grid(row=2, column=1, sticky='N', padx=10, pady=10)

        self.w.grid(row=0, column=2, columnspan=2, rowspan=3, sticky=W+E+N+S)

        self.root.mainloop()

    def line_prompt(self):
        r = Tk()
        r.title('Wprowadz dane')
        r.geometry('600x150')
        Label(r, text="X poczatkowe").grid(column=1, row=0, sticky=W)
        Label(r, text="Y poczatkowe").grid(column=1, row=1, sticky=W)
        Label(r, text="X koncowe").grid(column=3, row=0, sticky=W)
        Label(r, text="Y koncowe").grid(column=3, row=1, sticky=W)

        x_start_entry = Entry(r)
        y_start_entry = Entry(r)
        x_end_entry = Entry(r)
        y_end_entry = Entry(r)

        x_start_entry.grid(row=0, column=2)
        y_start_entry.grid(row=1, column=2)
        x_end_entry.grid(row=0, column=4)
        y_end_entry.grid(row=1, column=4)

        draw_line_button = Button(r, command=lambda: self.line(x_start_entry.get(), y_start_entry.get(), x_end_entry.get(), y_end_entry.get()), text='Rysuj')
        draw_line_button.grid(columnspan=4, row=2, column=1, padx=10, pady=10)

    def line_mouse(self):
        self.w.bind("<Button-1>", self.line_mouse_clicked)

    def line_mouse_clicked(self, event):
        if not self.mouse_line_start:
            self.mouse_line_start = {
                'x': event.x,
                'y': event.y
            }
        else:
            self.mouse_line_end = {
                'x': event.x,
                'y': event.y
            }
            self.line(self.mouse_line_start['x'], self.mouse_line_start['y'], self.mouse_line_end['x'], self.mouse_line_end['y'])
            self.mouse_line_start = None
            self.mouse_line_end = None

    def line(self, x_start, y_start, x_end, y_end):
        self.w.create_line(x_start, y_start, x_end, y_end)

    def rectangle_prompt(self):
        r = Tk()
        r.title('Wprowadz dane')
        r.geometry('600x150')
        Label(r, text="A - wspołrzędna X").grid(column=1, row=0, sticky=W)
        Label(r, text="A - wspołrzędna Y").grid(column=3, row=0, sticky=W)
        Label(r, text="D - wspołrzędna X").grid(column=1, row=1, sticky=W)
        Label(r, text="D - wspołrzędna Y").grid(column=3, row=1, sticky=W)

        a_x = Entry(r)
        a_y = Entry(r)
        d_x = Entry(r)
        d_y = Entry(r)

        a_x.grid(row=0, column=2)
        a_y.grid(row=0, column=4)
        d_x.grid(row=1, column=2)
        d_y.grid(row=1, column=4)

        draw_button = Button(r, command=lambda: self.rectangle(a_x.get(), a_y.get(), d_x.get(), d_y.get()), text='Rysuj')
        draw_button.grid(columnspan=3, row=4, column=1, padx=10, pady=10)

    def rectangle_mouse(self):
        self.w.bind("<Button-1>", self.rectangle_clicked)

    def rectangle_clicked(self, event):
        if not self.mouse_rectangle_a:
            self.mouse_rectangle_a = {
                'x': event.x,
                'y': event.y
            }
        else:
            self.mouse_rectangle_d = {
                'x': event.x,
                'y': event.y
            }
            self.rectangle(self.mouse_rectangle_a['x'], self.mouse_rectangle_a['y'], self.mouse_rectangle_d['x'], self.mouse_rectangle_d['y'])
            self.mouse_rectangle_a = None
            self.mouse_rectangle_d = None

    def rectangle(self, a_x, a_y, d_x, d_y):
        self.w.create_rectangle(a_x, a_y, d_x, d_y)


    def paint(self):
        if self.mode is not 'line':
            self.w.bind("<B1-Motion>", self.start_paint)
            self.mode = 'line'
        else:
            self.w.unbind("<B1-Motion>")
            self.mode = 'none'


    def start_paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.w.create_oval(x1, y1, x2, y2, fill='#000000')


Menu()