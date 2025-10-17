import discord,os,csv,datetime,json,time
import dukiGeneral
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
client = discord.Client(intents=discord.Intents.all())
GUILD_ID = 1418884951629369366
ADMIN_ROLE = [
    1419207667171459074,
    1422267076415848491
]

dukiGeneral.TryMakeDir("./data")
dukiGeneral.TryMakeDir("./temp")

@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    adminMenberIds = []

    for member in guild.members:
        for role in member.roles:
            if role.id in ADMIN_ROLE:
                adminMenberIds.append(str(member.id))
                break
    
    with open("data/adminList.json", mode="w") as f:
        json.dump(adminMenberIds , f)

@client.event
async def on_message(message:discord.Message):
    if message.channel.id!=1420095519543263282:
        return
    if len(message.attachments) != 0:
        for attachment in message.attachments:
            #print(f"attachments_detect! type:{attachment.content_type}")
            if "text/csv" in attachment.content_type:
                await attachment.save("temp/reciveCsvFile.csv")
                updateDataDict("temp/reciveCsvFile.csv")

                embed = discord.Embed(title="データを受け付けました",description="Data Recived")
                embed.set_footer(f"date:<t:{time.time()}:F>")
                await message.channel.send(embed=embed)


def updateDataDict(fileName:str):
    with open(fileName , mode="r", encoding="utf-8") as f:
        rawCsvData = csv.reader(f)

        __rankingData = []
        isFirst = True
        for i in rawCsvData:
            if isFirst:
                isFirst = False
                continue

            __rankingData.append({"name" : i[2],
                                  "point" : str(int((float(i[3]) + int(i[5]) * 5)*10)/10),
                                  "battleAmount" : i[5]})
    ## sort
    rankingData_ = []
    while len(__rankingData) != 0:
        index = 0
        maxPoint = -10**10
        maxIndex = 0
        for i in __rankingData:
            if float(i["point"]) > maxPoint:
                maxIndex = index
                maxPoint = float(i["point"])
            
            index += 1
        
        rankingData_.append(__rankingData[maxIndex])
        del __rankingData[maxIndex]
    
    rankingData = {"lastUpdate" : datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
                   "data" : rankingData_}
    
    with open("data/rankingData.json", mode="w") as f:
        json.dump(rankingData,f)



client.run(TOKEN)
