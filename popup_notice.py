import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

popup_form_class = uic.loadUiType("popup_notice.ui")[0]
class PopupNotice(QDialog, popup_form_class):
    def __init__(self, notice_data):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Notice Content")
        self.setGeometry(500, 500, 600, 400)
        # self.오브젝트이름.속성 을 통해서 속성을 지정하는 게
        # UI의 기본 골자!
        # Notice content display
        self.TextEdit.setReadOnly(True)
        self.TextEdit.setText(notice_data["content"])

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Example usage
    notice_data = {"title": "Notice Title", "content": "Notice Content", "date": "2021-06-01"}

    popup = PopupNotice(notice_data)
    popup.exec_()
    sys.exit(app.exec_())