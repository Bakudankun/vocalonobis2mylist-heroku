#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys, codecs, re, cgi, urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, http.cookiejar, xml.dom.minidom, time, json, os
userid=os.environ.get("V2M_USERID")
passwd=os.environ.get("V2M_PASSWD")


def getToken():
    html = urllib.request.urlopen("http://www.nicovideo.jp/my/mylist").read()
    for line in html.splitlines():
        mo = re.match(r'^\s*NicoAPI\.token = "(?P<token>[\d\w-]+)";\s*', line)
        if mo:
            token = mo.group('token')
            break
    assert token
    return token


def addvideo_tomylist(mid, item, desc):
    print("adding rank %s: %s\t%s" % (desc, item["smid"], item["title"]))
    cmdurl = "http://www.nicovideo.jp/api/mylist/add"
    q = {}
    q['group_id'] = mid
    q['item_type'] = 0
    q['item_id'] = item["smid"]
    q['description'] = desc
    q['token'] = token
    cmdurl += "?" + urllib.parse.urlencode(q)
    j = json.load( urllib.request.urlopen(cmdurl), encoding='utf8')


def clear_mylist(mid):
    j = json.load(urllib.request.urlopen("http://www.nicovideo.jp/api/mylist/list?group_id=" + str(mid)), encoding='utf8')
    id_list = []
    for item in j['mylistitem']:
        id_list.append(item['item_id'])
    cmdurl = "http://www.nicovideo.jp/api/mylist/delete?group_id=%s&token=%s" % ( mid, token )
    for item_id in id_list:
        cmdurl += "&" + urllib.parse.quote_plus( "id_list[0][]" ) + "=%s" % item_id
    k = json.load( urllib.request.urlopen(cmdurl), encoding='utf8')


def getRanking(mode):
    if mode == "daily" :
        type = "1"
    elif mode == "weekly" :
        type = "2"
    elif mode == "monthly" :
        type = "3"
    else :
        sys.exit(1)

    rss = urllib.request.urlopen("http://nobis.work/vocalo/feed/?type=" + type + "&pages=1")
    dom = xml.dom.minidom.parse(rss)
    rank = []
    for item in dom.getElementsByTagName("item"):
        rank.append({
            "title": item.getElementsByTagName("title")[0].firstChild.data,
            "smid": item.getElementsByTagName("link")[0].firstChild.data.rsplit('/', 1)[-1]
            })
    return rank


if __name__ == "__main__" :
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

    argv = sys.argv
    argc = len(argv)

    if argc < 2 :
        print("error: no mylist given")
        sys.exit(1)
    else :
        mid = argv[1]

        if argc == 2 :
            mode = "daily"
        elif argv[2] in ["daily", "weekly", "monthly"] :
            mode = argv[2]
        else :
            print("invalid mode: %s" % argv[2])
            sys.exit(1)

    #ランキング取得
    rank = getRanking(mode)

    #ログイン
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    urllib.request.install_opener(opener)
    urllib.request.urlopen("https://secure.nicovideo.jp/secure/login",
                    urllib.parse.urlencode( {"mail":userid, "password":passwd}) )

    #トークン取得
    token = getToken()

    #マイリストから動画を全削除
    clear_mylist(mid)

    #マイリストに動画を登録
    for i, item in enumerate(rank):
        addvideo_tomylist(mid, item, str(i+1).zfill(3) )
        time.sleep(1)
