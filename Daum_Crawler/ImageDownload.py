import urllib.request
import os
import boto3
import Constants

def download_webttoonImg(url, name):
    full_name = "daum_"+str(name) + ".jpg"
    path = Constants.WEBTOON_PATH
    name = os.path.join(path, full_name)
    print("파일 다운 시작" + name)
    urllib.request.urlretrieve(url, name)
    
    return full_name

def download_EpisodeImg(url, webtoonId, name):
    full_name = "daum_"+webtoonId+"_"+str(name) + ".jpg"
    path = Constants.EPISODE_PATH
    name = os.path.join(path, full_name)
    print("파일 다운 시작" + name)
    urllib.request.urlretrieve(url, name)

    return full_name

def sendEpisodeImg(q):
    print('s3로 이미지 보내기')
    path = Constants.EPISODE_PATH
    filenames = os.listdir(path)
    url = Constants.S3_URL
    sizeList=['small_200x200.jpg', 'middle_400x400.jpg','big_600x600.jpg']
    s3 = boto3.resource('s3')
    bucket = "original-inco"
    urlList = []

    for i in filenames:
        if(i == '.DS_Store'):
            continue
        array = i.split('_')
        print('주소 = %s'%url)
        files = open(path+'/'+i, 'rb')
        s3.Bucket('inco-original').put_object(Key=i, Body=files)

        for j in range(0, 3):
            urlList.append(Constants.S3_URL + '%s/%s/%s'%(array[1],array[2].split('.')[0],sizeList[j]))

        files.close()
        print('삭제합니다.')
        os.remove(path + '/' + i)
        print('삭제 완료되었습니다.')
        
        return urlList


 # 테스트용으로 주석 나중에 풀어야됨 
def sendWebtoonImg(temp):
    # print('s3로 이미지 보내기')
    path = Constants.WEBTOON_PATH
    filenames = os.listdir(path)
    url = Constants.S3_URL
    sizeList=['small_200x200.jpg', 'middle_400x400.jpg','big_600x600.jpg']

    # s3 = boto3.resource('s3')
    # bucket = "original-inco"
    urlList = []

    for i in filenames:
        if(i == '.DS_Store'):
            continue
        print("이미자 아아아아아 %s" %i)
        array = i.split('_')
        
        print('주소 = %s'%url)
        # files = open(path+'/'+i, 'rb')
        # s3.Bucket('inco-original').put_object(Key=i, Body=files)

        for j in range(0, 3):
            urlList.append(Constants.S3_URL+'%s/%s' %(array[1].split('.')[0], sizeList[j]))
        # files.close()
        # print('삭제합니다.')
        # os.remove(path + '/' + i)
        # print('삭제 완료되었습니다.')
        print("s3 안보냈지롱~")
        
        return urlList




