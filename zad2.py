from tkinter import *
from tkinter.filedialog import askopenfilename
import os
from PIL import Image, ImageTk
import time


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

    pixel_r = None
    pixel_g = None
    pixel_b = None

    def read_ppm(self, line):
        for value in line:
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

            self.read_pixels(value, )

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
                self.img = Image.new('RGB', (self.width, self.height),
                                     "black")  # create a new black image
                self.pixels = self.img.load()  # create the pixel map
            while bytes_read:
                for b in bytes_read:
                    if self.img is None:
                        self.img = Image.new('RGB', (self.width, self.height),
                                                   "black")  # create a new black image
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
                continue
            if self.width is None:
                self.width = int(element)
                continue
            if self.height is None:
                self.height = int(element)
                continue
            if self.max_color is None:
                self.max_color = int(element)
                # continue
            if self.type is not None and self.width and self.height and self.max_color:
                self.header_read = True
                break
            else:
                print('Something is wrong with the header')
                exit()

    def read_pixels(self, value):
        line_elements = value.split()
        for element in line_elements:
            if element.startswith('#') or element == '':
                continue
            element = element.split('#')[0]  # remove any comments that are not in the beginning

            if self.pixel_r is None:
                self.pixel_r = int(element)
                continue
            if self.pixel_g is None:
                self.pixel_g = int(element)
                continue
            if self.pixel_b is None:
                self.pixel_b = int(element)
                # continue
            if self.pixel_r is not None and self.pixel_g is not None and self.pixel_b is not None:
                if self.current_row == self.height:
                    continue
                self.pixels[self.current_column, self.current_row] = (self.pixel_r, self.pixel_g, self.pixel_b)
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


class Menu:
    CHUNKSIZE = 1024000
    root = Tk()
    w = Canvas(root,
               width=700,
               height=700,
               background='#ffffff')

    image = None

    def __init__(self):
        maincolor = '#0288d1'

        self.root.configure(bg=maincolor)
        self.root.title('Krzysztof Kosinski - program grafika komputerowa')
        self.root.minsize(width=800, height=600)

        load_ppm = Button(self.root, width=15, command=self.load_ppm, text='Wczytaj plik PPM', height=2)
        load_ppm.grid(row=0, column=1, sticky='N')

        load_jpg= Button(self.root, width=15, command=self.load_jpg, text='Wczytaj plik JPG', height=2)
        load_jpg.grid(row=1, column=1, sticky='N')

        save_jpg= Button(self.root, width=15, command=self.save_jpg_prompt, text='Zapisz plik JPG', height=2)
        save_jpg.grid(row=2, column=1, sticky='N')

        self.w.grid(row=0, column=2, columnspan=2, rowspan=9, sticky=W+E+N+S)

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
            tmp_lines = ppm_file.read().splitlines()
            while tmp_lines:
                ppm_object.read_ppm([line for line in tmp_lines])
                tmp_lines = ppm_file.read().splitlines()
            ppm_file.close()

        except:
            ppm_file.close()
            file = open(file, "rb")
            ppm_object.read_ppm_binary(file, self.CHUNKSIZE)
            file.close()

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
        r.geometry('600x300')
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


Menu()
