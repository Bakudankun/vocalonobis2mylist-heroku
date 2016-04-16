# vocalonobis2mylist-heroku

Heroku向け、[VOCALONOBIS](http://vocalonobis.com/)の[RSS](http://vocalonobis.com/feed/readme.html)から取得したデイリーランキングをマイリストに並べるスクリプト


## 使い方

1. Herokuにデプロイ
2. Config Variablesの設定で`V2M_USERID`、`V2M_PASSWD`（順にユーザーID、パスワード）を設定
3. 同じく`MID_DAILY`、`MID_WEEKLY`、`MID_MONTHLY`をそれぞれデイリー、ウィークリー、マンスリーランキング用マイリストのIDナンバーに設定
3. Heroku Schedulerあたりで毎日`daily``weekly``monthly`するように設定
4. 設定した時間になるまで待つ


## 補足

実際に動かして作ったマイリストはこちら。

- [デイリーランキング](http://www.nicovideo.jp/mylist/45420764)
- [ウィークリーランキング](http://www.nicovideo.jp/mylist/55502720)
- [マンスリーランキング](http://www.nicovideo.jp/mylist/55502735)

なおご覧のとおり例外処理を一切していないのでご利用は自己責任にて。
あとニコニコプロフィールの「公開・非公開設定」でマイリスト登録をニコレポに通知しない設定にしないと100件の通知爆撃が起こるので注意。
