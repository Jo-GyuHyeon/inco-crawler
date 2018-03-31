from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from Crawl_util import Util
from ControlToonVO import *
import CrawlDAO
from selenium.common.exceptions import NoSuchElementException
import time, datetime
import ImageDownload
import Constants

phantom_path = Constants.PHANTOMJS_DRIVER_PATH
driver = webdriver.PhantomJS(phantom_path)

#chrome_path = Constants.CHROMEJS_DRIVER_PATH
#driver = webdriver.Chrome(chrome_path)

class Naver_crawler:
    day = 0
    util = Util()
    wb_platform = "Naver"
    finish_day = "9"
    webtoonId = ""
    webtoonVO = None
    episodeVO = None

    def __init__(self):
        driver.get(Constants.TARGET_SITE)

    #해당 날짜의 모든 웹툰에 접근
    def accessDayWebToon(self, day):
        print("@@@@ ACESS DAY-WEBTOON @@@@")
        print("@@@@@@@@@ %s @@@@@@@@@@@" %day)

        intergerDay = day + 1
        real_webtoonList = []
        
        
        if(day == 9):
            WebDriverWait(webdriver, 300)
            intergerDay = 9
            path = """//*[@id="submenu"]/ul/li[7]/a"""
            driver.find_element_by_xpath(path).click()

        else:
            path = """//*[@id="content"]/ul/li[%d]/a""" %(intergerDay)
            driver.find_element_by_xpath(path).click()
            print(driver.current_url)

        count = driver.find_elements_by_css_selector("#content > div.list_area > ul > li")
    
        #해당 용일의 웹툰에 접근하여 real_webtoonList를 생성합니다.
        for i in range(1, len(count)+1):
            webtoon_selector = "#content > div.list_area > ul > li:nth-child(%d) > div > a" %i
            driver.find_element_by_css_selector(webtoon_selector).click()

            real_webtoonList.append(self.getInWebToon(day))
            print("@accessDayWebToon %d" %i + real_webtoonList[i-1].webtoonName + "를 추가하였습니다.")

            driver.back()

        return real_webtoonList

    #특정 웹툰 에피소드 들고오기
    def findWebtoon(self, WebtoonVO):
        print("@@@@@@ FIND WEBTOON @@@@@@@@")
        real_episodeList = []
        flag = 0
        temp_day = WebtoonVO.day.split(" ")
        integerDay = int(temp_day[0])
        dayList = [None, "1", "2", "3", "4", "5", "6", "7", "n", "c"]
        day = dayList[integerDay]

        print("클릭직전 %s"%integerDay)
        
        if(integerDay == 9):
            WebDriverWait(webdriver, 300)
            path = """//*[@id="submenu"]/ul/li[7]/a"""
            driver.find_element_by_xpath(path).click()

        else:
            path = """//*[@id="content"]/ul/li[%d]""" %(integerDay+1)
            driver.find_element_by_xpath(path).click()

        webtoon_name_list = driver.find_elements_by_css_selector("#content > div.list_area.daily_img > ul > li > dl > dt > a")
        print(len(webtoon_name_list))
        print("%s요일에서 찾습니다.(@findeWebtoon)" %day)

        #모든웹툰에 접근하여 real_episodeList를 생성합니다.
        for i in range(1, len(webtoon_name_list)+1):
            print("%s ?????? %s" %(webtoon_name_list[i-1].get_attribute("title"), WebtoonVO.webtoonName))
            if webtoon_name_list[i-1].get_attribute("title") == WebtoonVO.webtoonName:
                flag = 1
                print("%d번째에서 %s을 찾았다." %(i, webtoon_name_list[i-1].get_attribute("title")))
                
                driver.find_element_by_css_selector("#content > div.list_area.daily_img > ul > li:nth-child(%s) > div > a " %i).click()

                print("real_episodeList를 생성합니다.")
                real_episodeList = self.getWebToonEpisode(WebtoonVO)

                driver.back()
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
            
            if (changeDay == 'no' and WebtoonVO.day == '9'):
                if CrawlDAO.isCrawlExist(WebtoonVO.webtoonId, WebtoonVO.day) != 0:
                    print("%s의 날짜의 %s를 크롤리스트에서 삭제합니다."%(WebtoonVO.day, WebtoonVO.webtoonName))
                    CrawlDAO.deleteCrawlist(WebtoonVO.webtoonId, WebtoonVO.day)
                print("완결에서 사라졌기 때문에 삭제합니다.")
                CrawlDAO.deleteWebtoon(WebtoonVO.webtoonId)
                
        return real_episodeList

    #특정 웹툰을 가져옮
    def getInWebToon(self, day):
        print("@@@@ GET IN WEBTOON @@@@")
        real_webtoonList = []

        #ID
        self.webtoonId = self.util.makeUUID()

        #제목
        #name_selector = "#content > div.comicinfo > div.detail > h2"

        #설명
        introduce_selector = "#content > div.comicinfo > div.detail > p"

        #썸네일
        thumbnail_selector = "#content > div.comicinfo > div.thumb > a > img"

        #작가
        writer_selector = "#content > div.comicinfo > div.detail > h2 > span"

        mythumbnail = []

        
        #name = driver.find_element_by_css_selector(name_selector).text
        name = driver.find_element_by_css_selector(thumbnail_selector).get_attribute("title")
        thumbnail = driver.find_element_by_css_selector(thumbnail_selector).get_attribute("src")
        writers = driver.find_elements_by_css_selector(writer_selector)
        introduce = driver.find_element_by_css_selector(introduce_selector).text

        try:
            introduce = driver.find_element_by_xpath(introduce_selector).text
        except NoSuchElementException:
            pass

        #웹툰이름 초기화
        name = name.replace(writers[0].text, "").strip()

        # 작가 초기화
        writer = writers[0].text.replace(" / ", " ")
        
        #웹툰이 존재하지 않으면 이미지를 다운받습니다.
        if not CrawlDAO.isWebtoonExist(self.wb_platform, name):
            print("%s이 존재하지 않기 때문에 이미지를 다운받습니다.."%name)
            mythumbnail = '다운받았습니당.'
            #mythumbnail = ImageDownload.sendWebtoonImg(ImageDownload.download_webttoonImg(thumbnail, self.webtoonId))
            print("보내애애앰@@@@@@@")

            driver.get("http://comic.naver.com/search.nhn?keyword="+name)
            try:
                genre = driver.find_element_by_css_selector("#content > div:nth-child(2) > ul > li:nth-child(1) > ul > li:nth-child(2) > em").text
            except NoSuchElementException:
                genre = "미정"
            
            driver.back()
            return WebtoonVO(self.wb_platform, day, self.webtoonId, name, writer, 'mythumbnail[0]','mythumbnail[1]', 'mythumbnail[2]', introduce, genre, 0, "2010-01-02")

        return WebtoonVO(self.wb_platform, day, self.webtoonId, name, writer, '','mythumbnail[1]', 'mythumbnail[2]', introduce, "genre", 0, "2010-01-02")

    #에피소드를 크롤
    def getWebToonEpisode(self, WebtoonVO):

        print("웹툰의 에피소드를 읽습니다.")
        episodeList = []
        urlList = []
        flag = 0
        url = driver.current_url + "&page=999999"
        driver.get(url)
        
        #다음 페이지
        prev_button = driver.find_elements_by_css_selector("#content > div.paginate > div > a.pre > span.cnt_page")
        
        lastEpisode = CrawlDAO.getLastEpisode(WebtoonVO.webtoonId)

        if lastEpisode == None:
            flag = 1

        while True:
            #에피소드이름
            ep_titles = driver.find_elements_by_css_selector("#content > table > tbody > tr > td.title > a")
            #날짜
            ep_dates = driver.find_elements_by_css_selector("#content > table > tbody > tr > td.num")
            # 썸네일
            ep_thumbnails = driver.find_elements_by_css_selector("#content > table > tbody > tr > td > a > img")
            # 링크
            ep_links = driver.find_elements_by_css_selector("#content > table > tbody > tr > td.title > a")

            #초기화
            for i in reversed(range(len(ep_titles))):
                if(lastEpisode.episodeName == ep_titles[i].text):
                    flag = 1
                    continue

                if(flag == 1):
                    episodeId = self.util.makeUUID()
                    title = ep_titles[i].text
                    date = ep_dates[i].text.replace(".", "-")
                    thumbnail = ep_thumbnails[i].get_attribute("src")
                    link = ep_links[i-1].get_attribute("href")
                    #urlList = ImageDownload.sendEpisodeImg(ImageDownload.download_EpisodeImg(thumbnail, WebtoonVO.webtoonId, episodeId))
                    
                    episodeVO = EpisodeVO(WebtoonVO.webtoonId, episodeId, title, "urlList[0]", "urlList[1]", "urlList[2]", link, date, '0', None)
                    episodeList.append(episodeVO)

            #버튼이 없으면 루프 종료
            if len(prev_button) == 0:
                break
            
            #버튼이 있으면 페이지를 전환하고 새로운 버튼을 등록
            if len(prev_button) == 1:
                prev_button[0].click()
                prev_button = driver.find_elements_by_css_selector("#content > div.paginate > div > a.pre > span.cnt_page")

        return episodeList

    #웹툰 요일 변경확인
    def checkDayEntry(self, day):
        
        print("@@@@ %d의 Entry를 검사합니다. @@@@"%day)
        
        if(day == 8):
            return

        real_webtoonList = self.accessDayWebToon(day)
        real_count = len(real_webtoonList)

        for i in range(real_count):
            target = real_webtoonList[i]
            print("타겟 @@ = %s"%target.webtoonName)
            webtoon = CrawlDAO.getWebtoonVO(self.wb_platform, target.webtoonName)
            #웹툰이 없으면 신작이기 때문에 웹툰을 추가합니다.
            if not webtoon:
                print("%s는 신작이기때문에 추가합니다."%target.webtoonName)
                CrawlDAO.insertWebtoon(target)
                CrawlDAO.insertCrawlList(target, day)
            #웹툰이 있으면 요일이 바뀌었는지 체크해봅니다.
            else:
                print("else문 들어옴")
                print("타겟 = %s, 웹툰 = %s "%(target.webtoonName, webtoon.webtoonName))
                #해당요일이 레거시 웹툰요일에 포함되지 않았을때 변동이 된것이니 검사를 한다.
                if(str(day) not in str(webtoon.day)):
                    print("%s가 %s에 포함되어있지 않아서 isDayChange 호출"%(day, webtoon.day))
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
        print(WebtoonVO.webtoonName)

        dayList = [None, "1", "2", "3", "4", "5", "6", "7", "n", "c"]
        dayString = [None, "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        change_day = "";

        for i in range(1,9):

            if(i == 8):
                continue

            elif(i == 9):
                WebDriverWait(webdriver, 300)
                path = """//*[@id="submenu"]/ul/li[7]/a"""
                driver.find_element_by_xpath(path).click()
                
            else:
                path = """//*[@id="content"]/ul/li[%d]/a""" %(i+1)
                driver.find_element_by_xpath(path).click()

            flag = 0
            # day = dayList[i]
            wb_name = driver.find_elements_by_css_selector("#content > div.list_area.daily_img > ul > li > div > a > img")

            print("%s요일에서 %s를 찾습니다" %(day,WebtoonVO.webtoonName ))
            
            #찾으면 날짜를 추가합니다.
            for j in range(1, len(wb_name)+1):
                print(j)
                if wb_name[j-1].get_attribute('title') == WebtoonVO.webtoonName:
                    print("%d요일 %d번째에서 %s을 찾았다." %(i, j, wb_name[j-1].get_attribute('title')))
                    change_day += dayString[i] + " "
                    print("요일로 변경할 에정입니다.  %s ----->  %s" %(WebtoonVO.day, change_day))
                    flag = 1
                    break;

        if not change_day:
            print("더이상 서비스 하지 않는 웹툰입니다.");
            CrawlDAO.deleteWebtoon(WebtoonVO.webtoonId);
            return "no"
        
        elif (WebtoonVO.day == change_day):
            print("기존과 같아서 eqaul을 리턴합니다.(@isDayChange)")
            return "equal"

        else:
            print("변경될 요일을 반환합니다.. %s" %change_day)
            return change_day.strip()

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
            
            if len(target_episodeList) == 0:
                continue

            for j in range(0, len(target_episodeList)):
                
                compare_date = datetime.datetime.strptime(str(target_episodeList[j].episodeDate) + " 12:00:00", '%Y-%m-%d %H:%M:%S')
                compare_date = compare_date.date()

                if target_episodeList[j].episodeDate != target.lastDate or target_episodeList[j].episode != target.lastEpisode:
                    print("EPISODE를 추가합니다.")
                    CrawlDAO.insertEpisode(target_episodeList[j])

                    #월이나 그외이면서 타겟의 요일이 같고, 레진 경우에 10일 이상 차이가날경우 합당한 데이터입니다.
                    if int(target.day) <= 8 and int(target.day) == int(compare_date.weekday()+1) and (now - compare_date > datetime.timedelta(4)) == True:
                        isInsert = 1

                    #마지막 데이터의 날짜가 16일 이상 오래되었다면 휴재입니다.
                    elif (now - compare_date < datetime.timedelta(16)) == True:
                        print("휴재 중입니다.")
                        isInsert = 1

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
        