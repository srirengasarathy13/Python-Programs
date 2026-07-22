"""
list=["tea","eat","ate","listen","silent","python"]
#[[eat,tea,ate,listen,silent,python]]
dis={}
result = []
for i in list:
    key="".join(sorted(i))
    if key not in dis:
        dis[key] =[]
    dis[key].append(i)
for i in dis:
    result.append(dis[i])
print(result)

"""
lis=["tea","eat","ate","listen","silent","python"]
dis={}
for i in lis:
    key="".join(sorted(i))
    if key not in dis:
        dis[key] =[]
    dis[key].append(i)
result = list(dis.values())
print(result)

