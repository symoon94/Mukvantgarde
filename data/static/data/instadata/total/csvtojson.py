import csv , json
csv.field_size_limit(100000000)

csvFilePath = "chartdata.csv"
jsonFilePath = "chartdata.json"
arr = []
#read the csv and add the arr to a arrayn

with open (csvFilePath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    # print(csvReader)
    for csvRow in csvReader:
        arr.append(csvRow)
        # import ipdb; ipdb.set_trace()

# print(arr)

# write the data to a json file
with open(jsonFilePath, "w") as jsonFile:
    jsonFile.write(json.dumps(arr, indent = 4))