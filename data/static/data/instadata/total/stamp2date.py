from datetime import datetime
import pandas as pd
import csv


def store_info(timelist, timedata, categories, category):
    for i, row in timedata.iterrows():

        new = True
        timedict = {}
        timedata = str(datetime.fromtimestamp(row["timestamp"])).split("-")
        timedict["yr_mo"] = timedata[0] + " " + timedata[1]

        adrs = row["naver_address"].split(" ")[1]
        timedict["adrs"] = adrs
        categ = get_category(categories, row["category"])

        for i in range(len(timelist)):
            if timelist[i]["yr_mo"] == timedict["yr_mo"] and timelist[i]["adrs"] == timedict["adrs"]:
                timelist[i]["post"] += 1
                timelist[i]["categ"][categ] += 1
                new = False
                break
        if new:
            timedict["post"] = 1
            timedict["categ"] = category.copy()
            timedict["categ"][categ] += 1
            timedict["geo"] = row.geo

            timelist.append(timedict)

    return timelist


def get_category(categories, specific_categ):
    for x in categories:
        if x in specific_categ:
            return x


def main():
    timedata = pd.read_csv("timeorder_naver.csv")

    categories = ["중식", "카페,디저트", "술집", "분식", "멕시코,남미음식", "인도음식", "일식",
                  "양식", "한식", "브런치", "햄버거", "베트남음식", "특급호텔레스토랑", "패밀리레스토랑", "뷔페", "푸드코트",
                  "두부요리", "아시아음식", "태국음식", "이탈리아음식", "프랑스음식", "태국음식", "스페인음식",
                  "그리스,터키음식", "퓨전음식", "치킨,닭강정", "해물,생선요리", "스테이크,립", "피자", "샌드위치", "핫도그"]

    category = {"중식": 0, "카페,디저트": 0, "술집": 0, "분식": 0, "멕시코,남미음식": 0, "인도음식": 0, "일식": 0,
                "양식": 0, "한식": 0, "브런치": 0, "햄버거": 0, "베트남음식": 0, "특급호텔레스토랑": 0, "패밀리레스토랑": 0, "뷔페": 0, "푸드코트": 0,
                "두부요리": 0, "아시아음식": 0, "태국음식": 0, "이탈리아음식": 0, "프랑스음식": 0, "태국음식": 0, "스페인음식": 0,
                "그리스,터키음식": 0, "퓨전음식": 0, "치킨,닭강정": 0, "해물,생선요리": 0, "스테이크,립": 0, "피자": 0, "샌드위치": 0, "핫도그": 0}

    timelist = []
    import ipdb; ipdb.set_trace()
    timelist = store_info(timelist, timedata, categories, category)

    import ipdb; ipdb.set_trace()
    keys = timelist[0].keys()

    with open('stamp2json_yrmo.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(timelist)


if __name__ == '__main__':
    main()
