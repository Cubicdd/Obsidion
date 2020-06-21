import datetime
import inspect
import logging
import resource
import sys

import discord
from discord.ext import commands

from obsidion import __version__, constants
from obsidion.utils.chat_formatting import humanize_timedelta

log = logging.getLogger(__name__)


class miscellaneous(commands.Cog):
    """commands that are bot related"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="licenseinfo")
    async def license_info(self, ctx: commands.Context):
        """Info about the license which Obsidion is released under"""
        embed = discord.Embed(
            description=(
                "This bot is an instance of the Obsidion Discord Bot.\n"
                "Obsidion is an open source application made available to the public and "
                "licensed under the GNU AGPL v3. The full text of this license is available to you at "
                "<https://github.com/Darkflame72/Obsidion/blob/master/README.md>"
            ),
            color=0x00FF00,
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx: commands.Context):
        """invite the bot to your server"""
        embed = discord.Embed(
            description=f"**[Click here to add {self.bot.user.name} to your Discord server](https://discordapp.com/oauth2/authorize?client_id=691589447074054224&scope=bot&permissions=314432)**",
            color=0x00FF00,
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["upvote", "support"])
    async def vote(self, ctx: commands.Context):
        """Help support this bot by helping others to find it"""
        embed = discord.Embed(color=0x00FF00)
        embed.add_field(
            name="Vote:",
            value=(
                "Top gg: **[VOTE HERE](https://top.gg/bot/691589447074054224)**\n"
                "Bots For Discord: **[VOTE HERE](https://botsfordiscord.com/bot/691589447074054224)**\n"
                "Discord Boats List: **[VOTE HERE](https://discord.boats/bot/691589447074054224)**\n"
                "Discord Bot List: **[VOTE HERE](https://discordbotlist.com/bots/obsidion)**\n"
                "Discord Labs: **[VOTE HERE](https://bots.discordlabs.org/bot/691589447074054224)**\n"
                "Bots On Discord: **[REVIEW HERE](https://bots.ondiscord.xyz/bots/691589447074054224/review)**\n"
            ),
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """Check ping of the bot"""

        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(title="Bot's Ping", color=0x00FF00)
        embed.add_field(name="Discord Ping", value=f"`{latency}ms`")

        await ctx.send(embed=embed)

    @commands.command(aliases=["statistics", "botstats"])
    async def stats(self, ctx):
        """View statistics about the bot"""

        delta = datetime.datetime.utcnow() - self.bot.uptime
        uptime_str = humanize_timedelta(timedelta=delta)

        total_users = sum(len(guild.members) for guild in self.bot.guilds)
        text_channels = sum(len(guild.text_channels) for guild in self.bot.guilds)
        voice_channels = sum(len(guild.voice_channels) for guild in self.bot.guilds)

        ram = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, 2) / 1000
        print(self.bot.uptime)
        print(uptime_str)

        statics = (
            f"Guilds: `{len(self.bot.guilds):,}`\n"
            f"Users: `{total_users:,}`\n"
            f"Channels: `{text_channels+voice_channels:,}`\n"
            f"Memory Usage: `{ram}MB`\n"
            # f"Uptime: `{uptime_str}`\n"
            f"Discord.py: `v{discord.__version__}`"
        )

        links = (
            "[INVITE BOT](https://discordapp.com/oauth2/authorize?client_id=691589447074054224&scope=bot&permissions=314448)\n"
            "[GITHUB](https://github.com/Darkflame72/Obsidion)\n"
            "[SUPPORT SERVER](https://discord.gg/invite/7BRD7s6)\n"
            "[VOTE](https://top.gg/bot/691589447074054224)\n"
            "[TRELLO](https://trello.com/b/qZhxHkTq/obsidion)\n"
            "[WEBSITE](http://discord.obsidion-dev.com)"
        )

        embed = discord.Embed(title="Stats", color=0x00FF00)
        embed.add_field(name=":newspaper: STATS", value=statics, inline=True)
        embed.add_field(name=":link: LINKS", value=links, inline=True)
        embed.set_footer(text=f"{__version__} | Created by: Darkflame72#1150")

        await ctx.send(embed=embed)

    @commands.command(aliases=["information"])
    async def info(self, ctx: commands.Context):
        """Shows info about Red"""
        author_repo = "https://github.com/Darkflame72"
        # org_repo = "https://github.com/Obsidion-dev" # I need to move the repo over there at some point
        obsidion_repo = author_repo + "/Obsidion"
        support_server_url = "https://discord.gg/invite/7BRD7s6"
        dpy_repo = "https://github.com/Rapptz/discord.py"
        python_url = "https://www.python.org/"
        since = datetime.datetime(2020, 3, 23)
        days_since = (datetime.datetime.utcnow() - since).days
        dpy_version = f"[{discord.__version__}]({dpy_repo})"
        python_version = "[{}.{}.{}]({})".format(*sys.version_info[:3], python_url)
        about = (
            f"This bot is an instance of [Obsidion, an open source Discord bot]({obsidion_repo}) "
            f"created by [Darkflame72]({author_repo})\n\n"
            f"Obsidion is made for the community [Join us today]({support_server_url}) "
            f"and help us improve!\n\n"
            f"(c) Obsidion-dev"
        )

        embed = discord.Embed(color=0x00FF00)
        embed.add_field(name="Python", value=python_version)
        embed.add_field(name="discord.py", value=dpy_version)
        embed.add_field(name="Obsidion version", value=__version__)
        embed.add_field(name="About Obsidion", value=about, inline=False)

        embed.set_footer(
            text=f"Helping you unleash your creativity since March 23rd 2020 (over {days_since} days ago!)"
        )
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def source(self, ctx, *, command: str = None):
        """Displays my full source code or for a specific command.
        To display the source code of a subcommand you can separate it by
        periods, e.g. account.link for the link subcommand of the account command
        or by spaces.
        """
        source_url = "https://github.com/Darkflame72/Obsidion"
        branch = "master"
        if command is None:
            return await ctx.send(source_url)

        if command == "help":
            src = type(self.bot.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)
        else:
            obj = self.bot.get_command(command.replace(".", " "))
            if obj is None:
                return await ctx.send("Could not find command.")

            # since we found the command we're looking for, presumably anyway, let's
            # try to access the code itself
            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

        lines, firstlineno = inspect.getsourcelines(src)
        if not module.startswith("discord"):
            # not a built-in command
            location = os.path.relpath(filename).replace("\\", "/")
        else:
            location = module.replace(".", "/") + ".py"
            source_url = "https://github.com/Rapptz/discord.py"
            branch = "master"

        final_url = f"<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>"
        await ctx.send(final_url)

    @commands.command()
    @commands.cooldown(rate=1, per=600.0, type=commands.BucketType.user)
    async def feedback(self, ctx: commands.Context, *, content: str):
        """Gives feedback about the bot.
        This is a quick way to request features or bug fixes
        without being in the bot's server.
        The bot will communicate with you via PM about the status
        of your request if possible.
        You can only request feedback once every 10 minutes.
        """

        embed = discord.Embed(title="Feedback", colour=0x00FF00)
        channel = ctx.bot.get_channel(constants.Channels.feedback_channel)
        if channel is None:
            await ctx.send(
                "Feedback is currently disabled please join our support server [here](https://discord.gg/invite/7BRD7s6) to give it in person."
            )
            return

        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.description = content
        embed.timestamp = ctx.message.created_at

        if ctx.guild is not None:
            embed.add_field(
                name="Server",
                value=f"{ctx.guild.name} (ID: {ctx.guild.id})",
                inline=False,
            )

        embed.add_field(
            name="Channel", value=f"{ctx.channel} (ID: {ctx.channel.id})", inline=False
        )
        embed.set_footer(text=f"Author ID: {ctx.author.id}")

        await channel.send(embed=embed)
        await ctx.send("Successfully sent feedback")
