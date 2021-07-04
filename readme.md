

# CowinSlotNotifier

This a fully aSync client with a telegram bot integrated
to scan and notify users when a vaccination slot is available.
By default only 18+ slot not 45+ (easy to change check line no. 43 in main.py)
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/).

```bash
pip install -r requirement.txt
```

## Config

```python
Open Config.py

INVITATION_CODE = "" # The invite code you want  ​the user to input

BOT_TOKEN = "" #Telegram bot token

MONGODB_URl = "" #MongoDb atlas URL

OWNER_ID = 000000000 #Chat Id of the owner

PINCODES = ["000000"] #pincodes 

"""
Can track 10 pincodes with 30sec Interval 
after every round.(can be more then 10 if
interval is increased)

One round contains all pincodes data at once.
"""

MAIN_CLUSTER = "" 
USER_INFO_COLLECTION = "" # mainly bot stats like number of users 
                      ​
SUSER_DATA_COLLECTION = "" # mainly user data  
```
## Run

```python
python main.py
```

## Commands
```bash
/start - Start the bot
/track - Current tracking status
/status - check snooze status
/snooze - stop notifications
/unsnooze - restart notifications

/sendall - BroadCast message as announcement to all users snooze status does not matter(Owner Only)
/stats   - Returns number of users (Owner Only)
/getlogs - Get Error.txt file (Owner only)

```



## Todo (not confirmed)
1. Personalized pincode tracking.
2. Autobook (ground work already laid for database part)
3. Choices in Vaccine, Age-Group, Fee Type
4. Horizontal Scaling using tracking(requires proxies) only containers 
   and RabbitMQ communication in between.

## License
[MIT](https://choosealicense.com/licenses/mit/)
