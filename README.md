# CBNotification

main.py - UI 구현
- crawling - 데이터 요청, requests 처리, 데이터 처리
- data_process - 데이터 저장 및 로드


## 각 파트별 구현
### 구현 전 참고사항
- request는 무한히 보내지 않도록 항상 조심하기
- 전역변수를 최소화 할 것
- 크롤링 계열 함수 호출 시, 실패할 경우를 대비한 try - except 구문을 작성할 것
- 항상 주석을 달 것
- Chat-GPT를 사용할 것
- 모르면 물어볼 것(같이 찾아줌)

### UI 


### crawling



#### RequestSiteData():
기능: 공지사항으로 요청을 날려서 사이트 데이터를 가져온다. 이 함수는 프로그램 실행 초기에 1번만 실행하고 데이터를 전역변수 또는 파일로 저장해서 사용한다. dictionary 형태로 정리해서 저장하면 GOOD.
   추후, 프로그램이 실행되면 ‘데이터 확인 중’이라는 말과 함께 이 함수를 실행하고, UI를 띄워준다.

#### GetRecentNoticeNumber():
기능: 웹사이트의 가장 최근 공지사항 ‘번호’ 가져와서 return

#### GetNoticeContents(a, b):
기능: a번부터 b번까지의 공지사항 가져오기<br>
**단, 다음을 준수할 것:**
- **a와 b가 10 초과로 차이나면 10개로 줄여 실행할 것**
- **매 요청 사이에 1초 이상 간격을 둘 것**
- **이때의 번호는 공지 목록 좌측에 뜨는 번호를 기준으로 한다**
```py
def GetNoticeContents(a, b):
    if(b-a>10):
        a= b - 10
    <중략>

	for i in range(a, b+1):
		arr.append(GetNoticeContent(i))
        time.sleep(1)
        #asy
```

#### GetNoticeContent(number):
기능: 번호에 따른 공지사항 내용(& 링크) 가져와서 return하고, 최근 업데이트 시간 저장

### data_process