# vocalonobis2mylist-heroku

Heroku用、[VOCALONOBIS](http://vocalonobis.com/)の[RSS](http://vocalonobis.com/feed/?type=1&pages=1)から取得したデイリーランキングをマイリストに並べるスクリプト


## 使い方

1. Herokuにデプロイ
2. Config Variablesの設定でV2M_USERID、V2M_PASSWD、V2M_MID（順にユーザーID、パスワード、マイリストのIDナンバー）を設定
3. Heroku Schedulerあたりで毎日`python vocalonobis2mylist.py`するように設定
4. 設定した時間になるまで待つ


## 補足

実際に動かして作ったマイリストは[これ](http://www.nicovideo.jp/mylist/45420764)。

Pythonコードは７割方[ニコニコのマイリストAPIの使い方 - lolloo-htnの日記](http://d.hatena.ne.jp/lolloo-htn/20110115/1295105845)から引っ張ってきました。感謝。

なおご覧のとおり例外処理を一切していないのでご利用は自己責任にて。
あとニコニコプロフィールの「公開・非公開設定」でマイリスト登録をニコレポに通知しない設定にしないと100件の通知爆撃が起こるので注意。
