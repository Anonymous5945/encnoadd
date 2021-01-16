#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import io
import asyncio
import inspect
import os
import time
import sys
import traceback
import aiohttp
import json
import urllib.parse
import urllib.parse
import shlex
import requests
from telegraph import Telegraph
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup
)

from datetime import datetime
from pyrogram import Client, filters

from bs4 import BeautifulSoup
import urllib3

from tobrot import (
    MAX_MESSAGE_LENGTH,
    DOWNLOAD_LOCATION
)

from tobrot.helper_funcs.display_progress import progress_for_pyrogram

async def down_load_media_f(client, message):
    user_id = message.from_user.id
    print(user_id)
    mess_age = await message.reply_text("processing...", quote=True)
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    if message.reply_to_message is not None:
        start_t = datetime.now()
        download_location = "/app/"
        c_time = time.time()
        the_real_download_location = await client.download_media(
            message=message.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                "trying to download", mess_age, c_time
            )
        )
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        
        LOGGER.info(the_real_download_location)
        sam = os.path.basename(the_real_download_location)
        extension = os.path.splitext(the_real_download_location)[1]
        if extension == ".srt" or extension == ".vtt":
           with open(the_real_download_location) as myfile:
             head = [next(myfile) for x in range(7)]
             with open(u_output) as myfile:
               telegraph = Telegraph()
               telegraph.create_account(short_name='1337')
               response = telegraph.create_page(
                 'Subtitle Content',
                 html_content="".join([next(myfile) + "<br>" for x in range(50)])
                    )
               file_context= 'https://telegra.ph/{}'.format(response['path'])
             await mess_age.edit_text(f"<b>OUTPUT:</b>\n\n<code>{the_real_download_location}</code>\n\n<b>First 7 lines of Sub:</b>\n\n<code>{head}</code>\n\nFinished in <u>{ms}</u> seconds",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🌿 Subtitle Content 🌿', url=file_context)],]))
             the_real_download_location_g = os.path.basename(the_real_download_location)
             LOGGER.info(the_real_download_location_g)
        else:
           await mess_age.edit_text(f"<b>OUTPUT:</b>\n\n<code>{the_real_download_location}</code>\n\nFinished in <u>{ms}</u> seconds")
           the_real_download_location_g = os.path.basename(the_real_download_location)
           LOGGER.info(the_real_download_location_g)

    else:
        #await asyncio.sleep(4)
        await mess_age.edit_text("Reply to a Telegram Media, to save to the server.")


async def mass_down_load_media_f(client, message):
    user_id = message.from_user.id
    print(user_id)
    mess_age = await message.reply_text("processing...", quote=True)
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)    
    n=message.message_id
    w=message.reply_to_message.message_id
    tar_id = message.chat.id
    start_t = datetime.now()
    if message.reply_to_message is not None:
      try:
        u_out = message.text.split(" ")[1]
        new_name = os.path.basename(u_out)
        output_directory = os.path.dirname(os.path.abspath(new_name))
        f = os.path.join(output_directory, new_name) + "/"
        for i in range(w, n):
          u_id = int(i)
          m = await client.get_messages(tar_id, u_id)
          if m.media:
             await m.download(f)
             await asyncio.sleep(10)
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        await mess_age.edit_text(f"<b>OUTPUT:</b>\n\n <code>{f}</code> \n\ncompleted in <u>{ms}</u> seconds")
      except IndexError:
        pass
        await mess_age.edit("please type output folder name with run command")
    else:
        #await asyncio.sleep(4)
        await mess_age.edit_text("Reply to a Telegram Media, to save to the server.")


async def gp_f(client, message):
    status_message = await message.reply_text("Processing ...")
    async with aiohttp.ClientSession() as session:
      w=message.reply_to_message.message_id
      u_id = int(w)
      user_id = message.chat.id
      m = await client.get_messages(user_id, u_id)
      if m and m.text and m.text.lower().startswith("http"):
         link_text = m.text
         SHORTEN_LINK_API_KEY="04ff157ce8cb9727afca4641be87af6b5aa27a5d"
         SHORTEN_LINK_API_URL="https://gplinks.in/api?api={api_token}&url={long_url}&format=text"
         long_url = link_text
         request_url = SHORTEN_LINK_API_URL.format(api_token=SHORTEN_LINK_API_KEY, long_url=long_url)
         response_text = await (await session.get(request_url)).text()
      await status_message.edit(response_text)
        
async def scrap_seg_media_f(client, message):
    status_message = await message.reply_text("Processing ...") 
    http = urllib3.PoolManager()
    url = message.reply_to_message.text
    try:
      url_parts = shlex.split(message.text)
      if len(url_parts) == 2:
       n = url_parts[1]
       f1= "2"
      elif len(url_parts) == 3:
       n1 = url_parts[1]
       n2 = url_parts[2]
       f1 = "3"
      if f1 == "2":
       w=int(n)
       response = http.request('GET', url)
       soup = BeautifulSoup(response.data, "html.parser")
       links = soup.find_all('a')
       i=1
       for tag in links:
         link = tag.get('href',None)
         tght = tag.text.strip()
         if link and "ddrive" in link:
            if i < w:
               i = i+1
            else:
               await message.reply_text(f"<a href='{link}'>{tght}</a>")
               await asyncio.sleep(3)
      else:
       w1=int(n1)
       w2=int(n2)
       page = requests.get(url)
       soup = BeautifulSoup(page.text, 'html.parser')
       links = soup.find_all('a')
       i= 1
       for tag in links:
        link = tag.get('href',None)
        tght = tag.text.strip()
        if link and "www.iq.com/play" in link:
         if i > w1 and i < w2:
           await message.reply_text(link)
           await asyncio.sleep(3)
           i=i+1
         else:
            i=i+1
    except IndexError:
      pass
      await status_message.edit("please type limit with run command")
    await status_message.edit("Success")

async def wetv_f(client, message):
    status_message = await message.reply_text("Processing ...")
    with open("test.json", "w+") as fd:
      fd.write(message.reply_to_message.text)
    with open('test.json') as json_file:
      data = json.load(json_file)
    link = data['vurl']
    encodedStr = link
    tv = urllib.parse.unquote(encodedStr)
    await status_message.edit(tv)
    os.remove("test.json")
