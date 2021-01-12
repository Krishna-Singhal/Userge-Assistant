# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

import os
import importlib

from pyrogram import filters
from pyrogram.types import Message

from assistant import bot, cus_filters, DB, logging
from assistant.Config import PLUGINS_ID

_LOG = logging.getLogger(__name__)
path = "Userge-Assistant/temp_plugins/"


async def _init():
    if len(PLUGINS_ID) > 0:
        _LOG.info("Loading Temp PLugins...)
        plg_list = []
        msg = await bot.get_messages(DB.CHANNEL_ID, PLUGINS_ID)
        for i in len(PLUGINS_ID):
            file = msg[i]
            document = file.document
            if file and document:
                if document.file_name.endswith('.py') and document.file_size < 2 ** 20:
                    if not os.path.isdir(path):
                        os.makedirs(path)
                    t_path = path + document.file_name
                    if os.path.isfile(t_path):
                        os.remove(t_path)
                    await file.download(file_name=t_path)
                    plugin = '.'.join(
                        os.path.relpath(t_path, os.path.dirname(__file__)
                    ).split('/'))[:-3]
                    try:
                        load_plugin(plugin)
                    except Exception:
                        os.remove(t_path)
                    else:
                        plg_list.append(document.file_name)
        _LOG.info(f"Loaded Plugins: {plg_list}")


@bot.on_message(filters.command("load") & cus_filters.auth_chats & cus_filters.auth_users)
async def _loader(_, msg: Message):
    replied = msg.reply_to_message
    document = replied.document
    if replied and document:
        if document.file_name.endswith('.py') and document.file_size < 2 ** 20:
            k = await msg.reply("Loading...")
            if not os.path.isdir(path):
                os.makedirs(path)
            t_path = path + document.file_name
            if os.path.isfile(t_path):
                os.remove(t_path)
            await replied.download(file_name=t_path)
            plugin = '.'.join(
                os.path.relpath(t_path, os.path.dirname(__file__)
            ).split('/'))[:-3]
            try:
                load_plugin(plugin)
            except Exception as e:
                os.remove(t_path)
                await k.edit(f"`{str(e)}`")
            else:
                await k.edit(f"`Loaded {document.file_name} Successfully`", del_in=3)


def load_plugin(name: str):
    _LOG.info(f"Loading temp_plugins.{name.split('.')[-1]}")
    try:
        importlib.import_module(name)
    except ImportError as i_e:
        _LOG.error(i_e)
        raise
    else:
        _LOG.info(f"Loaded temp_plugins.{name.split('.')[-1]} Plugin Successfully!")
