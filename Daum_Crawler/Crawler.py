from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from Crawl_util import Util
from ControlToonVO import *
import CrawlDAO
from selenium.common.exceptions import NoSuchElementException
import time, datetime
import ImageDownload
import Constants
import time
import re
# phantom_path = Constants.PHANTOMJS_DRIVER_PATH
# driver = webdriver.PhantomJS(phantom_path)

# chrome_path = Constants.CHROMEJS_DRIVER_PATH
# driver = webdriver.Chrome(chrome_path)

options = webdriver.ChromeOptions()
options.set_headless(headless=True)
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("--log-level=3")

chrome_path = Constants.CHROMEJS_DRIVER_PATH
driver = webdriver.Chrome(chrome_path, chrome_options=options)

class Daum_crawler:
    day = 0
    util = Util()
    wb_platform = "Daum"
    finish_day = "9"
    webtoonId = ""
    webtoonVO = None
    episodeVO = None
    isLogin = False

    def __init__(self):
        driver.get(Constants.TARGET_SITE)

    def test(self):
        driver.maximize_window()
        driver.get("http://webtoon.daum.net/webtoon/view/perfect")
        WebtoonVO = CrawlDAO.getWebtoonVO("Daum","퍼펙트 게임")
        self.getWebToonEpisode(WebtoonVO)
    
    def login(self):
        try:
            loginUrl = "#btnMinidaumLogin"
            driver.find_element_by_css_selector(loginUrl).click()
            current_url = driver.current_url
            if "login" in current_url:
                print("login")
                driver.find_element_by_id('id').send_keys(Constants.DaumID)
                driver.find_element_by_id('inputPwd').send_keys(Constants.DaumPwd)
                driver.find_element_by_xpath("""//*[@id="loginBtn"]""").click()
                driver.maximize_window()

        except NoSuchElementException:
            pass

    #해당 날짜의 모든 웹툰에 접근
    def accessDayWebToon(self, day):
        print("@@@@ ACESS %s DAY-WEBTOON @@@@" %day)
        
        intergerDay = day
        real_webtoonList = []
        dayList = [None, "1", "2", "3", "4", "5", "6", "7", "n", "9"]
        day = dayList[day]
        selectDayList =[None, "#dayList1","#dayList2","#endList"]
        selectNum = 1

        #해당웹툰으로 접근합니다.
        self.selectDay(day)
            
        if(day == '9'):
            count = len(driver.find_elements_by_css_selector("#endList > li"))
            selectNum = 3
        elif(day == 'n'):
            return real_webtoonList
        else:
            driver.implicitly_wait(10)    
            countA = driver.find_elements_by_css_selector("#dayList1 > li")
            countB = driver.find_elements_by_css_selector("#dayList2 > li")
            count = len(countA) + len(countB)

        print("%s 요일의 웹툰 갯수 : %d" %(day,count))
            
        #해당 용일의 웹툰에 접근하여 real_webtoonList를 생성합니다.
        for i in range(1, count+1):
            
            print("%d 번째"%i)
            if(i > 8 and "9" not in day):
                selectNum = 2
                i -= 8
            
            print("i는 뭐다? : %d"%i)
            
            webtoon_selector = "%s > li:nth-child(%d) > a > span" %(selectDayList[selectNum],i)
            webtoon_element = driver.find_element_by_css_selector(webtoon_selector)
            driver.execute_script("arguments[0].click();", webtoon_element)

            driver.implicitly_wait(10)

            real_webtoonList.append(self.getInWebToon(intergerDay))
            print("@accessDayWebToon %d" %i + real_webtoonList[i-1].webtoonName + "를 추가하였습니다.")

            driver.back()
            driver.implicitly_wait(10)

        return real_webtoonList
    
    #해날 날짜로 접근
    def selectDay(self,day):
        print("@@@@@@ selectDay @@@@@@@@")
        driver.get(Constants.TARGET_SITE)
        driver.execute_script("window.scrollBy(0, -document.documentElement.scrollHeight)")
        time.sleep(3)
        driver.implicitly_wait(10)
        
        if(day == '9'):
            path = """//*[@id="cMain"]/div[1]/h3[2]/a"""
            driver.find_element_by_xpath(path).click()
            time.sleep(3)
        elif(day == 'n'):
            pass
        else:
            driver.find_element_by_xpath('//*[@id="cMain"]/div[1]/h3[1]/a').click()
            path = """//*[@id="dayListTab"]/li[%s]/a""" %day
            driver.find_element_by_xpath(path).click()
            time.sleep(3)
            driver.implicitly_wait(10)

    #특정 웹툰 에피소드 들고오기
    def findWebtoon(self, WebtoonVO):
        print("@@@@@@ FIND WEBTOON @@@@@@@@")
        real_episodeList = []
        flag = 0
        temp_day = WebtoonVO.day.split(" ")
        integerDay = int(temp_day[0])
        dayList = [None, "1", "2", "3", "4", "5", "6", "7", "n", "9"]
        day = dayList[integerDay]
        selectDayList =[None, "#dayList1","#dayList2","#endList"]
        selectNum = 1
      
        print("클릭직전 %s"%integerDay)
        #해당웹툰으로 접근합니다.
        self.selectDay(day)

        if(day == '9'):
            webtoon_name_list = driver.find_elements_by_css_selector("#endList > li > a > strong")
            selectNum = 3
        elif (day == '8'):
            return None
        else:             
            wb_name1 = driver.find_elements_by_css_selector("#dayList1 > li > a > strong")
            wb_name2 = driver.find_elements_by_css_selector("#dayList2 > li > a > strong")
            webtoon_name_list = wb_name1 + wb_name2
             
        driver.implicitly_wait(10)
        
        print("%s요일에서 찾습니다.(@findeWebtoon) %d 개" %(day,len(webtoon_name_list)))

        #모든웹툰에 접근하여 real_episodeList를 생성합니다.
        for i in range(1, len(webtoon_name_list)+1):
            if webtoon_name_list[i-1].text == WebtoonVO.webtoonName:
                flag = 1
                print("%d번째에서 %s을 찾았다." %(i, webtoon_name_list[i-1].text))
                if(i > 8 and "9" not in day):
                    selectNum = 2
                    i -= 8

                webtoon_selector = "%s > li:nth-child(%d) > a > span" %(selectDayList[selectNum],i)
                webtoon_element = driver.find_element_by_css_selector(webtoon_selector)
                driver.execute_script("arguments[0].click();", webtoon_element)

                print("real_episodeList를 생성합니다.")
                real_episodeList = self.getWebToonEpisode(WebtoonVO)

                break

            elif webtoon_name_list[i-1].text != WebtoonVO.webtoonName:
                print("다릅니다")
                print(webtoon_name_list[i-1].text + "/" +WebtoonVO.webtoonName)
        
        #해당 요일에 모든 웹툰을 비교하고, 웹툰이 없으면 isDayChange 실행 
        if(flag ==0):
            print("해당 날짜에서 findwebtoon을하였지만 찾을 수 없어 다른 날짜로 옮긴것인지 검사합니다.\n")
            changeDay = self.isDayChange(WebtoonVO)
            
            #동일하지 않고, 연재종료가 된것이 아니라면 추가합니다. 요일을 바꿔주고 크로울 리스트에서 삭제합니다. (크로울추가는 해당하는 요일에 어자피 시행됩니다.)
            if (WebtoonVO.day not in changeDay and changeDay != "no" ) :
                if CrawlDAO.isCrawlExist(WebtoonVO.webtoonId, WebtoonVO.day) != 0:
                    print("%s의 날짜의 %s를 크롤리스트에서 삭제합니다."%(WebtoonVO.day, WebtoonVO.webtoonName))
                    CrawlDAO.deleteCrawlist(WebtoonVO.webtoonId, WebtoonVO.day)
                WebtoonVO.day = changeDay
                CrawlDAO.updateDay(WebtoonVO)
                print("%s에서 %s로 날짜가 변경되었습니다.\n"%(WebtoonVO.day, changeDay))
            if(changeDay == 'no' and WebtoonVO.day == '9'):
                print("더이상 실존하지 않는 웹툰이기에 %s 웹툰을 삭제합니다. "%WebtoonVO.webtoonName)
                if CrawlDAO.isCrawlExist(WebtoonVO.webtoonId, WebtoonVO.day) != 0:
                    print("%s의 날짜의 %s를 크롤리스트에서 삭제합니다."%(WebtoonVO.day, WebtoonVO.webtoonName))
                    CrawlDAO.deleteCrawlist(WebtoonVO.webtoonId, WebtoonVO.day)
                print("완결에서 사라졌기 때문에 삭제합니다.")
                CrawlDAO.deleteWebtoon(WebtoonVO.webtoonId)
                #웹툰삭제
        return real_episodeList

    #특정 웹툰을 가져옮
    def getInWebToon(self, day):
        print("@@@@ GET IN WEBTOON @@@@ %d"%day)
        real_webtoonList = []

        #ID
        self.webtoonId = self.util.makeUUID()

        #제목
        name_selector = "#cSub > div.product_info > div > div > h3"
        #설명
        introduce_selector = """//*[@id="cSub"]/div[1]/div/div/dl/dd[2]"""
        #썸네일
        thumbnail_selector = "#cSub > div.product_info > div > img"
        #장르
        genre_selector ="#cSub > div.product_info > div > div > dl > dd.txt_genre"
        #작가
        writer_selector = "#cSub > div.writer_info > div.inner_writer > dl > dd.txt_writer > a"

        mythumbnail = []
        
        name = driver.find_element_by_css_selector(name_selector).text
        name = re.sub('\n+', " ", name).strip()
        thumbnail = driver.find_element_by_css_selector(thumbnail_selector).get_attribute("src")
        genres = driver.find_element_by_css_selector(genre_selector).text.replace(",","")

        #작가와 그림이 나누어질 경우
        try:
            writers = driver.find_element_by_css_selector(writer_selector).text
        except NoSuchElementException:
            #작가
            writer_selector = "#cSub > div.writer_info > div.inner_writer > dl > dd:nth-child(2) > strong > span > a"
            #그림
            painter_selector = "#cSub > div.writer_info > div.inner_writer > dl > dd:nth-child(3) > strong > span > a"
            
            writers = driver.find_element_by_css_selector(writer_selector).text
            painter = driver.find_element_by_css_selector(painter_selector).text
            writers += " " + painter

        writers = writers.replace("/"," ")

        print(name)
        print(writers)
        print(genres)

        introduce = ''

        try:
            introduce = driver.find_element_by_xpath(introduce_selector).text
        except NoSuchElementException:
            pass

        # # # 작가 초기화
        # writer = ''
        # for who in writers:
        #     writer += who + " "

        # # # 장르 초기화
        # genre = ''
        # for what in genres:
        #     genre += what + " "

        # #웹툰이 존재하지 않으면 이미지를 다운받습니다.
        if not CrawlDAO.isWebtoonExist(self.wb_platform, name):
            print("%s이 존재하지 않기 때문에 이미지를 다운받습니다.."%name)
            mythumbnail = ImageDownload.sendWebtoonImg(ImageDownload.download_webttoonImg(thumbnail, self.webtoonId))

            return WebtoonVO(self.wb_platform, day, self.webtoonId, name, writers, mythumbnail[0],mythumbnail[1], mythumbnail[2], introduce, genres, 0, "2010-01-02")

        return WebtoonVO(self.wb_platform, day, self.webtoonId, name, writers, '','mythumbnail[1]', 'mythumbnail[2]', introduce, genres, 0, "2010-01-02")

    #에피소드를 긁기
    def getWebToonEpisode(self, WebtoonVO):

        episodeList = []
        isLastEpisode = False

        #최신순
        url=driver.current_url+"#pageNo=1&sort=asc&type="
        driver.get(url)

        print(WebtoonVO.webtoonId)
        print(WebtoonVO.webtoonName)
        print("웹툰의 에피소드를 읽습니다.")
        time.sleep(4)
        driver.execute_script("window.scrollBy(0, document.documentElement.scrollHeight/3)")

        lastEpisode = CrawlDAO.getLastEpisode(WebtoonVO.webtoonId)

        if lastEpisode == None:
            isLastEpisode = True
            episodeName = None
        else:
            episodeName = lastEpisode.episodeName

        while True:
            time.sleep(3)
            driver.implicitly_wait(10)
            #에피소드이름
            ep_titles = driver.find_elements_by_css_selector("#episodeList > ul > li > a > strong")
            #날짜
            ep_dates = driver.find_elements_by_css_selector("#episodeList > ul > li > div > span.txt_date")
            # 썸네일
            ep_thumbnails = driver.find_elements_by_css_selector("#episodeList > ul > li > a > img")
            # 링크
            ep_links = driver.find_elements_by_css_selector("#episodeList > ul > li > a")
            
            driver.implicitly_wait(10)
            #현재  페이지
            cur_page = driver.find_element_by_css_selector("#episodeList > div.paging_number > span > em")
            #다음 페이지
            next_page = driver.find_element_by_css_selector("#episodeList > div.paging_number > span")
            #윈도우 페이지 리스트
            page = next_page.find_elements_by_class_name("link_page")
            #다음 페이지 버튼
            try:
                next_button = driver.find_element_by_css_selector("#episodeList > div.paging_number > span > a.btn_comm.btn_next")
            except NoSuchElementException:
                next_button = None

            #첫번째 페이지에서 무료회차 바로보기가 있다면 타이틀에서 0번째 인덱스 삭제
            if(int(cur_page.text) == 1):
                try:
                    driver.find_element_by_class_name("item_free")
                    print("무료회차 바로보기가 있어서 타이틀 0번째 인덱스 삭제합니다.")
                    del ep_titles[0]
                except NoSuchElementException:
                    pass

            print("타이틀 갯수 : %d "%len(ep_titles))
            #초기화
            for i in range(len(ep_titles)):
                print("%d번째 : "%i)
                if(episodeName == ep_titles[i].text):
                    isLastEpisode = True
                    continue

                if(isLastEpisode == True):
                    episodeId = self.util.makeUUID()
                    title = ep_titles[i].text

                    if('.' in ep_dates[i].text):
                        date = ep_dates[i].text.replace(".", "-")
                    elif ('일' in ep_dates[i].text):
                         #일단위 무료 날짜 계산
                        preDate = re.findall("\d+",ep_dates[i].text)
                        date = datetime.datetime.now() + datetime.timedelta(days = int(preDate[0]))
                        date = date.strftime('%Y-%m-%d')
                    elif (':' in ep_dates[i].text):
                        #시간단위 무료 날짜 계산
                        preDate = re.findall("\d+",ep_dates[i].text)
                        date = datetime.datetime.now() + datetime.timedelta(hours = int(preDate[0]))+datetime.timedelta(minutes = int(preDate[1]))
                        date = date.strftime('%Y-%m-%d')
                        
                    try:
                        thumbnail = ep_thumbnails[i].get_attribute("src")
                    except IndexError:
                        #미리 보기 썸네일
                        thumbnail = driver.find_elements_by_css_selector("#episodeList > ul > li:nth-child(%d) > a > span.thumb_g > img"%(i+1))[0].get_attribute("src")
                       
                    link = ep_links[i-1].get_attribute("href")
                    #유/무료
                    ep_charges = driver.find_elements_by_css_selector("#episodeList > ul > li:nth-child(%d) > div > span.txt_price"%(i+1))
                    charge = 0 if not ep_charges else 1
                    urlList = ImageDownload.sendEpisodeImg(ImageDownload.download_EpisodeImg(thumbnail, WebtoonVO.webtoonId, episodeId))
                    print(title)
                    print(date)
                    print(thumbnail)
                    print(link)
                    print(charge)

                    episodeVO = EpisodeVO(WebtoonVO.webtoonId, episodeId, title, urlList[0], urlList[1], urlList[2], link, date, None, charge)
                    episodeList.append(episodeVO)

            index = int(cur_page.text) % 5
            if(index != 0 and len(page) > index):        
                page[index].click()
                time.sleep(3)
                driver.execute_script("window.scrollBy(0, document.documentElement.scrollHeight/5)")
            elif(index ==0 or len(page) == index):
                #다음 페이지가 존재 하지 않으면 종료                
                if(next_button == None):
                    break
                #다음 페이지 존재 하면 페이지 전환
                else:
                    next_button.click()

        return episodeList

    #웹툰 요일 변경확인
    def checkDayEntry(self, day):
        
        print("@@@@ %d의 Entry를 검사합니다. @@@@"%day)
        real_webtoonList = self.accessDayWebToon(day)
        real_count = len(real_webtoonList)

        for i in range(real_count):
            target = real_webtoonList[i]
            webtoon = CrawlDAO.getWebtoonVO(self.wb_platform, target.webtoonName)
            
            if not webtoon:
                print("%s는 신작이기때문에 추가합니다."%target.webtoonName)
                CrawlDAO.insertWebtoon(target)
                CrawlDAO.insertCrawlList(target, day)
            #웹툰이 있으면 요일이 바뀌었는지 체크해봅니다.
            else:
                #해당요일이 레거시 웹툰요일에 포함되지 않았을때 변동이 된것이니 검사를 한다.
                if(str(day) not in str(webtoon.day)):
                    compare_day = self.isDayChange(webtoon)
                    #요일이 변동이 없을 때
                    if(compare_day == "equal"):
                        print("%s는 요일에 변동이 없습니다."%webtoon.webtoonName)

                        if CrawlDAO.isCrawlExist(webtoon.webtoonId, day) == 0:
                            CrawlDAO.insertCrawlList(webtoon, day)
                            continue

                    elif(compare_day == "no"):
                        continue

                    #요일이 변동이 있을 때
                    else:
                        #현재요일과 체크한 요일이 다르면 업데이트합니다.
                        if(webtoon.day != compare_day):
                            print("%s는 요일에 변동이 있어 요일을 변경합니다. %s => %s"%(webtoon.webtoonName, webtoon.day,compare_day))
                            webtoon.day = compare_day
                            CrawlDAO.updateDay(webtoon)
                            if str(webtoon.day) not in str(day) and CrawlDAO.isCrawlExist(webtoon.webtoonId, day) == 0:
                                CrawlDAO.deleteCrawlist(webtoon.webtoonId, day)
                                CrawlDAO.insertCrawlList(webtoon, day)
                else:
                    print("## 요일변동이 감지 되어있지 않습니다.")
                    
                    if CrawlDAO.isCrawlExist(webtoon.webtoonId, day) == 0:
                        CrawlDAO.insertCrawlList(webtoon, day)
                        continue
                    continue

        print("checkDayEntry를 종료합니다.")


    #어느 날짜로 이동해야할지 체크
    def isDayChange(self, WebtoonVO):
        print("날짜가 바뀌었기 때문에 찾아봅시다!!!!")

        dayList = [None, "1", "2", "3", "4", "5", "6", "7", "n", "9"]
        dayString = [None, "1", "2", "3", "4", "5", "6", "7", "n", "9"]
        change_day = "";

        for i in range(1,10):
            flag = 0
            day = dayList[i]
            
            self.selectDay(day)
            
            if(i == 9):
                webtoon_name_list = driver.find_elements_by_css_selector("#endList > li > a > strong")
            elif (i == 8):
                continue
            else:             
                wb_name1 = driver.find_elements_by_css_selector("#dayList1 > li > a > strong")
                wb_name2 = driver.find_elements_by_css_selector("#dayList2 > li > a > strong")
                webtoon_name_list = wb_name1 + wb_name2
             
            driver.implicitly_wait(10)

            print("날짜 바뀐것중 현재 %d 요일 찾고 있습니다."%i)

            print("%d 요일 %d 개 웹툰이 있습니다."%(i,len(webtoon_name_list)))

            print("%s요일에서 %s를 찾습니다" %(day,WebtoonVO.webtoonName ))
            
            #찾으면 날짜를 추가합니다.
            for j in range(1, len(webtoon_name_list)+1):
                print(webtoon_name_list[j-1].text.replace('성인', ''))
                if webtoon_name_list[j-1].text.replace('성인', '') == WebtoonVO.webtoonName:
                    print("%d요일 %d번째에서 %s을 찾았다." %(i, j, webtoon_name_list[j-1].text))
                    print(change_day)
                    print(dayString[i])

                    change_day +=  dayString[i] + " "
                    print(change_day)
                    print("chagne_day %s" %change_day)
                    flag = 1
                    break;

        if not change_day:
            print("더이상 서비스 하지 않는 웹툰입니다.");
            if not CrawlDAO.isWebtoonExist(self.wb_platform, WebtoonVO.webtoonName):
                CrawlDAO.deleteWebtoon(WebtoonVO.webtoonId)
            return "no"
        
        elif (WebtoonVO.day == change_day):
            print("기존과 같아서 eqaul을 리턴합니다.(@isDayChange)")
            return "equal"

        else:
            print("요일이 변경되었습니다. %s" %change_day)
            return change_day.strip()

    #첫 실행, 에러 난후 다시 재시작했을때의 루프
    def initRoop(self):
        print("@@@@ ROOP CRAWLIST @@@@")
        now = datetime.datetime.now().date()
        crawl_list = CrawlDAO.getCrawlList(self.wb_platform)
        count = len(crawl_list)

        print("Crawlist 몇번 = %s" %str(count))

        for i in range(count):
            isInsert = 0
            target= crawl_list[i]
            print("%d번째 target의 이름은 "%i + target.webtoonName + "입니다.")
            print("target의 라스트데이트는 = %s" %target.lastDate)
            target_episodeList = self.findWebtoon(target)
            if target_episodeList == []:
                isInsert = 1

            for j in range(len(target_episodeList)):
                CrawlDAO.insertEpisode(target_episodeList[j])

                if target_episodeList[j].episodeDate != target.lastDate or target_episodeList[j].episode != target.lastEpisode:
                    print("EPISODE를 추가합니다.")
                    isInsert =1

            if isInsert == 1:
                print("Crawllist에서 삭제")
                CrawlDAO.deleteCrawlist(target.webtoonId, target.day)

        test = CrawlDAO.getCrawlList(self.wb_platform)
        print("CRAWLIST 남은 웹툰 = %d개" %len(test))
        return test

    #계속 실행되는 루프
    def roopCrawllist(self):
        print("@@@@ ROOP CRAWLIST @@@@")
        now = datetime.datetime.now().date()
        crawl_list = CrawlDAO.getCrawlList(self.wb_platform)
        count = len(crawl_list)

        for i in range(count):
            isInsert = 0
            target= crawl_list[i]
            print("%d번째 target의 이름은 "%i + target.webtoonName + "입니다.")
            print("target의 라스트데이트는 = %s"%target.lastDate)
            target_episodeList = self.findWebtoon(target)

            print(target_episodeList)
            if len(target_episodeList) == 0:
                continue

            for j in range(0, len(target_episodeList)):
                
                compare_date = datetime.datetime.strptime(str(target_episodeList[j].episodeDate) + " 12:00:00", '%Y-%m-%d %H:%M:%S')
                compare_date = compare_date.date()

                if target_episodeList[j].episodeDate != target.lastDate or target_episodeList[j].episode != target.lastEpisode:
                    print("EPISODE를 추가합니다.")
                    CrawlDAO.insertEpisode(target_episodeList[j])

                    #월이나 그외이면서 타겟의 요일이 같고, 레진 경우에 10일 이상 차이가날경우 합당한 데이터입니다.
                    if int(target.day) <= 8 and int(target.day) == int(compare_date.weekday()+1) and (now - compare_date > datetime.timedelta(10)) == True:
                        isInsert = 1

                    #마지막 데이터의 날짜가 16일 이상 오래되었다면 휴재입니다.
                    elif (now - compare_date < datetime.timedelta(16)) == True:
                        isInsert = 1

                    #이부분 이상함 네이버 전용임
                    #elif int(target.day) == 8 and (now - compare_date < datetime.timedelta(4)) == True:
                    #    print("4일 이하로 차이가납니다.")
                    #    isInsert = 1
                    
                    #완결은 한번만 검사합니다.
                    elif int(target.day) == 9:
                        isInsert = 1

            if isInsert == 1:
                print("합당한 이유로 Crawllist에서 삭제")
                CrawlDAO.deleteCrawlist(target.webtoonId, target.day)

            elif time.localtime().tm_hour == 8:
                print("시간이 만료되었습니다.")
                return 0

        test = CrawlDAO.getCrawlList(self.wb_platform)
        print("CRAWLIST 남은 웹툰 = %d개" %len(test))
        return test
