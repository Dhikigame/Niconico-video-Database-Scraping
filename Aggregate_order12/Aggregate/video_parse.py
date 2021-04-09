# coding:utf-8
import urllib.request
import urllib.parse
import requests
import bs4
import json
import xml.etree.ElementTree as ET
from http.client import RemoteDisconnected

"""
ニコニコ動画のWeb APIから動画情報をパースできる形式に変換
@param {str} url WebAPIのURL
@param {str} videoID 動画ID
@returns {list} - 動画情報をパースしたリスト
"""
class Json_VideoData:
    def __init__(self, url):
        self.url = url
    def video_parse(self):
        # JSON形式からreadしたものを返す
        readopen = urllib.request.urlopen(self.url)
        response = readopen.read()
        json_video_data = json.loads(response)

        return json_video_data

class XML_VideoData(Json_VideoData):
    def __init__(self, url, videoID):
        super().__init__(url)
        self.videoID = videoID
    def video_parse(self):
        # XML形式からreadし、タグ先頭の情報(動画ID,タイトル)を返す
        try:
            req = urllib.request.Request(self.url + self.videoID)
            with urllib.request.urlopen(req) as response:
                XmlData = response.read()
                root = ET.fromstring(XmlData)
            return root
        except RemoteDisconnected:
            print("ERROR：" + self.videoID)
            root = [["novideo"]]
            return root

class HTML_VideoData:
    def __init__(self, url):
        self.url = url
    def user_parse(self):
        # Userページからフォロワー数とフォロー数を返す
        user = list()

        res = requests.get(self.url)
        print('Userページステータス' ,res.status_code)
        if res.status_code == "404":
            follow = None
            user.append(follow)
            follower = None
            user.append(follower)

        # res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        elems = soup.select('.num')
        count = 0
        for elem in elems:
            if count == 0:
                follow = elem.string
                follow = follow.replace(',', '')
                user.append(int(follow))
                print('フォロー数　' ,follow)
            if count == 1:
                follower = elem.string
                follower = follower.replace(',', '')
                user.append(int(follower))
                print('フォロワー数' ,follower)
            count = count + 1
        return user
