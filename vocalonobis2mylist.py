#!/usr/bin/env python3

import sys, urllib.request, urllib.parse, urllib.error, http.cookiejar, time, json, os
import xml.etree.ElementTree as ET


REQUEST_HEADER = {
    "X-Frontend-Id": "6",
    "X-Frontend-Version": "0",
    "X-Request-With": "https://www.nicovideo.jp",
}


def get_ranking(mode):
    if mode == "daily":
        type = "1"
    elif mode == "weekly":
        type = "2"
    elif mode == "monthly":
        type = "3"
    else:
        sys.exit(1)

    rss = urllib.request.urlopen(
        "http://nobis.work/vocalo/feed/?type=" + type + "&pages=1"
    )
    tree = ET.parse(rss)
    return [
        {
            "title": item.find("title").text,
            "smid": item.find("link").text.rsplit("/", 1)[-1],
        }
        for item in tree.findall("./channel/item")
    ]


def login(userid, passwd):
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
    )
    urllib.request.install_opener(opener)
    urllib.request.urlopen(
        "https://secure.nicovideo.jp/secure/login",
        urllib.parse.urlencode({"mail": userid, "password": passwd}).encode("utf-8"),
    )


def mylist_list(mid):
    cmdurl = f"https://nvapi.nicovideo.jp/v1/users/me/mylists/{mid}?pageSize=100&page=1"
    req = urllib.request.Request(cmdurl, headers=REQUEST_HEADER)
    doc = urllib.request.urlopen(req)
    j = json.load(doc, encoding="utf8")
    return j["data"]["mylist"]["items"]


def mylist_clear(mid):
    id_list = [item["itemId"] for item in mylist_list(mid)]
    if len(id_list) <= 0:
        return
    cmdurl = f"https://nvapi.nicovideo.jp/v1/users/me/mylists/{mid}/items"
    cmdurl += "?" + urllib.parse.urlencode({"itemIds": ",".join(map(str, id_list))})
    req = urllib.request.Request(cmdurl, method="DELETE", headers=REQUEST_HEADER)
    urllib.request.urlopen(req)


def mylist_add(mid, smid, desc):
    cmdurl = f"https://nvapi.nicovideo.jp/v1/users/me/mylists/{mid}/items"
    q = {}
    q["itemId"] = smid
    q["description"] = desc
    cmdurl += "?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(cmdurl, method="POST", headers=REQUEST_HEADER)
    urllib.request.urlopen(req)


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    if argc < 2:
        print("error: no mylist given")
        sys.exit(1)
    else:
        mid = argv[1]

        if argc == 2:
            mode = "daily"
        elif argv[2] in ["daily", "weekly", "monthly"]:
            mode = argv[2]
        else:
            print("invalid mode: %s" % argv[2])
            sys.exit(1)

    # ランキング取得
    rank = get_ranking(mode)

    # ログイン
    userid = os.environ.get("V2M_USERID")
    passwd = os.environ.get("V2M_PASSWD")
    login(userid, passwd)

    # マイリストから動画を全削除
    print("clearing mylist...")
    mylist_clear(mid)

    # マイリストに動画を登録
    for i, item in enumerate(rank):
        time.sleep(1)
        print(f"adding rank {i + 1:03}: {item['smid']}\t{item['title']}")
        mylist_add(mid, item["smid"], f"{i + 1:03}")
