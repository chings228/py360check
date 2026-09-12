import json

from pathlib import Path

list = []



data1 = {
    "name": "Alice",
    "age": 30,
    "city": "Hong Kong",
    "is_student": False,
    "skills": ["Python", "Data Analysis"],
    "add" : True
}




data2 = {
    "name": "Alice",
    "age": 30,
    "city": "Hong Kongo你好嗎👋",
    "is_student": False,
    "skills": ["Python", "Data Analysis"],
    "add" : True
}

print(data1)

print(data1["name"])

if (data1["add"]) :
    list.append(data1)

if (data2["add"]) :
    list.append(data2)

print(list)



hello = ['a','b','c']


for obja in hello :

    for objb in hello :

        if (obja != objb ):

            print(obja,objb)










with open("data.json", "w", encoding="utf-8") as file:
    json.dump(list, file, indent=4 ,ensure_ascii=False)