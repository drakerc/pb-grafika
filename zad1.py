import math
from functools import partial
from tkinter import *


class Line:
    a_x = None
    a_y = None
    b_x = None
    b_y = None

    def __init__(self, a_x, a_y, b_x, b_y):
        self.a_x = a_x
        self.a_y = a_y
        self.b_x = b_x
        self.b_y = b_y

    def draw(self, canvas):
        canvas.create_line(self.a_x, self.a_y, self.b_x, self.b_y)


class Rectangle:
    a_x = None
    a_y = None
    d_x = None
    d_y = None

    def __init__(self, a_x, a_y, d_x, d_y):
        self.a_x = a_x
        self.a_y = a_y
        self.d_x = d_x
        self.d_y = d_y

    def draw(self, canvas):
        canvas.create_rectangle(self.a_x, self.a_y, self.d_x, self.d_y)


class Circle:
    a_x = None
    a_y = None
    r = None

    def __init__(self, a_x, a_y, r):
        self.a_x = a_x
        self.a_y = a_y
        self.r = r

    def draw(self, canvas):
        canvas.create_oval(self.a_x - self.r, self.a_y - self.r, self.a_x + self.r, self.a_y + self.r)


class Menu:
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

    mouse_circle_a = None
    mouse_circle_r = None

    lines = []
    rectangles = []
    circles = []

    def __init__(self):
        maincolor = '#0288d1'

        self.root.configure(bg=maincolor)
        self.root.title('Krzysztof Kosinski - program grafika komputerowa')
        self.root.minsize(width=800, height=600)

        line_prompted = Button(self.root, width=15, command=self.line_prompt, text='Linia - tekstowe', height=2)
        line_prompted.grid(row=0, column=1, sticky='N')

        rectangle_prompted = Button(self.root, width=15, command=self.rectangle_prompt, text='Prostokąt - tekstowe', height=2)
        rectangle_prompted.grid(row=1, column=1, sticky='N')

        circle_prompted = Button(self.root, width=15, command=self.circle_prompt, text='Okrąg - tekstowe', height=2)
        circle_prompted.grid(row=2, column=1, sticky='N')

        line_mouse = Button(self.root, width=15, command=self.line_mouse, text='Linia - mysz', height=2)
        line_mouse.grid(row=3, column=1, sticky='N', padx=10, pady=10)

        rectangle_mouse = Button(self.root, width=15, command=self.rectangle_mouse, text='Prostokąt - mysz', height=2)
        rectangle_mouse.grid(row=4, column=1, sticky='N', padx=10, pady=10)

        circle_mouse = Button(self.root, width=15, command=self.circle_mouse, text='Okrąg - mysz', height=2)
        circle_mouse.grid(row=5, column=1, sticky='N', padx=10, pady=10)

        self.w.grid(row=0, column=2, columnspan=2, rowspan=6, sticky=W+E+N+S)

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

        draw_line_button = Button(r, command=lambda: self.add_line(x_start_entry.get(), y_start_entry.get(), x_end_entry.get(), y_end_entry.get()), text='Rysuj')
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
            self.add_line(self.mouse_line_start['x'], self.mouse_line_start['y'], self.mouse_line_end['x'], self.mouse_line_end['y'])
            self.mouse_line_start = None
            self.mouse_line_end = None

    def add_line(self, x_start, y_start, x_end, y_end):
        line = Line(x_start, y_start, x_end, y_end)
        self.lines.append(line)
        line.draw(self.w)

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

        draw_button = Button(r, command=lambda: self.add_rectangle(a_x.get(), a_y.get(), d_x.get(), d_y.get()), text='Rysuj')
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
            self.add_rectangle(self.mouse_rectangle_a['x'], self.mouse_rectangle_a['y'], self.mouse_rectangle_d['x'], self.mouse_rectangle_d['y'])
            self.mouse_rectangle_a = None
            self.mouse_rectangle_d = None

    def add_rectangle(self, a_x, a_y, d_x, d_y):
        rectangle = Rectangle(a_x, a_y, d_x, d_y)
        self.rectangles.append(rectangle)
        rectangle.draw(self.w)

    def circle_prompt(self):
        r = Tk()
        r.title('Wprowadz dane')
        r.geometry('600x150')
        Label(r, text="A - wspołrzędna X").grid(column=1, row=0, sticky=W)
        Label(r, text="A - wspołrzędna Y").grid(column=3, row=0, sticky=W)
        Label(r, text="Promien").grid(column=1, row=1, sticky=W)

        a_x = Entry(r)
        a_y = Entry(r)
        radius = Entry(r)

        a_x.grid(row=0, column=2)
        a_y.grid(row=0, column=4)
        radius.grid(row=1, column=2)

        draw_button = Button(r, command=lambda: self.add_circle(a_x.get(), a_y.get(), radius.get()), text='Rysuj')
        draw_button.grid(columnspan=3, row=4, column=1, padx=10, pady=10)

    def circle_mouse(self):
        self.w.bind("<Button-1>", self.circle_clicked)

    def circle_clicked(self, event):
        if not self.mouse_circle_a:
            self.mouse_circle_a = {
                'x': event.x,
                'y': event.y
            }
        else:
            radius_distance = math.sqrt(((self.mouse_circle_a['x']-event.x)**2)+((self.mouse_circle_a['y']-event.y)**2))
            self.mouse_circle_r = radius_distance
            self.add_circle(self.mouse_circle_a['x'], self.mouse_circle_a['y'], self.mouse_circle_r)
            self.mouse_circle_a = None
            self.mouse_circle_r = None

    def add_circle(self, a_x, a_y, r):
        circle = Circle(int(a_x), int(a_y), int(r))
        self.rectangles.append(circle)
        circle.draw(self.w)


Menu()
