from asyncCowin.asyncCowinWrapper import  fetch_all
import bot
import asyncio 
import aiohttp
from dBase import *





def periodic(period):
    """
    This is a function decorator which help as to readd a task to 
    the event loop after a set interval
    """
    def scheduler(fcn):
        async def wrapper(*args, **kwargs):
            while True:
                asyncio.create_task(fcn(*args, **kwargs))
                await asyncio.sleep(period)
        return wrapper
    return scheduler


@periodic(30)
async def scan():
   async with aiohttp.ClientSession() as session:
        data = await fetch_all(session, config.PINCODES)
        await parseData(data)
    



async def parseData(data):
    """
    Parses the Json data returned from the Api and calls the broadcast message.
    """
    if(data == None):
        print("None")
        return
    for y in data:
        for x in y["sessions"]:           
            if(x["available_capacity"]>1 and x["min_age_limit"] == 18):
               await bot.broadcast(x,"SLOT")

async def main():
    await asyncio.gather(
        bot.dp.start_polling(),
        scan(),
    )

#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())