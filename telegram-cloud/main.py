from telethon import TelegramClient, events, utils

import argparse
from telegram_config import fetch_app_data

parser = argparse.ArgumentParser()

# Read arguments from the command line
parser.add_argument("--name", "-n", help = "That unique name you've set at the first", required = True)
parser.add_argument("--username", "-u", help = "Set target username for sending file/files to her/him", required = True)
parser.add_argument("--path", "-p", help = "Path of the file/files you want to upload", required = True)
parser.add_argument("--mode", "-m", help="Change mode to upload or download", required=True)
parser.add_argument("--caption", "-c", help = "Give me caption to write it under file", default = '', required = False)

args = parser.parse_args()

# Get session name from CLI
unique_name = args.name

# Get the session data to use TelegramClient
api_id, api_hash, name = fetch_app_data(unique_name)
client = TelegramClient(name, api_id, api_hash)

async def main():

    # Get username target 
    username = args.username

    # Convert and handle all types of username and chat id to target chat 
    if ('-' in username or '+' in username) and (username[1].isdigit() == True):
        target_chat = await client.get_entity(int(username))
    else:
        target_chat = await client.get_entity(username)

    # Retrieve and download a file from its name or caption, from specific target_chat
    if args.mode == 'download':
        if args.caption and args.path and username:
            async for message in client.iter_messages(entity=username, search=args.caption):
                await client.download_media(message, args.path)

    # Upload file to specific target_chat and retrieve the file_id
    elif args.mode == 'upload':
        if args.path and username:
            message = await client.send_file(entity=target_chat, file=args.path, caption=args.caption)
            print("File id: " + message.file.id)

with client:
    client.loop.run_until_complete(main())
