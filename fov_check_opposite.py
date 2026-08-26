
from pathlib import Path
import json
import sys



if (len(sys.argv) < 2) :
    sys.exit("\n\nno code , pls refer to python3 fov.py {code}\n\n")



code = sys.argv[1]

print(code)


filename = f"fovresult-{code}.json"

# Read data from file
with open(filename, "r", encoding="utf-8") as file:
    datas = json.load(file)


for data in datas :

    print(data['fromfilePath'])


