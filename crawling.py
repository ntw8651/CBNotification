# 필요한 함수를 Import 합니다.
import requests # 요청을 보내는 라이브러리입니다.
from bs4 import BeautifulSoup # HTML을 파싱하는 라이브러리입니다.
import os

'''
requests와 bs4 사용법 익혀보기

지금 당장은 함수 형태로 구현하지 않고, 원하는 데이터를 추출해볼 겁니다.

오늘의 내용을 잘 익혀주시기 바랍니다. 
이미 만들어져 있으니 끝 아냐? 라고 생각하시면 안됩니다.

내부 내용을 긁어오도록 바꾸기도 해야하고,
다른 사이트에서도 긁어오도록 바꾸기도 해야하기 떄문입니다.
이븐하게 잘 익혀두시기 바랍니다.
'''


# Requests
# requests 라이브러리는 HTTP 요청을 보내는 라이브러리입니다.
# 우리가 사용할 코드는 아래와 같습니다
# requests.get(url) : GET 요청을 보냅니다.
# 이때, url은 문자열이어야 합니다.


###################################
# 예시

# url에 주소를 문자열로 담습니다
url = 'https://www.cbnu.ac.kr/www/selectBbsNttList.do?key=813&bbsNo=8&pageUnit=10&searchCnd=all&pageIndex=1'


# requests.get(url)을 통해서 요청을 보내고, 그 결과를 response에 담습니다
response = requests.get(url)


# response의 text를 출력합니다. 이때, text는 HTML 코드입니다.
#[:120]은 120글자까지만 출력하라는 의미입니다. 너무 길어서 120글자만 출력해보겠습니다.
# print(response.text[:120])
###################################


'''

https://www.cbnu.ac.kr/www/selectBbsNttView.do;JSESSIONID=18DE7F79B7555297A85A9DD84840DE88?key=813&bbsNo=8&nttNo=153575&pageUnit=10&searchCnd=all&pageIndex=1
'''
dictionary = {}
# 자 이제, html 코드를 파싱해보겠습니다.
html = response.text

# 충북대 홈페이지의 공지는 모두 <tbody class="text_center"> 하위에 <tr>요소로 존재합니다.
# select를 이용해서 가져와봅시다.
# select는 CSS Selector를 이용해서 원하는 요소를 "배열로" 가져옵니다
# 즉, select('tbody tr')은 모든 tbody 하위의 tr 요소를 가져옵니다.

notices = BeautifulSoup(html, 'html.parser')
notices = notices.select('tbody tr:not(.p-notice)')

# print(notices[0]) # 주석을 해제하세요

# 뒤에 붙는 :not(.p-notice)는 .p-notice가 아닌 요소를 가져오라는 의미입니다.
# 공지사항을 잘 보면, 고정 공지사항과 일반 공지사항이 있습니다.
# 고정 공지사항은 p-notice 클래스를 가지고 있습니다.
# 이를 제외하고 가져오기 위해서 :not(.p-notice)를 사용했습니다.


'''
하나의 <tr>에 여러 항목이 존재하는데요, 위에서부터 순서대로
<td> 번호
<td> 카테고리
<td> 제목
<td> 파일 첨부 내용
<td> 작성 부서
<td> 작성일
<td> 조회수
입니다. 대충 이런식으로 생겼습니다. 물론 안에는 또 세부적으로 나뉘어있긴 하지만요.

이때, td가 여러개가 있네요. 그렇다면 뭘 사용해야 할까요?
아까 했던대로, select를 사용하면 됩니다.

우선, 각 공지사항에 대해 하나씩 해야하니까, for문을 사용하겠습니다.
'''

# 이미 함수로 구현했으므로 이곳에 있던 코드는 삭제합니다.

# 위를 통해서 아래 함수를 채워보세요.

def GetNotices(link): #link page에 해당하는 게시글들을 긁어온다
    dictionary = {}

    print("GetNotices 함수 실행")

    responselink = requests.get(link)
    htmllink = responselink.text 

    noticeslink = BeautifulSoup(htmllink, 'html.parser').select('tbody tr:not(.p-notice)')
    # 요청을 보낼 곳은 link입니다.    
   

    for noticelink in noticeslink: # 이 구문은 모든 notices에 담긴 원소를 하나씩 notice에 담습니다
        elementsl = noticelink.select('td') # 각 notice의 td 요소를 가져옵니다.
    # 참고로, 이미 notice는 bs4 객체이므로, select를 사용할 수 있습니다.
    # 그러니 최초 한번만 위~~에서처럼 BeautifulSoup으로 감싸주면 됩니다.    

    
        numberl = elementsl[0].find(class_ = 'bbs_num').string # 번호 가져오기
    
        titlel = elementsl[2].text # 제목
        titlel = titlel.replace("\n", "").replace("\t", "").strip() #의미 없는 부분 제거

        linkl= elementsl[2].find('a')['href'] # 링크
        
        #단! 이때 상대경로로 지정된 링크는 절대 경로로 바뀌어서 저장되어야 합니다~
        linkl = 'https://www.cbnu.ac.kr/www' + linkl[1:] #여기서 [1:]은 맨 앞의 .을 제거하기 위함입니다.

        datel = elementsl[5].text # 작성일
        datel = datel.replace("\n", "").replace("\t", "").strip() #의미 없는 부분 제거

        '''
        체크용 코드는 주석처리 했습니다.

        print("번호: ", numberl)
        print("제목: ", titlel)
        print("링크: ", linkl)
        print("작성일: ", datel)
        print("\n\n")
        '''


        
        dictionary[numberl] = {
            "title":titlel,
            "link":linkl,
            "date":datel
        }
    
    return dictionary
        
#GetNotices(url)

def GetNoticeContent(link, id):
    linkcon = link

    '''
    변경 사항은 다음과 같습니다.
    - 줄바꿈 기호 추가
    - None타입 무시
    '''
    # 1. 공지사항 목록 페이지 요청
    response = requests.get(linkcon)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    file=soup.find_all(class_="attach_item")

    for i in file:
        file_name=i.find(class_="text").string
        file_link='https://www.cbnu.ac.kr/www'+i.find('a')['href'][1:]
        download(file_link,file_name,id)

    
    
    
    
    text =[]
    tarr=[]
    soup = soup.find(class_='contenttext')
    child=list(soup.children)

    for cchild in child:
        if cchild.name=='table':
            for tab in cchild.find_all('tr'):
                rows=tab.find_all('td')
                data=[]
                for row in rows:
                    data.append(str(row.text).replace('\xa0', ' ').strip())
                tarr.append(data)
            text.append(tarr)
        else:
            #for tag in cchild.find_all(True):  # 모든 태그를 탐색
                #tag.attrs = {}  # 태그의 속성을 제거
            if(cchild.string != None):
                text.append(str(cchild.text).replace('\xa0', ' ').strip())

    for i in text:
        print(i)
    
    return text



def download(url,file_name, id):
    os.makedirs(f"./files/{id}", exist_ok=True)

    with open(f"./files/{id}/{file_name}","wb") as file:
        response=requests.get(url)
        file.write(response.content)


#GetNoticeContent("https://www.cbnu.ac.kr/www/selectBbsNttView.do?key=813&bbsNo=8&nttNo=153751&pageUnit=10&searchCnd=all&pageIndex=4", 123)
#download(url,"iml.jpg")


