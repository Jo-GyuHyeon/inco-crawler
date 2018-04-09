from GetConnection import db_session
from ControlToonTable import WebtoonTable, EpisodeTable, WriterTable, PlatformTable, GenreTable, DayTable, CrawllistTable
from sqlalchemy import and_, join
from ControlToonVO import WebtoonVO, EpisodeVO, CrawllistVO

def insertWebtoon(WebtoonVO):
    addWebtoon = WebtoonTable(WebtoonVO)
    addWriter = WriterTable(WebtoonVO)
    addPlatform = PlatformTable(WebtoonVO)
    addGenre = GenreTable(WebtoonVO)
    addDay = DayTable(WebtoonVO)

    try:
        db_session.add(addWebtoon)
        db_session.commit()

        db_session.add(addWriter)
        db_session.add(addPlatform)
        db_session.add(addGenre)
        db_session.add(addDay)
        db_session.commit()
    except:
        db_session.rollback()
        db_session.query(WebtoonTable).filter(WebtoonTable.webtoonId == WebtoonVO.webtoonId).delete()
        db_session.commit()

def insertEpisode(EpisodeVO):
    addEpisode = EpisodeTable(EpisodeVO)
    db_session.add(addEpisode)
    db_session.commit()

def insertEpisodeList(episodeList):
    #에피소드 리스트 Insert
    for EpisodeVO in episodeList:
        addEpisode = EpisodeTable(EpisodeVO)
        db_session.add(addEpisode)
        db_session.commit()

def insertCrawlList(WebtoonVO, day):
    #getWebtoonList에서 만들어진 List를 Crawlist에 추가

    addCrawllist = CrawllistTable(WebtoonVO.webtoonId, WebtoonVO.webtoonName, WebtoonVO.lastDate, "None", WebtoonVO.platform, day)
    db_session.add(addCrawllist)
    db_session.commit()

def isWebtoonExist(platform, webtoonName):
    return db_session.query(WebtoonTable).join(PlatformTable, PlatformTable.platform==platform).filter(WebtoonTable.webtoonName == webtoonName).count()>0

def getWebtoonList(platform, day):
    #platForm이랑 day를 이용해서 해당 날자의 모든 webtoon을 List형태로 받아오기
    rows=[]
    webtoonVOlist=[]
    for row in db_session.query(WebtoonTable, PlatformTable, DayTable).distinct().join(PlatformTable, PlatformTable.platform == platform).filter(DayTable.day.like('%'+day+'%')).filter(and_(WebtoonTable.webtoonId == DayTable.webtoonId), (WebtoonTable.webtoonId == PlatformTable.webtoonId)):
        rows.append(row)
    for list in rows:
        VO = WebtoonVO(list[1].platform, list[2].day, list[0].webtoonId, list[0].webtoonName, "", list[0].webtoonThumbnail_s, list[0].webtoonThumbnail_m, list[0].webtoonThumbnail_b, list[0].webtoonIntroduce, "", list[0].isNew, list[0].lastDate)
        webtoonVOlist.append(VO)
    return webtoonVOlist

def getWebtoonCount(platform, day):
    #해당 날짜의 웹툰의 총갯수
    return db_session.query(WebtoonTable.webtoonId).distinct().join(PlatformTable, PlatformTable.platform == platform).join(DayTable, DayTable.day == day).count()

def getEpisodeList(webtoonId):
    #웹툰VO.id로 select * from episode where webtoonid = 웹툰VO.id 를 이용해 lastEpisode 반환받기
    rows=[]
    webtoonVOlist=[]
    for row in db_session.query(EpisodeTable).filter(EpisodeTable.webtoonId == webtoonId).order_by(EpisodeTable.episodeTimestamp.asc()):
        rows.append(row)
    return rows

def getCrawlList(platform):
    #select  * from crawllist 한 후에 crawlVO를 이용해서 list 형태로 반환받기
    rows=[]
    crawlVOlist = []
    for row in db_session.query(CrawllistTable).filter(CrawllistTable.platform == platform):
        rows.append(row)
    for list in rows:
        vo = CrawllistVO(list.webtoonId, list.webtoonName, list.lastDate, list.lastEpisode, list.platform, list.day)
        crawlVOlist.append(vo)
    return crawlVOlist

def getEpisodeCount(webtoonId):
    return db_session.query(EpisodeTable.webtoonId).filter(EpisodeTable.webtoonId == webtoonId).count()
    
def getLastEpisode(webtoonId):
    #웹툰VO.id로 select * from episode where webtoonid = 웹툰VO.id 를 이용해 lastEpisode 반환받기
    rows = []
    for row in db_session.query(EpisodeTable).filter(EpisodeTable.webtoonId == webtoonId).order_by(EpisodeTable.episodeNo.desc()).limit(1):
        rows.append(row)
    for list in rows:
        vo = EpisodeVO(list[0].webtoonId, list[0].episodeId, list[0].episodeName,  list[0].episodeThumbnail_s, list[0].episodeThumbnail_m, list[0].episodeThumbnail_b, list[0].episodeLink, list[0].episodeDate, list[0].charge, list[0].episodeTimestamp)
        if vo is not None:
            return vo
        else:
            return None

def deleteWebtoon(webtoonId):
    db_session.query(WebtoonTable).filter(WebtoonTable.webtoonId == webtoonId).delete()
    db_session.commit()

def deleteCrawlist(webtoonId, day):
    #crawlist에서 webtoon한개 삭제
    db_session.query(CrawllistTable).filter(CrawllistTable.webtoonId == webtoonId).filter(CrawllistTable.day == day).delete()
    db_session.commit()

def deleteEpisode(webtoonId):
    db_session.query(EpisodeTable).filter(EpisodeTable.webtoonId == webtoonId).delete()
    db_session.commit()

def deleteAllEpisode(webtoonId):
    print("전체삭제")

def updateisNew(WebtoonVO):
    q = db_session.query(WebtoonTable).filter(WebtoonTable.webtoonId == WebtoonVO.webtoonId)
    record = q.one()
    record.isNew = WebtoonVO.isNew
    db_session.commit()

def updateCharge(EpisodeVO, charge):
    #에피소드 유료 int 변환
    print("%s akakakakakakakka"%EpisodeVO.episodeId)

    q = db_session.query(EpisodeTable).filter(EpisodeTable.episodeId == EpisodeVO.episodeId)
    
    record = q.one()
    record.charge = charge
    db_session.commit()

def updateGenre(GenreVO):
    # update genre set genre="~~~" where webtoonId=105767
    q = db_session.query(GenreTable).filter(GenreTable.webtoonId == GenreVO.webtoonId)
    record = q.one()
    record.genre = GenreVO.genre
    db_session.commit()

def updateDay(WebtoonVO):
    # update day  set day="완결" where webtoonId=105767;
    q = db_session.query(DayTable).filter(DayTable.webtoonId == WebtoonVO.webtoonId)
    record = q.one()
    record.day = WebtoonVO.day
    db_session.commit()

def isCrawlExist(webtoonId, day):
    return db_session.query(CrawllistTable).filter(and_(CrawllistTable.webtoonId == webtoonId, CrawllistTable.day == day)).count()

def getWebtoonDay(platform, webtoonName):
    return db_session.query(DayTable.day).distinct().filter(WebtoonTable.webtoonId == DayTable.webtoonId).filter(WebtoonTable.webtoonName == webtoonName).filter(PlatformTable.platform == platform)[0][0]

def getWebtoonVO(platform, webtoonName):
    rows = []
    for row in db_session.query(WebtoonTable, DayTable).join(PlatformTable, PlatformTable.platform==platform).filter(WebtoonTable.webtoonName == webtoonName).filter(WebtoonTable.webtoonId == DayTable.webtoonId):
        rows.append(row)
    for list in rows:
        vo = WebtoonVO(platform, list[1].day, list[0].webtoonId, list[0].webtoonName, "",  list[0].webtoonThumbnail_s, list[0].webtoonThumbnail_m, list[0].webtoonThumbnail_b, list[0].webtoonIntroduce, "", list[0].isNew, list[0].lastDate)
    
        if vo is not None:
            return vo
        else:
            return None

def getThumbnail():
    thumbnail = []
    for row in db_session.query(WebtoonTable.webtoonThumbnail, WebtoonTable.webtoonId).filter(WebtoonTable.webtoonId == PlatformTable.webtoonId).filter(PlatformTable.platform == "Naver"):
        thumbnail.append(row)
    return thumbnail
