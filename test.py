import json

x = {
    "id": "1",
    "data": {
        {"model": "BMW 230", "mpg": 27.5},
        {"model": "Ford Edge", "mpg": 24.1}}
}

y = json.loads(x)

print(y)
