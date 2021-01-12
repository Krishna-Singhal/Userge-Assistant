# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__all__ = ["Config"]

import os
import importlib

from dotenv import load_dotenv
from assistant import bot, cus_filters, DB, logging

_LOG = logging.getLogger(__name__)

path = "Userge-Assistant/temp_plugins/"

if os.path.isfile("config.env"):
    load_dotenv("config.env")


class Config:
    """ assistant configs """
    APP_ID = int(os.environ.get("APP_ID", 0))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    AUTH_CHATS = set([-1001481357570])  # @UserGeOt
    if os.environ.get("AUTH_CHATS"):
        AUTH_CHATS.update(map(int, os.environ.get("AUTH_CHATS").split()))
    WHITELIST_CHATS = set([-1001465749479])  # @UserGeSpam
    if os.environ.get("WHITELIST_CHATS"):
        WHITELIST_CHATS.update(map(int, os.environ.get("WHITELIST_CHATS").split()))
    PLUGINS_ID = []
    if os.environ.get("PLUGINS_ID"):
        PLUGINS_ID = [
            int(x.strip()) for x in os.environ.get("PLUGINS_ID").split() if x.strip()
        ]
    DEV_USERS = (
        1158855661,  # @Krishna_Singhal
        1110621941,  # @PhycoNinja13b
        921420874,   # @juznem
        837784353    # @rking_32
    )
    ADMINS = {}
    MAX_MSG_LENGTH = 4096


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
