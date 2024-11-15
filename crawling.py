# 필요한 함수를 Import 합니다.
import requests # 요청을 보내는 라이브러리입니다.
from bs4 import BeautifulSoup # HTML을 파싱하는 라이브러리입니다.


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
print(response.text[:120]) # 주석을 해제하세요

###################################




# 자 이제, html 코드를 파싱해보겠습니다.
html = response.text

# 충북대 홈페이지의 공지는 모두 <tbody class="text_center"> 하위에 <tr>요소로 존재합니다.
# select를 이용해서 가져와봅시다.
# select는 CSS Selector를 이용해서 원하는 요소를 "배열로" 가져옵니다
# 즉, select('tbody tr')은 모든 tbody 하위의 tr 요소를 가져옵니다.

notices = BeautifulSoup(html, 'html.parser').select('tbody tr:not(.p-notice)')

print(notices[0]) # 주석을 해제하세요

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

for notice in notices: # 이 구문은 모든 notices에 담긴 원소를 하나씩 notice에 담습니다
    elements = notice.select('td') # 각 notice의 td 요소를 가져옵니다.
    # 참고로, 이미 notice는 bs4 객체이므로, select를 사용할 수 있습니다.
    # 그러니 최초 한번만 위~~에서처럼 BeautifulSoup으로 감싸주면 됩니다.    

    
    number = elements[0].find(class_ = 'bbs_num').string # 번호 가져오기
    
    title = elements[2].text # 제목
    title = title.replace("\n", "").replace("\t", "").strip() #의미 없는 부분 제거

    link = elements[2].find('a')['href'] # 링크

    date = elements[5].text # 작성일
    date = date.replace("\n", "").replace("\t", "").strip() #의미 없는 부분 제거

    
    print("번호: ", number)
    print("제목: ", title)
    print("링크: ", link)
    print("작성일: ", date)
    print("\n\n")



# 위를 통해서 아래 함수를 채워보세요.
def GetNotices(link):
    
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
        titlel = title.replace("\n", "").replace("\t", "").strip() #의미 없는 부분 제거

        linkl= elementsl[2].find('a')['href'] # 링크

        datel = elementsl[5].text # 작성일
        datel = datel.replace("\n", "").replace("\t", "").strip() #의미 없는 부분 제거

        
    print("번호: ", numberl)
    print("제목: ", titlel)
    print("링크: ", linkl)
    print("작성일: ", datel)
    print("\n\n")

GetNotices(url)