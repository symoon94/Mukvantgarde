"""
extract non-local names and concat all jsonl files
"""

import pandas as pd

def del_district(mydata):
    """'지구'가 들어간 단어를 타이틀에서 삭제하고 mydataframe을 return.
    Args:
        mydata(myDataFrame): a total mydata.
    """

    probe = 0
    for each in mydata["title"]:
        # print(each)

        # TODO: "청담 고수", "양군", "YAT", "Jung Sik Dang" 도 없애 버리는거 막기
        excpt = ["청담 고수", "양군", "YAT", "Jung Sik Dang"]
        if each in excpt:
            continue

        index = pd.Index(mydata.title).get_loc(each)

        if (each[-2:] in ["지구", "거리", "센터"]) or \
                (each[-3:] in ["우리집", "어딘가", "신도시"]) or \
                (each[-6:] in ["center", "Center"]) or \
                ("University" in each) or ("신혼집" in each) or \
                ("Gwanghwamun" in each) or ("Airport" in each):
            mydata = mydata.drop([index + probe])
            probe += 1
            continue

        words = each.split()

        if "신도시" in words:
            words.remove("신도시")

        mydata, probe = del_area(words, mydata, index, probe)

    return mydata

def del_area(localname, mydata, index, probe):

    loc_data = pd.read_csv("loc_ko_eng.txt", sep="	")
    local_set = set(loc_data["시도"]).union(set(loc_data["시군구"]), \
                                          set(loc_data["읍면동"]), \
                                          set(loc_data["영문 표기"]))
    local_set = local_set.union({"강원도", "제주도", "서울시", "전라도", "경상도", "충청도", "대전시", "울산시", "광주시", "인천시", "대구시", "부산시"})
    local_set = {x for x in local_set if x == x}  # remove nan(float)

    name_yes_no = []

    try:
        for name in localname:

            if len(name) == 1:  # e.g., "Anh 안"
                return mydata, probe

            loc_name_check = any(x for x in local_set if name in x)
            name_yes_no.append(loc_name_check)


        if not False in name_yes_no:
            mydata = mydata.drop([index + probe])
            probe += 1
            return mydata, probe

    except:
        pass


    return mydata, probe

def check_k(post):
    if "k" in post and "." in post:
        post = post.replace(".", "").replace("k", "00")
    elif "k" in post:
        post = post.replace("k", "000")
    elif "," in post:
        post = post.replace(",", "")
    elif "m" in post and "." in post:
        post = post.replace(".", "").replace("m", "00000")
    elif "m" in post:
        post = post.replace("m", "000000")
    try:
        post = int(post)
    except:
        pass
    return post

def readfile(path, names):
    for i in range(len(names)):
        mydata = pd.read_csv(path + names[i] + "/" + names[i] + "_loc_geo_post_naver.csv", error_bad_lines=False)
        data = del_district(mydata)
        if i == 0:
            init_df = data[["loc_id", "title", "post", "geo", "naver_address", "naver_title", "broadcastInfo", "category", "thumUrl"]]
        else:
            for index, row in data.iterrows():
                row["post"] = check_k(row["post"])
                if row["loc_id"] in init_df["loc_id"].unique():
                    continue
                else:
                    newline = pd.DataFrame({"loc_id": row["loc_id"], "title": row["title"], \
                                  "post": row["post"], "geo": row["geo"], \
                                  "naver_address": row["naver_address"], \
                                  "naver_title": row["naver_title"], \
                                   "tel": row["tel"], \
                                  "broadcastInfo": row["broadcastInfo"], \
                                  "category": row["category"], "thumUrl": row["thumUrl"]}, index=[0])
                    init_df = init_df.append(newline, ignore_index = True)
    return init_df

def concat_duplicates(df):
    pass

def main():
    path = "../"
    names = ["jmt2", "onn", "mukstagram1"]
    concated_info =readfile(path, names)

    # TEST용
    concated_info.to_csv("concated_output.csv", index=False)
    # # import ipdb; ipdb.set_trace()
    # concated_info = pd.read_csv("concated_output.csv")
    orderedata = pd.read_csv("/Users/munsuyeong/git/symoon94/inssaroad/mukbangtour/page/static/page/instadata/dates/sortdates.csv")
    for i, row in orderedata.iterrows():
        try:
            infoindex = pd.Index(concated_info.loc_id).get_loc(row["loc_id"])
            infoline = pd.DataFrame({"naver_address": concated_info["naver_address"][infoindex], \
                                     "category": concated_info["category"][infoindex], \
                                     "title": concated_info["title"][infoindex], \
                                      "post": concated_info["post"][infoindex], \
                                     "geo": concated_info["geo"][infoindex], \
                                      "naver_title": concated_info["naver_title"][infoindex], \
                                     "tel": concated_info["tel"][infoindex], \
                                      "broadcastInfo": concated_info["broadcastInfo"][infoindex], \
                                      "thumUrl": concated_info["thumUrl"][infoindex]}, index=[0])
            dateline = pd.DataFrame(pd.DataFrame({"timestamp": row[
                "timestamp"], "address": row["address"], "loc_id": row["loc_id"], "like": row["like"], "tags": row["tags"], "url": row["url"], \
                                                  "owner_id": row["owner_id"], \
                                                  "text": row["text"]}, index=[0]))
            merged = pd.concat([dateline, infoline], axis=1, sort=False)

            # column: timestamp,address,loc_id,like,tags,url,owner_id,text,
            # naver_address,category,title,post,geo,naver_title,
            # tel,broadcastInfo,thumUrl
            merged.to_csv("timeorder_naver.csv", mode="a", index=False, header=False)
        except:
            continue

if __name__ == '__main__':
    main()