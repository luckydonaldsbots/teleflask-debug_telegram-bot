# -*- coding: utf-8 -*-
import json

from pytgbot import Bot
from pytgbot.api_types.receivable.updates import Update
from luckydonaldUtils.logger import logging
from flask import Flask, request, jsonify
from teleflask import Teleflask
from teleflask.messages import HTMLMessage
from html import escape

from .utils import to_json_remove_api_key, msg_get_reply_params
from .secrets import API_KEY, EVENT_CHANNEL, SERVER_BASE_URL
from .commands import bot as commands_tbp
from .features import bot as features_tbp
from .gitinfo import bot as versions_tbp

__author__ = 'luckydonald'
logger = logging.getLogger(__name__)

logging.add_colored_handler(level=logging.DEBUG)


app = Flask(__name__)

bot = Teleflask(API_KEY)

if SERVER_BASE_URL:
    logger.debug(f'Bot is now using base URL {SERVER_BASE_URL!r} for telegram requests.')
    _bot = Bot(API_KEY),
    _bot._base_url = SERVER_BASE_URL
    bot._bot = _bot
# end if

bot.init_app(app)  # postponed until the bot is set

bot.register_tblueprint(commands_tbp)
bot.register_tblueprint(features_tbp)
bot.register_tblueprint(versions_tbp)


@app.route("/info/<api_key>/<command>")
@to_json_remove_api_key
def info(api_key, command):

    """
    Issue commands. E.g. /info/getMe

    :param command:
    :return:
    """
    if api_key != API_KEY:
        error_msg = "Wrong API key: {wrong_key}".format(wrong_key=api_key)
        logger.warning(error_msg)
        return error_msg, 403
    # end if
    logger.debug("COMMAND: {cmd}, ARGS: {args}".format(cmd=command, args=request.args))
    return repr(bot.bot.do(command, **request.args)).replace(API_KEY, "<API_KEY>")
# end def


@bot.on_update()
def income(update):
    assert isinstance(update, Update)
    reply_chat_id, reply_message_id = msg_get_reply_params(update)
    if reply_chat_id is None:
        logger.error("could not find chat:\n{}".format(update))
        reply_chat_id = EVENT_CHANNEL
    # end if
    if update._raw:
        string = json.dumps(update._raw, indent=4, sort_keys=True, ensure_ascii=False)
    else:
        string = json.dumps(update.to_array(), indent=4, sort_keys=True, ensure_ascii=False)
    # end if
    return HTMLMessage(
        "<pre>{}</pre>".format(escape(string)),
        receiver=reply_chat_id, reply_id=reply_message_id
    )
# end def


@app.route("/")
def hello():
    return "<h1>Your advertisements could be here!</h1>"
# end def


@app.route("/healthcheck")
@to_json_remove_api_key
def healthcheck():
    overall_status = True
    # TODO

    status = {
        "health": overall_status,
    }
    status_response = jsonify(status)
    """:type status_status_response: Response"""
    status_code = 200 if overall_status else 500
    return status_response, status_code
# end def



if __name__ == "__main__":  # no nginx
    # "__main__" means, this python file is called directly.
    # not to be confused with "main" (because main.py) when called from from nginx
    app.run(host='0.0.0.0', debug=True, port=80)  # python development server if no nginx
# end if

