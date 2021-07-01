
from aiogram.dispatcher.filters import state
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher ,executor,types
from aiogram.types import ParseMode, message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import config
from dBase import *


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())


class adFrom(StatesGroup):
    messag = State()

class Form(StatesGroup):
    inviteCode = State()
    Name = State()
    Phonenumber = State()




async def MsgAdmin(METHOD):
    id = config.OWNER_ID   
    if(METHOD =="ERROR"):
       try:
           await bot.send_document(id,document=open("Error.txt", 'rb'))
       except:
           await bot.send_message(id,"logs are empty")
    
async def AdminBroadcast(data):
    ids = await getChatids(True) 
    if(ids == []):
        return

    for id in ids:
        await bot.send_message(
            id,
            md.text(
                md.text("📢 ",md.bold("BROADCAST")),
                md.text(" "),
                md.text(data),
                sep="\n",
            ),
            parse_mode=ParseMode.MARKDOWN
        )

async def broadcast(data,Mtype):  
    ids = await getChatids() 
    if(ids == []):
        return
          
    if(Mtype == "SLOT"):
        for id in ids:
            await bot.send_message(
                id,
                md.text(
                    md.text(md.bold("✅ SLOT AVAILABLE ")),
                    md.text(" "),
                    md.text(md.bold("ChatID: "),id),
                    md.text(md.bold("CenterID: "),data['center_id']),
                    md.text(md.bold("Name: "),data['name']),
                    md.text(md.bold("Pincode: "),data['pincode']),
                    md.text(md.bold("Min Age Limit:"),data["min_age_limit"]),
                    md.text(md.bold("Vaccine: "), data["vaccine"]),
                    md.text(md.bold("Availability ✅")),
                    md.text(md.bold(" Dose 1: "),data["available_capacity_dose1"]),
                    md.text(md.bold(" Dose 2: "),data["available_capacity_dose1"]),
                    md.text(" "),
                    md.text("Book at https://selfregistration.cowin.gov.in"),
                    sep='\n',              
                ),
                parse_mode=ParseMode.MARKDOWN,
            )
            await bot.send_message(
                id,
                md.text(
                    md.text("✅Booked your slot ?"),
                    md.text("You can stop these spams by\n using /snooze"),
                    sep="\n",
                ),
                parse_mode=ParseMode.MARKDOWN,
            )

@dp.message_handler(commands=['stats'])
async def stats(message: types.Message):
    id = config.OWNER_ID
    data = await GetStats()
    await bot.send_message(
        id,
        md.text(
            md.text(md.bold("Total Users: "),data['TotalUsers']),
            md.text(md.bold("Unauthenticated Users: "),(data['TotalUsers']-data['AutenticatedUser'])),
            md.text(md.bold("Authenticated Users: "),data['AutenticatedUser']),
            sep="\n",
        ),
        parse_mode=ParseMode.MARKDOWN,
    )

@dp.message_handler(commands=['sendall'])
async def send_all(message: types.Message):
    await adFrom.messag.set()
    
    await bot.send_message(
            message.chat.id,
            md.text(
                md.bold("Enter the Message to broadcast"),
            ),
            parse_mode=ParseMode.MARKDOWN,
    )

@dp.message_handler(state=adFrom.messag)
async def process_broadcast(message: types.Message, state: FSMContext):
    await AdminBroadcast(message.text)
    await state.finish()

@dp.message_handler(commands=['getlogs'])
async def status(message:types.Message): 
    await MsgAdmin("ERROR")   

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command  
    """
    await UpdateTotal()
    if(await CheckIDExist(message.chat.id)):
       await  bot.send_message(
           message.chat.id,
           md.text(
               md.text("Hi!\nI'm GetVaccinated!"),
               md.text("I will ping you when a slot is available"),
               md.text("Currently Tracking", md.bold(732101), "for 18+ slot"),
               md.text(md.bold("To check tracking status use /track")),
               md.text("Planned Feature : Autobook :)"),
               md.text("Made with ❤️ by @Rajd333p"),
               sep='\n',
           ),
            parse_mode=ParseMode.MARKDOWN,
       )

    else:
        await Form.inviteCode.set()
        await bot.send_message(
            message.chat.id,
            md.text(
                md.bold("Enter the Invitation Code"),
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

@dp.message_handler(commands=['snooze'])
async def snooze(message:types.Message):
    await snoozing(message.chat.id,"snooze")
    await bot.send_message(
            message.chat.id,
            md.text(
                md.text("Your chat has been snoozed permanently"),
                md.text(md.underline("To unsnooze use /unsnooze")),
                sep="\n"
            ),
            parse_mode=ParseMode.MARKDOWN,
    )

@dp.message_handler(commands=['status'])
async def status(message:types.Message):
    if(message.chat.id not in await getChatids()):
        await message.reply("Your current status is Snoozed")
    else:
        await message.reply("Your current status is Unsnoozed")

@dp.message_handler(commands=['unsnooze'])
async def unsnooze(message:types.Message):
        await snoozing(message.chat.id,"unsnooze")
        
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text("Your chat has been unsnoozed"),
                md.text(md.underline("To snooze use /snooze")),
                sep="\n"
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

@dp.message_handler(commands=['track'])
async def tracker(message:types.Message):
    await bot.send_message(message.chat.id,
    md.text(
        md.text("Currently tracking ",md.bold("732101"),"for 18+ slot")
    ), 
    parse_mode=ParseMode.MARKDOWN
    )
    
@dp.message_handler(state=Form.inviteCode)
async def process_code(message: types.Message, state: FSMContext):
    """
    Process invitation code
    """
    async with state.proxy() as data:
        data['invitecode'] = message.text        

    if(data['invitecode'] == config.INVITATION_CODE):
        await UpdateAuthUser()     
        await Form.next()
        await bot.send_message(
            message.chat.id,
            md.text(
                md.bold("Enter your nickname")
            ),
            parse_mode=ParseMode.MARKDOWN,
        )    

    else:
        await message.reply("Invalid Code\nMaybe you have misspelled the code\nUse /start to restart")

@dp.message_handler(state=Form.Name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process name
    """
    await Form.next()
    async with state.proxy() as data:
        data['name'] = message.text 
    
    await bot.send_message(
    message.chat.id,
    md.text(
        md.bold("Enter your Phone number")
    ),
    parse_mode=ParseMode.MARKDOWN,
    )   

@dp.message_handler(lambda message: message.text.isdigit(),state=Form.Phonenumber)
async def process_phone_number(message: types.Message, state: FSMContext):
    """
    Process phone number 
    """
    async with state.proxy() as data:
        data['phonenumber'] = int(message.text) 
    
    await  bot.send_message(
        message.chat.id,
        md.text(
            md.text("Hi!\nI'm GetVaccinated!"),
            md.text("I will ping you when a slot is available"),
            md.text("Currently Tracking", md.bold(732101),"and" ,md.bold(732128)),
            md.text(md.bold("To check tracking status use /track")),
            md.text("Planned Feature : Autobook :)"),
            md.text("Made with ❤️ by @Rajd333p"),
            sep='\n',
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
    await InsertChatID(message.chat.id, data['invitecode'],data['name'],data['phonenumber'])
    await state.finish()



    


# async def main():
#     await asyncio.gather(
#    # dp.start_polling(),
#     data()
#     )  
    

  

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())


