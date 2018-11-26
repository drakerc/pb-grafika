from tkinter import *
from tkinter.filedialog import askopenfilename
import os
from PIL import Image, ImageTk
import time
import copy
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

        grayscale = Button(self.root, width=15, command=self.grayscale_prompt, text='Skala szarosci', height=2)
        grayscale.grid(row=2, column=0, sticky='N')

        grayscale_formula = Button(self.root, width=15, command=self.grayscale_prompt_formula, text='Skala szarosci wzor', height=2)
        grayscale_formula.grid(row=2, column=1, sticky='N')

        erosion = Button(self.root, width=15, command=self.erosion, text='Erozja', height=2)
        erosion.grid(row=3, column=0, sticky='N')

        dilatation = Button(self.root, width=15, command=self.dilatation, text='Dylatacja', height=2)
        dilatation.grid(row=3, column=1, sticky='N')

        opening = Button(self.root, width=15, command=self.opening, text='Otwarcie', height=2)
        opening.grid(row=3, column=2, sticky='N')

        closing = Button(self.root, width=15, command=self.closing, text='Domkniecie', height=2)
        closing.grid(row=3, column=3, sticky='N')

        self.w.grid(row=5, column=0, columnspan=4, rowspan=9, sticky=W+E+N+S)

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

    def get_filter_pixel(self, image, x, y, mode=0):
        try:
            return image.getpixel((x, y))
        except IndexError:
            if mode is 0:  # dilatation
                return 0, 0, 0
            else:
                return 255, 255, 255

    def scale_pixel(self, max, value):
        return round(255 / max * value)

    def erosion(self, multiple=False):
        # self.grayscale_prompt_formula()
        original_image = copy.deepcopy(self.image)

        for i in range(self.image.width):
            for j in range(self.image.height):
                top_left = self.get_filter_pixel(original_image, i-1, j-1, 1)
                top = self.get_filter_pixel(original_image, i, j-1, 1)
                top_right = self.get_filter_pixel(original_image, i+1, j-1, 1)

                center_left = self.get_filter_pixel(original_image, i-1, j, 1)
                center = self.get_filter_pixel(original_image, i, j, 1)
                center_right = self.get_filter_pixel(original_image, i+1, j, 1)

                bottom_left = self.get_filter_pixel(original_image, i-1, j+1, 1)
                bottom = self.get_filter_pixel(original_image, i, j+1, 1)
                bottom_right = self.get_filter_pixel(original_image, i+1, j+1, 1)

                all_points_list = [top_left, top, top_right, center_left, center, center_right, bottom_left, bottom, bottom_right]
                minimum = min(all_points_list)

                self.image.putpixel((i, j), (minimum[0], minimum[1], minimum[2]))

        if multiple is False:
            tkimage = ImageTk.PhotoImage(self.image)
            self.w.create_image(350, 350, image=tkimage)
            self.root.mainloop()

    def dilatation(self, multiple=False):
        # self.grayscale_prompt_formula()
        original_image = copy.deepcopy(self.image)

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

                all_points_list = [top_left, top, top_right, center_left, center, center_right, bottom_left, bottom, bottom_right]

                maximum = max(all_points_list)
                self.image.putpixel((i, j), (maximum[0], maximum[1], maximum[2]))

        if multiple is False:
            tkimage = ImageTk.PhotoImage(self.image)
            self.w.create_image(350, 350, image=tkimage)
            self.root.mainloop()

    def opening(self):
        self.erosion(True)
        self.dilatation(True)
        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()

    def closing(self):
        self.dilatation(True)
        self.erosion(True)
        tkimage = ImageTk.PhotoImage(self.image)
        self.w.create_image(350, 350, image=tkimage)
        self.root.mainloop()


Menu()
