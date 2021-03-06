# coding:utf-8
import sys
import time
import urllib.parse
import video_parse
import random
#from db.db_insert import
from datetime import datetime 
import datetime as measure_datetime
import pytz
from xml.etree import ElementTree
from db.db_select import new_videoid_select
from db.db_insert import db_regist, db_regist_novideo

"""
現在新しく投稿されている動画IDを取得する(smXXXXXXXX,soXXXXXXXX,nmXXXXXXXX)
@returns {str} - 最新の動画ID
"""
def new_video_search():
        keyword_set = "アニメ OR ゲーム OR 実況プレイ動画 OR 東方 OR アイドルマスター OR ラジオ OR 描いてみた OR TRPG OR\
                    エンターテイメント OR 音楽 OR 歌ってみた OR 演奏してみた OR 踊ってみた OR VOCALOID OR ニコニコインディーズ OR ASMR OR MMD OR バーチャル OR\
                    動物 OR 料理 OR 自然 OR 旅行 OR スポーツ OR ニコニコ動画講座 OR 車載動画 OR 歴史 OR 鉄道 OR\
                    科学 OR ニコニコ技術部 OR ニコニコ手芸部 OR 作ってみた OR\
                    政治 OR\
                    例のアレ OR その他 OR 日記"
        # カテゴリタグから最新の動画をJSON形式で取得
        new_video_url = 'https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search?q=' + urllib.parse.quote(keyword_set) + '&targets=tagsExact&fields=contentId&_sort=' + urllib.parse.quote("-") + 'startTime&_limit=100'
        # JSON形式からreadできる形式に変換
        json_video = video_parse.Json_VideoData(new_video_url)
        json_video_data = json_video.video_parse()
        # parseして動画IDを返す
        return json_video_data['data'][0]['contentId']


"""
最新動画IDから動画IDを順序通りに取得する(smXXXXXXXX,soXXXXXXXX,nmXXXXXXXX)
@param {str} videoID 動画ID
"""
def video_search(videoID, new_regist_videoid=0):
    while True:
        # 動画IDの形式(sm,so,nm)を切り取る
        # videoID = videoID[2:]
        if new_regist_videoid == 0:
            # 更新した日時が一番新しい動画IDを取得する
            new_regist_videoid = new_videoid_select()

        novideo_count = 0
        # new_regist_videoidに動画IDの情報があればそのIDから取得開始、なければ動画ID1から取得開始
        if new_regist_videoid == None or new_regist_videoid == "":
            for i in range(20000001, int(videoID)):                
                format_rand_videoID = format_video_search(i)

                if format_rand_videoID == "novideo":
                    novideo_count += 1
                    if novideo_count >= 10000:
                        break
                    # 以前動画情報が登録してあればDBに状態を登録
                    # db_regist_novideo(str(i))
                    continue
                else:
                    novideo_count = 0
                    print ("------------------------------")
                    print(format_rand_videoID + str(i))
                    # 動画ID取得したらDBに登録
                    db_regist(format_rand_videoID + str(i))

                ### 04:00まで実行する為に時間測定(本番環境用) ###
                dt = measure_datetime.datetime.now()
                date_now = str(dt.hour) + ':' + str(dt.minute)
                print(date_now)
                if (date_now == "4:0" or date_now == "4:1" or date_now == "4:2" or date_now == "4:3" or 
                date_now == "4:4" or date_now == "4:5" or date_now == "4:6" or date_now == "4:7" or 
                date_now == "4:8" or date_now == "4:9" or date_now == "4:10"):
                    sys.exit()

            new_regist_videoid = 20000001
        else:    
            for i in range(int(new_regist_videoid), int(videoID)):
                format_rand_videoID = format_video_search(i)

                if format_rand_videoID == "novideo":
                    novideo_count += 1
                    if novideo_count >= 10000:
                        break
                    # 以前動画情報が登録してあればDBに状態を登録
                    # db_regist_novideo(str(i))
                    continue
                else:
                    novideo_count = 0
                    print ("------------------------------")
                    print(format_rand_videoID + str(i))
                    # 動画ID取得したらDBに登録
                    db_regist(format_rand_videoID + str(i))
                    
                ### 04:00まで実行する為に時間測定(本番環境用) ###
                dt = measure_datetime.datetime.now()
                date_now = str(dt.hour) + ':' + str(dt.minute)
                print(date_now)
                if (date_now == "4:0" or date_now == "4:1" or date_now == "4:2" or date_now == "4:3" or 
                date_now == "4:4" or date_now == "4:5" or date_now == "4:6" or date_now == "4:7" or 
                date_now == "4:8" or date_now == "4:9" or date_now == "4:10"):
                    sys.exit()

            new_regist_videoid = 20000001

"""
動画IDから形式を取得する(sm,so,nm)
@param {str} videoID 形式を省いた動画ID
@returns {str} 取得した形式(取得できなかったら消去・非公開にされているため、"novideo"を返す)
"""
def format_video_search(videoID):
    # XML形式からreadできる形式に変換
    sm_xml_video = video_parse.XML_VideoData("http://ext.nicovideo.jp/api/getthumbinfo/sm", str(videoID))
    so_xml_video = video_parse.XML_VideoData("http://ext.nicovideo.jp/api/getthumbinfo/so", str(videoID))
    nm_xml_video = video_parse.XML_VideoData("http://ext.nicovideo.jp/api/getthumbinfo/nm", str(videoID))

    sm_root = sm_xml_video.video_parse()
    so_root = so_xml_video.video_parse()
    nm_root = nm_xml_video.video_parse()

    # 形式がsmか判定
    if "sm" in str(sm_root[0][0].text):
        return "sm"
    else:
        video_no_found = "novideo"
    # 形式がsoか判定
    if "so" in str(so_root[0][0].text):
        return "so"
    else:
        video_no_found = "novideo"
    # 形式がnmか判定
    if "nm" in str(nm_root[0][0].text):
        return "nm"
    else:
        video_no_found = "novideo"
    
    return video_no_found


class Video_Eval:
    def __init__(self, videoID):
        # XML形式からreadできる形式に変換
        xml_video = video_parse.XML_VideoData("http://ext.nicovideo.jp/api/getthumbinfo/", str(videoID))
        xml = xml_video.video_parse()
        self.xml = xml
    # XML形式から取得した投稿日付を日付型に変換 (xml[0][4].text: %Y-%m-%dT%H:%M:%S+09:00 -> %Y-%m-%d %H:%M:%S)
    def date_video(self):
        date = self.xml[0][4].text
        date = date[:-6]
        date = date.replace('T', ' ') 
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return date
    # XML形式から取得した時間を取得
    def time_video(self):
        time = self.xml[0][5].text
        # 時間が0の場合は0で返す
        if time == "0":
            time = 0
            return time
        else:
            m, s = [int(i) for i in time.split(':')]
            time = 60*m + s
            return time
    # XML形式から投稿者IDを取得する
    def contributor_id_video(self):
        contributor_id = int(self.xml[0][19].text)
        return contributor_id
    # XML形式から投稿者の名前を取得する
    def contributor_video(self):
        return self.xml[0][20].text
    # XML形式からタイトル取得する
    def title_video(self):
        return self.xml[0][1].text
    # XML形式から再生数取得する
    def view_video(self):
        view = int(self.xml[0][9].text)
        return view
    # XML形式からコメント数取得する
    def comment_video(self):
        comment = int(self.xml[0][10].text)
        return comment
    # XML形式からマイリスト数取得する
    def mylist_video(self):
        mylist = int(self.xml[0][11].text)
        return mylist
    # XML形式からタグをリストに格納する
    def tag_video(self):
        video_tags = list()
        # 登録タグが見つからない場合
        if self.xml[0][17] == None or self.xml[0][17] == "":
            tmp_tag = "No category"
            video_tags.append(str(tmp_tag))
            return video_tags
        # 11個まで登録タグをリストに格納する
        else:
            for i in range(0, len(self.xml[0][17])):
                if i > 11:
                    return video_tags
                tmp_tag = self.xml[0][17][i].text
                video_tags.append(str(tmp_tag))
            return video_tags