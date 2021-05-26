async def confirmation(
    ctx,
    description: str,
    title: str,
    color=discord.Color.blurple(),
    footer: t.Optional[str] = None,
) -> t.Optional[bool]:
    emojis = {"✅": True, "❌": False}

    embed = discord.Embed(title=title, description=description, color=color)

    if footer is not None:
        embed.set_footer(text=footer)

    message = await ctx.send(embed=embed)
    user = ctx.author

    for emoji in emojis:
        await message.add_reaction(emoji)

    try:
        reaction, user = await ctx.wait_for(
            "reaction_add",
            check=lambda r, u: (r.message.id == message.id)
            and (u.id == user.id)
            and (r.emoji in emojis),
            timeout=30,
        )
    except asyncio.TimeoutError:
        confirmed = None
        return
    finally:
        try:
            await message.clear_reactions()
            await message.delete()
        except discord.Forbidden:
            pass

    confirmed = emojis[reaction.emoji]
    return confirmed
