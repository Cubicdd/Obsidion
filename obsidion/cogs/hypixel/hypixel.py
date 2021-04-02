"""Images cog."""
import logging
import datetime
from dpymenus import Page, PaginatedMenu

import discord
from asyncpixel import Hypixel as _Hypixel
from discord.ext import commands
from obsidion.core import get_settings
from obsidion.core.i18n import cog_i18n
from obsidion.core.i18n import Translator
from obsidion.core.utils.chat_formatting import humanize_timedelta
from obsidion.core.utils.utils import divide_array
from typing import Optional

log = logging.getLogger(__name__)

_ = Translator("Hypixel", __file__)


@cog_i18n(_)
class Hypixel(commands.Cog):
    def __init__(self, bot) -> None:
        """Init."""
        self.bot = bot
        self.hypixel = _Hypixel(get_settings().HYPIXEL_API_TOKEN)

    @commands.command()
    async def watchdogstats(self, ctx: commands.Context) -> None:
        """Get the current watchdog statistics."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel.watchdog_stats()
        embed = discord.Embed(title=_("Watchdog Stats"), colour=self.bot.color)
        embed.add_field(
            name=_("Total Bans"), value=f"{(data.watchdog_total + data.staff_total):,}"
        )
        embed.add_field(
            name=_("Watchdog Rolling Daily"), value=f"{data.watchdog_rolling_daily:,}"
        )
        embed.add_field(name=_("Staff Total"), value=f"{data.staff_total:,}")
        embed.add_field(
            name=_("Staff Rolling Daily"), value=f"{data.staff_rolling_daily:,}"
        )
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)
    @commands.command()
    async def boosters(self, ctx:commands.Context) -> None:
        """Get the current boosters online."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel.boosters()
        embed = discord.Embed(title=_("Boosters"), description=_(f"Total Boosters online: {len(data.boosters)}"), colour=self.bot.color)
        embed.set_author(name=_("Hypixel"), url="https://hypixel.net/forums/skyblock.157/", icon_url="https://hypixel.net/favicon-32x32.png")
        embed.set_thumbnail(url="https://hypixel.net/styles/hypixel-v2/images/header-logo.png")
        embed.timestamp = ctx.message.created_at

        await ctx.send(embed=embed)
    @commands.command()
    async def playercount(self, ctx: commands.Context) -> None:
        """Get the current players online."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel.player_count()
        embed = discord.Embed(title=_("Players Online"), description=_(f"Total players online: {data}"), colour=self.bot.color)
        embed.set_author(name=_("Hypixel"), url="https://hypixel.net/forums/skyblock.157/", icon_url="https://hypixel.net/favicon-32x32.png")
        embed.set_thumbnail(url="https://hypixel.net/styles/hypixel-v2/images/header-logo.png")
        embed.timestamp = ctx.message.created_at

        await ctx.send(embed=embed)
    @commands.command()
    async def skyblocknews(self, ctx: commands.Context) -> None:
        """Get current news for skyblock."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel.news()
        embed = discord.Embed(title=_("Skyblock News"), description=_(f"There are currently {len(data)} news articles."), colour=self.bot.color)
        embed.set_author(name=_("Hypixel"), url="https://hypixel.net/forums/skyblock.157/", icon_url="https://hypixel.net/favicon-32x32.png")
        embed.set_thumbnail(url="https://hypixel.net/styles/hypixel-v2/images/header-logo.png")

        for i in range(len(data)):
            embed.add_field(name=_(f"{data[i].title}"), value=f"[{data[i].text}]({data[i].link})")

        embed.timestamp = ctx.message.created_at

        await ctx.send(embed=embed)
    @commands.command()
    async def playerstatus(self, ctx: commands.Context, username: Optional[str] = None) -> None:
        """Get the current status of an online player."""
        await ctx.channel.trigger_typing()
        
        player_data = await self.bot.mojang_player(ctx.author, username)
        uuid = player_data["uuid"]

        data = await self.hypixel.player_status(uuid)

        if data.online == False:
            await ctx.send("That player is not currently online.")
            return
        else:
            embed = discord.Embed(title=_("Player Status"), description=_(f"Current status of Player {username}"), colour=self.bot.color)
            embed.set_author(name=_("Hypixel"), url="https://hypixel.net/forums/skyblock.157/", icon_url="https://hypixel.net/favicon-32x32.png")
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/{uuid}")
            
            embed.add_field(name=_("Current game: "), value=_(f"{data.game_type.CleanName}"))
            embed.add_field(name=_("Current game mode: "), value=_(f"{data.mode}"))

            embed.timestamp = ctx.message.created_at

        await ctx.send(embed=embed)
    @commands.command()
    async def playerfriends(self, ctx: commands.Context, username: Optional[str] = None) -> None:
        """Get the current friends of a player."""
        await ctx.channel.trigger_typing()
        player_data = await self.bot.mojang_player(ctx.author, username)
        uuid = player_data["uuid"]
        
        data = await self.hypixel.player_friends(uuid)

        embed = discord.Embed(title=_("Player Friends"), description=_(f"Current Friends for {username}"), colour=self.bot.color)
        embed.set_author(name=_("Hypixel"), url="https://hypixel.net/forums/skyblock.157/", icon_url="https://hypixel.net/favicon-32x32.png")
        embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/{uuid}")
        embed.timestamp = ctx.message.created_at


        for i in range(len(data)):
            if str(data[i].uuid_receiver) == str(uuid):
                friendUsername = await self.bot.mojang_player(ctx.author, data[i].uuid_sender)
            else:
                friendUsername = await self.bot.mojang_player(ctx.author, data[i].uuid_receiver)
            
            friendUsername = friendUsername["username"]
            
            delta = datetime.datetime.now(tz=datetime.timezone.utc) - data[i].started
            friendStarted = humanize_timedelta(timedelta=delta)
            friendStartedSplit = friendStarted.split(", ")
            friendStarted = friendStartedSplit[0] + ", " + friendStartedSplit[1]

            embed.add_field(name=_(f"{friendUsername}"), value =_(f"Been friends for {friendStarted}"))

        await ctx.send(embed=embed)
    @commands.command()
    async def bazaar(self, ctx: commands.Context) -> None:
        """Get Bazaar NPC stats."""
        await ctx.channel.trigger_typing()

        menu = PaginatedMenu(ctx)
        data = await self.hypixel.bazaar()
        split = list(divide_array(data.bazaar_items, 15))
        pagesend = []

        for bazaarloop in range(len(split)):
            pagebazaar = Page(title=_("Bazaar NPC Stats"), description=_(f"Page {bazaarloop + 1} of {(len(split))}"), color=self.bot.color)
            pagebazaar.set_author(name=_("Hypixel"), icon_url="https://hypixel.net/favicon-32x32.png")
            pagebazaar.set_thumbnail(url="https://hypixel.net/styles/hypixel-v2/images/header-logo.png")
            for item in range(len(split[bazaarloop])):
                name = split[bazaarloop][item].product_id.replace("_", " ").title()
                sellprice = round(split[bazaarloop][item].quick_status.sell_price)
                buyprice = round(split[bazaarloop][item].quick_status.buy_price)
                pagebazaar.add_field(name=_(name), value=_(f"Sell Price: {sellprice} \n Buy Price: {buyprice}"))
            pagesend.append(pagebazaar)
        
        menu.add_pages(pagesend)
        menu.set_timeout(90)

        await menu.open()
    @commands.command()
    async def auctions(self, ctx: commands.Context) -> None:
        """Get the first 30 auctions."""

        await ctx.channel.trigger_typing()
        data = await self.hypixel.auctions()
        menu = PaginatedMenu(ctx)
        split = list(divide_array(data.auctions, 9))
        auctionitems = split[:3]
        pagesend = []

        for auctionsloop in range(len(auctionitems)):
            pageauctions = Page(title=_("Current Auctions"), description=_(f"Page {auctionsloop + 1} of {(len(auctionitems))}"), color=self.bot.color)
            pageauctions.set_author(name=_("Hypixel"), icon_url="https://hypixel.net/favicon-32x32.png")
            pageauctions.set_thumbnail(url="https://hypixel.net/styles/hypixel-v2/images/header-logo.png")
            for item in range(len(auctionitems[auctionsloop])):
                name = auctionitems[auctionsloop][item].item_name
                category = auctionitems[auctionsloop][item].category
                tier = auctionitems[auctionsloop][item].tier
                start_bid = auctionitems[auctionsloop][item].starting_bid
                won = auctionitems[auctionsloop][item].claimed
                highest_bid = auctionitems[auctionsloop][item].highest_bid_amount
                pageauctions.add_field(name=_(name), value=_(f"Item Category: {category} \n Item Tier: {tier} \n Starting Bid: {start_bid} \n Item Won: {won} \n Highest Bid: {highest_bid}"))
            pagesend.append(pageauctions)
        
        menu.add_pages(pagesend)

        await menu.open()
    @commands.command()
    async def guild(self, ctx: commands.Context, guildname: str) -> None:
        """Get's guild info by guild name."""
        await ctx.channel.trigger_typing()
        data = await self.hypixel.guild_by_name(guildname)
        menu = PaginatedMenu(ctx)
        
        embed = discord.Embed(title=_("Guild Info"), description=_(f"Guild info for {guildname}"), colour=self.bot.color)
        embed.set_author(name=_("Hypixel"), url="https://hypixel.net/forums/skyblock.157/", icon_url="https://hypixel.net/favicon-32x32.png")
        embed.set_thumbnail(url="https://hypixel.net/styles/hypixel-v2/images/header-logo.png")
        embed.add_field(name=_("Guild Name: "), value=_(data.id))
        embed.add_field(name=_("Guild Name: "), value=_(data.name))
        embed.add_field(name=_("Guild Description: "), value=_(data.description))
        embed.add_field(name=_("Guild Tag: "), value=_(data.tag))
        embed.add_field(name=_("Guild Experience Points: "), value=_(data.exp))
        embed.add_field(name=_("Joinable: "), value=_(data.joinable))
        embed.add_field(name=_("Public: "),value=_(data.publicly_listed))

        await ctx.send(embed=embed)