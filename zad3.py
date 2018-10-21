from tkinter import *
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

class Menu:
    root = Tk()
    color_r = None
    color_g = None
    color_b = None

    color_c = None
    color_m = None
    color_y = None
    color_k = None

    def __init__(self):
        maincolor = '#ffffff'

        self.root.configure(bg=maincolor)
        self.root.title('Krzysztof Kosinski - program grafika komputerowa')
        self.root.minsize(width=400, height=400)

        # RGB
        Label(self.root, text="R (red)").grid(column=0, row=0, sticky=W)
        Label(self.root, text="G (green)").grid(column=0, row=1, sticky=W)
        Label(self.root, text="B (blue)").grid(column=0, row=2, sticky=W)

        self.color_r = Entry(self.root)
        self.color_g = Entry(self.root)
        self.color_b = Entry(self.root)

        self.color_r.grid(row=0, column=1)
        self.color_g.grid(row=1, column=1)
        self.color_b.grid(row=2, column=1)

        # CMYK
        Label(self.root, text="").grid(column=0, row=3, sticky=W)
        Label(self.root, text="C (cyan)").grid(column=0, row=4, sticky=W)
        Label(self.root, text="M (magenta)").grid(column=0, row=5, sticky=W)
        Label(self.root, text="Y (yellow)").grid(column=0, row=6, sticky=W)
        Label(self.root, text="K (black)").grid(column=0, row=7, sticky=W)

        self.color_c = Entry(self.root)
        self.color_m = Entry(self.root)
        self.color_y = Entry(self.root)
        self.color_k = Entry(self.root)

        self.color_c.grid(row=4, column=1)
        self.color_m.grid(row=5, column=1)
        self.color_y.grid(row=6, column=1)
        self.color_k.grid(row=7, column=1)

        color_picker = Button(self.root, command=self.color_picker, text='Wybor koloru od zera', height=2)
        color_picker.grid(row=8, column=0, sticky='N')

        color_picker = Button(self.root, command=lambda: self.color_picker('rgb'), text='Wybor koloru RGB', height=2)
        color_picker.grid(row=8, column=1, sticky='N')

        color_picker_cmyk = Button(self.root, command=lambda: self.color_picker('cmyk'), text='Wybor koloru CMYK', height=2)
        color_picker_cmyk.grid(row=8, column=3, sticky='N')

        # x_start_entry.insert(0, kwargs.get('x_start_value', ''))
        # y_start_entry.insert(0, kwargs.get('y_start_value', ''))
        # x_end_entry.insert(0, kwargs.get('x_end_value', ''))
        # y_end_entry.insert(0, kwargs.get('y_end_value', ''))

        self.root.mainloop()

    def show_error(self, message):
        r = Tk()
        r.configure(bg='#FF0000')
        r.title('Blad')
        r.geometry('350x50')
        rlbl = Label(r, text=message)
        rlbl.pack()
        return

    def cmyk_to_rgb(self, c, m, y, k):
        red = 1 - min(1, c*(1-k)+k)
        green = 1 - min(1, m*(1-k)+k)
        blue = 1 - min(1, y*(1-k)+k)
        return round(red), round(green), round(blue)

    def rgb_to_cmyk(self, r, g, b):
        k = min(1-r, 1-g, 1-b)  # black
        c = (1-r-k)/(1-k)
        m = (1-g-k)/(1-k)
        y = (1-b-k)/(1-k)
        return round(c, 3), round(m, 3), round(y, 3), round(k, 3)

    def color_picker(self, mode=None):
        color_picker_widget = Gtk.ColorSelectionDialog("Wybierz kolor")

        if mode is 'rgb':
            r = int(self.color_r.get())
            g = int(self.color_g.get())
            b = int(self.color_b.get())

            if r is '' or g is '' or b is '':
                self.show_error('Nie podales wartosci RGB.')
                return

            color_gdk_formatted = "#%02x%02x%02x" % (r, g, b)
            current_color = Gdk.color_parse(color_gdk_formatted)
            if current_color:
                color_picker_widget.get_color_selection().set_current_color(current_color)
            else:
                self.show_error('Nie udalo sie pobrac koloru, prawdopodobnie wprowadziles zle wartosci RGB')
                return

        if mode is 'cmyk':
            c = float(self.color_c.get())
            m = float(self.color_m.get())
            y = float(self.color_y.get())
            k = float(self.color_k.get())

            if c is '' or m is '' or y is '' or k is '':
                self.show_error('Nie podales wartosci CMYK.')
                return

            r, g, b = self.cmyk_to_rgb(c, m, y, k)
            color_gdk_formatted = "#%02x%02x%02x" % (r, g, b)
            current_color = Gdk.color_parse(color_gdk_formatted)
            if current_color:
                color_picker_widget.get_color_selection().set_current_color(current_color)
            else:
                self.show_error('Nie udalo sie pobrac koloru, prawdopodobnie wprowadziles zle wartosci RGB')
                return

        if color_picker_widget.run() != getattr(Gtk, 'RESPONSE_OK', Gtk.ResponseType.OK):
            print('Nie wybrales koloru')
            exit()

        color = color_picker_widget.get_color_selection().get_current_color()
        red = int(color.red / 256)
        green = int(color.green / 256)
        blue = int(color.blue / 256)

        self.color_r.delete(0, 'end')
        self.color_g.delete(0, 'end')
        self.color_b.delete(0, 'end')
        self.color_c.delete(0, 'end')
        self.color_m.delete(0, 'end')
        self.color_y.delete(0, 'end')
        self.color_k.delete(0, 'end')

        self.color_r.insert(0, red)
        self.color_g.insert(0, green)
        self.color_b.insert(0, blue)

        cyan, magenta, yellow, black = self.rgb_to_cmyk(red, green, blue)
        self.color_c.insert(0, cyan)
        self.color_m.insert(0, magenta)
        self.color_y.insert(0, yellow)
        self.color_k.insert(0, black)

        # color_picker_widget = None
        color_picker_widget.destroy()
        # Gtk.main()
        # Gdk.threads_leave()
        # self.root.mainloop()

        return



Menu()
