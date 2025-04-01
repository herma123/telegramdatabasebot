import json

def __read__(name):
	with open(f"{name}.json", "r") as _data:
		return json.load(_data)

def __write__(name, _dict):
	with open(f"{name}.json", "w") as _data:
		_data.write(json.dumps(_dict))

def createData(name):
	with open(f"{name}.json", "w") as _data:
		_data.write(json.dumps({}))

def appendKey(name, key, argument):
	data = __read__(name)
	data[f"{key}"] = argument
	__write__(name, data)

def removeKey(name, key) -> None:
	data = __read__(name)
	del data[f"{key}"]
	__write__(name, data)

def removeKeys(name):
	__write__(name, {})

def getKey(name, key):
	data = __read__(name)
	return data[f"{key}"]