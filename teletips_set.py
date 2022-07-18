#Copyright ©️ 2021 TeLe TiPs. All Rights Reserved
#You are free to use this code in any of your project, but you MUST include the following in your README.md (Copy & paste)
# ##Credits - [Countdown Timer Telegram bot by TeLe TiPs] (https://github.com/teletips/CountdownTimer-TeLeTiPs)

# Changing the code is not allowed! Read GNU AFFERO GENERAL PUBLIC LICENSE: https://github.com/teletips/CountdownTimer-TeLeTiPs/blob/main/LICENSE
 
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
import asyncio
from plugins.teletips_t import *
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.raw.functions.messages import UpdatePinnedMessage

bot=Client(
    "Countdown-TeLeTiPs",
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
    bot_token = os.environ["BOT_TOKEN"]
)

footer_message = os.environ["FOOTER_MESSAGE"]

stoptimer = False

TELETIPS_MAIN_MENU_BUTTONS = [
            [
                InlineKeyboardButton('❓ হেল্প', callback_data="HELP_CALLBACK")
            ],
            [
                InlineKeyboardButton('👥 সাপোর্ট', callback_data="GROUP_CALLBACK"),
                InlineKeyboardButton('📣 চ্যানেল', url='https://t.me/Edu_Mentors'),
                InlineKeyboardButton('👨‍💻 প্রস্তুতকারী', url='https://t.me/Edu_Mentors')
            ],
            [
                InlineKeyboardButton('➕ আপনি নিজে তৈরী করতে... ➕', callback_data="TUTORIAL_CALLBACK")
            ]
        ]

@bot.on_message(filters.command(['start','help']) & filters.private)
async def start(client, message):
    text = START_TEXT
    reply_markup = InlineKeyboardMarkup(TELETIPS_MAIN_MENU_BUTTONS)
    await message.reply(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

@bot.on_callback_query()
async def callback_query(client: Client, query: CallbackQuery):
    if query.data=="HELP_CALLBACK":
        TELETIPS_HELP_BUTTONS = [
            [
                InlineKeyboardButton("⬅️ ফিরুন", callback_data="START_CALLBACK")
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_HELP_BUTTONS)
        try:
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="GROUP_CALLBACK":
        TELETIPS_GROUP_BUTTONS = [
            [
                InlineKeyboardButton("চ্যানেল", url="https://t.me/Edu_Mentors")
            ],
            [
                InlineKeyboardButton("⬅️ ফিরুন", callback_data="START_CALLBACK"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_GROUP_BUTTONS)
        try:
            await query.edit_message_text(
                GROUP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass    

    elif query.data=="TUTORIAL_CALLBACK":
        TELETIPS_TUTORIAL_BUTTONS = [
            [
                InlineKeyboardButton("🎥 ভিডিও", url="https://youtube.com/channel/UCx_5rSPlRMoZqtnvOLBZWDQ")
            ],
            [
                InlineKeyboardButton("⬅️ ফিরুন", callback_data="START_CALLBACK"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_TUTORIAL_BUTTONS)
        try:
            await query.edit_message_text(
                TUTORIAL_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass      
          
    elif query.data=="START_CALLBACK":
        TELETIPS_START_BUTTONS = [
            [
                InlineKeyboardButton('❓ হেল্প', callback_data="HELP_CALLBACK")
            ],
            [
                InlineKeyboardButton('👥 সাপোর্ট', callback_data="GROUP_CALLBACK"),
                InlineKeyboardButton('📣 চ্যানেল', url='https://t.me/Edu_Mentors'),
                InlineKeyboardButton('👨‍💻 প্রস্তুতকারী', url='https://t.me/Edu_Mentors')
            ],
            [
                InlineKeyboardButton('➕ আপনি নিজে তৈরী করতে... ➕', callback_data="TUTORIAL_CALLBACK")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_START_BUTTONS)
        try:
            await query.edit_message_text(
                START_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass    

@bot.on_message(filters.command('set'))
async def set_timer(client, message):
    global stoptimer
    try:
        if message.chat.id>0:
            return await message.reply('⛔️ গ্রুপে কমান্ড দিন')
        elif not (await client.get_chat_member(message.chat.id,message.from_user.id)).privileges:
            return await message.reply('👮🏻‍♂️ দুঃখিত, শুধুমাত্র **অ্যাডমিন** এই কমান্ড দেয়ার ক্ষমতা রাখে')    
        elif len(message.command)<3:
            return await message.reply('❌ **ভূল ফরম্যাট**\n\n✅ এভাবে দেয়া উচিত,\n<code> /set সময় (সেকেন্ডে) "বিষয়ের নাম"</code>\n\n**যেমন**:\n <code>/set 10 "১০ সেকেন্ড কাউন্টডাউন" (ইংরেজিতে)</code>')    
        else:
            user_input_time = int(message.command[1])
            user_input_event = str(message.command[2])
            get_user_input_time = await bot.send_message(message.chat.id, user_input_time)
            await get_user_input_time.pin()
            if stoptimer: stoptimer = False
            if 0<user_input_time<=10:
                while user_input_time and not stoptimer:
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**s**\n\n<i>{}</i>'.format(user_input_event, s, footer_message)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(1)
                    user_input_time -=1
                await finish_countdown.edit("🚨 টুং! টুং!! বিপ! বিপ!!! **সময় হয়ে গেছে!!!**")
            elif 10<user_input_time<60:
                while user_input_time>0 and not stoptimer:
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**s**\n\n<i>{}</i>'.format(user_input_event, s, footer_message)   
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(3)
                    user_input_time -=3
                await finish_countdown.edit("🚨 টুং! টুং!! বিপ! বিপ!!! **সময় হয়ে গেছে!!!**")
            elif 60<=user_input_time<3600:
                while user_input_time>0 and not stoptimer:
                    m=user_input_time%3600//60
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**m** : {:02d}**s**\n\n<i>{}</i>'.format(user_input_event, m, s, footer_message)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(3)
                    user_input_time -=3
                await finish_countdown.edit("🚨 টুং! টুং!! বিপ! বিপ!!! **সময় হয়ে গেছে!!!**")
            elif 3600<=user_input_time<86400:
                while user_input_time>0 and not stoptimer:
                    h=user_input_time%(3600*24)//3600
                    m=user_input_time%3600//60
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**h** : {:02d}**m** : {:02d}**s**\n\n<i>{}</i>'.format(user_input_event, h, m, s, footer_message)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(7)
                    user_input_time -=7
                await finish_countdown.edit("🚨 টুং! টুং!! বিপ! বিপ!!! **সময় হয়ে গেছে!!!**")
            elif user_input_time>=86400:
                while user_input_time>0 and not stoptimer:
                    d=user_input_time//(3600*24)
                    h=user_input_time%(3600*24)//3600
                    m=user_input_time%3600//60
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**d** : {:02d}**h** : {:02d}**m** : {:02d}**s**\n\n<i>{}</i>'.format(user_input_event, d, h, m, s, footer_message)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(9)
                    user_input_time -=9
                await finish_countdown.edit("🚨 টুং! টুং!! বিপ! বিপ!!! **সময় হয়ে গেছে!!!**")
            else:
                await get_user_input_time.edit(f"🤷🏻‍♂️ দুঃখিত, আমি {user_input_time} এই সময় থেকে কাউন্টডাউন করতে পারব না")
                await get_user_input_time.unpin()
    except FloodWait as e:
        await asyncio.sleep(e.value)

@bot.on_message(filters.command('stopc'))
async def stop_timer(Client, message):
    global stoptimer
    try:
        if (await bot.get_chat_member(message.chat.id,message.from_user.id)).privileges:
            stoptimer = True
            await message.reply('🛑 কাউন্টডাউন থামানো হয়েছে।')
        else:
            await message.reply('👮🏻‍♂️ দুঃখিত, শুধুমাত্র **অ্যাডমিন** এই কমান্ড দেয়ার ক্ষমতা রাখে')
    except FloodWait as e:
        await asyncio.sleep(e.value)

print("কাউন্টডাউন চলছে.....!!!")
bot.run()

#Copyright ©️ 2021 EduMentors. All Rights Reserved
