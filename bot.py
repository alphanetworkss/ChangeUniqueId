from telethon import TelegramClient, events, Button
from telethon.errors.rpcerrorlist import UserNotParticipantError, ChatAdminRequiredError
from os import getenv
from utils import link_gen
import logging
from dotenv import load_dotenv

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from .env file

api_id = getenv("API_ID")
api_hash = getenv("API_HASH")
bot_token = getenv("BOT_TOKEN")
force_sub_channel = getenv("FORCE_SUB", "my_introvert_world")

if not api_id or not api_hash or not bot_token:
    raise ValueError("API ID, API HASH, and BOT TOKEN must be set")

bot = TelegramClient(
    'Linkchanger',
    api_id=api_id,
    api_hash=api_hash
).start(
    bot_token=bot_token
)

async def check_subscription(event):
    try:
        await bot.get_permissions(force_sub_channel, event.sender_id)
        return True
    except UserNotParticipantError:
        await event.respond(
            "🛡 Subscribe Our Channels If You Want To Start The Bot And Download From It:\n\n"
            "➤ @Team_AlphaNetwork\n\n"
            "☑️ Done Subscribed! Click ✅CHECK",
            buttons=[
                Button.url("Subscribe", f"https://t.me/{force_sub_channel}"),
                Button.inline("✅CHECK", b"check_subscription")
            ]
        )
        return False
    except ChatAdminRequiredError:
        await event.respond(f"Please make me an admin in @{force_sub_channel} to use this bot.")
        return False

@bot.on(events.CallbackQuery(data=b"check_subscription"))
async def callback_check_subscription(event):
    if await check_subscription(event):
        await event.respond("You have successfully subscribed! You can now use the bot.")

# @bot.on(events.NewMessage(pattern='/start'))
# async def start(event):
#     await event.respond(
#             "*Follow Steps To Generate Link In Bulk*\n"
#             "1. Generate Your Secret ID:\n"
#             "- Click on the \"Get Secret ID\" button.\n"
#             "- The bot will send you a message with your secret ID in monospace format.\n"
#             "- Copy this ID for later use.\n\n"
#             "2. Start Bulk Link Maker Panel:\n"
#             "- Click on the \"Get script\" button to initiate the link maker panel.\n\n"
#             "3. Enter Your Details:\n"
#             "- Paste your JSON data: Enter the JSON data required for the script.\n"
#             "- Select Quality: Choose the desired quality setting for your script.\n"
#             "- Paste your Secret ID: Enter the secret ID you obtained from the Alpha bot.\n"
#             "4. Send File to Telegram Bot:\n"
#             "- Click on the \"Send to Telegram bot\" button to submit your details and start the link changing process.",
#             buttons=[
#                 Button.inline("Get Secret ID", b"get_chat_id")
#             ]
#         )

@bot.on(events.NewMessage(pattern='/start'))
async def bulk(event):
    if await check_subscription(event):
        await event.respond(
            f"*Follow Steps To Generate Script*\n"
            f"1. Generate Your Secret ID:\n"
            f"- Click on the \"Get Secret ID\" button.\n"
            f"- The bot will send you a message with your secret ID in monospace format.\n"
            f"- Copy this ID for later use.\n\n"
            # "2. Start Script Maker Panel:\n"
            # "- Click on the \"Get script\" button to initiate the link maker panel.\n\n"
            f"2. Enter Your Details:\n"
            f"- Paste your JSON data: Enter the JSON data required for the script.\n"
            f"- Select Quality: Choose the desired quality setting for your script.\n"
            f"- Paste your Secret ID: Enter the secret ID you obtained from the Alpha bot.\n"
            f"3. Send File to Telegram Bot:\n"
            f"- Click on the \"Send to Telegram bot\" button to submit your details and start the Script Making process.",
            buttons=[
                Button.url("For Pc", "https://t.me/Alpha_Script_Robot/AlphaNetwork")   
            ]
            buttons=[
                Button.url("For Phone", "https://t.me/Alpha_Script_Robot/mobile")
            ]
            buttons=[
                Button.inline("Get Secret ID", b"get_chat_id")
            ]
        )

@bot.on(events.CallbackQuery(data=b"get_chat_id"))
async def get_chat_id_callback(event):
    if await check_subscription(event):
        chat_id = event.chat_id
        await event.respond(f"Your Secret ID is: `{chat_id}`")

@bot.on(events.NewMessage(pattern='/secretid'))
async def get_chat_id_command(event):
    if await check_subscription(event):
        chat_id = event.chat_id
        await event.respond(f"Your Secret ID is: `{chat_id}`")

logger.info("Bot started..")
bot.run_until_disconnected()
