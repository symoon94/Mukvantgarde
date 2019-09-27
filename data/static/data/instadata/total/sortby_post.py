import pandas as pd


def readfile(filename):
    csvdata = pd.read_csv(filename)
    newlist = []
    for i, row in csvdata.iterrows():
        duple = False
        for x in newlist:
            if row.naver_address == x[4] and row.naver_title == x[5]:
                x[2] += row.post
                duple = True
                break
        if duple == False:
            newlist.append([row.loc_id, row.title, row.post, row.geo, row.naver_address,
                            row.naver_title, row.category,
                            row.thumUrl, row.broadcastInfo])
    return newlist

def sortbypost(alist):
    df = pd.DataFrame(alist)
    df.columns = ["loc_id", "title", "post", "geo", "naver_address",
                            "naver_title", "category",
                            "thumUrl", "broadcastInfo"]
    df.sort_values('post')
    return df

def main():
    filename = "concated_output.csv"
    except_duplic = readfile(filename)
    sorted = sortbypost(except_duplic)
    sorted.to_csv("sorted_by_post.csv")

if __name__ == '__main__':
    main()