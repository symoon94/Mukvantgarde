from datetime import datetime
import pandas as pd
import csv

def make_geo(geostring):

    geolist = geostring.strip("[]").split(", ")
    lon = geolist[0]
    lat = geolist[1]
    return lat, lon

def make_tag_dict(tagstring):
    tagdict = {}
    if tagstring == "[]":
        return tagdict
    taglist = tagstring.strip("[]").replace("'","").split(", ")
    i = 0
    while i < len(taglist):
        tagdict[taglist[i]] = 1
        i += 1
    return tagdict

def add_tag(tagdict, tagstring):
    if tagstring == []:
        return tagdict
    taglist = tagstring.strip("[]").replace("'", "").split(", ")
    i = 0
    while i < len(taglist):
        if taglist[i] in tagdict:
            tagdict[taglist[i]] += 1
        else:
            tagdict[taglist[i]] = 1
        i += 1
    return tagdict



def store_info(timelist, timedata, categories):
    for i, row in timedata.iterrows():

        new = True

        timedict = {}
        timedata = str(datetime.fromtimestamp(row["timestamp"])).split("-")
        timedict["yr_mo"] = timedata[0] + " " + timedata[1]

        title = row["naver_title"]
        if title in ["한성돈까스","다다미","산성대가","연경","사이공장","큰여","페이버릿","갓덴스시 강남점",
                     "카페스토리","김덕후의곱창조 홍대본점"]:
            import ipdb; ipdb.set_trace()

        timedict["naver_title"] = title

        adrs1 = row["naver_address"].split(" ")[1]
        adrs2 = row["naver_address"].split(" ")[2]
        timedict["adrs1"] = adrs1
        timedict["adrs2"] = adrs2

        categ = get_category(categories, row["category"])

        for i in range(len(timelist)):
            if timelist[i]["yr_mo"] == timedict["yr_mo"] and timelist[i][
                "adrs1"] == timedict["adrs1"] and timelist[i][
                "adrs2"] == timedict["adrs2"] and timelist[i]["naver_title"] ==\
                    timedict["naver_title"]:
                timelist[i]["post"] += 1
                timelist[i]["like"] += int(row.like)
                timelist[i]["tags"] = add_tag(timelist[i]["tags"], row.tags)
                new = False
                break
        if new:
            timedict["post"] = 1
            timedict["like"] = int(row.like)
            timedict["categ"] = categ
            timedict["lat"], timedict["lon"] = make_geo(row.geo)
            timedict["img_url"] = row.url
            timedict["tags"] = make_tag_dict(row.tags)
            timedict["naver_address"] = row.naver_address
            timedict["broadcastInfo"] = row.thumUrl


            timelist.append(timedict)

    return timelist


def get_category(categories, specific_categ):
    for x in categories:
        if x in specific_categ:
            return x


def main():
    timedata = pd.read_csv("timeorder_naver.csv")
    categories = ["중식", "카페,디저트", "술집", "분식", "멕시코,남미음식", "인도음식", "일식",
                  "양식", "한식", "브런치", "햄버거", "베트남음식", "특급호텔레스토랑", "패밀리레스토랑",
                  "뷔페", "푸드코트",
                  "두부요리", '육류,고기요리', "아시아음식", "태국음식", "이탈리아음식", "프랑스음식",
                  "태국음식", "스페인음식",
                  "그리스,터키음식", "퓨전음식", "치킨,닭강정", "해물,생선요리", "스테이크,립", "피자",
                  "샌드위치", "핫도그"]


    timelist = []
    timelist = store_info(timelist, timedata, categories)

    keys = timelist[0].keys()

    with open('stamp2json_yrmo_title.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(timelist)


if __name__ == '__main__':
    main()
