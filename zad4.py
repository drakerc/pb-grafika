from tkinter import *
from tkinter.filedialog import askopenfilename
import os
from PIL import Image, ImageTk
import time
import math


class PPM:
    header_read = False
    type = None  # 0 - P3, 1 - P6
    width = None
    height = None
    max_color = None
    pixel_spacing = None
    current_row = 0
    current_column = 0
    img = None
    pixels = None
    pixels_positions = None
    drawn_pixels = 0

    pixel_r = None
    pixel_g = None
    pixel_b = None

    def read_ppm(self, file):
        tmp_lines = file.read().splitlines()
        for index, value in enumerate(tmp_lines):
            if value.startswith('#') or value == '':
                continue
            value = value.split('#')[0]  # remove any comments that are not in the beginning
            if not self.header_read:
                self.read_header(value)
                continue

            # if self.type == 1:
            #     print('The P6/P3 header does not match its real type')
            #     exit()

            if self.img is None:
                self.img = Image.new('RGB', (self.width, self.height), "black")  # create a new black image
                self.pixels = self.img.load()  # create the pixel map

            self.read_pixels(value)

    def read_ppm_binary(self, file, chunk_size):
        while not self.header_read:
            value = file.readline().decode('Cp1250').splitlines()  # stupid but works
            value = value[0]
            if value.startswith('#') or value == '':
                continue
            value = value.split('#')[0]  # remove any comments that are not in the beginning
            self.read_header(value)

        if self.header_read:
            if self.type == 0:
                print('The P6/P3 header does not match its real type')
                exit()
            bytes_read = file.read(chunk_size)
            if self.img is None:
                self.img = Image.new('RGB', (self.width, self.height), "black")  # create a new black image
                self.pixels = self.img.load()  # create the pixel map
            while bytes_read:
                for b in bytes_read:
                    if self.img is None:
                        self.img = Image.new('RGB', (self.width, self.height), "black")  # create a new black image
                        self.pixels = self.img.load()  # create the pixel map
                    self.read_pixels(str(b))

                bytes_read = file.read(chunk_size)

    def read_header(self, value):
        line_elements = value.split()

        for element in line_elements:
            if self.type is None:
                if element == 'P3':
                    self.type = 0
                elif element == 'P6':
                    self.type = 1
                else:
                    print('Bad type (P3/P6)')
                    exit()
                continue
            if self.width is None:
                if not element.isdigit():
                    print('Bad width')
                    exit()
                self.width = int(element)
                continue
            if self.height is None:
                if not element.isdigit():
                    print('Bad height')
                    exit()
                self.height = int(element)
                continue
            if self.max_color is None:
                if not element.isdigit():
                    print('Bad max color')
                    exit()
                self.max_color = int(element)
                # continue
            if self.type is not None and self.width and self.height and self.max_color:
                self.header_read = True
                break
            else:
                print('Something is wrong with the header')
                exit()

    def scale_pixel(self, value):
        return round(255 / self.max_color * value)

    def read_pixels(self, value):
        line_elements = value.split()
        for element in line_elements:
            if element.startswith('#') or element == '':
                continue
            element = element.split('#')[0]  # remove any comments that are not in the beginning

            if self.pixel_r is None:
                if self.max_color != 255:
                    self.pixel_r = self.scale_pixel(int(element))
                else:
                    self.pixel_r = int(element)
                continue
            if self.pixel_g is None:
                if self.max_color != 255:
                    self.pixel_g = self.scale_pixel(int(element))
                else:
                    self.pixel_g = int(element)
                continue
            if self.pixel_b is None:
                if self.max_color != 255:
                    self.pixel_b = self.scale_pixel(int(element))
                else:
                    self.pixel_b = int(element)
                # continue
            if self.pixel_r is not None and self.pixel_g is not None and self.pixel_b is not None:
                if self.current_row == self.height:
                    continue
                self.pixels[self.current_column, self.current_row] = (self.pixel_r, self.pixel_g, self.pixel_b)
                self.drawn_pixels += 1
                self.pixel_r = None
                self.pixel_g = None
                self.pixel_b = None
                self.current_column += 1
                if self.current_column == self.width:
                    self.current_column = 0
                    self.current_row += 1
            else:
                continue

    def show_image(self):
        self.img.show()

    def get_image(self):
        return self.img

    def save_image(self):
        self.img.save('wyjscie.bmp')


class Menu:
    CHUNKSIZE = 10240
    root = Tk()
    w = Canvas(root,
               width=1000,
               height=1000,
               background='#ffffff')

    image = None

    def __init__(self):
        maincolor = '#ffffff'

        self.root.configure(bg=maincolor)
        self.root.title('Krzysztof Kosinski - program grafika komputerowa')
        self.root.minsize(width=800, height=600)

        load_ppm = Button(self.root, width=15, command=self.load_ppm, text='Wczytaj plik PPM', height=2)
        load_ppm.grid(row=0, column=0, sticky='N')

        load_jpg = Button(self.root, width=15, command=self.load_jpg, text='Wczytaj plik JPG', height=2)
        load_jpg.grid(row=0, column=1, sticky='N')

        save_jpg = Button(self.root, width=15, command=self.save_jpg_prompt, text='Zapisz plik JPG', height=2)
        save_jpg.grid(row=0, column=2, sticky='N')

        add_values = Button(self.root, width=15, command=self.add_values_prompt, text='Dodawanie', height=2)
        add_values.grid(row=0, column=3, sticky='N')

        remove_values = Button(self.root, width=15, command=self.remove_values_prompt, text='Odejmowanie', height=2)
        remove_values.grid(row=1, column=0, sticky='N')

        multiply_values = Button(self.root, width=15, command=self.multiply_values_prompt, text='Mnozenie', height=2)
        multiply_values.grid(row=1, column=1, sticky='N')

        divise_values = Button(self.root, width=15, command=self.divise_values_prompt, text='Dzielenie', height=2)
        divise_values.grid(row=1, column=2, sticky='N')

        change_brightness = Button(self.root, width=15, command=self.change_brightness_prompt, text='Zmien jasnosc', height=2)
        change_brightness.grid(row=1, column=3, sticky='N')

        grayscale = Button(self.root, width=15, command=self.grayscale_prompt, text='Skala szarosci', height=2)
        grayscale.grid(row=2, column=0, sticky='N')

        grayscale_formula = Button(self.root, width=15, command=self.grayscale_prompt_formula, text='Skala szarosci wzor', height=2)
        grayscale_formula.grid(row=2, column=1, sticky='N')

        averaging_filter = Button(self.root, width=15, command=self.averaging_filter, text='Filtr usredniajacy', height=2)
        averaging_filter.grid(row=2, column=2, sticky='N')

        median_filter = Button(self.root, width=15, command=self.median_filter, text='Filtr medianowy', height=2)
        median_filter.grid(row=2, column=3, sticky='N')

        sobel_filter = Button(self.root, width=15, command=self.sobel_filter, text='Filtr sobela', height=2)
        sobel_filter.grid(row=3, column=0, sticky='N')

        highpass_filter = Button(self.root, width=15, command=self.highpass_filter, text='Filtr\n gornoprzepustowy', height=2)
        highpass_filter.grid(row=3, column=1, sticky='N')

        gaussian_blur = Button(self.root, width=15, command=self.gaussian_blur, text='Rozmycie\n gaussowskie', height=2)
        gaussian_blur.grid(row=3, column=2, sticky='N')

        convolution = Button(self.root, width=15, command=self.convolution, text='Splot maski', height=2)
        convolution.grid(row=3, column=3, sticky='N')

        self.w.grid(row=4, column=0, columnspan=4, rowspan=9, sticky=W+E+N+S)

        self.root.mainloop()

    def resize_image(self, image):
        wpercent = (700 / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        if image.size[0] > 700 or image.size[1] > 700:
            return image.resize((700, hsize), Image.ANTIALIAS)
        return image

    def load_ppm(self):
        file = askopenfilename()
        start_time = time.time()

        filename, file_extension = os.path.splitext(file)
        if file_extension != '.ppm' and file_extension != '.pbm':
            print('Wrong file selected')
            exit()

        ppm_object = PPM()
        ppm_file = open(file, 'r', encoding='cp1250')

        try:
            ppm_object.read_ppm(ppm_file)
            ppm_file.close()

        except:
            ppm_file.close()
            file = open(file, "rb")
            ppm_object.read_ppm_binary(file, self.CHUNKSIZE)
            file.close()

        if ppm_object.drawn_pixels != ppm_object.width * ppm_object.height:
            print('Wrong amount of pixels drawn')
            exit()

        self.image = self.resize_image(ppm_object.get_image())
        print("--- %s seconds ---" % (time.time() - start_time))
        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()

    def load_jpg(self):
        file = askopenfilename()
        filename, file_extension = os.path.splitext(file)
        if file_extension != '.jpg' and file_extension != '.jpeg':
            print('Wrong file selected')
            exit()

        self.image = self.resize_image(Image.open(file))
        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()

    def save_jpg_prompt(self):
        if self.image is None:
            print('No images available!')
            return

        r = Tk()
        r.title('Wprowadz dane')
        r.geometry('300x150')
        Label(r, text="Kompresja").grid(column=1, row=0, sticky=W)
        Label(r, text="Nazwa pliku").grid(column=1, row=1, sticky=W)

        compression = Scale(r, from_=0, to=100, orient=HORIZONTAL)
        file_name = Entry(r)

        compression.set(90)
        file_name.insert(0, 'output.jpg')

        compression.grid(row=0, column=2)
        file_name.grid(row=1, column=2)

        save_button = Button(r, command=lambda: self.save_jpg(compression.get(), file_name.get()), text='Zapisz')
        save_button.grid(columnspan=4, row=2, column=1, padx=10, pady=10)

    def save_jpg(self, compression, file_name):
        self.image.save(file_name, quality=compression)
        r = Tk()
        r.configure(bg='#00ff00')
        r.title('Sukces')
        r.geometry('350x50')
        rlbl = Label(r, text='\nPomyslnie zapisano plik.',)
        rlbl.pack()

    def add_values_prompt(self):
        r = Tk()
        r.title('Wprowadz wartosc')
        r.geometry('600x150')

        Label(r, text="Wprowadz wartosc R").grid(column=1, row=0, sticky=W)
        add_value_r = Entry(r)
        add_value_r.insert(0, '0')
        add_value_r.grid(row=0, column=2)

        Label(r, text="Wprowadz wartosc G").grid(column=1, row=1, sticky=W)
        add_value_g = Entry(r)
        add_value_g.insert(0, '0')
        add_value_g.grid(row=1, column=2)

        Label(r, text="Wprowadz wartosc B").grid(column=1, row=2, sticky=W)
        add_value_b = Entry(r)
        add_value_b.insert(0, '0')
        add_value_b.grid(row=2, column=2)

        draw_button = Button(r, command=lambda: self.add_values(add_value_r.get(), add_value_g.get(), add_value_b.get()), text='Zrob to')
        draw_button.grid(columnspan=3, row=4, column=1, padx=10, pady=10)

    def add_values(self, r_value, g_value, b_value):
        for i in range(self.image.width):
            for j in range(self.image.height):
                r, g, b = self.image.getpixel((i, j))
                self.image.putpixel((i, j), (r+int(r_value), g+int(g_value), b+int(b_value)))

        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()

    def remove_values_prompt(self):
        r = Tk()
        r.title('Wprowadz wartosc')
        r.geometry('600x150')

        Label(r, text="Wprowadz wartosc R").grid(column=1, row=0, sticky=W)
        add_value_r = Entry(r)
        add_value_r.insert(0, '0')
        add_value_r.grid(row=0, column=2)

        Label(r, text="Wprowadz wartosc G").grid(column=1, row=1, sticky=W)
        add_value_g = Entry(r)
        add_value_g.insert(0, '0')
        add_value_g.grid(row=1, column=2)

        Label(r, text="Wprowadz wartosc B").grid(column=1, row=2, sticky=W)
        add_value_b = Entry(r)
        add_value_b.insert(0, '0')
        add_value_b.grid(row=2, column=2)

        draw_button = Button(r, command=lambda: self.remove_values(add_value_r.get(), add_value_g.get(), add_value_b.get()), text='Zrob to')
        draw_button.grid(columnspan=3, row=4, column=1, padx=10, pady=10)

    def remove_values(self, r_value, g_value, b_value):
        for i in range(self.image.width):
            for j in range(self.image.height):
                r, g, b = self.image.getpixel((i, j))
                self.image.putpixel((i, j), (r-int(r_value), g-int(g_value), b-int(b_value)))

        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()

    def multiply_values_prompt(self):
        r = Tk()
        r.title('Wprowadz wartosc')
        r.geometry('600x150')

        Label(r, text="Wprowadz wartosc R").grid(column=1, row=0, sticky=W)
        add_value_r = Entry(r)
        add_value_r.insert(0, '1')
        add_value_r.grid(row=0, column=2)

        Label(r, text="Wprowadz wartosc G").grid(column=1, row=1, sticky=W)
        add_value_g = Entry(r)
        add_value_g.insert(0, '1')
        add_value_g.grid(row=1, column=2)

        Label(r, text="Wprowadz wartosc B").grid(column=1, row=2, sticky=W)
        add_value_b = Entry(r)
        add_value_b.insert(0, '1')
        add_value_b.grid(row=2, column=2)

        draw_button = Button(r, command=lambda: self.multiply_values(add_value_r.get(), add_value_g.get(), add_value_b.get()), text='Zrob to')
        draw_button.grid(columnspan=3, row=4, column=1, padx=10, pady=10)

    def multiply_values(self, r_value, g_value, b_value):
        for i in range(self.image.width):
            for j in range(self.image.height):
                r, g, b = self.image.getpixel((i, j))
                self.image.putpixel((i, j), (r*int(r_value), g*int(g_value), b*int(b_value)))

        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()

    def divise_values_prompt(self):
        r = Tk()
        r.title('Wprowadz wartosc')
        r.geometry('600x150')

        Label(r, text="Wprowadz wartosc R").grid(column=1, row=0, sticky=W)
        add_value_r = Entry(r)
        add_value_r.insert(0, '1')
        add_value_r.grid(row=0, column=2)

        Label(r, text="Wprowadz wartosc G").grid(column=1, row=1, sticky=W)
        add_value_g = Entry(r)
        add_value_g.insert(0, '1')
        add_value_g.grid(row=1, column=2)

        Label(r, text="Wprowadz wartosc B").grid(column=1, row=2, sticky=W)
        add_value_b = Entry(r)
        add_value_b.insert(0, '1')
        add_value_b.grid(row=2, column=2)

        draw_button = Button(r, command=lambda: self.divise_values(add_value_r.get(), add_value_g.get(), add_value_b.get()), text='Zrob to')
        draw_button.grid(columnspan=3, row=4, column=1, padx=10, pady=10)

    def divise_values(self, r_value, g_value, b_value):
        for i in range(self.image.width):
            for j in range(self.image.height):
                r, g, b = self.image.getpixel((i, j))
                self.image.putpixel((i, j), (r/int(r_value), g/int(g_value), b/int(b_value)))

        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()

    def change_brightness_prompt(self):
        r = Tk()
        r.title('Wprowadz wartosc')
        r.geometry('600x150')

        Label(r, text="Wprowadz wartosc").grid(column=1, row=0, sticky=W)
        add_value_r = Entry(r)
        add_value_r.insert(0, '1')
        add_value_r.grid(row=0, column=2)

        draw_button = Button(r, command=lambda: self.change_brightness(add_value_r.get()), text='Zrob to')
        draw_button.grid(columnspan=3, row=4, column=1, padx=10, pady=10)

    def change_brightness(self, value):
        for i in range(self.image.width):
            for j in range(self.image.height):
                r, g, b = self.image.getpixel((i, j))
                self.image.putpixel((i, j), (r + int(value), g + int(value), b + int(value)))

        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()

    def grayscale_prompt(self):
        for i in range(self.image.width):
            for j in range(self.image.height):
                r, g, b = self.image.getpixel((i, j))
                average = int(r + g + b / 3)

                self.image.putpixel((i, j), (average, average, average))

        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()

    def grayscale_prompt_formula(self):
        for i in range(self.image.width):
            for j in range(self.image.height):
                r, g, b = self.image.getpixel((i, j))
                value = int(0.21 * r + 0.72 * g + 0.07 * b)

                self.image.putpixel((i, j), (value, value, value))

        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()

    def get_filter_pixel(self, image, x, y):
        try:
            # r, g, b = image.getpixel((x, y))
            return image.getpixel((x, y))
        except IndexError:
            return 0, 0, 0

    def averaging_filter(self):
        original_image = self.image
        for i in range(self.image.width):
            for j in range(self.image.height):
                top_left = self.get_filter_pixel(original_image, i-1, j-1)
                top = self.get_filter_pixel(original_image, i, j-1)
                top_right = self.get_filter_pixel(original_image, i+1, j-1)

                center_left = self.get_filter_pixel(original_image, i-1, j)
                center = self.get_filter_pixel(original_image, i, j)
                center_right = self.get_filter_pixel(original_image, i+1, j)

                bottom_left = self.get_filter_pixel(original_image, i-1, j+1)
                bottom = self.get_filter_pixel(original_image, i, j+1)
                bottom_right = self.get_filter_pixel(original_image, i+1, j+1)

                new_value_r = int((top_left[0] + top[0] + top_right[0] + center_left[0] + center[0] + center_right[0] + bottom_left[0] + bottom[0] + bottom_right[0]) / 9)
                new_value_g = int((top_left[1] + top[1] + top_right[1] + center_left[1] + center[1] + center_right[1] + bottom_left[1] + bottom[1] + bottom_right[1]) / 9)
                new_value_b = int((top_left[2] + top[2] + top_right[2] + center_left[2] + center[2] + center_right[2] + bottom_left[2] + bottom[2] + bottom_right[2]) / 9)

                self.image.putpixel((i, j), (new_value_r, new_value_g, new_value_b))

        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()

    def median_filter(self):
        original_image = self.image
        for i in range(self.image.width):
            for j in range(self.image.height):
                top_left = self.get_filter_pixel(original_image, i-1, j-1)
                top = self.get_filter_pixel(original_image, i, j-1)
                top_right = self.get_filter_pixel(original_image, i+1, j-1)

                center_left = self.get_filter_pixel(original_image, i-1, j)
                center = self.get_filter_pixel(original_image, i, j)
                center_right = self.get_filter_pixel(original_image, i+1, j)

                bottom_left = self.get_filter_pixel(original_image, i-1, j+1)
                bottom = self.get_filter_pixel(original_image, i, j+1)
                bottom_right = self.get_filter_pixel(original_image, i+1, j+1)

                values_array_r = [top_left[0], top[0], top_right[0], center_left[0], center[0], center_right[0], bottom_left[0], bottom[0], bottom_right[0]]
                values_array_g = [top_left[1], top[1], top_right[1], center_left[1], center[1], center_right[1], bottom_left[1], bottom[1], bottom_right[1]]
                values_array_b = [top_left[2], top[2], top_right[2], center_left[2], center[2], center_right[2], bottom_left[2], bottom[2], bottom_right[2]]

                values_array_r.sort()
                values_array_g.sort()
                values_array_b.sort()

                median_value_r = values_array_r[4]
                median_value_g = values_array_g[4]
                median_value_b = values_array_b[4]

                self.image.putpixel((i, j), (median_value_r, median_value_g, median_value_b))

        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()

    def scale_pixel(self, max, value):
        return round(255 / max * value)

    def sobel_filter(self):
        sobel_x = [[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]]

        sobel_y = [[-1, -2, -1],
                   [0, 0, 0],
                   [1, 2, 1]]

        original_image = self.image

        edges = []
        top_edge = 0

        for i in range(self.image.width):
            for j in range(self.image.height):
                top_left = self.get_filter_pixel(original_image, i-1, j-1)
                top = self.get_filter_pixel(original_image, i, j-1)
                top_right = self.get_filter_pixel(original_image, i+1, j-1)

                center_left = self.get_filter_pixel(original_image, i-1, j)
                center = self.get_filter_pixel(original_image, i, j)
                center_right = self.get_filter_pixel(original_image, i+1, j)

                bottom_left = self.get_filter_pixel(original_image, i-1, j+1)
                bottom = self.get_filter_pixel(original_image, i, j+1)
                bottom_right = self.get_filter_pixel(original_image, i+1, j+1)

                pixel_x = (sobel_x[0][0] * top_left[0]) + (sobel_x[0][1] * top[0]) + (sobel_x[0][2] * top_right[0]) + (sobel_x[1][0] * center_left[0]) + (sobel_x[1][1] * center[0]) + (sobel_x[1][2] * center_right[0]) + (sobel_x[2][0] * bottom_left[0]) + (sobel_x[2][1] * bottom[0]) + (sobel_x[2][2] * bottom_right[0])
                pixel_y = (sobel_y[0][0] * top_left[0]) + (sobel_y[0][1] * top[0]) + (sobel_y[0][2] * top_right[0]) + (sobel_y[1][0] * center_left[0]) + (sobel_y[1][1] * center[0]) + (sobel_y[1][2] * center_right[0]) + (sobel_y[2][0] * bottom_left[0]) + (sobel_y[2][1] * bottom[0]) + (sobel_y[2][2] * bottom_right[0])
                value = math.sqrt((pixel_x*pixel_x) + (pixel_y*pixel_y))
                value = int(value)

                edges.append({
                    'i': i,
                    'j': j,
                    'edge': value
                })

                if value > top_edge:
                    top_edge = value

        for edge in edges:
            value = self.scale_pixel(top_edge, edge['edge'])
            self.image.putpixel((edge['i'], edge['j']), (value, value, value))

        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()

    def highpass_filter(self):
        x = 1

    def gaussian_blur(self):
        x = 1

    def convolution(self):
        x = 1


Menu()
