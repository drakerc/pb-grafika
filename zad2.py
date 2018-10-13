from tkinter import *
from tkinter.filedialog import askopenfilename
import os
from PIL import Image
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

    def read_ppm(self, line, mode):
        for value in line:
            if value.startswith('#') or value == '':
                continue
            value = value.split('#')[0]  # remove any comments that are not in the beginning
            if not self.header_read:
                self.read_header(value)
                continue

            if self.img is None:
                self.img = Image.new('RGB', (self.width, self.height), "black")  # create a new black image
                self.pixels = self.img.load()  # create the pixel map

            self.read_pixels(value)

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
                continue
            # else:
            #     print('Something is wrong with the header')
            #     exit()

    def read_pixels(self, value):
        line_elements = value.split()
        for element in line_elements:
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
        self.img.save('fileee', 'BMP')
        # self.img.show()


class Menu:
    root = Tk()

    def __init__(self):
        maincolor = '#0288d1'

        self.root.configure(bg=maincolor)
        self.root.title('Krzysztof Kosinski - program grafika komputerowa')
        self.root.minsize(width=800, height=600)

        load_ppm = Button(self.root, width=15, command=self.load_ppm, text='Wczytaj plik PPM', height=2)
        load_ppm.grid(row=0, column=1, sticky='N')

        self.root.mainloop()

    def load_ppm(self):
        file = askopenfilename()
        start_time = time.time()

        filename, file_extension = os.path.splitext(file)
        if file_extension != '.ppm' and file_extension != '.pbm':
            print('Wrong file selected')
            exit()

        mode = 0  # 0 - r, 1 - rb

        ppm_object = PPM()


        ppm_file = open(file, 'r')
        try:
            tmp_lines = ppm_file.read().splitlines()
            while tmp_lines:
                ppm_object.read_ppm([line for line in tmp_lines], mode)
                tmp_lines = ppm_file.read(mode).splitlines()

            ppm_object.show_image()
            print("--- %s seconds ---" % (time.time() - start_time))
        except:
            ppm_file.close()
            CHUNKSIZE = 10240
            file = open(file, "rb")

            while not ppm_object.header_read:
                value = file.readline().decode('Cp1250').splitlines()  # stupid but works
                value = value[0]
                if value.startswith('#') or value == '':
                    continue
                value = value.split('#')[0]  # remove any comments that are not in the beginning
                ppm_object.read_header(value)

            if ppm_object.header_read:
                try:
                    bytes_read = file.read(CHUNKSIZE)
                    while bytes_read:
                        for b in bytes_read:
                            if ppm_object.img is None:
                                ppm_object.img = Image.new('RGB', (ppm_object.width, ppm_object.height),
                                                     "black")  # create a new black image
                                ppm_object.pixels = ppm_object.img.load()  # create the pixel map

                            ppm_object.read_pixels(str(b))

                        bytes_read = file.read(CHUNKSIZE)
                finally:
                    file.close()
                    ppm_object.show_image()
                    print("--- %s seconds ---" % (time.time() - start_time))





            #
            # mode = 1
            # ppm_file = open(file, 'rb')
            # tmp_lines = ppm_file.read()
            # while tmp_lines:
            #     ppm_object.read_ppm(tmp_lines, mode)
            #     tmp_lines = ppm_file.read(mode)


        # while tmp_lines:
        #     ppm_object.read_ppm([line for line in tmp_lines], mode)
        #     tmp_lines = ppm_file.read(mode).splitlines()
        #
        # ppm_object.show_image()
        # print("--- %s seconds ---" % (time.time() - start_time))


Menu()