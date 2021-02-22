import os
import valorant
import discord

from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive

from commands import lft, register, rank
from util import sql, methods

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.bans = True
intents.voice_states = True
intents.presences = True

vclient = valorant.Client(os.getenv("KEY"))
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("'Valorant Public Bot' logged in")
    sql.create_table()


@bot.event
async def on_member_join(member):
    channel_support = bot.get_channel(806112383693094942)
    channel_rules = bot.get_channel(806088311848435732)
    await channel_support.send(content=
    'Welcome to the Public Valorant Server, ' + member.mention + '\n\nStart of by reading the rules in ' + channel_rules.mention +
    ' and have a look into the server tutorial.' + '\n\nNow you have full access on the Discord Server, if any questions come up feel free to tag an Moderator or an Administrator for important questions.\n'
    , delete_after=900)


@bot.event
async def on_member_remove(member):
    if member.nick is not None:
        if not member.bot:
            sql.delete_user(member.id)


def is_bot(message):
    return message.author != bot.get_user(806461492450426900)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.channel == bot.get_channel(806109172336689162):
        if message.author != bot.get_user(806461492450426900):
            await message.delete()


@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.get_user(806461492450426900):
        await lft.lft_event_add(reaction, user, bot)


@bot.event
async def on_reaction_remove(reaction, user):
    await lft.lft_event_remove(reaction, user, bot)


@bot.event
async def on_voice_state_update(member, before, after):
    join_to_create = bot.get_channel(809430391177084969)
    join_to_create_category = join_to_create.category

    if before.channel != after.channel:
        if not member.bot:
            if after.channel == join_to_create:
                if member.nick is not None:
                    new_voice = await member.guild.create_voice_channel(name=member.nick + "'s channel", category=join_to_create_category)
                    await member.move_to(new_voice)

        if before.channel is not None:
            # delete temp channels
            if before.channel.category == join_to_create_category:
                if before.channel != join_to_create:
                    if len(before.channel.members) == 0:
                        await before.channel.delete()
                    # delete channel reaction
                    await lft.lft_leave_channel(member, before, bot)

        if after.channel is not None:
            if after.channel.category == join_to_create_category:
                if after.channel != join_to_create:
                    if len(after.channel.members) >= 5:
                        if sql.channel_exists(after.channel):
                            await methods.set_closed(after.channel, bot)


@bot.command(name="register", pass_context=True)
async def register_command(ctx, name=None, rank=None):
    await register.register(ctx, name, rank, vclient, bot)


@bot.command(name="rank", pass_context=True)
async def rank_command(ctx, role=None):
    await rank.rank(ctx, role, bot)


@bot.command(name="lft", pass_context=True)
async def lft_command(ctx):
    await lft.lft(ctx, bot)


@bot.command(name="update", pass_context=True)
async def update_command(ctx):
    if ctx.channel == bot.get_channel(806084486869417984):
        await methods.check_profile(ctx.author, vclient)
        await ctx.send("Your profile has been updated.")


@bot.command(name="close", pass_context=True)
async def close_command(ctx):
    if ctx.author.voice is not None:
        if sql.channel_exists(ctx.author.voice.channel):
            await methods.set_closed(ctx.author.voice.channel, bot)
        else:
            await bot.get_channel(806112383693094942).send(content=ctx.author.mention + ", you need to use !lft before using !close.", delete_after=30)


@bot.event
async def on_disconnect():
    sql.mydb.close()
    print("Valorant Bot logged out")


keep_alive()
bot.run(os.getenv("TOKEN"))