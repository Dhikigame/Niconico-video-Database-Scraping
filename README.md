# Niconico-video-Database-Scraping

ニコニコ動画の情報を集めるデータベースを更新し続けるスクリプト

A script that keeps updating the database that collects information on Nico Nico Douga

# DEMO

以下は出力されるログとDB内の内容

The following is the output log and the contents in the DB

<img width="991" alt="スクリーンショット 2021-04-11 午前2 23 24" src="https://user-images.githubusercontent.com/12876144/114278933-f60b1900-9a6c-11eb-85c6-db1a2e741772.png">
<img width="1050" alt="スクリーンショット 2021-04-11 午前2 49 01" src="https://user-images.githubusercontent.com/12876144/114279741-23f25c80-9a71-11eb-8938-d2b07402923e.png">

# Requirement
* Python3
* SQLite3
* niconicoAPI
  * getthumbinfo
  * スナップショット検索API v2 (https://site.nicovideo.jp/search-api-docs/snapshot)

### Operating environment
* Amazon Lightsail
* CentOS7
* Portainer
* Docker
  * docker-compose


# Features

- 動画IDの若い順から順に動画データの情報を取得していく
- 以下のような動画データを取得する
  - 動画ID(smXXX,soXXX,nmXXX)
  - タイトル
  - 再生数
  - コメント数
  - マイリスト数
  - 動画データ更新日
  - 動画投稿日
  - タグ(11個)
  - 投稿者ID
  - 投稿者名
  - 総合ポイント(広告ポイント抜き)
  - 投稿者のフォロー数
  - 投稿者のフォロワー数
  - 動画再生時間


# Usage
```bash
yum install -y python3 python3-libs python3-devel python3-pip
pip3.6 install python-twitter requests pytz bs4
cp -f /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
```


# Author
* Dhiki(Infrastructure engineer & Video contributor)
* https://twitter.com/DHIKI_pico


# License
ご自由に使用いただいて構いません。

Feel free to use it.
