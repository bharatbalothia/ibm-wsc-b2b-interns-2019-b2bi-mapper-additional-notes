import requests
r = requests.get('http://9.199.145.193:5984/additionalnotes/_all_docs\?include_docs\=true')
data=r.json()
print(r)
