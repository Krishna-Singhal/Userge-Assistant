# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge-Assistant > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Userge-Assistant/blob/master/LICENSE >
#
# All rights reserved.

from assistant import bot, Config, DB, logging

_LOG = logging.getLogger(__name_)
path = "Userge-Assistant/assistant/plugins/"

async def _init():
    _LOG.info(len(Config.PLUGINS_ID))
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
    try:
        importlib.import_module(name)
    except ImportError as i_e:
        _LOG.error(i_e)
        raise
