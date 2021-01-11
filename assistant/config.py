# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

__all__ = ["Config"]

import os

from dotenv import load_dotenv

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
    DEV_USERS = (
        1158855661,  # @Krishna_Singhal
        1110621941,  # @PhycoNinja13b
        921420874,   # @juznem
        837784353    # @rking_32
    )
    ADMINS = {}
    LOAD_ADDITIONAL_PLUGINS = True
    MAX_MSG_LENGTH = 4096

if Config.LOAD_ADDITIONAL_PLUGINS:
    _LOG.info("Loading Additional Plugins...")
    os.system("git clone --depth=1 https://github.com/Krishna-Singhal/Assistant-Plugins.git")
    os.system("pip3 install -U pip && pip3 install -r Assistant-Plugins/requirements.txt")
    os.system("mv Assistant-Plugins/plugins/ Userge-Assistant/plugins/ && rm -rf Assistant-Plugins/")
    _LOG.info("UnOfficial Plugins Loaded Successfully!")
