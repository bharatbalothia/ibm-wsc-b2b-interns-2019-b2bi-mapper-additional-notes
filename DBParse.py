import pandas as pd
import os

os.system('curl -X GET http://127.0.0.1:5984/additionalnotes/_all_docs\?include_docs\=true > db.json')
d = []
all_data = pd.read_json("db.json")
for row in all_data['rows']:
    # print(data['rows'][5]['doc']['usage'][0]['fileName'])
    for col in row['doc']['usage']:
        record = row['doc']['email'], row['doc']['username'], col['fileName'], col['time']
        d.append(record)
pd.DataFrame(columns=['Email', 'Name', 'Mapname', 'Time'], data=d).to_excel("db.xlsx",index=False)
