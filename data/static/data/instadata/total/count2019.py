import pandas as pd
import json


df = pd.read_csv("stamp2json_yrmo_title.csv")

this_year = []
for i, row in df.iterrows():
    contain = False
    temp = {}
    if row["yr_mo"].split()[0] == "2019":
        for store in this_year:
            if store["naver_title"] == row["naver_title"]:
                store["count"] += 1
                store["like"] += row["like"]
                contain = True
                break

        if contain == False:
            temp["yr_mo"] = row["yr_mo"]
            temp["naver_title"] = row["naver_title"]
            temp["count"] = 1
            temp["adrs1"] = row["adrs1"]
            temp["adrs2"] = row["adrs2"]
            temp["categ"] = row["categ"]
            temp["like"] = row["like"]
            temp["lat"] = row["lat"]
            temp["lon"] = row["lon"]
            temp["img_url"] = row["img_url"]
            tgjs = json.loads(row["tags"].replace("'", "\""))
            temp["tags"] = sorted(tgjs.items(), key=lambda kv: kv[1])
            temp["like_post"] = 0

            this_year.append (temp)


import ipdb; ipdb.set_trace()
new_df = pd.DataFrame(this_year)

for i, row in new_df.iterrows():
    new_df["like_post"][i] = int(row["like"]) / int(row["count"])

import ipdb; ipdb.set_trace()
new_df = new_df.sort_values(by=["like_post"])
new_df.to_csv("count2019.csv", index=False)