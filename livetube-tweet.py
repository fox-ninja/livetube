# coding: utf-8

from urllib2 import urlopen, URLError
from requests_oauthlib import OAuth1Session
import os,json
import bitly

if os.path.exists('livejson') is False:
        os.mkdir('livejson')

jsonurl = 'http://livetube.cc/index.live.json'

r = urlopen(jsonurl)

root = json.loads(r.read())

def twitterAPIkey():
    f = open('livejson\confg.json','r')
    key = json.load(f)
    f.close()

    return(key)

#サムネイルなしのツイート
def livetweet(title,liveurl,tags):
    key = twitterAPIkey()

    bitlylogin = 'XXXXXXXXXXXXXXXXXXXXXX'
    apikey = 'XXXXXXXXXXXXXXXXXXXXXX'

    #bitly認証
    bitly_api = bitly.Api(login=bitlylogin, apikey=apikey)

    # ツイート投稿用のURL
    url_text = "https://api.twitter.com/1.1/statuses/update.json"

    # OAuth認証で POST method で投稿
    twitter = OAuth1Session(key['CK'], key['CS'], key['AT'], key['AS'])

    #タグ整形
    tag = "".join([" #" + v for v in tags])

    short_url = bitly_api.shorten(liveurl)
    req = twitter.post(url_text, params = {"status":  u"【配信開始】" + title + tag + "\n" + short_url})
    print u"【配信開始】" + title + tag + "\n" + short_url

    # レスポンスを確認
    if req.status_code == 200:
        print ("サムネなしOK")
    else:
        print ("Error: %d" % req.status_code)

#サムネイルありのツイート
def livetweet_with_image(title,liveurl,tags):
    key = twitterAPIkey()

    bitlylogin = 'XXXXXXXXXXXXXXXXXXXXXX'
    apikey = 'XXXXXXXXXXXXXXXXXXXXXX'

    #bitly認証
    bitly_api = bitly.Api(login=bitlylogin, apikey=apikey)

    # ツイート投稿用のURL
    url_media = "https://upload.twitter.com/1.1/media/upload.json"
    url_text = "https://api.twitter.com/1.1/statuses/update.json"

    # OAuth認証で POST method で投稿
    twitter = OAuth1Session(key['CK'], key['CS'], key['AT'], key['AS'])

    # 画像投稿
    files = {"media" : open('thumbnail.jpg', 'rb')}
    req_media = twitter.post(url_media, files = files)

    # レスポンスを確認
    if req_media.status_code != 200:
        print ("画像アップデート失敗: %s", req_media.text)
        exit()

    # Media ID を取得
    media_id = json.loads(req_media.text)['media_id']

    short_url = bitly_api.shorten(liveurl)

    #タグ整形
    tag = "".join([" #" + v for v in tags])

    # Media ID を付加してテキストを投稿
    params = {'status': u"【配信開始】" + title + tag + "\n" + short_url , "media_ids": [media_id]}
    #req = twitter.post(url_text, params = {"status":  u"【サムネあり】201509080847"})
    req_media = twitter.post(url_text, params = params)

    # レスポンスを確認
    if req_media.status_code == 200:
        print ("サムネありOK")

    else:
        print ("テキストアップデート失敗: %s", req_media.status_code)
        exit()

# 画像のダウンロード
def imgdownload(title,id,link,tags):
    url = 'http://livetube.cc/stream/' + id + '.snapshot.jpg'
    liveurl = 'http://livetube.cc/' + link

    try:
        img = urlopen(url)
        f = open("thumbnail.jpg", "wb")
        f.write(img.read())
        f.close()
        livetweet_with_image(title,liveurl,tags)
    except URLError, e:
        livetweet(title,liveurl,tags)


for entry in xrange(len(root)):
    if root[entry]['author'] == u'配信者名':
        entrynum = entry
        entryid = root[entry]['id']

        if os.path.exists('livejson\live.json') is False:
            f = open("livejson\live.json", "w")
            dict = {"author": "","id": "","link":"","title":""}
            json.dump(dict, f, sort_keys=True, indent=4)
            f.close()

        f = open('livejson\live.json', 'r')
        live_json = json.load(f)

        if live_json['id'] == entryid:
            f.close()
            exit()

        elif live_json['id'] != entryid:
            f.close()

            with open('livejson\live.json', 'w') as f:
                json.dump(root[entry], f, sort_keys=True, indent=4)
                f.close()


            title = root[entry]['title']
            link = root[entry]['link']
            id = root[entry]['id']
            tags = root[entry]['tags']

            imgdownload(title,id,link,tags)



