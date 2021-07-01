import asyncio
import aiohttp
import hashlib
from datetime import datetime, timedelta
import logging

'''
The code below is for the logging operations
'''

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('Error.txt')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

'''
Logger code ends
'''


headers = {
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "content-type": "application/json",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8"
}



async def GenerateTxnID(PhoneNumber):
    """
    Generates the TxnID for for the cowinApi
    or in simple terms sends Otp
    
    """
    async with aiohttp.ClientSession() as session:
        url = "https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP"
        payload = {
        "secret": "U2FsdGVkX185IhCpUiZkwVEroiAfmO+YQtAN5fYcOIDtZM5TYkwl1XDprWMkNNpCd5PiD9kT7z8HlgIdi8g6Tw==",
        "mobile": PhoneNumber}

        async with session.post(url,json=payload,headers=headers) as resp:
            if(resp.status != 200):
               print("Getting rate limited")
               return

            txnid = await resp.json()
            return txnid['txnId']



async def GenerateToken(TxnID,Otp):
    """
    This generates the JWT webtoken after verifying the Otp
    """
    async with aiohttp.ClientSession() as session:
        url = "https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp"    
        payload = {
            "otp": hashlib.sha256(str(Otp).encode()).hexdigest(),
            "txnId": TxnID}

        async with session.post(url,json=payload,headers=headers) as resp:
            token = await resp.json()
            return token['token']

async def GetBenificiaries(Token):
    """
    This returns the list of benificiries as python objects
    
    """
    headers.update({"authorization":"Bearer {}".format(Token)})
    async with aiohttp.ClientSession() as session:
        url = "https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries"    
        
        async with session.get(url,headers=headers) as resp:
            Benificiaries = await resp.json()
            return Benificiaries


async def GetSlotInfo(session,pincode):
    """
    This Api returns data about all centers for a given pincode and a date (mainly tomorrow)

    """
    async with aiohttp.ClientSession() as session:    
        url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={(datetime.today() + timedelta(days=1)).strftime("%d-%m-%y")}'
        
        async with session.get(url,headers=headers) as resp:              
            data = await resp.json()
            
            if(resp.status != 200):
                logger.error("Getting rate limited")
                return "FORBIDDEN"

            logger.info("Requested data for {}".format(pincode))
            return data                  
            
                
            

async def fetch_all(session, pincodes):
    
    """
    This function creates GetSlotInfo task and adds them to the eventloop
    Currently every pincode has its own task 
    This was designed tobe used in docker and scaled horizontally as tracking only containers 
    using RabbitMQ communication (never implemented that but possible) in between them.

    If running one container it can Track 10 pincodes with 30Sec interval, so it wont hit the rate limit.

    """
    


    tasks = []
    for pin in pincodes:
        task = asyncio.create_task(GetSlotInfo(session, pin))
        tasks.append(task)      
    results = await asyncio.gather(*tasks)
    return results

# @periodic(3)
# async def scan():
#    async with aiohttp.ClientSession() as session:
#         htmls = await fetch_all(session, [""])
#         #print(htmls)
   

# # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(scan())