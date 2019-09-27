# 크롤링 데이터에서 음식점이 아닌 것들을 골라내는 작업

import pandas as pd

def del_district(mydata):
    """'지구'가 들어간 단어를 타이틀에서 삭제하고 mydataframe을 return.
    Args:
        mydata(myDataFrame): a total mydata.
    """

    probe = 0
    for each in mydata["title"]:
        # print(each)

        excpt = ["청담 고수", "양군", "YAT", "Jung Sik Dang", "The Market Kitchen", "Pizza Mall 신촌점"]
        if each in excpt:
            continue

        index = pd.Index(mydata.title).get_loc(each)

        if (each[-2:] in ["지구", "거리", "센터", "상가", "후문"]) or \
                (each[-3:] in ["우리집", "어딘가", "신도시"]) or \
                (each[-4:] in ["한옥마을"]) or \
                (each[-6:] in ["center", "Center"]) or \
                ("University" in each) or ("신혼집" in each) or \
                ("Gwanghwamun" in each) or ("Palace" in each) or \
                ("Beach" in each) or (" Lake" in each) or ("대학로/" in each) or\
                ("Centum" in each) or ("Hotel" in each) or ("HOTEL" in each) \
                or (
                "InterContinental" in each) or ("Station" in each) or (
                "Market" in each) or ("Hilton" in each) or ("Hyatt" in each) or\
                ("Mall" in each) or ("SongDo" in each) or ("율동공원" in each) or\
                ("벽화마을" in each) or ("바다마을" in each) or ("근처" in each):
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
    local_set = local_set.union({"강원도", "제주도", "서울시", "전라도", "경상도", "충청도",
                                 "대전시", "울산시", "광주시", "인천시", "대구시", "부산시",
                                 "신시가지", "Square", "Wirye", "위례", "서판교",
                                 "운중동", "서초동", "Seochodong", "아브뉴프랑", "Avenue France", "Sujigu", "Daebudo", "Ikseondong", "Cherwon", "선릉", "Seolleung", "신불당동", "Taejongdae", "Grand Park", "수변공원", "바다", "Gyeongbokgung", "Coex"})
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


def main():
    filename = "/Users/munsuyeong/git/symoon94/inssaroad/mukbangtour/page/static/page/instadata/total/concated_output.csv"  # read data

    mydata = pd.read_csv(filename, error_bad_lines=False)
    mydata = del_district(mydata)

    mydata.to_csv(filename, index=False)

if __name__ == '__main__':
    main()
