import time, datetime
from Crawler import Daum_crawler
import CrawlDAO

crawler = Daum_crawler()
print("Test 크롤링 시작해 보자!!")
crawler.login()
# crawler.accessDayWebToon(2)
# crawler.checkDayEntry(1)

def daum_initialize():
    for i in range(1,10):
        crawler.checkDayEntry(i)
    # crawler.roopCrawllist()
    
#getWebToonEpisode 코드 수정하기
daum_initialize()


#크로울리스트가 최초 실행시 모든 데이터를 점검합니다.
def initialize():
    for i in range(8, 9):
        crawler.checkDayEntry(i)
    crawler.roopCrawllist()

#하루에 한번 해당 날짜의 웹툰들을 Crallist에 추가합니다.
def routine():
    print("rountine이 실행됩니다.")
    print(time.ctime())
    now = datetime.datetime.now()
    day = now.weekday()+1
    print("%s를 긁어봅시다!" %day)
    crawler.checkDayEntry(day)
    print("rountine이 종료되었습니다. %s" %str(time.ctime()))

#하루에 한번 특정시간에 job이 수행됩니다.
def job():
    #rounie()을 이용해 해당 요일의 웹툰을 추가합니다.
    routine()
    print(time.ctime())
    #Crawllist에 있는 웹툰들을 크롤링합니다.
    while(True) :
        if crawl.roopCrawllist() == 0:
            print("crawl 리스트 갯수가 0개가 되어 job이 종료됩니다. ")
            break

        if time.localtime().tm_hour > 4:
            print("시간이 되서 job이 종료됩니다.")
            break
