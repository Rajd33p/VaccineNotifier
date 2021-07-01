import asyncio
import motor.motor_asyncio
import config

cluster = motor.motor_asyncio.AsyncIOMotorClient(config.MONGODB_URl)

db = cluster[config.MAIN_CLUSTER]
UserData = db[config.USER_DATA_COLLECTION]
UserInfo= db[config.USER_INFO_COLLECTION]

async def Insertbeneficiaries(chatid,beneficiaries=[]):
    await UserData.update_one({"chatid":chatid},{"$set":{"beneficiariesID":beneficiaries}})

async def InsertChatID(chatid,invitationCode,name,phonenumber):
    await UserData.insert_one({"chatid":chatid,"Codeused":invitationCode,"status":"unsnoozed","Name":name,"Phone":phonenumber,"beneficiariesID":[],"Token":"","Autobook":"off","pincode":config.PINCODES})

async def getChatids(Broadcast=False):
    data = list()
    if(not Broadcast):
        async for document in UserData.find({'status':'unsnoozed'}, {'chatid':1,'_id':0}):
            data.append(document['chatid'])
    else:
        async for document in UserData.find({}, {'chatid':1,'_id':0}):
            data.append(document['chatid'])      
    return data

async def getToken():
    data = list()
    async for document in UserData.find({'Autobook':'on'},{{'Token':1,'Phone':1,'chatid':1,'_id':0}}):
        data.append(document)
    return data

async def snoozing(chatid,action):
    if(action == "snooze"):
        await UserData.update_one({"chatid":chatid},{"$set":{'status':'snoozed'}})
    else:
        await UserData.update_one({"chatid":chatid},{"$set":{'status':'unsnoozed'}})

async def CheckIDExist(chatid):
    if(await UserData.count_documents({ 'chatid': chatid }, limit = 1) != 0):
        return True
    else:
        return False

async def UpdateTotal():
    
    await UserInfo.update_one({'Field':"Data"},{'$inc':{'TotalUsers':1}})
 
async def UpdateAuthUser():
    await UserInfo.update_one({'Field':"Data"},{'$inc':{'AutenticatedUser':1}})
    
async def GetStats():
    data = await UserInfo.find_one({'Field':'Data'},{'_id':0})
    return data

