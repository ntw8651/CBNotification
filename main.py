from data_process import * #데이터 처리 코드들 가져오기
from crawling import * #크롤링 코드들 가져오기

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

###################
#Global Variables
G_notions_dict = LoadData() #공지사항들 데이터 불러오기
###################


################### 이곳에 pyqt 디자이너로 만든 ui 파일 경로를 적기
#main.py와 같은 폴더에 넣고 파일명만 적으면 됨
form_class = uic.loadUiType("untitled.ui")[0]
###################


###################
# 이곳에 각 위젯 작성
###################

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        for i in G_notions_dict.keys():
            self.listWidget.addItem(i)




# main 실행은 맨 마지막에 두기
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()