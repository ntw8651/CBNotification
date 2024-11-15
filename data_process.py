import json
'''
json파일에서 데이터를 가져오는 함수와
json파일에 데이터를 저장하는 함수가 저장되어 있다.

load_data

'''

def LoadData(file_path="data.json"):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def SaveData(data, file_path="data.json"):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
