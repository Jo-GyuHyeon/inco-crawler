# platform, webtoon, webtoon_info, writer 관련 Table객체
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from GetConnection import Base
from sqlalchemy.sql import func


class WebtoonTable(Base):
    __tablename__ = 'webtoon'
    webtoonId = Column(String, primary_key=True)
    webtoonName = Column(String)
    webtoonThumbnail_s = Column(String)
    webtoonThumbnail_m = Column(String)
    webtoonThumbnail_b = Column(String)
    webtoonIntroduce = Column(String)
    isNew = Column(TINYINT)
    lastDate = Column(Date)

    def __init__(self, WebtoonVO):
        self.webtoonId = WebtoonVO.webtoonId
        self.webtoonName = WebtoonVO.webtoonName
        self.webtoonThumbnail_s = WebtoonVO.webtoonThumbnail_s
        self.webtoonThumbnail_m = WebtoonVO.webtoonThumbnail_m
        self.webtoonThumbnail_b = WebtoonVO.webtoonThumbnail_b
        self.isNew = WebtoonVO.isNew
        self.lastDate = WebtoonVO.lastDate
        self.webtoonIntroduce = WebtoonVO.webtoonIntroduce


class WriterTable(Base):
    __tablename__ = 'writer'
    webtoonId = Column(String, primary_key=True)
    writer = Column(String)

    def __init__(self, WebtoonVO):
        self.webtoonId = WebtoonVO.webtoonId
        self.writer = WebtoonVO.writer


class PlatformTable(Base):
    __tablename__ = 'platform'
    webtoonId = Column(String, primary_key=True)
    platform = Column(String)

    def __init__(self, WebtoonVO):
        self.webtoonId = WebtoonVO.webtoonId
        self.platform = WebtoonVO.platform


class GenreTable(Base):
    __tablename__ = 'genre'
    webtoonId = Column(String, primary_key=True)
    genre = Column(String)

    def __init__(self, WebtoonVO):
        self.webtoonId = WebtoonVO.webtoonId
        self.genre = WebtoonVO.genre


class DayTable(Base):
    __tablename__ = 'day'
    webtoonId = Column(String, primary_key=True)
    day = Column(String)

    def __init__(self, WebtoonVO):
        self.webtoonId = WebtoonVO.webtoonId
        self.day = WebtoonVO.day


class EpisodeTable(Base):
    __tablename__ = 'episode'
    episodeNo = Column(String, primary_key=True)
    webtoonId = Column(String, primary_key=True)
    episodeId = Column(String)
    episodeName = Column(String)
    episodeThumbnail_s = Column(String)
    episodeThumbnail_m = Column(String)
    episodeThumbnail_b = Column(String)
    episodeLink = Column(String)
    episodeDate = Column(Date)
    episodeTimestamp = Column(DateTime(6), server_default=func.now(6))
    charge = Column(String)

    def __init__(self, EpisodeVO):
        self.webtoonId = EpisodeVO.webtoonId
        self.episodeId = EpisodeVO.episodeId
        self.episodeName = EpisodeVO.episodeName
        self.episodeThumbnail_s = EpisodeVO.episodeThumbnail_s
        self.episodeThumbnail_m = EpisodeVO.episodeThumbnail_m
        self.episodeThumbnail_b = EpisodeVO.episodeThumbnail_b
        self.episodeLink = EpisodeVO.episodeLink
        self.episodeDate = EpisodeVO.episodeDate
        self.charge = EpisodeVO.charge


class CrawllistTable(Base):
    __tablename__ = 'crawllist'
    webtoonId = Column(String, primary_key=True)
    webtoonName = Column(String)
    lastDate = Column(DateTime)
    lastEpisode = Column(String)
    platform = Column(String)
    day = Column(String, primary_key=True)

    def __init__(self, webtoonId, webtoonName, lastDate, lastEpisode, platform, day):
        self.webtoonId = webtoonId
        self.webtoonName = webtoonName
        self.lastDate = lastDate
        self.lastEpisode = lastEpisode
        self.platform = platform
        self.day = day
