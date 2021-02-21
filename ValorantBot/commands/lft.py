from util import methods, sql

old_channel_map = {}
reaction_map = {}


async def lft(ctx, bot):
    if ctx.channel == bot.get_channel(806109172336689162):
        dcUser = ctx.author
        if dcUser.voice is not None:
            if dcUser.voice.channel.category == bot.get_channel(809430391177084969).category:
                await methods.set_lft(dcUser, bot)
            else:
                await bot.get_channel(806112383693094942).send(
                    ctx.author.mention + ", you have to be in a temporary channel to use this command.",
                    delete_after=30)
        else:
            await bot.get_channel(806112383693094942).send(
                ctx.author.mention + ", you have to be in a temporary channel to use this command.", delete_after=30)
    else:
        await bot.get_channel(806112383693094942).send(
            ctx.author.mention + ", you can't use this command here, got to " + bot.get_channel(
                806109172336689162).mention, delete_after=30)


async def lft_event_add(reaction, user, bot):
    user_role = methods.get_rank(user)
    member_position = user_role.position
    if reaction.message.author == bot.get_user(806461492450426900):
        if user.voice is not None:
            old_channel_map[reaction] = user.voice.channel
            lft_author = await methods.get_executor(reaction.message, bot)
            channel_to_move = lft_author.voice.channel
            channel_members = channel_to_move.members
            if user != lft_author:
                if not any(abs(methods.get_rank(member).position - member_position) > 3 for member in channel_members):
                    await user.move_to(channel_to_move)
                    reaction_map[user] = reaction
                    lft_author_role = methods.get_rank(lft_author)
                    content = lft_author.mention + " is looking for teammates for ranked, he is " + lft_author_role.name + ". Join a channel and react to the message to join the channel. There are currently " + str(
                        len(lft_author.voice.channel.members)) + "/5 players in the channel."
                    await reaction.message.edit(content=content)
                else:
                    await bot.get_channel(806112383693094942).send(
                        content=user.mention + ", there are people with too high ranks for you in this channel.",
                        delete_after=30)
                    await reaction.remove(user)
            else:
                await reaction.remove(lft_author)
        else:
            await bot.get_channel(806112383693094942).send(
                content=user.mention + ", you have to be in a voice channel to use this reaction", delete_after=30)
            await reaction.remove(user)


async def lft_event_remove(reaction, user, bot):
    if reaction.message.author == bot.get_user(806461492450426900):
        if user.voice is not None:
            lft_author = await methods.get_executor(reaction.message, bot)
            user_role = methods.get_rank(lft_author)
            await user.move_to(old_channel_map[reaction])
            del old_channel_map[reaction]
            content = lft_author.mention + " is looking for teammates for ranked, he is " + user_role.name + ". Join a channel and react to the message to join the channel. There are currently " + str(
                len(lft_author.voice.channel.members)) + "/5 players in the channel."
            await reaction.message.edit(content=content)


async def lft_leave_channel(member, before, bot):
    if member.nick is not None:
        if member in reaction_map:
            if reaction_map[member] is not None:
                member_reaction = reaction_map[member]
                if member_reaction.message is not None:
                    lft_author = await methods.get_executor(member_reaction.message, bot)
                    user_role = methods.get_rank(lft_author)
                    content = lft_author.mention + " is looking for teammates for ranked, he is " + user_role.name + ". Join a channel and react to the message to join the channel. There are currently " + str(
                        len(lft_author.voice.channel.members)) + "/5 players in the channel."
                    await member_reaction.message.edit(content=content)
                    await member_reaction.remove(member)
                    del reaction_map[member]
        elif sql.executor_exists(member):
            await methods.set_casual(before.channel, bot)
            [reaction_map.pop(member, None) for member in before.channel.members]
