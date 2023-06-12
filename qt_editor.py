import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PIL import Image

app = QApplication([])
window = QWidget()
window.resize(1000,500)
window.setWindowTitle('Qt Editor')

image_holder = QLabel('Image')


flip_btn = QPushButton('Flip')
thumb_btn = QPushButton('Thumbnail')
crop_btn = QPushButton('Crop')
baw_btn = QPushButton('B/W')
show_btn = QPushButton('See unmodificated image')
return_btn = QPushButton('Return to original')
tools_group = QGroupBox()

load_file_btn = QPushButton('Load file')
save_btn = QPushButton('Save image')
clear_btn = QPushButton('Clear')


m_layout = QHBoxLayout()
image_layout = QVBoxLayout()
tools_layout = QHBoxLayout()
file_layout = QVBoxLayout()

dialog_file_layout = QVBoxLayout()

dir_btn = QPushButton('Directory')
files_list = QListWidget()
conf_file_btn = QPushButton('Confirm')

dialog_file_layout.addWidget(dir_btn)
dialog_file_layout.addWidget(files_list)
dialog_file_layout.addWidget(conf_file_btn)


image_layout.addWidget(image_holder)

tools_layout.addWidget(flip_btn)
tools_layout.addWidget(thumb_btn)
tools_layout.addWidget(crop_btn)
tools_layout.addWidget(baw_btn)
tools_layout.addWidget(show_btn)
tools_layout.addWidget(return_btn)

file_layout.addWidget(load_file_btn)
file_layout.addWidget(save_btn)
file_layout.addWidget(clear_btn)

tools_v_layout = QVBoxLayout()
tools_group.setLayout(tools_layout)
m_layout.addLayout(image_layout,stretch = 40)
tools_v_layout.addWidget(tools_group)
tools_v_layout.setAlignment(Qt.AlignTop)
m_layout.addLayout(tools_v_layout,stretch = 0)
m_layout.addLayout(file_layout)
window.setLayout(m_layout)

graphical_extensions = ['.jpg','.png','.jpeg','.gif','.bmp']

homedir = os.getcwd()

savedir = 'Modifications/'

filedir = ''

workpath = os.path.join(homedir,savedir)

if not(os.path.exists(workpath) or os.path.isdir(workpath)):
    os.mkdir(workpath)


def chooseFiledir():
    global filedir
    filedir = ''
    filedir = QFileDialog.getExistingDirectory()

def filtration(files,extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenamesList():
    global filedir
    chooseFiledir()
    if filedir != '':
        filenames = filtration(os.listdir(filedir),graphical_extensions)
        files_list.clear()
        for filename in filenames:
            files_list.addItem(filename)

dir_btn.clicked.connect(showFilenamesList)

class ImageWorker():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.path = None
        self.original = None
    def check_image_availability(self):
        availability = self.image != None
        return availability
    def check_original_availability(self):
        availability = self.original != None
        return availability
    def loadImage(self,dir,filename):
        self.dir = dir
        self.filename = filename
        self.path = os.path.join(self.dir,self.filename)
        self.image = Image.open(self.path)
        self.original = self.image
    def show_image(self,path):
        image_holder.hide()
        pixmapimage = QPixmap(path)
        self.path = path
        w,h = image_holder.width(),image_holder.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        image_holder.setPixmap(pixmapimage)
        image_holder.show()
    def copy_image(self):
        self.path = os.path.join(workpath,self.filename)
        self.image.save(self.path)
    def do_baw(self):
        if self.check_image_availability == True:
            self.image = self.image.convert('L')
            self.save_image()
            self.show_image(self.path)
    def do_flip(self):
        if self.check_image_availability == True:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.save_image()
            self.show_image(self.path)
    def do_left(self):
        if self.check_image_availability == True:
            self.image = self.image.transpose(Image.ROTATE_90)
                self.save_image()
                self.show_image(self.path)
    def do_right(self):
        if self.check_image_availability == True:
            self.image = self.image.transpose(Image.ROTATE_270)
                self.save_image()
                self.show_image(self.path)
    #def do_crop(self):
        #if self.check_image_availability == True:
            #left_cor
            #up_cor
            #right_cor
            #down_cor
            #if right_cor>left and down_cor > up_cor:
                #new_crop = (left_cor,up_cor,right_cor,down_cor)
                #self.image = self.image.crop(new_crop)
                #self.save_image()
                #self.show_image(self.path)
    def do_thumbnail(self):
        if self.check_image_availability == True:
            n_width = text, ok = QInputDialog.getText(self, 'Input Dialog', "Enter image's new width:")
            n_height = text, ok = QInputDialog.getText(self, 'Input Dialog', "Enter image's new height:")
            if n_width > 0 and n_height > 0:
                new_size = (n_width,n_height)
                self.image = self.image.thumbnail(new_size)
                self.save_image()
                self.show_image(self.path)
    def show_image_in_other_window(self):
        if self.check_image_availability == True:
            self.image.show()
    def show_original(self):
        if self.check_original_availability == True:
            self.original.show()
    def save_image(self):
        if self.check_image_availability == True:
            self.image.save(self.path)
    def return_original(self):
        if self.check_original_availability == True:
            self.image = self.original
            self.save_image()
            self.show_image(self.path)
            
        

work_image = ImageWorker()

def showChosenImage():
    if files_list.currentRow() >= 0:
        filename = files_list.currentItem().text()
        work_image.loadImage(filedir,filename)
        image_path = os.path.join(work_image.dir,work_image.filename)
        work_image.show_image(image_path)

def loadFile():
    fdialog = QDialog()
    fdialog.resize(300,200)
    fdialog.setWindowTitle('File dialog')
    fdialog.setLayout(dialog_file_layout)
    fdialog.exec()

def copy_file():
    global fdialog
    if work_image.check_image_availability == True:
        work_image.copy_image()
        fdialog.done()



files_list.currentRowChanged.connect(showChosenImage)
load_file_btn.clicked.connect(loadFile)
conf_file_btn.clicked.connect(copy_file)
baw_btn.clicked.connect(work_image.do_baw)
flip_btn.clicked.connect(work_image.do_flip)
thumb_btn.clicked.connect(work_image.do_thumbnail)
show_btn.clicked.connect(work_image.show_original)
return_btn.clicked.connect(work_image.return_original)
save_btn.clicked.connect(work_image.save_image)



window.show()
app.exec()