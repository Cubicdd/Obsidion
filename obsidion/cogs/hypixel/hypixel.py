"""Images cog."""
import logging

from discord.ext import commands

from obsidion.core.i18n import cog_i18n
from obsidion.core.i18n import Translator

log = logging.getLogger(__name__)

_ = Translator("Hypixel", __file__)


@cog_i18n(_)
class Hypixel(commands.Cog):
    def __init__(self, bot) -> None:
        """Init."""
        self.bot = bot