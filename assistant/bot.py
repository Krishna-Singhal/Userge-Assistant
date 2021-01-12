# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__all__ = ["bot", "START_TIME"]

import time

from pyrogram import Client

from . import Config, logging

path = "Userge-Assistant/temp_plugins/"

_LOG = logging.getLogger(__name__)
START_TIME = time.time()

bot = Client(":memory:",
             api_id=Config.APP_ID,
             api_hash=Config.API_HASH,
             bot_token=Config.BOT_TOKEN,
             plugins={'root': "assistant.plugins"})


async def _init():
    if len(Config.PLUGINS_ID) > 0:
        _LOG.info("Loading Temp PLugins...")
        plg_list = []
        msg = await bot.get_messages(DB.CHANNEL_ID, Config.PLUGINS_ID)
        for i in len(Config.PLUGINS_ID):
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
                    plugin = '.'.join(t_path.split('/'))[:-3]
                    try:
                        load_plugin(plugin)
                    except Exception:
                        os.remove(t_path)
                    else:
                        plg_list.append(document.file_name[:-3])
        _LOG.info(f"Loaded Plugins: {plg_list}")


def load_plugin(name: str):
    _LOG.info(f"Loading temp_plugins.{name.split('.')[-1]}")
    try:
        importlib.import_module(name)
    except ImportError as i_e:
        _LOG.error(i_e)
        raise
    else:
        _LOG.info(f"Loaded temp_plugins.{name.split('.')[-1]} Plugin Successfully!")


_LOG.info("assistant-bot initialized!")
