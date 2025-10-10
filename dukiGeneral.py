import os,json

RANKINGDATA_ONBLANK = {"lastUpdate" : "----/--/-- --:--:--",
               "data" : []}

RANKINGDATA_PATH = "data/rankingData.json"

def TryMakeDir(path:str) -> bool:
    if not os.path.isdir(path):
        os.mkdir(path)
        return True
    else:
        return False

def GetRankingData(path:str) -> dict:
    if os.path.isfile(path):
        with open(path) as f:
            rankingData = json.load(f)
    else:
        rankingData = RANKINGDATA_ONBLANK
    return rankingData

if __name__=="main":
    pass