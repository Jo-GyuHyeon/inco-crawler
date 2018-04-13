class WebtoonVO():

    def __init__(self, platform, day, webtoonId, webtoonName, writer, webtoonThumbnail_s,webtoonThumbnail_m, webtoonThumbnail_b, webtoonIntroduce, genre, isNew,
                 lastDate):
        self.__webtoonId = webtoonId
        self.__webtoonName = webtoonName
        self.__webtoonThumbnail_s = webtoonThumbnail_s
        self.__webtoonThumbnail_m = webtoonThumbnail_m
        self.__webtoonThumbnail_b = webtoonThumbnail_b
        self.__isNew = isNew
        self.lastDate = lastDate
        self.__webtoonIntroduce = webtoonIntroduce
        self.__writer = writer
        self.__platform = platform
        self.__genre = genre
        self.__day = day

    @property
    def webtoonId(self):
        return self.__webtoonId

    @webtoonId.setter
    def webtoonId(self, webtoonId):
        self.__webtoonId = webtoonId

    @property
    def webtoonName(self):
        return self.__webtoonName

    @webtoonName.setter
    def webtoonName(self, webtoonName):
        self.__webtoonName = webtoonName

    @property
    def webtoonThumbnail_s(self):
        return self.__webtoonThumbnail_s

    @webtoonThumbnail_s.setter
    def webtoonThumbnail_s(self, webtoonThumbnail_s):
        self.__webtoonThumbnail_s = webtoonThumbnail_s

    @property
    def webtoonThumbnail_m(self):
        return self.__webtoonThumbnail_m

    @webtoonThumbnail_m.setter
    def webtoonThumbnail_m(self, webtoonThumbnail_m):
        self.__webtoonThumbnail_m = webtoonThumbnail_m

    @property
    def webtoonThumbnail_b(self):
        return self.__webtoonThumbnail_b

    @webtoonThumbnail_b.setter
    def webtoonThumbnail_b(self, webtoonThumbnail_b):
        self.__webtoonThumbnail_b = webtoonThumbnail_b

    @property
    def isNew(self):
        return self.__isNew

    @isNew.setter
    def isNew(self, isNew):
        self.__isNew = isNew

    @property
    def lastDate(self):
        return self.__lastDate

    @lastDate.setter
    def lastDate(self, lastDate):
        self.__lastDate = lastDate

    @property
    def webtoonIntroduce(self):
        return self.__webtoonIntroduce

    @webtoonIntroduce.setter
    def webtoonIntroduce(self, webtoonIntroduce):
        self.__webtoonIntroduce = webtoonIntroduce

    @property
    def writer(self):
        return self.__writer

    @writer.setter
    def writer(self, writer):
        self.__writer = writer

    @property
    def platform(self):
        return self.__platform

    @platform.setter
    def platform(self, platform):
        self.__platform = platform

    @property
    def genre(self):
        return self.__genre

    @genre.setter
    def genre(self, genre):
        self.__genre = genre

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day):
        self.__day = day

    @property
    def episodeList(self):
        return self.__episodeList

    @episodeList.setter
    def episodeList(self, episodeList):
        self.__episodeList = episodeList


class EpisodeVO():

    def __init__(self, webtoonId, episodeId, episodeName, episodeThumbnail_s, episodeThumbnail_m, episodeThumbnail_b, episodeLink, episodeDate, episodeTimestamp, charge):
        self.__webtoonId = webtoonId
        self.__episodeId = episodeId
        self.__episodeName = episodeName
        self.episodeThumbnail_s = episodeThumbnail_s
        self.episodeThumbnail_m = episodeThumbnail_m
        self.episodeThumbnail_b = episodeThumbnail_b
        self.__episodeLink = episodeLink
        self.__episodeDate = episodeDate
        self.__episodeTimestamp = episodeTimestamp
        self.__charge = charge

    @property
    def episodeNo(self):
        return self.__episodeNo

    @episodeNo.setter
    def episodeNo(self, episodeNo):
        self.__episodeNo = episodeNo

    @property
    def webtoonId(self):
        return self.__webtoonId

    @webtoonId.setter
    def webtoonId(self, webtoonId):
        self.__webtoonId = webtoonId

    @property
    def episodeId(self):
        return self.__episodeId

    @episodeId.setter
    def episodeId(self, episodeId):
        self.__episodeId = episodeId

    @property
    def episodeName(self):
        return self.__episodeName

    @episodeName.setter
    def episodeName(self, episodeName):
        self.__episodeName = episodeName

    @property
    def episodeThumbnail_s(self):
        return self.__episodeThumbnail_s

    @episodeThumbnail_s.setter
    def episodeThumbnail_s(self, episodeThumbnail_s):
        self.__episodeThumbnail_s = episodeThumbnail_s

    @property
    def episodeThumbnail_m(self):
        return self.__episodeThumbnail_m

    @episodeThumbnail_m.setter
    def episodeThumbnail_m(self, episodeThumbnail_m):
        self.__episodeThumbnail_m = episodeThumbnail_m

    @property
    def episodeThumbnail_b(self):
        return self.__episodeThumbnail_b

    @episodeThumbnail_b.setter
    def episodeThumbnail_b(self, episodeThumbnail_b):
        self.__episodeThumbnail_b = episodeThumbnail_b

    @property
    def episodeLink(self):
        return self.__episodeLink

    @episodeLink.setter
    def episodeLink(self, episodeLink):
        self.__episodeLink = episodeLink

    @property
    def episodeDate(self):
        return self.__episodeDate

    @episodeDate.setter
    def episodeDate(self, episodeDate):
        self.__episodeDate = episodeDate

    @property
    def episodeTimestamp(self):
        return self.__episodeTimestamp

    @episodeTimestamp.setter
    def episodeTimestamp(self, episodeTimestamp):
        self.__episodeTimestamp = episodeTimestamp

    @property
    def charge(self):
        return self.__charge

    @charge.setter
    def charge(self, charge):
        self.__charge = charge

    @property
    def count(self):
        return self.__count

    @charge.setter
    def count(self, count):
        self.__count = count


class CrawllistVO():

    def __init__(self, webtoonId, webtoonName, lastDate, lastEpisode, platform, day):
        self.__webtoonId = webtoonId
        self.__webtoonName = webtoonName
        self.__lastDate = lastDate
        self.__lastEpisode = lastEpisode
        self.__platform = platform
        self.__day = day

    @property
    def webtoonId(self):
        return self.__webtoonId

    @webtoonId.setter
    def webtoonId(self, webtoonId):
        self.__webtoonId = webtoonId

    @property
    def webtoonName(self):
        return self.__webtoonName

    @webtoonName.setter
    def webtoonName(self, webtoonName):
        self.__webtoonName = webtoonName

    @property
    def lastDate(self):
        return self.__lastDate

    @lastDate.setter
    def lastDate(self, lastDate):
        self.lastDate = lastDate

    @property
    def lastEpisode(self):
        return self.__lastEpisode

    @lastEpisode.setter
    def lastEpisode(self, lastEpisode):
        self.lastEpisode = lastEpisode

    @property
    def platform(self):
        return self.__platform

    @platform.setter
    def platform(self, platform):
        self.__platform = platform

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day):
        self.__day = day
