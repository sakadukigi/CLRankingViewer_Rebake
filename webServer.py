from flask import *
import time,csv,os,math,requests
import dukiGeneral,uuid,logging
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
OWNER_DISCORD_ID = os.getenv("OWNER_DISCORD_ID")


while not os.path.isfile("data/adminList.json"):
    print("waitingGenerateData...")
    time.sleep(1)

with open("data/adminList.json") as f:
    adminList = json.load(f)

RANKINGDATA_ONBLANK = {"lastUpdate" : "----/--/-- --:--:--",
               "data" : []}

loginSessions = {}

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
        result += f'<th class="class-{i}">{i}</th>'
    result += "</tr>\n"

    result += '<tr><th class="class-S">飛び級</th>'
    for i in RANK_SKIPAREA:
        if(i==0.0):
            result += f"<td>-----</td>"
        else:
            result += f"<td>{math.floor(playerCount*i)}位以上</td>"
    result += "</tr>\n"

    result += '<tr><th class="class-A">昇級</th>'
    for i in RANK_UPAREA:
        result += f"<td>{math.ceil(playerCount*i)}位以上</td>"
    result += "</tr>\n"
    
    result += '<tr><th class="class-C">維持</th>'
    for i in RANK_KEEPAREA:
        result += f"<td>{math.floor(playerCount*i)}位以上</td>"
    result += "</tr>\n"

    result += '<tr><th class="class-B">降格</th>'
    for i in RANK_KEEPAREA:
        result += f"<td>{math.floor(playerCount*i)+1}位以下</td>"
    result += "</tr>\n"
    result += "</table>\n<br>"

    result += "<table>\n"
    result += "<tr><th>Rank</th><th>PlayerName</th><th>Points</th><th>G</th></tr>\n"
    for i in rankingData["data"]:
        index += 1
        result += f'<tr><td class="rank-{index}">{index}</td><td>{i["name"]}</td><td>{i["point"]}</td><td>{i["battleAmount"]}</td></tr>\n'
    result += "</table>"

    return result

@app.route("/css/<cssdata>")
def ReturnCSS(cssdata:str):
    return render_template(f"css/{cssdata}")

@app.route("/auth/discord", methods = ["GET","POST"])
def discordAuth():
    code = request.args.get("code")
    if code == None:
        return redirect("https://discord.com/oauth2/authorize?client_id=1420093711110508595&response_type=code&redirect_uri=https%3A%2F%2Fvrchat.sakaduki.com%2Fauth%2Fdiscord&scope=identify")
    else:
        jsonBody = {
            "grant_type" : "authorization_code",
            "code" : code,
            "redirect_uri" : "https://vrchat.sakaduki.com/auth/discord",
        }
        r = requests.post("https://discordapp.com/api/oauth2/token", json=jsonBody)
        if r.status_code != 200:
            logging.error(f"Failed Code Request\n{r.content}")
            return "<h1>Failed Auth by Discord</h1><br><p>500 Internal Server Error</p><br><p>サーバー管理者にお問い合わせください</p>", 500
    
        token = f"Bearer {r.json['access_token']}"
        headers = {"Authorization": token}
        r = request.get("https://discordapp.com/api/users/@me", headers=headers, auth = (CLIENT_ID, CLIENT_SECRET))

        if r.status_code != 200:
            logging.error(f"Failed UserData Request\n{r.content}")
            return "<h1>Failed Auth by Discord</h1><br><p>500 Internal Server Error</p><br><p>サーバー管理者にお問い合わせください</p>", 500
        if r.json["id"] not in adminList:
            logging.warning(f"Cant Auth User\n{r.content}")
            return "<h1>Failed Auth by Discord</h1><br><p>403 Forbidden</p><br><p>権限がありません</p>", 403
        else:
            response = make_response("Auth!!!")
            sessionID = str(uuid.uuid4())
            maxAge = time.time() + 3600
            response.set_cookie("sessionID", value=sessionID, max_age=maxAge)

            loginSessions[sessionID] = {"id": r.json["id"],"token": token}

            return response

    
    

if __name__=="__main__":
    app.run(debug=False,port=10000)