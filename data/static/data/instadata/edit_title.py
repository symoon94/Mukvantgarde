import pandas as pd

FILE = 'jmt2'
csv = pd.read_csv(f'{FILE}/{FILE}_loc_geo_post.csv')

data = {}
index = []
loc_id = []
address = []
title = []
geo = []
post = []

for i in range(len(csv)):
    loc_id.append(csv.iloc[i].loc_id)
    pre_address = csv.iloc[i].address
    try:
        pre_address = pre_address.strip("[']").split("', '")
    except:
        pass
    address.append(pre_address)
    pre_title = csv.iloc[i].title.replace(",", "").replace("-", "")
    if pre_title in title:
        pre_title = pre_address[0] + " " + pre_title
        if pre_title in title:
            try:
                pre_title = pre_address[1] + " " + pre_title
            except:
                pre_title = " " + pre_title

    title.append(pre_title)
    geo.append(csv.iloc[i].geo)
    post.append(csv.iloc[i].post)

data['loc_id']=loc_id
data['address']=address
data['title']=title
data['geo']=geo
data['post']=post

df = pd.DataFrame(data)
df.to_csv('output.csv', index=True)
