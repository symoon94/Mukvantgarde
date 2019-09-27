import pandas as pd
import json


def readcsv(filename):
    df = pd.read_csv(filename)

    Korea = []

    for i, row in df.iterrows():
        breakpoint = False
        loc = row.naver_address.split(" ")[0:2]

        if any(city["name"] == loc[0] for city in Korea):
            for city in Korea:
                if breakpoint == True:
                    break
                if city["name"] == loc[0]:
                    if any(state["name"] == loc[1] for state in city["children"]):
                        for state in city["children"]:
                            if state["name"] == loc[1]:
                                state["children"].append(row.naver_title)
                                breakpoint = True
                                break

                    else:
                        city["children"].append({"name":loc[1], "children":[
                            row.naver_title]})
                        break


        else:
            Korea.append({"name":loc[0], "children":[{"name":loc[
                1], "children":[[row.naver_title]]}]})


    return Korea

# class JSONEncoder(json.JSONEncoder):
#
#     def default(self, obj):
#         # import ipdb; ipdb.set_trace()
#         if hasattr(obj,'to_dict'):
#             return obj.to_dict()
#         return json.JSONEncoder.default(self, obj)

def main():
    filename = "/Users/munsuyeong/git/symoon94/inssaroad/mukbangtour/page/static/page/instadata/total/sorted_by_post.csv"
    Korea = readcsv(filename)

    # import ipdb; ipdb.set_trace()
    # kr = str(Korea)
    # import re
    # test = re.sub('\'', '\"', kr)
    # abc = json.loads(test)
    # dede = json.dumps(test)

    # Korea = json.dumps(Korea, cls=JSONEncoder)

    # with open('sorted_by_loc.json', 'w') as json_file:
    #     json.dump(test, json_file)

    # f = open('sorted_by_loc_2.json', 'w')
    # import ipdb; ipdb.set_trace()
    Korea = pd.DataFrame(Korea)
    Korea.to_json("sorted_by_loc.json", orient="records")


if __name__ == '__main__':
    main()