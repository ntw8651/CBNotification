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
        for i in notice_data["content"]:
            if(type(i) == list):
                self.TextEdit.append(self.ArrayToHtml(i) + "\n")
            else:
                self.TextEdit.append(i + "\n")
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

    def ArrayToHtml(self, data):
        # 2차원 배열을 HTML 테이블로 변환
        html = "<table border='1' style='border-collapse: collapse; width: 100%;'>"
        for row_idx, row in enumerate(data):
            html += "<tr>"
            for cell in row:
                # 첫 번째 행은 헤더로 처리
                if row_idx == 0:
                    html += f"<th style='padding: 8px; text-align: left;'>{cell}</th>"
                else:
                    html += f"<td style='padding: 8px; text-align: left;'>{cell}</td>"
            html += "</tr>"
        html += "</table>"
        return html

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Example usage
    notice_data = {
        "title": "충북대학교 초빙교원 채용공고(국제교류본부)",
        "link": "https://www.cbnu.ac.kr/www/selectBbsNttView.do;JSESSIONID=5A3AE411184EB8A2D87E3E85C692C08E?key=813&bbsNo=8&nttNo=154042&pageUnit=10&searchCnd=all&pageIndex=1",
        "date": "2024-12-04",
        "content": [
            "",
            "충북대학교 공고 제2024-0424호",
            "",
            "[ 초빙교원 채용공고 ]",
            "",
            "",
            "충북대학교 초빙교원 채용을 다음과 같이 실시하오니 많은 지원 바랍니다.",
            "○ 채용분야 및 인원",
            "",
            [
                [
                    "채용(근무)부서",
                    "임용기간",
                    "담당예정 업무",
                    "채용인원"
                ],
                [
                    "국제교류본부",
                    "2025. 1. 1. ~ 2025. 12. 31.",
                    "∘ 강의담당(학기별 최대 3개 강좌 강의 가능)    - 글로벌비즈니스 교과목  ∘ 외국인전용학과 학생관리",
                    "1명"
                ]
            ],
            "",
            "○ 접수기간: 12. 4.(수) ~ 12. 10.(화) 18시까지",
            "○ 접수처: 충청북도 청주시 서원구 충대로 1, 충북대학교 국제교류본부(N10동) 151호",
            "○ 문의사항: 043-261-3284",
            ""
        ],
        'id' : '3288'
    }
    popup = PopupNotice(notice_data)
    popup.exec_()
    sys.exit(app.exec_())