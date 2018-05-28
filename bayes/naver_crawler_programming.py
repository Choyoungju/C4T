'''
네이버 지식인 "프로그래밍" 검색
네이버 지식인 질문들 제목 크롤링
베이지안 필터 학습용
'''

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

# 프로그래밍 검색 시 지식인 url
# start 뒤에 번호는 1, 11, 21 ... 이런식으로 증가
query_url = "https://kin.naver.com/search/list.nhn?query=%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D&page="
page_number = 1

# 해당하는 페이지 번호의 질문글들 href를 리스트에 저장해서 반환함
def get_question_hrefs(page_number) :
    url = query_url + str(page_number)
    html = urlopen(url)
    bsObj = bs(html, "html.parser")
    ul = bsObj.find("ul", {"class": "basic1"})
    lis = ul.find_all("li", {"class":""})

    hrefs = []
    for li in lis :
        href = li.find("a").get('href')
        hrefs.append(href)

    return hrefs

# herf들에 있는 질문글들의 질문내용 텍스트를 파일 f에 저장하는 함수
def save_question_text(hrefs, f) :
    for href in hrefs :
        url = href.split("§")[0]
        html = urlopen(url)
        bsObj = bs(html, "html.parser")
        endTitleText = bsObj.find("h3", {"class" : "_endTitleText"})
        try :
            text = endTitleText.get_text()
            text = text.strip()
            f.write(text + "\n")
        except :
            pass
        
# 위 과정을 실행시키는 함수
def run() :
    # 파일은 1번부터 시작해서 30개 단위로 끊으며 파일번호 증가함
    file_cnt = 1
    filename = "programming" + str(file_cnt) + ".txt"
    f = open(filename, "a", encoding='utf-8')

    # 네이버 질문글 페이지 번호는 1번부터 150번까지 있음.
    for page_number in range(1,151) :
        print("Now Page Number :", page_number)
        # 페이지 번호 전달해서 hrefs 얻고 파일로 저장함.
        hrefs = get_question_hrefs(page_number)
        save_question_text(hrefs, f)
    f.close()

# 위 로직 실행
run()