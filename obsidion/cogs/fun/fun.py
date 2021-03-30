"""Images cog."""
import json
import logging
from datetime import datetime
from random import choice

import discord
from discord.ext import commands
from obsidion.core import get_settings
from obsidion.core.i18n import cog_i18n
from obsidion.core.i18n import Translator
from discord_slash import cog_ext


log = logging.getLogger(__name__)

_ = Translator("Fun", __file__)

minecraft = (
    "ᔑ",
    "ʖ",
    "ᓵ",
    "↸",
    "ᒷ",
    "⎓",
    "⊣",
    "⍑",
    "╎",
    "⋮",
    "ꖌ",
    "ꖎ",
    "ᒲ",
    "リ",
    "𝙹",
    "!",
    "¡",
    "ᑑ",
    "∷",
    "ᓭ",
    "ℸ",
    " ̣",
    "⚍",
    "⍊",
    "∴",
    " ̇",
    "|",
    "|",
    "⨅",
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X",
)
alphabet = "abcdefghijklmnopqrstuvwxyz123456789"


@cog_i18n(_)
class Fun(commands.Cog):
    def __init__(self, bot) -> None:
        """Init."""
        self.bot = bot

    @commands.command(aliases=["villagerspeak", "villagerspeech", "hmm"])
    async def villager(self, ctx: commands.Context, *, speech: str) -> None:
        """Hmm hm hmmm Hm hmmm hmm."""
        split = speech.split(" ")
        sentence = ""
        for _ in split:
            sentence += " " + choice(("hmm", "hm", "hmmm"))
        response = sentence.strip()
        await ctx.reply(response)

    @commands.command()
    async def enchant(self, ctx: commands.Context, *, msg: str) -> None:
        """Enchant a message."""
        response = ""
        for letter in msg:
            if letter in alphabet:
                response += minecraft[alphabet.index(letter)]
            else:
                response += letter
        await ctx.send(f"{ctx.message.author.mention}, `{response}`")

    @commands.command()
    async def unenchant(self, ctx: commands.Context, *, msg: str) -> None:
        """Disenchant a message."""
        response = ""
        for letter in msg:
            if letter in minecraft:
                response += alphabet[minecraft.index(letter)]
            else:
                response += letter
        await ctx.send(f"{ctx.message.author.mention}, `{response}`")

    @commands.command()
    async def creeper(self, ctx) -> None:
        """Aw man."""
        await ctx.send("Aw man")

    @cog_ext.cog_slash(name="creeper")
    async def slash_creeper(self, ctx):
        await ctx.defer()
        await self.creeper(ctx)

    @commands.command()
    async def rps(self, ctx: commands.Context, user_choice: str = None) -> None:
        """Play Rock Paper Shears."""
        options = ["rock", "paper", "shears"]
        if not user_choice or user_choice not in options:
            await ctx.send(
                _(
                    "That is an invalid option can you please choose from "
                    "rock, paper or shears"
                )
            )
            return
        c_choice = choice(options)
        if user_choice == options[options.index(user_choice) - 1]:
            await ctx.send(
                _("You chose {user_choice}, I chose {c_choice} I win.").format(
                    user_choice=user_choice, c_choice=c_choice
                )
            )
        elif c_choice == user_choice:
            await ctx.send(
                _(
                    "You chose {user_choice}, I chose {c_choice} looks like we have a tie."
                ).format(user_choice=user_choice, c_choice=c_choice)
            )
        else:
            await ctx.send(
                _("You chose {user_choice}, I chose {c_choice} you win.").format(
                    user_choice=user_choice, c_choice=c_choice
                )
            )

    @cog_ext.cog_slash(name="rps")
    async def slash_rps(self, ctx, user_choice: str = None):
        await ctx.defer()
        await self.creeper(ctx, user_choice)
