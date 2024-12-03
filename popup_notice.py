import sys
import os
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
        self.notice_id = notice_data['id']
        print(notice_data['id'])
        # 첨부파일 클릭시 해당 파일 열기 시그널
        self.tableWidget.cellDoubleClicked.connect(self.OpenFile)

        # 특정 폴더에서 모든 파일 가져오기
        self.folder_path = f"./files/{notice_data['id']}" 
        print(self.folder_path)
        try:
            self.file_list = os.listdir(self.folder_path)
            self.tableWidget.setRowCount(len(self.file_list))
            self.now = 0
            for file_name in self.file_list:
                self.tableWidget.setItem(self.now, 0, QTableWidgetItem(file_name))
                self.now+=1
        except:
            pass#파일이 없는 것이므로 패스
        self.show()
    
    def OpenFile(self, row, col):
        file_name = self.tableWidget.item(row, 0).text()
        file_path = f"{os.getcwd()}/files/{self.notice_id}/{file_name}"
        try:
            os.startfile(file_path)
        except Exception as e:
            QMessageBox.about(self, f"오류 발생: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Example usage
    notice_data = {"title": "Notice Title", "content": "Notice Content", "date": "2021-06-01"}

    popup = PopupNotice(notice_data)
    popup.exec_()
    sys.exit(app.exec_())