from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon import functions, types
from os import listdir, mkdir
from sys import argv
from re import search
from colorama import Fore
import asyncio, argparse

# Arguments parser
parser = argparse.ArgumentParser(description='A tool for reporting Telegram channels', add_help=False)
parser.add_argument('-an', '--add-number', help='Add a new account')
parser.add_argument('-r', '--run', help='Set count of reports', type=int)
parser.add_argument('-t', '--target', help='Enter target (without @)', type=str)
parser.add_argument('-m', '--mode', help='Set reason of reports', choices=['spam', 'fake_account', 'violence', 'child_abuse', 'pornography', 'geoirrelevant'])
parser.add_argument('-re', '--reasons', help='Show list of reasons', action='store_true')
parser.add_argument('-h', '--help', action='store_true')
args = parser.parse_args()

# Create sessions directory if it doesn't exist
try:
    mkdir('sessions')
except: pass

sesis = listdir('sessions')
sesis.sort()
api_id = '24043364'
api_hash = 'b27094593db92b4e76ad1be7fb4ec817'

if args.help:
    print(f'''Help:
  -an {Fore.LIGHTBLUE_EX}NUMBER{Fore.RESET}, --add-number {Fore.LIGHTBLUE_EX}NUMBER{Fore.RESET} ~> {Fore.YELLOW}add account to script{Fore.RESET}
  example: python3 {argv[0]} -an {Fore.LIGHTBLUE_EX}+1512****{Fore.RESET}

  -r {Fore.LIGHTBLUE_EX}COUNT{Fore.RESET}, --run {Fore.LIGHTBLUE_EX}COUNT{Fore.RESET} ~> {Fore.YELLOW}set count of reports{Fore.RESET}
  -t {Fore.LIGHTBLUE_EX}TARGET{Fore.RESET}, --target {Fore.LIGHTBLUE_EX}TARGET{Fore.RESET} ~> {Fore.YELLOW}set target (without @){Fore.RESET}
  -m {Fore.LIGHTBLUE_EX}MODE{Fore.RESET}, --mode {Fore.LIGHTBLUE_EX}MODE{Fore.RESET} ~> {Fore.YELLOW}set type of reports (spam,...){Fore.RESET}
  example: python3 {argv[0]} -r {Fore.LIGHTBLUE_EX}1000{Fore.RESET} -t {Fore.LIGHTBLUE_EX}mmdChannel{Fore.RESET} -m {Fore.LIGHTBLUE_EX}spam{Fore.RESET}

  -re, --reasons ~> {Fore.YELLOW}show list of reasons for reporting{Fore.RESET}
  -h, --help ~> {Fore.YELLOW}show help{Fore.RESET}''')
elif args.reasons:
    print(f'''List of reasons:
    {Fore.YELLOW}*{Fore.RESET} spam
    {Fore.YELLOW}*{Fore.RESET} fake_account
    {Fore.YELLOW}*{Fore.RESET} violence
    {Fore.YELLOW}*{Fore.RESET} child_abuse
    {Fore.YELLOW}*{Fore.RESET} pornography
    {Fore.YELLOW}*{Fore.RESET} geoirrelevant''')
elif args.add_number:
    number = args.add_number
    if sesis:
        nums = [int(search('Ac(\d+)\.session', x).group(1)) for x in sesis]
        nums.sort()
        ses = TelegramClient(f'sessions/Ac{nums[-1]+1}', api_id, api_hash)
    else:
        ses = TelegramClient(f'sessions/Ac1', api_id, api_hash)
    try:
        ses.start(number)
        print(f' [{Fore.GREEN}✅{Fore.RESET}] Your account added successfully :D')
    except PhoneNumberInvalidError:
        print(f' [{Fore.RED}!{Fore.RESET}] The phone number was invalid!')
elif args.run and args.target and args.mode:
    if not sesis:
        print(f' [{Fore.RED}!{Fore.RESET}] Please add an account to reporting!')
    else:
        count = args.run
        target = args.target
        async def report(client):
            async with client:
                selfName = await client.get_entity('self')
                selfName = selfName.first_name
                try:
                    repMes = await client.get_messages(target, limit=3)
                except ValueError:
                    print(f' [{Fore.RED}!{Fore.RESET}] The link of the channel was invalid!')
                    return
                
                repMess = [m.id for m in repMes]
                async for dialog in client.iter_dialogs():
                    if dialog.is_channel and dialog.entity.username == target:
                        exi = True
                        break
                else:
                    exi = False
                
                if not exi:
                    await client(JoinChannelRequest(target))
                    await asyncio.sleep(1)
                
                for r in range(count):
                    if args.mode == 'spam':
                        reason = types.InputReportReasonSpam()
                    elif args.mode == 'fake_account':
                        reason = types.InputReportReasonFake()
                    elif args.mode == 'violence':
                        reason = types.InputReportReasonViolence()
                    elif args.mode == 'child_abuse':
                        reason = types.InputReportReasonChildAbuse()
                    elif args.mode == 'pornography':
                        reason = types.InputReportReasonPornography()
                    elif args.mode == 'geoirrelevant':
                        reason = types.InputReportReasonGeoIrrelevant()
                    
                    result = await client(functions.messages.ReportRequest(peer=target, id=repMess, reason=reason, message="This channel sends offensive content"))
                    if result:
                        print(f" [{Fore.GREEN}✅{Fore.RESET}] Reported :) Ac:{Fore.YELLOW}{selfName}{Fore.RESET} count:{Fore.LIGHTBLUE_EX}{r}{Fore.RESET}")
                    else:
                        print(f" [{Fore.RED}!{Fore.RESET}] Error :( Ac:{Fore.YELLOW}{selfName}{Fore.RESET}, count:{Fore.LIGHTBLUE_EX}{r}{Fore.RESET}")

        async def main():
            tasks = [report(TelegramClient(f'sessions/Ac{num}', api_id, api_hash)) for num in range(1, len(sesis) + 1)]
            await asyncio.gather(*tasks)

        asyncio.run(main())
elif args.run and (not args.target or not args.mode):
    print(f" [{Fore.RED}!{Fore.RESET}] Please use this format: python3 {argv[0]} -r 10000 -t mmdChannel -m reportReason")
else:
    print(f"""
    _____    _ __    t.me/{Fore.MAGENTA}Mr3rf1{Fore.RESET}    💀
   |_   _|__| |  _ \ ___ _ __   ___ _ __
     | |/ _ \ | |_) / _ \ '_ \ / _ \ '__|
     | |  __/ |  _ <  __/ |_) |  __/ |
     |_|\___|_|_| \_\___| .__/ \___|_|
                         |_|
     github.com/e811-py
{Fore.YELLOW}-----------------------------------------------{Fore.RESET}
a tool for reporting telegram channels by @Mr3rf1
use --help to see help: python3 {argv[0]} --help
    """)

### Requirements for Termux
1. Python
2. Telethon
3. Colorama

### Commands to Install Requirements in Termux
```bash
pkg update && pkg upgrade
pkg install python
pip install telethon colorama
