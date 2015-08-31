# coding: utf-8

import urllib2,json
from requests_oauthlib import OAuth1Session
import os
import bitly

if os.path.exists('livejson') is False:
        os.mkdir('livejson')

jsonurl = 'http://livetube.cc/index.live.json'

r = urllib2.urlopen(jsonurl)

root = json.loads(r.read())

def livetweet(title,liveurl):
    CK = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'                             # Consumer Key
    CS = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'         # Consumer Secret
    AT = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # Access Token
    AS = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'         # Accesss Token Secert

    bitlylogin = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    apikey = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    #bitly認証
    bitly_api = bitly.Api(login=bitlylogin, apikey=apikey)

    # ツイート投稿用のURL
    url_media = "https://upload.twitter.com/1.1/media/upload.json"
    url_text = "https://api.twitter.com/1.1/statuses/update.json"

    # OAuth認証で POST method で投稿
    twitter = OAuth1Session(CK, CS, AT, AS)

    short_url = bitly_api.shorten(liveurl)
    req = twitter.post(url_text, params = {"status":  u"【配信開始】" + title + "\n" + short_url})

    # レスポンスを確認
    if req.status_code == 200:
        print ("OK")
    else:
        print ("Error: %d" % req.status_code)

# 画像のダウンロード
def imgdownload(url):
    img = urllib2.urlopen(url)
    f = open("thumbnail.jpg", "wb")
    f.write(img.read())
    f.close()

for entry in xrange(len(root)):
    if root[entry]['author'] == u'配信者名':
        entrynum = entry
        entryid = root[entry]['id']

        if os.path.exists('livejson\live.json') is False:
            f = open("livejson\live.json", "w")
            dict = {"author": "","id": "","link":"","title":""}
            json.dump(dict, f, sort_keys=True, indent=4)
            f.close()

        with open('livejson\live.json', 'r') as f:
            fenrifja_dic = json.load(f)

        if fenrifja_dic['id'] == entryid:
            f.close()
            exit()

        elif fenrifja_dic['id'] != entryid:
            with open('livejson\live.json', 'w') as f:
                json.dump(root[entry], f, sort_keys=True, indent=4)
                f.close()

            title = root[entry]['title']
            liveurl = 'http://livetube.cc/' + root[entry]['link']

            livetweet(title,liveurl)



