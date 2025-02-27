import logging
logger = logging.getLogger(__name__)

import asyncio
from pyrogram import filters
from bot import feedback
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from translation import Translation
from config import Config

@feedback.on_message(filters.text)
async def text(c, m):
      if m.from_user.id in Config.LOGIN:
         if m.text == Config.PASS:
            Config.LOGIN.remove(m.from_user.id)
            Config.OWNER.append(m.from_user.id)
            await m.reply_text(text="From now you will receive feedbacks. Untill this bot restart.  If you want to get feedbacks permanently add your id in config vars")
         if m.text != Config.PASS:
            Config.LOGIN.remove(m.from_user.id)
            await m.reply_text(text="**PASSWORD SALAH ⚠️**", parse_mode="markdown")
      if m.from_user.id in Config.feedback:
         button = [[
                   InlineKeyboardButton("Ya", callback_data="yes"),
                   InlineKeyboardButton("Tidak", callback_data="cancel")
                  ]]
         markup = InlineKeyboardMarkup(button)
         await m.reply_text(text="Apakah Kamu Telah Yakin untuk Mengirimkan Umpan Balik Ini?",
                            reply_markup=markup,
                            quote=True)
      try:
          if Config.SEND is not None:
             id = Config.SEND[0]
             await c.send_message(chat_id=int(id), text=m.text, parse_mode="markdown")
             Config.SEND.remove(id)
             await c.send_message(chat_id=m.chat.id, text="Notified successfully")
      except:
          pass

@feedback.on_message(filters.command(["start"]))
async def start(c, m):
      button = [[
                InlineKeyboardButton("Umpan Balik", callback_data="feedback"),
                InlineKeyboardButton("Peraturan", callback_data="rules"),
                ],
                [
                InlineKeyboardButton("Tentang", callback_data="about"),
                InlineKeyboardButton("Login", callback_data="login"),
               ]]
      markup = InlineKeyboardMarkup(button)
      await c.send_message(chat_id=m.chat.id,
                           text=Translation.START,
                           disable_web_page_preview=True,
                           reply_to_message_id=m.message_id,
                           reply_markup=markup)
