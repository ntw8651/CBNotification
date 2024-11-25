from data_process import * #데이터 처리 코드들 가져오기
from crawling import * #크롤링 코드들 가져오기

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from popup_notice import PopupNotice #팝업창 코드 가져오기

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
'''
작성할 것들
1. 가장 먼저 그냥 지금 갖고 있는 게시글 모두 보여주기

1. 가장 최근 공지 목록으로 request 보내기
    거기서 모든 공지의 id가 이미 딕셔너리에 등록되어 있다면 종료
    아니라면 추가하고 다음 페이지로 또 request 보내기
    만약 1달 이상 과거의 자료와 만나면 멈추기(아니면 무수히 먼 과거까지 가게 되고, 이건 리소스 낭비 + 서버에 무분별한 요청을 보내게 되므로)
    (한 학기 기준...정도인거지) 아 근데 21페이지를 넘겨도 1달 전이면 이건... 1달만...하자 일단은
    기본적으로 10개씩 존재하니까 나중에 인덱싱되지 않은 id를 10단위로 역산해서 찾아보면 될 듯
    
    아 콘텐츠 내용 가져오는 걸 가장 최근 문서부터 10초에 하나씩 가져오자

1-2. 위에서 진행되는 과정(특정 페이지 공지사항을 모두 긁어왔을 때)마다 데이터 저장 및 화면 업데이트

2. 공지사항 클릭시 해당 공지사항의 내용을 보여주기

'''

class CrawlerThread(QThread):
    # 해당 쓰레드 및 크롤링은 현재 굉장히 비효율적으로 만들어졌습니다.
    # 딕셔너리를 죄다 반환한다거나... 매번 세이브 한다거나...
    # 이런 것들은 추후에 수정이 필요합니다.

    # 이 클래스는 크롤링을 위한 쓰레드 클래스입니다.
    # 메인 쓰레드와 별도로 크롤링을 실행하기 위해 사용합니다.
    # 이 덕분에 GUI가 멈추지 않고 크롤링이 가능합니다!

    # 시그널
    # 크롤링이 끝났을 때, 데이터를 업데이트할 수 있도록 시그널을 만들어줍니다.
    view_update_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.now_page = 1
        self.is_running = True

    def run(self):
        while self.is_running:
            self.UpdateNotions()
            # 목록 업데이트 시그널 발생
            self.view_update_signal.emit()

            self.sleep(2)
            self.UpdateContents()
            
            self.now_page+=1

    def UpdateNotions(self):
        global G_notions_dict
        
        # ~ 크롤링 코드 실행 ~
        # dictionary 구조의 update란?
        # a.update(b)를 하면 a에 b를 더해줌
        # 만약 겹치는 데이터의 경우, b의 데이터로 덮어씌워짐
        new_notice_dictionary = GetNotices(f"https://www.cbnu.ac.kr/www/selectBbsNttList.do?key=813&bbsNo=8&pageUnit=10&searchCnd=all&pageIndex={self.now_page}")
        for i in new_notice_dictionary.keys():
            if(G_notions_dict.get(i) == None):
                G_notions_dict[i] = new_notice_dictionary[i]
            else:
                continue
        
        #데이터 저장
        SaveData(G_notions_dict)
        

    def UpdateContents(self):
        global G_notions_dict
        for i in G_notions_dict.keys():
            if(G_notions_dict[i].get('content') == None):
                G_notions_dict[i]['content'] = GetNoticeContent(G_notions_dict[i]['link'])
                SaveData(G_notions_dict)
                self.view_update_signal.emit()
                self.sleep(2)
            else:
                continue
        
        SaveData(G_notions_dict)

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self) #여기까진 기본 셋업
        
        # 게시글 목록 보여주기
        self.ViewNoticeList()
        
        # 공지사항 클릭시 해당 공지사항의 내용을 보여주기위한 시그널 연결
        self.Notices.cellDoubleClicked.connect(self.ShowNoticeContent)

        # 크롤링 쓰레드 생성
        self.crawler_thread = CrawlerThread()
        self.crawler_thread.view_update_signal.connect(self.ViewNoticeList)
        self.crawler_thread.start()

    def ShowNoticeContent(self, row, column):
        notice_id = self.Notices.item(row, 0).text()
        if(G_notions_dict[notice_id].get('content') != None):    
            popup = PopupNotice(G_notions_dict[notice_id])
            popup.exec_()
        # 아직 콘텐츠가 로딩되지 않은 자료는 무시


    def ViewNoticeList(self):
        # 추후 업데이트 된 부분만 추가하도록 변경

        # self.Notices는 테이블 위젯

        # 행의 개수를 공지사항의 개수로 설정
        self.Notices.setRowCount(len(G_notions_dict.keys()))
        now = 0

        # 공지사항들을 테이블에 추가
        for i in G_notions_dict.keys():
            self.Notices.setItem(now, 0, QTableWidgetItem(i))
            self.Notices.setItem(now, 1, QTableWidgetItem(G_notions_dict[i]['title']))
            self.Notices.setItem(now, 2, QTableWidgetItem(G_notions_dict[i]['date']))
            
            #현재 content가 없는 녀석은 회색으로 표시
            if(G_notions_dict[i].get('content') == None):
                self.Notices.item(now, 0).setBackground(QColor(200, 200, 200))
                self.Notices.item(now, 1).setBackground(QColor(200, 200, 200))
                self.Notices.item(now, 2).setBackground(QColor(200, 200, 200))

            now+=1

# main 실행은 맨 마지막에 두기
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()