"""The checks in this module run on every command."""
from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from obsidion.core.bot import Obsidion


def init_global_checks(bot: Obsidion):
    """Initiate global checks."""

    @bot.check_once
    async def check_message_is_eligible_as_command(ctx: commands.Context) -> bool:
        """Check wether message is eligible."""
        return await ctx.bot.message_eligible_as_command(ctx.message)
