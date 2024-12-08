import random
import sys

import cv2
import qrcode
from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtCore, QtGui, QtWidgets

PUSH_BUTTON_STYLE = """
QPushButton{
    border:3px solid black;
    border-radius:15px;
    background:blue;
    color:white;
}
QPushButton:hover{
    border:1px solid gray;
    border-radius:15px;
    background:black;
    color:white;
}
"""

LINE_EDIT_STYLE = """
QLineEdit{
    background:white;
}
"""

class UiForm(object):
    """
    UI class responsible for setting up the form
    and handling widget interactions.
    """
    def setup_ui(self, form: QtWidgets.QWidget) -> None:
        """
        Set up the UI components and layout of the form.

        Args:
            form (QtWidgets.QWidget): The form widget where the UI is set up.
        """
        form.setObjectName("form")
        form.resize(799, 594)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        form.setFont(font)
        form.setStyleSheet("QWidget{\n"
                           "background:rgb(85, 170, 255);\n"
                           "\n"
                           "}")
        self.pushButton = QtWidgets.QPushButton(form)
        self.pushButton.setGeometry(QtCore.QRect(460, 30, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.clicked.connect(self.capture)
        self.pushButton.setStyleSheet(PUSH_BUTTON_STYLE)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(form)
        self.label.setGeometry(QtCore.QRect(190, 30, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(form)
        self.label_2.setGeometry(QtCore.QRect(70, 150, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(form)
        self.label_3.setGeometry(QtCore.QRect(70, 230, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(form)
        self.label_4.setGeometry(QtCore.QRect(70, 310, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(form)
        self.label_5.setGeometry(QtCore.QRect(70, 390, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(form)
        self.label_6.setGeometry(QtCore.QRect(70, 490, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lineEdit = QtWidgets.QLineEdit(form)
        self.lineEdit.setGeometry(QtCore.QRect(360, 140, 381, 31))
        self.lineEdit.setStyleSheet(LINE_EDIT_STYLE)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(form)
        self.lineEdit_2.setGeometry(QtCore.QRect(360, 220, 381, 31))
        self.lineEdit_2.setStyleSheet(LINE_EDIT_STYLE)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(form)
        self.lineEdit_3.setGeometry(QtCore.QRect(360, 300, 381, 31))
        self.lineEdit_3.setStyleSheet(LINE_EDIT_STYLE)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(form)
        self.lineEdit_4.setGeometry(QtCore.QRect(360, 390, 381, 31))
        self.lineEdit_4.setStyleSheet(LINE_EDIT_STYLE)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(form)
        self.lineEdit_5.setGeometry(QtCore.QRect(360, 480, 381, 31))
        self.lineEdit_5.setStyleSheet(LINE_EDIT_STYLE)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_2 = QtWidgets.QPushButton(form)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 540, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.clicked.connect(self.generate_idcard)
        self.pushButton_2.setStyleSheet(PUSH_BUTTON_STYLE)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslate_ui(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def capture(self) -> None:
        """
        Capture an image using the webcam, crop it,
        and save it as 'person.jpg'.
        """
        camera = cv2.VideoCapture(0)
        while True:
            _, image = camera.read()
            image = cv2.flip(image, 1)
            cv2.imshow('image', image)
            if cv2.waitKey(1) == 13:
                height, width = image.shape[:2]
                start_row, start_col = int(height*.25), int(width*.25)
                end_row, end_col = int(height*.80), int(width*.80)
                cropped_img = image[start_row:end_row, start_col:end_col]
                cv2.imwrite('person.jpg', cropped_img)
                break
        camera.release()
        cv2.destroyAllWindows()

    def generate_idcard(self) -> None:
        """
        Generate an ID card image using the input data and webcam photo.
        This includes adding text, QR code, and saving the final card.
        """
        # Generating Blank White Image
        image = Image.new('RGB', (1000, 900), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('arial.ttf', size=45)

        (x, y) = (50, 50)
        message = self.lineEdit.text()
        company = message
        color = 'rgb(0, 0, 0)'
        font = ImageFont.truetype('arial.ttf', size=80)
        draw.text((x, y), message, fill=color, font=font)

        # generating ID NO randomly You can also ask user to enter
        (x, y) = (50, 350)
        id_no = random.randint(1000000, 9000000)
        message = str('ID ' + str(id_no))
        font = ImageFont.truetype('arial.ttf', size=60)
        color = 'rgb(255, 0, 0)'  # color
        draw.text((x, y), message, fill=color, font=font)

        # Asking user Full name
        (x, y) = (50, 250)
        message = self.lineEdit_2.text()
        name = message
        color = 'rgb(0, 0, 0)'  # black color
        font = ImageFont.truetype('arial.ttf', size=45)
        draw.text((x, y), message, fill=color, font=font)

        # Asking about user gender
        (x, y) = (50, 550)
        message = self.lineEdit_3.text()
        color = 'rgb(0, 0, 0)'  # black color
        draw.text((x, y), message, fill=color, font=font)

        # Asking User about his phone number
        (x, y) = (50, 650)
        message = self.lineEdit_5.text()
        color = 'rgb(0, 0, 0)'  # black color
        draw.text((x, y), message, fill=color, font=font)

        # Asking user about his Adress
        (x, y) = (50, 750)
        message = self.lineEdit_4.text()
        color = 'rgb(0, 0, 0)'  # black color
        draw.text((x, y), message, fill=color, font=font)

        # save the edited image
        image.save(str(name) + '.png')

        # pasting person image taken by camera on card image
        card_image = Image.open(name + '.png')
        person_image = Image.open('person.jpg', 'r')
        card_image.paste(person_image, (600, 75))
        card_image.save("card.jpg")
        # this info. is added in QR code, also add other things
        img = qrcode.make(str(company) + str(id_no))
        img.save(str(id_no) + '.bmp')

        til = Image.open('card.jpg')
        im = Image.open(str(id_no) + '.bmp')  # 25x25
        til.paste(im, (600, 400))
        til.save(name + '.png')
        self.hide()

    def retranslate_ui(self, form: QtWidgets.QWidget) -> None:
        """
        Retranslate the UI to apply the text to the widgets.

        Args:
            form (QtWidgets.QWidget): The form widget to update the text for.
        """
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "form"))
        self.pushButton.setText(_translate("form", "Capture Image"))
        self.label.setText(_translate("form", "Capture Your Image "))
        self.label_2.setText(_translate("form", "Your Company Name"))
        self.label_3.setText(_translate("form", "Your Full Name"))
        self.label_4.setText(_translate("form", "Your Gender"))
        self.label_5.setText(_translate("form", "Your Current Adress"))
        self.label_6.setText(_translate("form", "Your Active Phone Number"))
        self.pushButton_2.setText(_translate("form", "Generate Id Card"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = UiForm()
    ui.setup_ui(form)
    form.show()
    sys.exit(app.exec_())