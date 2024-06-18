from telethon.tl.types import ReplyKeyboardMarkup, KeyboardButtonRow, KeyboardButton
from telethon.tl.custom import Button


async def link_gen(link_hash, bot, event):
    async with bot.conversation(event.chat_id, timeout=200) as conv:
        try:
            await conv.send_message(
            'Please select the quality:',   
            buttons = ReplyKeyboardMarkup(
                rows=[
                    KeyboardButtonRow(
                        buttons=[
                            KeyboardButton(text="240"),
                            KeyboardButton(text="360"),
                            KeyboardButton(text="480"),
                            KeyboardButton(text="720"),
                        ]
                    )
                ],
                resize=True,
                persistent=True,
                placeholder="Please select the quality:"
            ))

            quality = await conv.get_response()
            await conv.send_message(
                "Please enter the name of the lecture:",
                buttons = Button.clear()
            )
            name = await conv.get_response()
            new_link = f"""
__**Download link for Bot**__
`https://pw.jarviis.workers.dev?v={link_hash}&quality={quality.raw_text} -n {name.raw_text} (@Team_AlphaNetwork)`


__**1DM link**__
`https://pw.jarviis.workers.dev?v={link_hash}`

"""
                        
            await conv.send_message(
                new_link
                
            )

        except TimeoutError:
            await event.respond(
                f"Timed out, try again",
                buttons = Button.clear()
                
            )
