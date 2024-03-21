from sys import argv
from sys import exit
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from cv2 import GaussianBlur
from cv2 import Canny
from cv2 import split
from cv2 import equalizeHist
from cv2 import merge
from cv2 import threshold
from cv2 import bitwise_not
from cv2 import THRESH_BINARY
from cv2 import bitwise_and
from cv2 import cvtColor
from cv2 import COLOR_GRAY2BGR
from cv2 import add
from cv2 import imread
from numpy import zeros

def EdgeDetection(imgInput):
    # canny(): 边缘检测
    img1 = GaussianBlur(imgInput, (3, 3), 0)
    canny = Canny(img1, 50, 150)
    return canny

def HistogramEqualization(imgInput):
    (b, g, r) = split(imgInput)      # 通道分解
    bH = equalizeHist(b)
    gH = equalizeHist(g)
    rH = equalizeHist(r)
    result = merge((bH, gH, rH),)    # 通道合成
    return result
    
def add(img1, img2):
    rows, cols = img2.shape[:2]
    roi = img1[:rows, :cols]

    img2gray = img2
    ret, mask = threshold(img2gray, 10, 255, THRESH_BINARY)
    mask_inv = bitwise_not(mask)

    img1bg = bitwise_and(roi, roi, mask=mask_inv)
    img2 = cvtColor(img2, COLOR_GRAY2BGR)
    img2 = bitwise_and(img2, (0, 255, 0))
    dst = add(img1bg, img2)
    return dst

img = zeros((10, 10, 3),)
imgshow = img
 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
 
        self.setWindowTitle("OpenCV Image Viewer")
        self.resize(640, 500)
 
        self.button1 = QPushButton("打开图片", self)
        self.button1.clicked.connect(self.open_image)

        self.button2 = QPushButton("直方图均衡化", self)
        self.button2.clicked.connect(self.showHE)
        
        self.button3 = QPushButton("边缘检测", self)
        self.button3.clicked.connect(self.showED)

        self.button4 = QPushButton("显示原图", self)
        self.button4.clicked.connect(self.showOR)
 
        self.button1.setFixedHeight(50)
        self.button1.setFixedWidth(100)
        self.button2.setFixedHeight(50)
        self.button2.setFixedWidth(170)
        self.button3.setFixedHeight(50)
        self.button3.setFixedWidth(100)
        self.button4.setFixedHeight(50)
        self.button4.setFixedWidth(100)
        
        self.label = QLabel(self)
        self.label.setFixedSize(640, 480)
        self.label.setStyleSheet("border: 2px solid black; border-radius: 5px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
 
        layout = QGridLayout()
        layout.addWidget(self.button1, 0, 0, 1, 1)
        layout.addWidget(self.button2, 0, 1, 1, 1)
        layout.addWidget(self.button3, 0, 2, 1, 2)
        layout.addWidget(self.button4, 0, 3, 1, 1)
        layout.addWidget(self.label, 1, 0, 1, 5)
 
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
 
    def open_image(self):
        global img, imgshow
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", options=options)
        if file_name:
            img = imread(file_name)
            self.label.setFixedSize(img.shape[1], img.shape[0])
            # resHE = HistogramEqualization(img)
            # resED = add(img, EdgeDetection(img))
            imgshow = img

            if img is not None:
                height, width, channel = img.shape
                bytesPerLine = 3 * width
                qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
                self.label.setPixmap(QPixmap.fromImage(qImg))

    def showED(self):
        global imgshow
        imgshow = add(imgshow, EdgeDetection(imgshow))
        if imgshow is not None:
            height, width, channel = imgshow.shape
            bytesPerLine = 3 * width
            qImg = QImage(imgshow.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            self.label.setPixmap(QPixmap.fromImage(qImg))

    def showHE(self):
        global imgshow
        imgshow = HistogramEqualization(imgshow)
        if imgshow is not None:
            height, width, channel = imgshow.shape
            bytesPerLine = 3 * width
            qImg = QImage(imgshow.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            self.label.setPixmap(QPixmap.fromImage(qImg))

    def showOR(self):
        global imgshow
        imgshow = img
        if img is not None:
            height, width, channel = img.shape
            bytesPerLine = 3 * width
            qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            self.label.setPixmap(QPixmap.fromImage(qImg))
 
if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    exit(app.exec_())