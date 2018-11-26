import math
from tkinter import *
from scipy.spatial import distance

class Menu:
    root = Tk()
    w = Canvas(root,
               width=700,
               height=700,
               background='#ffffff')

    mode = 'none'
    mouse_line_start = None
    mouse_line_end = None

    mouse_rectangle_a = None
    mouse_rectangle_d = None

    mouse_circle_a = None
    mouse_circle_r = None

    mouse_move_selected_object = None
    mouse_move_selected_end_position = None

    control_points = []

    def __init__(self):
        maincolor = '#0288d1'

        self.root.configure(bg=maincolor)
        self.root.title('Krzysztof Kosinski - program grafika komputerowa')
        self.root.minsize(width=800, height=600)

        create_point_text = Button(self.root, width=15, command=self.add_point_prompt, text='Tworz - tekstowe', height=2)
        create_point_text.grid(row=0, column=1, sticky='N')

        edit_point_text = Button(self.root, width=15, command=self.edit_point_prompt, text='Edytuj - tekstowe', height=2)
        edit_point_text.grid(row=1, column=1, sticky='N')

        create_point_mouse = Button(self.root, width=15, command=self.add_point_mouse, text='Tworz - mysz', height=2)
        create_point_mouse.grid(row=5, column=1, sticky='N', padx=10, pady=10)

        create_point_text = Button(self.root, width=15, command=self.move_mouse, text='Edytuj - mysz', height=2)
        create_point_text.grid(row=6, column=1, sticky='N', padx=10, pady=10)

        self.w.grid(row=0, column=2, columnspan=2, rowspan=9, sticky=W+E+N+S)

        self.root.mainloop()

    def add_point_prompt_elements(self, **kwargs):
        r = Tk()
        r.title('Wprowadz dane')
        r.geometry('600x150')
        Label(r, text="X").grid(column=1, row=0, sticky=W)
        Label(r, text="Y").grid(column=1, row=1, sticky=W)

        x_start_entry = Entry(r)
        y_start_entry = Entry(r)

        x_start_entry.insert(0, kwargs.get('x_start_value', ''))
        y_start_entry.insert(0, kwargs.get('y_start_value', ''))

        x_start_entry.grid(row=0, column=2)
        y_start_entry.grid(row=1, column=2)

        return r, x_start_entry, y_start_entry

    def add_point_prompt(self):
        r, x_start_entry, y_start_entry = self.add_point_prompt_elements()

        draw_line_button = Button(r, command=lambda: self.add_control_point(x_start_entry.get(), y_start_entry.get()), text='Dodaj')
        draw_line_button.grid(columnspan=4, row=2, column=1, padx=10, pady=10)

    def add_point_mouse(self):
        self.w.unbind("<B1-Motion>")
        self.w.unbind('<ButtonRelease-1>')
        self.w.bind("<Button-1>", self.add_point_clicked)


    def edit_point_prompt(self):
        self.w.unbind("<B1-Motion>")
        self.w.unbind('<ButtonRelease-1>')
        self.w.bind("<Button-1>", self.edit_point_clicked)

    def edit_point_clicked(self, event):
        self.mouse_move_selected_object = self.get_closest_primitive(event.x, event.y)
        r = Tk()
        r.title('Wprowadz dane')
        r.geometry('600x150')
        Label(r, text="X").grid(column=1, row=0, sticky=W)
        Label(r, text="Y").grid(column=1, row=1, sticky=W)

        x_start_entry = Entry(r)
        y_start_entry = Entry(r)

        x_start_entry.insert(0, self.control_points[self.mouse_move_selected_object][0])
        y_start_entry.insert(0, self.control_points[self.mouse_move_selected_object][1])

        x_start_entry.grid(row=0, column=2)
        y_start_entry.grid(row=1, column=2)

        draw_line_button = Button(r, command=lambda: self.edit_clicked_point(x_start_entry.get(), y_start_entry.get()), text='Zedytuj')
        draw_line_button.grid(columnspan=4, row=2, column=1, padx=10, pady=10)

    def edit_clicked_point(self, x, y):
        self.control_points[self.mouse_move_selected_object] = (int(x), int(y))
        self.draw_bezier_curve()

    def add_point_clicked(self, event):
        self.add_control_point(event.x, event.y)

    def add_control_point(self, x, y):
        self.control_points.append((int(x), int(y)))
        self.draw_bezier_curve()

    def draw_bezier_curve(self):
        steps = 1000

        self.w.delete('all')

        current_point = self.control_points[0]

        self.w.create_oval(current_point[0], current_point[1], current_point[0] + 5, current_point[1] + 5)

        for point in get_bezier_curve_points(steps, self.control_points):
            self.w.create_line(current_point[0], current_point[1], point[0], point[1])
            current_point = point

        for index, point in enumerate(self.control_points):
            self.w.create_oval(point[0], point[1], point[0] + 5, point[1] + 5)
            self.w.create_text(point[0]+15, point[1]+15, text=index+1)

    def move_mouse(self):
        self.w.unbind("<B1-Motion>")
        self.w.unbind('<ButtonRelease-1>')
        self.w.unbind("<Button-1>")

        self.w.bind("<B1-Motion>", self.move_mouse_held)
        self.w.bind('<ButtonRelease-1>', self.move_mouse_released)

    def move_mouse_held(self, event):
        if not self.mouse_move_selected_object:
            self.mouse_move_selected_object = self.get_closest_primitive(event.x, event.y)
        else:
            self.control_points[self.mouse_move_selected_object] = (event.x, event.y)
            self.draw_bezier_curve()

    def move_mouse_released(self, event):
        self.mouse_move_selected_object = None
        # self.w.unbind("<B1-Motion>")

    def closest_point(self, point, points):
        closest_index = distance.cdist([point], points).argmin()
        return closest_index

    def get_closest_primitive(self, clicked_point_x, clicked_point_y):
        points = []
        for index, value in enumerate(self.control_points):
            points.append({'id': index, 'x': value[0], 'y': value[1]})

        point_coordinates = []
        for value in points:
            point_coordinates.append((value['x'], value['y']))

        closest_point_index = self.closest_point((clicked_point_x, clicked_point_y), point_coordinates)

        return closest_point_index

def calculate_binomial(i, n):
    return math.factorial(n) / float(math.factorial(i) * math.factorial(n - i))


def calculate_bernstein(t, i, n):
    return calculate_binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))


def bezier(t, points):
    n = len(points) - 1
    x = y = 0
    for i, pos in enumerate(points):
        bernstein = calculate_bernstein(t, i, n)
        x += pos[0] * bernstein
        y += pos[1] * bernstein

    return x, y


def get_bezier_curve_points(n, points):
    for i in range(n):
        t = i / float(n - 1)
        yield bezier(t, points)


Menu()