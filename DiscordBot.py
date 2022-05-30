import sys
import asyncio
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='-')
bot.remove_command('help')


# готовность бота
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


# автореакт ideas
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author != bot.user and message.channel.id == 723158412136808472:
        await message.add_reaction(':wYep:863417394622103563')
        await message.add_reaction(':wNope:863417394920030208')
    if message.author != bot.user and message.channel.id == 606176067933306880:
        await message.add_reaction('👍')
        await message.add_reaction('👎')


# хелп
@bot.command(name='help')
async def help_command(ctx: commands.context.Context):
    await ctx.message.delete()
    help_embed = discord.Embed(
        color=0x1427DF)
    help_embed.set_author(name='Help')
    help_embed.add_field(name='clear', value='clear <кол-во> \nОчищает чат.', inline=False)
    help_embed.add_field(name='mute',
                         value='mute <никнейм> <время(s/m/h)> <причина (не обязательно)>'
                               '\nЗапрещает участнику писать в чат.',
                         inline=False)
    help_embed.add_field(name='unmute', value='unmute <никнейм> \nСнимает с участника мут.', inline=False)
    help_embed.set_footer(text='Версия 1.1.2')
    await ctx.send(embed=help_embed)


# очистка чата
@bot.command(name='clear')
@commands.has_any_role(863450810645348362, 888860282976342096)
async def clear_command(ctx: commands.context.Context, amount: int):
    await ctx.message.delete()
    clear_embed = discord.Embed(
        title='_<:wNope:863417394920030208>_ **Значение аргумента не может быть меньше 1!**',
        color=0xD11818)
    amount_purged = await ctx.channel.purge(limit=amount)
    if not amount > 0:
        await ctx.send(embed=clear_embed, delete_after=5)
    else:
        clear_embed = discord.Embed(
            title=f'_<:wYep:863417394622103563>_ **Удалено {len(amount_purged)} сообщений!**',
            color=0x20D714)
        await ctx.send(embed=clear_embed, delete_after=5)


# mute
@bot.command(name='mute')
@commands.has_any_role(863450810645348362, 888860282976342096)
async def mute_command(ctx: commands.context, member: discord.Member, mute_time, reason='Без причины'):
    mute_role = discord.utils.get(ctx.guild.roles, id=705885683566510140)
    if not ctx.channel.id == 393868048475488256:
        await ctx.message.delete()
        mute_embed = discord.Embed(
            title='_<:wNope:863417394920030208>_ **Эту команду нельзя использовать здесь!**',
            color=0xD11818)
        await ctx.send(embed=mute_embed, delete_after=5)
    if member.top_role >= ctx.author.top_role:
        await ctx.message.delete()
        mute_embed = discord.Embed(
            title='_<:wNope:863417394920030208>_ **Нельзя выдать мут участнику с такой же ролью, как у вас или выше!**',
            color=0xD11818)
        await ctx.send(embed=mute_embed, delete_after=5)
    end_time = mute_time[-1:]
    time = int(mute_time[:-1])
    if time <= 0:
        await ctx.message.delete()
        mute_embed = discord.Embed(
            title='_<:wNope:863417394920030208>_ **Время не может быть меньше или равно 0!**',
            color=0xD11818)
        await ctx.send(embed=mute_embed, delete_after=5)
    else:
        await ctx.message.delete()
        mute_embed = discord.Embed(
            title=f'_<:wYep:863417394622103563>_ **{member} получает мут по причине: {reason}!**',
            color=0x20D714)
        await ctx.send(embed=mute_embed)
        if end_time == 's':
            await member.add_roles(mute_role)
            await asyncio.sleep(time)
            await member.remove_roles(mute_role)
        if end_time == 'm':
            await member.add_roles(mute_role)
            await asyncio.sleep(time * 60)
            await member.remove_roles(mute_role)
        if end_time == 'h':
            await member.add_roles(mute_role)
            await asyncio.sleep(time * 3600)
            await member.remove_roles(mute_role)


# анмут
@bot.command(name='unmute')
@commands.has_any_role(863450810645348362, 888860282976342096)
async def un_mute(ctx: commands.context, member: discord.Member):
    if not ctx.channel.id == 393868048475488256:
        await ctx.message.delete()
        mute_embed = discord.Embed(
            title='_<:wNope:863417394920030208>_ **Эту команду нельзя использовать здесь!**',
            color=0xD11818)
        await ctx.send(embed=mute_embed, delete_after=5)
    else:
        mute_role = discord.utils.get(ctx.guild.roles, id=705885683566510140)
        await member.remove_roles(mute_role)
        unmute_embed = discord.Embed(title=f'_<:wYep:863417394622103563>_ **С {member} снят мут!**',
                                     color=0x20D714)
        await ctx.send(embed=unmute_embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.message.delete()
        error_embed = discord.Embed(
            title='_<:wNope:863417394920030208>_ **У вас недостаточно прав для выполнения команды!**',
            color=0xD11818)
        await ctx.send(embed=error_embed, delete_after=5)
    if isinstance(error, commands.MissingRequiredArgument):
        error_embed = discord.Embed(
            title='_<:wNope:863417394920030208>_ **Не указаны необходимые аргументы!**',
            color=0xD11818)
        await ctx.message.delete()
        await ctx.send(embed=error_embed, delete_after=5)
    if isinstance(error, commands.MemberNotFound):
        error_embed = discord.Embed(
            title='_<:wNope:863417394920030208>_ **Этого участника нет на сервере!**',
            color=0xD11818)
        await ctx.message.delete()
        await ctx.send(embed=error_embed, delete_after=5)


@bot.command(name='say')
@commands.has_permissions(administrator=True)
async def say_command(ctx):
    await ctx.message.delete()
    await ctx.send('<a:animated:980423304621981747>')


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# token
bot.run('...')
