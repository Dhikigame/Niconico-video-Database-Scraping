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
            
        # ユーザーページの情報をjson形式で取得
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        userinfo = soup.find(id='js-initial-userpage-data').get('data-initial-data')
        userinfo_json = json.loads(userinfo)

        # ユーザ情報がNullの場合、リストを空で返す
        if userinfo_json['userDetails']['userDetails']['user'] is None:
            print("ユーザー退会済み、もしくはアカウント停止の可能性")
            return user

        # フォロー数とフォロワー数を取得する
        follow = userinfo_json['userDetails']['userDetails']['user']['followeeCount']
        user.append(int(follow))
        print('フォロー数　' ,follow)
        follower = userinfo_json['userDetails']['userDetails']['user']['followerCount']
        user.append(int(follower))
        print('フォロワー数' ,follower)

        return user