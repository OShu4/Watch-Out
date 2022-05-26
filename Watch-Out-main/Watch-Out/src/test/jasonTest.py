import json
from traceback import print_tb

with open('Watch-Out/src/main/python/assets/Enemy/Json/Enemy0.json') as f:
  data = json.load(f)

result_count = data["frames"]["images"] ["frame"] 
print (result_count)