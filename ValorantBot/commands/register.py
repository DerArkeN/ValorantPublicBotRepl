from util import methods, sql
import discord


async def register(ctx, name, rank, vclient, bot):
    if ctx.channel == methods.get_channel_commands(bot):
        if name is not None:
            if rank is not None:
                if type(rank) == discord.role.Role:
                    try:
                      valUser = vclient.get_user_by_name(name, delim="#")
                      valTag = valUser.__getattribute__("tagLine")
                      valName = valUser.__getattribute__("gameName")
                      valPUUID = valUser.__getattribute__("puuid")
                    except:
                        await ctx.send("There was an error with the Riot API. (Check your name and tag and/or try again later).")
                        return

                    dcUser = ctx.author

                    if any(ext in rank.name for ext in methods.valid_roles):
                        role = rank

                        reg = sql.insert_userdata(dcUser.id, valPUUID, valName, valTag, role)
                        if reg == 0:
                            try:
                                await dcUser.edit(nick=valName + "#" + valTag)
                            except:
                                await ctx.send("There was an error setting your username.")
                            await methods.set_rank(dcUser, role)
                            await ctx.send("Your nickname was set to your Valorant name and your rank has been updated.")
                        elif reg == 1:
                            await ctx.send('You are already registered with this Valorant UUID. Use !rank "rank". (Please contact a moderator if you are the account owner and someone else registered with your account).')
                        elif reg == 2:
                            await ctx.send('You are already registered with this Discord ID. Use !rank "rank". (Please leave the Discord with your old account or contact a moderator if you do not have access to your old account).')
                    else:
                        await ctx.send("You can't give yourself this role.")
                else:
                  await ctx.send("You have to mention this role with @")
            else:
                await ctx.send("You have to enter a rank.")
        else:
            await ctx.send("You have to enter a name.")
    else:
        await methods.get_channel_support(bot).send(content=ctx.author.mention + "you can't use this command here, got to " + methods.get_channel_commands(bot).mention, delete_after=30)
        await ctx.channel.purge(limit=1)
