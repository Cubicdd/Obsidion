"""Images cog."""
import asyncio
import logging

import discord
from discord.ext import commands

from obsidion.core.i18n import cog_i18n
from obsidion.core.i18n import Translator
from obsidion.core import get_settings

log = logging.getLogger(__name__)

_ = Translator("Images", __file__)


@cog_i18n(_)
class Images(commands.Cog):
    def __init__(self, bot) -> None:
        """Init."""
        self.bot = bot

    @commands.command()
    async def achievement(
        self, ctx: commands.Context, block_name: str, title: str, *, text: str
    ) -> None:
        """Create your very own custom Minecraft achievements."""
        text = text.replace(" ", "%20")
        embed = discord.Embed(color=self.bot.color)
        embed.set_author(
            name=_("Obsidion Advancement Generator"), icon_url=self.bot.user.avatar_url
        )
        embed.set_image(
            url=(
                f"{get_settings().API_URL}/images/advancement?item={block_name}&title={title}&text={text}"
            )
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def sign(
        self,
        ctx: commands.Context,
        *,
        text: str,
    ) -> None:
        """Create a Minecraft sign with custom text."""
        split = text.replace(" ", "%20").split("|")
        line1 = split[0] if len(split) >= 1 else "%20"
        line2 = split[1] if len(split) >= 2 else "%20"
        line3 = split[2] if len(split) >= 3 else "%20"
        line4 = split[3] if len(split) >= 4 else "%20"
        embed = discord.Embed(color=self.bot.color)
        embed.set_author(
            name=_("Obsidion Sign Generator"), icon_url=self.bot.user.avatar_url
        )
        embed.set_image(
            url=(
                f"{get_settings().API_URL}/images/sign?line1={line1}&line2={line2}&line3={line3}&line4={line4}"
            )
        )
        await ctx.send(embed=embed)

    # @commads.command()
    async def book(self, ctx: commands.Context):
        pass
        embed = discord.Embed(color=self.bot.color)
        embed.set_author(
            name=_("Obsidion Sign Generator"), icon_url=self.bot.user.avatar_url
        )
        embed.set_image(
            url=(
                f"{get_settings().API_URL}/images/sign?line1={line1}&line2={line2}&line3={line3}&line4={line4}"
            )
        )
        await ctx.send(embed=embed)

    # @commads.command()
    async def death(self, ctx: commands.Context):
        pass
        embed = discord.Embed(color=self.bot.color)
        embed.set_author(
            name=_("Obsidion Sign Generator"), icon_url=self.bot.user.avatar_url
        )
        embed.set_image(
            url=(
                f"{get_settings().API_URL}/images/death?line1={line1}&line2={line2}&line3={line3}&line4={line4}"
            )
        )
        await ctx.send(embed=embed)

    # @commads.command()
    async def splashscreen(self, ctx: commands.Context):
        pass
        embed = discord.Embed(color=self.bot.color)
        embed.set_author(
            name=_("Obsidion Sign Generator"), icon_url=self.bot.user.avatar_url
        )
        embed.set_image(
            url=(
                f"{get_settings().API_URL}/images/splashscreen?line1={line1}&line2={line2}&line3={line3}&line4={line4}"
            )
        )
        await ctx.send(embed=embed)

    # @commads.command()
    async def motd(self, ctx: commands.Context):
        pass
        embed = discord.Embed(color=self.bot.color)
        embed.set_author(
            name=_("Obsidion Sign Generator"), icon_url=self.bot.user.avatar_url
        )
        embed.set_image(
            url=(
                f"{get_settings().API_URL}/images/motd?line1={line1}&line2={line2}&line3={line3}&line4={line4}"
            )
        )
        await ctx.send(embed=embed)

    # @commads.command()
    async def recipie(self, ctx: commands.Context):
        pass
        embed = discord.Embed(color=self.bot.color)
        embed.set_author(
            name=_("Obsidion Sign Generator"), icon_url=self.bot.user.avatar_url
        )
        embed.set_image(
            url=(
                f"{get_settings().API_URL}/images/recipie?line1={line1}&line2={line2}&line3={line3}&line4={line4}"
            )
        )
        await ctx.send(embed=embed)

    # @commads.command()
    async def banner(self, ctx: commands.Context):
        pass
        embed = discord.Embed(color=self.bot.color)
        embed.set_author(
            name=_("Obsidion Sign Generator"), icon_url=self.bot.user.avatar_url
        )
        embed.set_image(
            url=(
                f"{get_settings().API_URL}/images/banner?line1={line1}&line2={line2}&line3={line3}&line4={line4}"
            )
        )
        await ctx.send(embed=embed)

    # @commads.command()
    async def image(self, ctx: commands.Context):
        pass
        embed = discord.Embed(color=self.bot.color)
        embed.set_author(
            name=_("Obsidion Sign Generator"), icon_url=self.bot.user.avatar_url
        )
        embed.set_image(
            url=(
                f"{get_settings().API_URL}/images/image?line1={line1}&line2={line2}&line3={line3}&line4={line4}"
            )
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx: commands.Context, username: str) -> None:
        """Renders a Minecraft players face."""
        await self.render(ctx, "face", username)

    @commands.command()
    async def skull(self, ctx: commands.Context, username: str = None) -> None:
        """Renders a Minecraft players skull."""
        await self.render(ctx, "head", username)

    @commands.command()
    async def skin(self, ctx: commands.Context, username: str) -> None:
        """Renders a Minecraft players skin."""
        await self.render(ctx, "full", username)

    @commands.command()
    async def bust(self, ctx: commands.Context, username: str) -> None:
        """Renders a Minecraft players bust."""
        await self.render(ctx, "bust", username)

    @commands.command()
    async def render(
        self, ctx: commands.Context, render_type: str, username: str
    ) -> None:
        """Renders a Minecraft players skin in 6 different ways.

        You can choose from these 6 render types: face,
        front, full, head, bust & skin.
        """
        await ctx.channel.trigger_typing()
        renders = ["face", "front", "frontfull", "head", "bust", "full", "skin"]
        if render_type not in renders:
            await ctx.reply(
                _(
                    "Please supply a render type. Your "
                    "options are:\n `face`, `front`, `full`, `head`, `bust`, "
                    "`skin` \n Type: ?render <render type> <username>"
                )
            )
            return
        uuid = (await self.bot.mojang_player(username))["uuid"]
        embed = discord.Embed(
            description=_(
                "Here is: `{username}`'s {render_type}! \n "
                "**[DOWNLOAD](https://visage.surgeplay.com/{render_type_lower}"
                "/512/{uuid})\n[RAW](https://sessionserver.mojang.com/session/minecraft/profile/{uuid})**"
            ).format(
                username=username,
                render_type=render_type.capitalize(),
                render_type_lower=render_type,
                uuid=uuid,
            ),
            color=0x00FF00,
        )
        embed.set_image(url=f"https://visage.surgeplay.com/{render_type}/512/{uuid}")

        await ctx.send(embed=embed)
