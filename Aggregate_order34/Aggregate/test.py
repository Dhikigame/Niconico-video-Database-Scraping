import time
import video_parse


videoID = "sm9333876"

xml_video = video_parse.XML_VideoData("http://ext.nicovideo.jp/api/getthumbinfo/", str(videoID))
xml = xml_video.video_parse()
time = xml[0][5].text

if time == '0':
    print("okok")
# m, s = [int(i) for i in time.split(':')]
# time = 60*m + s