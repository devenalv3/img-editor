from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import ImageFilter, ImageEnhance
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)
from PIL import Image
import os
app = QApplication([])

#application window parameters
notes_win = QWidget()
notes_win.setWindowTitle('Easy Editor')
notes_win.resize(900, 600)

btn_folder = QPushButton("Folder")
btn_left = QPushButton("Left")
btn_bw = QPushButton("B&W")
btn_right = QPushButton("Right")
btn_mirror = QPushButton("Mirror")
btn_sharp = QPushButton("Sharpness")
btn_saturation = QPushButton("Saturation")
btn_brightness = QPushButton("Brightness")
btn_contrast = QPushButton("Contrast")
btn_blur = QPushButton("Blur")
btn_smooth = QPushButton("Smooth")
btn_undo = QPushButton("Undo")
btn_redo = QPushButton("Redo")
list_files = QListWidget()
img = QLabel("Image")

baris_btn = QHBoxLayout()
baris_btn.addWidget(btn_left)
baris_btn.addWidget(btn_right)
baris_btn.addWidget(btn_mirror)
baris_btn.addWidget(btn_bw)
baris_btn.addWidget(btn_sharp)
baris_2 = QHBoxLayout()
baris_2.addWidget(btn_saturation)
baris_2.addWidget(btn_contrast)
baris_2.addWidget(btn_blur)
baris_2.addWidget(btn_smooth)
baris_2.addWidget(btn_brightness)
baris_gbr = QHBoxLayout()
baris_gbr.addWidget(img)
kolom2 = QVBoxLayout()
kolom2.addLayout(baris_gbr)
kolom2.addLayout(baris_btn)
kolom2.addLayout(baris_2)
kolom1 = QVBoxLayout()
kolom1.addWidget(btn_folder)
kolom1.addWidget(list_files)
kolom1.addWidget(btn_undo)
kolom1.addWidget(btn_redo)

utama = QHBoxLayout()
utama.addLayout(kolom1, 20)
utama.addLayout(kolom2, 80)
notes_win.setLayout(utama)
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenameList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    list_files.clear()
    for filename in filenames:
        list_files.addItem(filename)
btn_folder.clicked.connect(showFilenameList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
        self.history = []
        self.redo_history = []

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    
    def showImage(self, path):
        img.hide()
        pixmapimage = QPixmap(path)
        w, h = img.width(), img.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        img.setPixmap(pixmapimage)
        img.show()

    def save_history(self):
        if self.image:
            self.history.append(self.image.copy())

            # Batasi history agar tidak terlalu banyak memori
            if len(self.history) > 20:
                self.history.pop(0)

            # Setiap edit baru, redo dibersihkan
            self.redo_history.clear()

    def do_bw(self):
        self.save_history()
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_sharp(self):
        self.save_history()
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_mirror(self):
        self.save_history()
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.save_history()
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.save_history()
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_saturation(self):
        self.save_history()
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(2.0)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_brightness(self):
        self.save_history()
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(1.5)   # 1 = normal
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_contrast(self):
        self.save_history()
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(1.8)   # 1 = normal
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_blur(self):
        self.save_history()
        self.image = self.image.filter(BLUR)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_smooth(self):
        self.save_history()
        self.image = self.image.filter(SMOOTH)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)

        self.image.save(fullname)

    def undo(self):
        if not self.history:
            return

        self.redo_history.append(self.image.copy())

        self.image = self.history.pop()

        self.saveImage()

        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def redo(self):
        if not self.redo_history:
            return

        self.history.append(self.image.copy())

        self.image = self.redo_history.pop()

        self.saveImage()

        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
workimage = ImageProcessor()
def showChosenImage():
    if list_files.currentRow() >= 0:
        filename = list_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)
list_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_sharp.clicked.connect(workimage.do_sharp)
btn_mirror.clicked.connect(workimage.do_mirror)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_saturation.clicked.connect(workimage.do_saturation)
btn_brightness.clicked.connect(workimage.do_brightness)
btn_contrast.clicked.connect(workimage.do_contrast)
btn_blur.clicked.connect(workimage.do_blur)
btn_smooth.clicked.connect(workimage.do_smooth)
btn_redo.clicked.connect(workimage.redo)
btn_undo.clicked.connect(workimage.undo)

notes_win.show()
app.exec()