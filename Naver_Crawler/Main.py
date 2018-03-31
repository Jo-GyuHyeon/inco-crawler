import time
import datetime
#from Crawler import Lezhin_crawl
import schedule
import CrawlDAO
import Manager
from ControlToonVO import *

platform = "Naver"

# WebtoonVO = WebtoonVO("Naver", "1", "a548a7e9-6c61-4338-b942-262e82f12251", "name", "writer", "mythumbnail","", "", "introduce", "genre", 0, "2010-01-02")

# target_count = CrawlDAO.getLastEpisode(WebtoonVO.webtoonId)
# if (target_count != None):
#     print(target_count.episodeName)

Manager.initialize()

# schedule.every().day.at("20:30").do(Manager.job)

# while True:
#     schedule.run_pending()
#     time.sleep(60)
