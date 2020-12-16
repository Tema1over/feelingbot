import discord #библиотека
from discord.ext import commands 
import datetime
from discord.utils import get
import youtube_dl

import os

PREFIX = 'w.'

client = commands.Bot(command_prefix = PREFIX ) #это_префикс_бота
client.remove_command( 'help' )

@client.event

async def on_ready():
	print( 'STARTED' )

	await client.change_presence( status = discord.Status.do_not_disturb, activity=discord.Streaming(name="w.help", url = 'https://www.twitch.tv/feeling_bot' ))
#========================================
#========================================
#clear
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def clear( ctx, amount = 50 ):
	await ctx.channel.purge( limit = amount )
#========================================
#kick
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def kick( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.kick( reason = reason )
	
	await ctx.send( f'Кикнут: { member.mention }' )

	emb = discord.Embed( title = 'Пользователь кикнут. Кикнул:', coulor = discord.Color.red() )
	
	emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
	await ctx.send( embed = emb )
#========================================
#ban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def ban( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.ban( reason = reason )
	#await ctx.send( f'Пользователь { member.mention } был забанен. Причина : {reason}' )
	await ctx.send( f'Забанен: { member.mention }. Причина: {reason}' )

	emb = discord.Embed( title = 'Пользователь забанен. Забанил:', coulor = discord.Color.red() )
	
	emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
	await ctx.send( embed = emb )
#========================================
#unban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def unban( ctx, *, member ):
	await ctx.channel.purge( limit = 1 )

	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user

		await ctx.guild.unban( user )
		await ctx.send( 'Бан с пользователя был снят. Добавить его у меня не получиться :D' )

		return

#========================================
#help
@client.command( pass_context = True )

async def help( ctx ):
	emb = discord.Embed( title = 'Команды', coulor = discord.Color.green )

	emb.add_field( name = '{}clear'.format( PREFIX ), value = 'Очистка чата' )
	emb.add_field( name = '{}kick'.format( PREFIX ), value = 'Исключение участника' )
	emb.add_field( name = '{}ban'.format( PREFIX ), value = 'Бан участника' )
	emb.add_field( name = '{}unban'.format( PREFIX ), value = 'Разбан' )
	emb.add_field( name = '{}time'.format( PREFIX ), value = 'Время' )
	emb.add_field( name = '{}invite'.format( PREFIX ), value = 'Ссылка для добавления бота' )

	emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )

	await ctx.send( embed = emb )
#========================================
#time
@client.command( pass_context = True )

async def time( ctx ):
	emb = discord.Embed()

	emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )

	now_date = datetime.datetime.now()

	emb.add_field( name = 'Time', value = 'Time : {}'.format( now_date ) )

	await ctx.send( embed = emb )
#========================================
#connect
@client.command()
async def join(ctx):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		await ctx.send(f'Бот присоеденился к {channel}')

#leave
@client.command()
async def leave(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await connect.channel()
		await ctx.send(f'Бот отключился от {channel}')
#========================================
#invite
@client.command(pass_context = True)

async def invite( ctx ):
	emb = discord.Embed( title = 'Добавить бота', coulor = discord.Color.green(), url = 'https://discord.com/oauth2/authorize?client_id=755376009116909629&scope=bot&permissions=8' )

	emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )

	await ctx.send( embed = emb )

#========================================
token = open( 'token.txt', 'r' ).readline()

client.run( token )