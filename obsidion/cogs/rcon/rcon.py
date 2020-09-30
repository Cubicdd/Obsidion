"""Rcon cog."""

from discord.ext import commands
from asyncrcon import AsyncRCON, AuthenticationException


class Rcon(commands.Cog):
    """Rcon."""

    def __init__(self, bot) -> None:
        """Init."""
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def rsend(
        self, ctx: commands.Context, addr: str, pw: str, message: str
    ) -> None:
        """Send an rcon message to a minecraft server."""
        await ctx.trigger_typing()

        _rcon = AsyncRCON(addr, pw)
        try:
            await _rcon.open_connection()
        except AuthenticationException:
            await ctx.send("Login failed: Unauthorized.")
            return

        res = await _rcon.command(message)
        await ctx.send(res)

        _rcon.close()
