from flask import *
import time,csv,os,math
import dukiGeneral

app = Flask(__name__)

RANKINGDATA_ONBLANK = {"lastUpdate" : "----/--/-- --:--:--",
               "data" : []}

RANK_LIST = ["D","C","B","A","S","SS","SSS"]
RANK_SKIPAREA = [0.25, 0.20, 0.15, 0.10, 0.0, 0.0, 0.0]
RANK_UPAREA = [0.50, 0.40, 0.30, 0.25, 0.20, 0.15, 0.10]
RANK_KEEPAREA = [0.90, 0.80, 0.70, 0.65, 0.60, 0.60, 0.60]

dukiGeneral.TryMakeDir("data")
dukiGeneral.TryMakeDir("temp")



@app.route("/download")
def DataDownload():
    rankingData = dukiGeneral.GetRankingData(dukiGeneral.RANKINGDATA_PATH)
    
    return jsonify(rankingData)

@app.route("/web_viewer")
def webViewer():
    rankingData = dukiGeneral.GetRankingData(dukiGeneral.RANKINGDATA_PATH)
    playerCount = len(rankingData["data"])

    index = 0
    result = ""
    result += '<link rel="stylesheet" href="/css/webViewer.css">'
    result += "<title>ChampionLeague ランキング</title>\n"
    result += f"TotalPlayer : {playerCount}\n"
    result += f'<p>Update : {rankingData["lastUpdate"]}</p>\n'

    result += "<table>\n<tr><th></th>"
    for i in RANK_LIST:
        result += f"<th>{i}</th>"
    result += "</tr>\n"

    result += "<tr><th>飛び級ボーダー</th>"
    for i in RANK_SKIPAREA:
        if(i==0.0):
            result += f"<td>-----</td>"
        else:
            result += f"<td>{math.floor(playerCount*i)}位以上</td>"
    result += "</tr>\n"

    result += "<tr><th>昇級ボーダー</th>"
    for i in RANK_UPAREA:
        result += f"<td>{math.ceil(playerCount*i)}位以上</td>"
    result += "</tr>\n"
    
    result += "<tr><th>維持ボーダー</th>"
    for i in RANK_KEEPAREA:
        result += f"<td>{math.floor(playerCount*i)}位以上</td>"
    result += "</tr>\n"

    result += "<tr><th>降格ボーダー</th>"
    for i in RANK_KEEPAREA:
        result += f"<td>{math.floor(playerCount*i)+1}位以下</td>"
    result += "</tr>\n"
    result += "</table>\n"

    result += "<table>\n"
    result += "<tr><th>Rank</th><th>PlayerName</th><th>Points</th><th>G</th></tr>\n"
    for i in rankingData["data"]:
        index += 1
        result += f'<tr><td>{index}</td><td>{i["name"]}</td><td>{i["point"]}</td><td>{i["battleAmount"]}</td></tr>\n'
    result += "</table>"

    return result

@app.route("/css/<cssdata>")
def ReturnCSS(cssdata:str):
    return template_rendered(f"css/{cssdata}")

if __name__=="__main__":
    app.run(debug=False,port=10000)