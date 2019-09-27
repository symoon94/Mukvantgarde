import pandas as pd
import csv


def make_geo(geostring):
    try:
        geolist = geostring.strip("[]").split(", ")
        lon = geolist[0]
        lat = geolist[1]
    except:
        import ipdb; ipdb.set_trace()
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

def store_info(chartlist, timedata, categories):
    for i, row in timedata.iterrows():

        new = True

        chartdict = {}

        title = row["naver_title"]
        chartdict["상호명"] = title

        adrs1 = row["naver_address"].split(" ")[1]
        adrs2 = row["naver_address"].split(" ")[2]
        chartdict["시/군/구"] = adrs1
        chartdict["읍/면/동"] = adrs2
        chartdict["주소"] = row["naver_address"]


        categ = get_category(categories, row["category"])

        for i in range(len(chartlist)):
            if chartlist[i]["시/군/구"] == chartdict["시/군/구"] and chartlist[i][
                "읍/면/동"] == chartdict["읍/면/동"] and chartlist[i]["상호명"]\
                    ==\
                    chartdict["상호명"]:
                chartlist[i]["포스트 수"] += 1
                chartlist[i]["좋아요 수"] += int(row.like)
                chartlist[i]["태그"] = add_tag(chartlist[i]["태그"], row.tags)
                new = False
                break
        if new:
            chartdict["포스트 수"] = 1
            chartdict["좋아요 수"] = int(row.like)
            chartdict["카테고리"] = categ
            chartdict["lat"], chartdict["lon"] = make_geo(row.geo)
            chartdict["img_url"] = row.url
            chartdict["태그"] = make_tag_dict(row.tags)

            chartlist.append(chartdict)

    return chartlist


def get_category(categories, specific_categ):
    for x in categories:
        if x in specific_categ:
            return x

def organize(alist):
    rates = []
    for each in alist:

        # 태그 (수)
        taglist = []
        tuplelist = sorted(each["태그"].items(), reverse=True,
                           key=lambda x: x[1])
        for i in range(len(tuplelist)):
            if tuplelist[i][0] != '':
                taglist.append(str(tuplelist[i][0]) + " (" + str(tuplelist[i][
                                                                     1]) + ")")
            if i == 10: # 태그 빈도 상위 최대 11개까지 모으기
                break

        each.update({"태그 (수)": ", ".join(taglist)})

        # 포스트 당 좋아요
        rate = int(each["좋아요 수"] / each["포스트 수"])
        rates.append(float(rate))
        each.update({"포스트 당 좋아요" : float(rate)})



    max_r = max(rates)
    # min_r = min(rates)
    # gap = (max_r - min_r)/3
    gap = max_r / 3

    for each in alist:
        each.update({"별점": "⭐" * 2})
        for i in range(3):
            if each["포스트 당 좋아요"] >= i*gap:
                each.update({"별점": "⭐"*(i+3)})

    return alist


def main():
    timedata = pd.read_csv("timeorder_naver.csv")
    categories = ["중식", "카페,디저트", "술집", "분식", "멕시코,남미음식", "인도음식", "일식",
                  "양식", "한식", "브런치", "햄버거", "베트남음식", "특급호텔레스토랑", "패밀리레스토랑",
                  "뷔페", "푸드코트",
                  "두부요리", "육류,고기요리", "아시아음식", "태국음식", "이탈리아음식", "프랑스음식",
                  "태국음식", "스페인음식",
                  "그리스,터키음식", "퓨전음식", "치킨,닭강정", "해물,생선요리", "스테이크,립", "피자",
                  "샌드위치", "핫도그"]


    chartlist = []
    chartlist = store_info(chartlist, timedata, categories)
    chartlist = organize(chartlist)

    keys = chartlist[0].keys()

    with open('chartdata.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(chartlist)


if __name__ == '__main__':
    main()
