# import http.client

# conn = http.client.HTTPSConnection("solved.ac")
# headers = {"Content-Type": "application/json"}
# conn.request("GET", "/api/v3/search/user?query=9776mk&page=1", headers=headers)
# res = conn.getresponse()
# data = res.read()

# print(type(data))
# print(data[0])
# print(data)
# print(type(data.decode("utf-8")))
# print(data.decode("utf-8"))
# data_ = data.decode("utf-8")
# print(data_[:10])

# if "tier" in data_:
#     a = data_.index("tier")
#     print(a)
#     print(data_[535:545])


import http.client

conn = http.client.HTTPSConnection("solved.ac")
headers = {"Content-Type": "application/json"}
conn.request("GET", "/api/v3/user/show?handle=9776mk", headers=headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
data_ = data.decode("utf-8")
print(type(data.decode("utf-8")))

if "tier" in data_:
    a = data_.index("tier")
    print(a)  # 515
    print(data_[515:525])
    print(f"티어 : {data_[521:523]}")
