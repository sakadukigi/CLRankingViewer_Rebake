from flask import *
import time,csv,os
import dukiGeneral

app = Flask(__name__)

RANKINGDATA_ONBLANK = {"lastUpdate" : "----/--/-- --:--:--",
               "data" : []}

dukiGeneral.TryMakeDir("data")
dukiGeneral.TryMakeDir("temp")

def GetRankingData(path:str) -> dict:
    if os.path.isfile(path):
        with open(path) as f:
            rankingData = json.load(f)
    else:
        rankingData = RANKINGDATA_ONBLANK
    return rankingData

    

@app.route("/download")
def DataDownload():
    rankingData = GetRankingData("data/rankingData.json")
    
    return jsonify(rankingData)

@app.route("/web_viewer")
def webViewer():
    rankingData = GetRankingData("data/rankingData.json")

    index = 0
    result = ""
    result += "<title>ChampionLeague ランキング</title>\n"
    result += f'<p>Update : {rankingData["lastUpdate"]}</p>\n'
    result += "<table>\n"
    result += "<tr><th>Rank</th><th>PlayerName</th><th>Points</th><th>G</th></tr>\n"
    for i in rankingData["data"]:
        index += 1
        result += f'<tr><td>{index}</td><td>{i["name"]}</td><td>{i["point"]}</td><td>{i["battleAmount"]}</td></tr>\n'
    result += "</table>"

    return result

if __name__=="__main__":
    app.run(debug=False,port=10000)