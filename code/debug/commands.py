from teleflask import TBlueprint
from teleflask.messages import HTMLMessage

from html import escape
from .gitinfo import VERSION_STR

bot = TBlueprint(__name__)


@bot.command('version')
def cmd_version(update, text):
    return HTMLMessage('Version <code>{version}</code> of bot <a href="tg://user?id={bot_id}">@{bot_username}</a>'.format(
        version=escape(VERSION_STR)), bot_id=escape(str(bot.user_id)), bot_username=escape(bot.username)
    )
# end def
