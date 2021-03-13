import json
import textwrap
import typing as t

import discord
from discord import Color, Embed
from discord.ext import menus
from discord.ext.commands import (
    BotMissingPermissions, BotMissingRole,
    BucketType, Cog, CommandOnCooldown, Context,
    DisabledCommand, ExpectedClosingQuoteError,
    InvalidEndOfQuotedStringError,
    MaxConcurrencyReached, MissingPermissions,
    MissingRole, NoPrivateMessage, NotOwner,
    NSFWChannelRequired, PrivateMessageOnly,
    UnexpectedQuoteError, errors
)
from loguru import logger

from bot import Bot


class ErrorHandler(Cog):
    """This cog handles the errors invoked from commands."""

    def __init__(self, bot: Bot):
        self.bot = bot

    async def error_embed(
        self,
        ctx: Context,
        title: t.Optional[str] = None,
        description: t.Optional[str] = None,
    ) -> None:
        """Utility method to send error embeds easily."""
        await ctx.send(
            embed=Embed(title=title, description=description,
                        color=Color.red())
        )

    async def command_syntax_error(
        self, ctx: Context, error: errors.UserInputError
    ) -> None:
        """Handle invalid command syntax error."""
        command = ctx.command
        parent = command.full_parent_name

        command_name = str(
            command) if not parent else f"{parent} {command.name}"
        command_syntax = f"```{command_name} {command.signature}```"

        aliases = [
            f"`{alias}`" if not parent else f"`{parent} {alias}`"
            for alias in command.aliases
        ]
        aliases = ", ".join(sorted(aliases))

        command_help = f"{command.help or 'No description provided.'}"

        await self.error_embed(
            ctx,
            title="Invalid command syntax",
            description=textwrap.dedent(
                f"""
                The command syntax you used is incorrect.
                **`{error}`**
                **Command Description**
                {command_help}
                **Command syntax**
                {command_syntax}
                Aliases: {aliases if aliases else None}
                """
            ),
        )

    @classmethod
    def _get_missing_permission(cls, error) -> str:
        """Missing permissions utility handler."""
        missing_perms = [
            perm.replace("_", " ").replace("guild", "server").title()
            for perm in error.missing_perms
        ]

        if len(missing_perms) > 2:
            message = f"{'**, **'.join(missing_perms[:-1])}, and {missing_perms[-1]}"
        else:
            message = " and ".join(missing_perms)

        return message

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: errors.CommandError) -> None:
        """Common error handler for the bot, so It doesnt interrupt and runs perfectly."""
        logger.warning(type(error))

        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, errors.CommandNotFound):
            return

        elif isinstance(error, BotMissingPermissions):
            missing_perms = self._get_missing_permission(error)
            message = (
                f"I need the **{missing_perms}** permission(s) to run this command."
            )
            await self.error_embed(ctx, message)
            return

        elif isinstance(error, MissingPermissions):
            missing_perms = self._get_missing_permission(error)
            message = (
                f"You need the **{missing_perms}** permission(s) to use this command."
            )
            await self.error_embed(ctx, message)
            return

        elif isinstance(error, BotMissingRole):
            message = f"I need the **{error.missing_role}** role to run this command."
            await self.error_embed(ctx, message)
            return

        elif isinstance(error, MissingRole):
            message = f"You need the **{error.missing_role}** permission(s) to use this command."
            await self.error_embed(ctx, message)
            return

        elif isinstance(error, (CommandOnCooldown, MaxConcurrencyReached)):
            cooldowns = {
                BucketType.default: "for the whole bot.",
                BucketType.user: "for you.",
                BucketType.guild: "for this server.",
                BucketType.channel: "for this channel.",
                BucketType.member: "cooldown for you.",
                BucketType.category: "for this channel category.",
                BucketType.role: "for your role.",
            }

            await self.error_embed(
                ctx,
                title="Command on cooldown",
                description=f"The command `{ctx.command}` is on cooldown {cooldowns[error.cooldown.type]} You can "
                f"retry in `{error.retry_after}`",
            )
            return

        elif isinstance(error, errors.UserInputError):
            await self.command_syntax_error(ctx, error)
            return

        elif isinstance(error, PrivateMessageOnly):
            await self.error_embed(
                ctx,
                description=f"❌ The command `{ctx.command}` can be used only in in private messages.",
            )
            return

        elif isinstance(error, NoPrivateMessage):
            await self.error_embed(
                ctx,
                description=f"❌ The command `{ctx.command}` can not be used in private messages.",
            )
            return

        elif isinstance(error, errors.CheckFailure):
            if isinstance(error, NotOwner):
                msg = "❌ This command is only for the bot owners."
            else:
                msg = "❌ You don't have enough permission to run this command."

            await self.error_embed(ctx, description=msg)
            return

        elif (
            isinstance(error.original, discord.HTTPException)
            and error.original.code == 50034
        ):
            await self.error_embed(
                ctx,
                "❌ You can only bulk delete messages that are under 14 days old",
            )
            return

        elif isinstance(error.original, menus.CannotEmbedLinks):
            await self.error_embed(
                ctx,
                "I need to be able to send embeds to show menus. Please give me permission to Embed Links.",
            )
            return

        elif isinstance(error.original, menus.CannotAddReactions):
            await self.error_embed(
                ctx,
                "I need to be able to add reactions to show menus. Please give me permission to Add Reactions",
            )
            return

        elif isinstance(error.original, menus.CannotReadMessageHistory):
            await self.error_embed(
                ctx,
                "I need to be able to read message history to show menus. Please give me permission to Read "
                "Message History",
            )
            return

        elif isinstance(error.original, (discord.Forbidden, menus.CannotSendMessages)):
            await self.error_embed(
                ctx,
                f"I am missing permissions for {ctx.command.qualified_name} in #{ctx.channel.name} in "
                f"{ctx.guild.name}.",
            )
            logger.warning(
                f"Missing Permissions for {ctx.command.qualified_name} in #{ctx.channel.name} in {ctx.guild.name}"
            )
            return

        error_messages = {
            NSFWChannelRequired: f"The command `{ctx.command}` can only be ran in a NSFW channel.",
            DisabledCommand: f"The command `{ctx.command}` has been disabled.",
            ExpectedClosingQuoteError: f"You missed a closing quote in the parameters passed to the `{ctx.command}` "
            f"command.",
            UnexpectedQuoteError: f"There was an unexpected quote in the parameters passed to the `{ctx.command}` "
            f"command.",
            InvalidEndOfQuotedStringError: f"The quoted argument must be separated from the others with space in "
            f"`{ctx.command}`",
        }

        error_message = error_messages.get(type(error))
        if error_message is not None:
            await self.error_embed(ctx, title="Error", description=error_message)
            return

        elif isinstance(error, errors.CommandInvokeError):
            error_cause = error.__cause__

            if error_cause is not None:
                await self.error_embed(
                    ctx,
                    title="Unhandled Error",
                    description=textwrap.dedent(
                        f"""
                        An error has occurred which isn't properly handled.
                        **Error log**
                        ```{error_cause.__class__.__name__}: {error_cause}```
                        """
                    ),
                )
                logger.error(
                    f"Exception {error_cause.__repr__()} has occurred from "
                    f"the message({ctx.message.content}) invoked by {ctx.author.id} in {ctx.guild.name}[{ctx.guild.id}]"
                )
            raise error_cause

        await self.error_embed(
            ctx,
            title="Unhandled exception",
            description=textwrap.dedent(
                f"""
                An error has occurred which isn't properly handled.
                **Error**
                ```{error.__class__.__name__}: {error}```
                """
            ),
        )
        logger.error(
            f"Exception {error.__repr__()} has occurred from "
            f"the message({ctx.message.content}) invoked by {ctx.author.id} in {ctx.guild.name}[{ctx.guild.id}]"
        )
