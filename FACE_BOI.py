#Diemart
import mysql.connector
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import datetime
from discord.utils import get
import time
import os
import sys
import random
import string
import aiohttp
import aiofiles
from crontab import CronTab
from pathlib import Path
import subprocess

actionDict = ["replying !SendFace","replying !next","replying !next","sending the photo you wish to be placed in cryo","sending the identity verification photo","waiting for mods to approve your picture and confirm your identity","doing nothing, you are done unless you would like to update your photo with !UpdateFace"]

async def checkDBAccount(id, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT * FROM fb_states WHERE id = '" + str(id) + "'")
		data = mycursor.fetchone()
		if data is None:
			print("Creating new database entry for "+str(id))
			sql = "INSERT INTO fb_states (id, state, banned, modMsgId) VALUES (%s, %s, %s, %s)"
			val = (str(id), '0', '0', '0')
			mycursor.execute(sql, val)
			mydb.commit()
			
			mycursor.execute("SELECT * FROM fb_states WHERE id = '" + str(id) + "'")
			data = mycursor.fetchone()
			if data is not None:
				print("Created new database entry for "+str(id))
				mydb.close()
				mycursor.close()
				return True
			else:
				print("FAILED Creating new database entry for "+str(id))
				return False
		else:
			print("Database entry found for "+str(id))
			mydb.close()
			mycursor.close()
			return True
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (1)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def checkFaceAccount(id, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT * FROM fb_faces WHERE id = '" + str(id) + "'")
		data = mycursor.fetchone()
		if data is None:
			print("Creating new Face database entry for "+str(id))
			keyFound = False
			randStr = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
			while keyFound == False:
				randStr = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
				mycursor.execute("SELECT * FROM fb_faces WHERE RandomImageName = '" + randStr + "'")
				data = mycursor.fetchone()
				if data is None:
					keyFound = True
			sql = "INSERT INTO fb_faces (id, RandomImageName, posted) VALUES (%s, %s, %s)"
			val = (str(id), randStr, '0')
			mycursor.execute(sql, val)
			mydb.commit()
			
			mycursor.execute("SELECT * FROM fb_faces WHERE id = '" + str(id) + "'")
			data = mycursor.fetchone()
			if data is not None:
				print("Created new Face database entry for "+str(id))
				mydb.close()
				mycursor.close()
				return True
			else:
				print("FAILED Creating new Face database entry for "+str(id))
				return False
		else:
			print("Database entry found for "+str(id))
			mydb.close()
			mycursor.close()
			return True
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (2)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def getPrivateKey(id, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT RandomImageName FROM fb_faces WHERE id = '" + str(id) + "'")
		data = mycursor.fetchone()
		if data is not None:
			print("RandomKey found for "+str(id) + " : " + str(data[0]))
			mydb.close()
			mycursor.close()
			return str(data[0])
		else:
			print("FAILED finding RandomKey for "+str(id))
			return False
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (2)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def setState(id, newState, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("UPDATE fb_states SET state = '"+ str(newState) +"' WHERE id = '" + str(id) + "'")
		mydb.commit()
		mycursor.execute("SELECT state FROM fb_states WHERE id = '" + str(id) + "'")
		data = mycursor.fetchone()
		if data is not None:
			mydb.close()
			mycursor.close()
			if(int(data[0]) == int(newState)):
				print("Updated state for "+str(id) + " to " + str(newState))
				return True
			else:
				print("FAILED updating state for "+str(id))
		else:
			print("FAILED updating state for "+str(id))
			return False
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (3)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def getState(id, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT state FROM fb_states WHERE id = '" + str(id) + "'")
		data = mycursor.fetchone()
		if data is not None:
			print("State found for "+str(id) + " : " + str(data[0]))
			mydb.close()
			mycursor.close()
			return int(data[0])
		else:
			print("FAILED finding state for "+str(id))
			return False
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (4)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def setBan(id, newState, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("UPDATE fb_states SET banned = '"+ str(newState) +"' WHERE id = '" + str(id) + "'")
		mydb.commit()
		mycursor.execute("SELECT banned FROM fb_states WHERE id = '" + str(id) + "'")
		data = mycursor.fetchone()
		if data is not None:
			mydb.close()
			mycursor.close()
			if(int(data[0]) == int(newState)):
				print("Updated ban state for "+str(id) + " to " + str(newState))
				return True
			else:
				print("FAILED updating ban state for "+str(id))
		else:
			print("FAILED updating state for "+str(id))
			return False
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (5)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def getBan(id, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT banned FROM fb_states WHERE id = '" + str(id) + "'")
		data = mycursor.fetchone()
		if data is not None:
			print("Ban State found for "+str(id) + " : " + str(data[0]))
			mydb.close()
			mycursor.close()
			return int(data[0])
		else:
			print("FAILED finding ban state for "+str(id))
			return False
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (6)")
		python = sys.executable
		os.execl(python, python, * sys.argv)

async def saveImage(url, secretKey, message, veri, exten):
	if(veri):
		try:
			async with aiohttp.ClientSession() as session:
				async with session.get(message.attachments[0].url) as resp:
					if resp.status == 200:
						my_file = Path("C:\\FaceBot\\private\\Verification\\"+secretKey+exten)
						if not my_file.is_file():
							f = await aiofiles.open("C:\\FaceBot\\private\\Verification\\"+secretKey+exten, mode='w')
							await f.close()
						f = await aiofiles.open("C:\\FaceBot\\private\\Verification\\"+secretKey+exten, mode='wb')
						await f.write(await resp.read())
						await f.close()
		except Exception as e:
			print(e)
			await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
			print ("Database Connection Failed! (6)")
			python = sys.executable
			os.execl(python, python, * sys.argv)
	else:
		try:
			async with aiohttp.ClientSession() as session:
				async with session.get(message.attachments[0].url) as resp:
					if resp.status == 200:
						my_file = Path("C:\\inetpub\\wwwroot\\FaceBot\\public\\Faces\\"+secretKey+exten)
						if not my_file.is_file():
							f = await aiofiles.open("C:\\inetpub\\wwwroot\\FaceBot\\public\\Faces\\"+secretKey+exten, mode='w')
							await f.close()
						f = await aiofiles.open("C:\\inetpub\\wwwroot\\FaceBot\\public\\Faces\\"+secretKey+exten, mode='wb')
						await f.write(await resp.read())
						await f.close()
		except Exception as e:
			print(e)
			await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
			print ("Database Connection Failed! (6)")
			python = sys.executable
			os.execl(python, python, * sys.argv)

async def removeImages(secretKey, message):
	allowedexts = [".jpg",".jpeg",".png"]
	for ext in allowedexts:
		my_file = Path("C:\\FaceBot\\private\\Verification\\"+secretKey+ext)
		if my_file.is_file():
			os.remove("C:\\FaceBot\\private\\Verification\\"+secretKey+ext)
		
		my_file = Path("C:\\inetpub\\wwwroot\\FaceBot\\public\\Faces\\"+secretKey+ext)
		if my_file.is_file():
			os.remove("C:\\inetpub\\wwwroot\\FaceBot\\public\\Faces\\"+secretKey+ext)
			
async def getExt(secretKey, veri, message):
	allowedexts = [".jpg",".jpeg",".png"]
	for ext in allowedexts:
		if(veri):
			my_file = Path("C:\\FaceBot\\private\\Verification\\"+secretKey+ext)
			if my_file.is_file():
				return ext
		else:
			my_file = Path("C:\\inetpub\\wwwroot\\FaceBot\\public\\Faces\\"+secretKey+ext)
			if my_file.is_file():
				return ext
				
async def setModMsg(id, message, modMsg):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("UPDATE fb_states SET modMsgId = '"+ str(modMsg.id) +"' WHERE id = '" + str(id) + "'")
		mydb.commit()
		mycursor.execute("SELECT modMsgId FROM fb_states WHERE id = '" + str(id) + "'")
		data = mycursor.fetchone()
		if data is not None:
			mydb.close()
			mycursor.close()
			if(int(data[0]) == int(modMsg.id)):
				print("Updated modMsgId for "+str(id) + " to " + str(modMsg.id))
				return True
			else:
				print("FAILED updating modMsgId for "+str(id))
		else:
			print("FAILED updating modMsgId for "+str(id))
			return False
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (5)")
		python = sys.executable
		os.execl(python, python, * sys.argv)

async def getModMsg(id, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT modMsgId FROM fb_states WHERE id = '" + str(id) + "'")
		data = mycursor.fetchone()
		if data is not None:
			print("modMsgId found for "+str(id) + " : " + str(data[0]))
			mydb.close()
			mycursor.close()
			return int(data[0])
		else:
			print("FAILED finding modMsgId for "+str(id))
			return False
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (6)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def getModMsgTwo(id, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT modMsgId FROM fb_modmsg WHERE msgId3 = '" + str(id) + "'")
		data = mycursor.fetchone()
		if data is not None:
			print("modMsgId found for "+str(id) + " : " + str(data[0]))
			mydb.close()
			mycursor.close()
			return int(data[0])
		else:
			print("FAILED finding modMsgId for "+str(id))
			return False
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (6)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def getUserID(id, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT id FROM fb_states WHERE modMsgId = '" + str(id) + "'")
		data = mycursor.fetchone()
		if data is not None:
			print("id found for "+str(id) + " : " + str(data[0]))
			mydb.close()
			mycursor.close()
			return int(data[0])
		else:
			print("FAILED finding id for "+str(id))
			return False
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (6)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def checkExtMsgAccount(ModMsgId, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT * FROM fb_modmsg WHERE modMsgId = '" + str(ModMsgId) + "'")
		data = mycursor.fetchone()
		if data is None:
			print("Creating new modmsg entry for "+str(ModMsgId))
			sql = "INSERT INTO fb_modmsg (modMsgId, msgId1, msgId2, msgId3) VALUES (%s, %s, %s, %s)"
			val = (str(ModMsgId), '0', '0', '0')
			mycursor.execute(sql, val)
			mydb.commit()
			
			mycursor.execute("SELECT * FROM fb_modmsg WHERE modMsgId = '" + str(ModMsgId) + "'")
			data = mycursor.fetchone()
			if data is not None:
				print("Created new modmsg entry for "+str(ModMsgId))
				mydb.close()
				mycursor.close()
				return True
			else:
				print("FAILED Creating new modmsg entry for "+str(ModMsgId))
				return False
		else:
			print("modmsg entry found for "+str(ModMsgId))
			mydb.close()
			mycursor.close()
			return True
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (7)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def setExtMsg(OrigId, message, ModMsgId, modMsgOneId, modMsgTwoId, modMsgThreeId):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("UPDATE fb_modmsg SET modMsgId = '"+ str(ModMsgId) + "', msgId1 = '"+ str(modMsgOneId) + "', msgId2 = '"+ str(modMsgTwoId) + "', msgId3 = '"+ str(modMsgThreeId) + "' WHERE modMsgId = '" + str(OrigId) + "'")
		mydb.commit()
		mycursor.execute("SELECT * FROM fb_modmsg WHERE modMsgId = '" + str(ModMsgId) + "'")
		data = mycursor.fetchone()
		if data is not None:
			mydb.close()
			mycursor.close()
			print("Updated modMsgId for "+str(OrigId) + " to " + str(ModMsgId))
			return True
		else:
			print("FAILED updating modMsgId for "+str(OrigId))
			return False
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (8)")
		python = sys.executable
		os.execl(python, python, * sys.argv)

async def getExtMsgOne(modMsgId, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT msgId1 FROM fb_modmsg WHERE modMsgId = '" + str(modMsgId) + "'")
		data = mycursor.fetchone()
		if data is not None:
			print("msgId1 found for "+str(modMsgId) + " : " + str(data[0]))
			mydb.close()
			mycursor.close()
			return int(data[0])
		else:
			print("FAILED finding msgId1 for "+str(modMsgId))
			return False
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (9)")
		python = sys.executable
		os.execl(python, python, * sys.argv)

async def getExtMsgTwo(modMsgId, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT msgId2 FROM fb_modmsg WHERE modMsgId = '" + str(modMsgId) + "'")
		data = mycursor.fetchone()
		if data is not None:
			print("msgId2 found for "+str(modMsgId) + " : " + str(data[0]))
			mydb.close()
			mycursor.close()
			return int(data[0])
		else:
			print("FAILED finding msgId2 for "+str(modMsgId))
			return False
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (9)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def getExtMsgThree(modMsgId, message):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT msgId3 FROM fb_modmsg WHERE modMsgId = '" + str(modMsgId) + "'")
		data = mycursor.fetchone()
		if data is not None:
			print("msgId3 found for "+str(modMsgId) + " : " + str(data[0]))
			mydb.close()
			mycursor.close()
			return int(data[0])
		else:
			print("FAILED finding msgId3 for "+str(modMsgId))
			return False
	except Exception as e:
		print(e)
		await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
		print ("Database Connection Failed! (9)")
		python = sys.executable
		os.execl(python, python, * sys.argv)

class MyClient(discord.Client):
	async def on_ready(self):	
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		game = discord.Game("!SendFace")
		await self.change_presence(status=discord.Status.online, activity=game)
		print("Connecting to database")
		
		try:
			mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		except Exception as e:
			print ("Database Connection Failed!(-2)")
			python = sys.executable
			os.execl(python, python, * sys.argv)
		
		if(mydb != None):
			if (mydb):
				mycursor = mydb.cursor(buffered=True)
				print ("Database Connection successful")
				mydb.close()
				mycursor.close()
			else:
				print ("Database Connection Failed! (0)")
				python = sys.executable
				os.execl(python, python, * sys.argv)
		else:
			print ("Database Connection Failed! (-1)")
			python = sys.executable
			os.execl(python, python, * sys.argv)
			
	async def on_raw_reaction_add(self, payload):
		channel = client.get_channel(516126209139277834)
		guild = client.get_guild(516084784745807874)
		mod = guild.get_role(516106024546074624)
		mods = len(mod.members)
		message = await channel.get_message(payload.message_id)
		if message:
			yes = 0
			no = 0
			ban = 0
			for emote in message.reactions:
				if(emote.emoji == '✅'): # check mark
					yes += emote.count
				if(emote.emoji == '❌'): # x
					no += emote.count
				if(emote.emoji == '🚫'): # ban
					ban = 1
			#remove messages on all of these
			if(ban > 0):
				#modMsg = await getModMsgTwo(payload.message_id, message)
				userID = await getUserID(payload.message_id, message)
				pKey = await getPrivateKey(userID, message)
				if(await setBan(int(userID), 1, message) == True):
					if(await setState(userID, -1, message) == True):
						epicUser = await client.get_user_info(userID)
						bannedUser = epicUser.dm_channel
						if(type(bannedUser) == type(None)):
							await epicUser.create_dm()
							bannedUser = epicUser.dm_channel
						await bannedUser.send("You have been banned by a moderator from using this bot. For reference if speaking to <@143478947621896192> about your ban, use your privateKey - ``"+pKey+"``")
						NewMSG = await channel.get_message(int(await getExtMsgOne(payload.message_id , message)))
						await NewMSG.delete()
						NewMSG = await channel.get_message(int(await getExtMsgTwo(payload.message_id , message)))
						await NewMSG.delete()
						NewMSG = await channel.get_message(int(await getExtMsgThree(payload.message_id , message)))
						await NewMSG.delete()
						NewMSG = await channel.get_message(int(payload.message_id))
						await NewMSG.delete()
						await message.channel.send("<@"+str(userID)+"> has been banned from using Face-Bot")
					else:
						await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
				else:
					await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
			else:
				if(yes > mods/2):
					#modMsg = await getModMsgTwo(payload.message_id, message)
					userID = await getUserID(payload.message_id, message)
					pKey = await getPrivateKey(userID, message)
					if(await getState(userID, message) == 5):
						if(await setState(userID, 6, message) == True):
							epicUser = await client.get_user_info(userID)
							bannedUser = epicUser.dm_channel
							if(type(bannedUser) == type(None)):
								await epicUser.create_dm()
								bannedUser = epicUser.dm_channel
							await bannedUser.send("Your Cryogen submission has been approved and will be displayed in the next rollout. If speaking to an admin about any questions that involves possible changes to your submission, use your privateKey - ``"+pKey+"``")
							NewMSG = await channel.get_message(int(await getExtMsgOne(payload.message_id , message)))
							await NewMSG.delete()
							NewMSG = await channel.get_message(int(await getExtMsgTwo(payload.message_id , message)))
							await NewMSG.delete()
							NewMSG = await channel.get_message(int(await getExtMsgThree(payload.message_id , message)))
							await NewMSG.delete()
							NewMSG = await channel.get_message(int(payload.message_id))
							await NewMSG.delete()
							await message.channel.send("<@"+str(userID)+"> has been placed into cryo and will be displayed in the next rollout")
						else:
							await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
					else:
						await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
				else:
					if(no >= mods/2):
						#modMsg = await getModMsgTwo(payload.message_id, message)
						userID = await getUserID(payload.message_id, message)
						pKey = await getPrivateKey(userID, message)
						if(await getState(userID, message) == 5):
							if(await setState(userID, 0, message) == True):
								epicUser = await client.get_user_info(userID)
								bannedUser = epicUser.dm_channel
								if(type(bannedUser) == type(None)):
									await epicUser.create_dm()
									bannedUser = epicUser.dm_channel
								await bannedUser.send("Your Cryogen submission has been denied. You may re-apply at any time.")
								NewMSG = await channel.get_message(int(await getExtMsgOne(payload.message_id , message)))
								await NewMSG.delete()
								NewMSG = await channel.get_message(int(await getExtMsgTwo(payload.message_id , message)))
								await NewMSG.delete()
								NewMSG = await channel.get_message(int(await getExtMsgThree(payload.message_id , message)))
								await NewMSG.delete()
								NewMSG = await channel.get_message(int(payload.message_id))
								await NewMSG.delete()
								await message.channel.send("<@"+str(userID)+"> has been denied")
							else:
								await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
						else:
							await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
			
	# don't do drugs kids
	async def on_message(self, message):
		global actionDict
		if not message.author.bot:
			if message.content.upper().startswith("!PING"):
				before = time.monotonic()
				origMsg = await message.channel.send("Pong!")
				ping = (time.monotonic() - before) * 1000
				await origMsg.edit(content="Pong! Took "+str(ping)+"ms to respond.")
			if not message.attachments:
				if isinstance(message.channel,discord.DMChannel):
					extfound = False
					if(await checkDBAccount(message.author.id, message)):
						if(await getBan(message.author.id, message) == 0):
							curState = await getState(message.author.id, message)
							if(curState == 3 or curState == 4):
								await message.channel.send("Sent a link instead of an image. We only accept direct file uploads of embeddable images (.png, .jpg, .jpeg)\nPlease send the image you would like to be placed in #cryogenic in an extension that embeds within discord")
						else:
							await message.channel.send("Sorry, but you have been banned by a moderator from using this bot.")
					else:
						await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
			else:
				if isinstance(message.channel,discord.DMChannel):
					allowedexts = [".jpg",".jpeg",".png"]
					extfound = False
					if(await checkDBAccount(message.author.id, message)):
						if(await getBan(message.author.id, message) == 0):
							curState = await getState(message.author.id, message)
							for ext in allowedexts:
								print(str(message.attachments))
								if (message.attachments[0].url.upper().endswith(ext.upper())):
									extfound = True
									print(message.attachments[0].size)
									if (await checkFaceAccount(message.author.id, message)):
										secretKey = await getPrivateKey(message.author.id, message)
										if(curState == 3):
											if(message.attachments[0].size > 0 and message.attachments[0].size <= 8000000):
												print("Image 1 Author: "+str(message.author.id))
												print("Image 1 URL: "+message.attachments[0].url)
												await saveImage(message.attachments[0].url, secretKey, message, False, ext)
												await message.channel.send("Cryo Image received!\nNext, please send another photo of you with your face looking the same as the last image (in an extension that embeds within discord) and holding a piece of paper containing the following info(in your own HANDWRITING)\n https://opifexdev.net/facebot/public/template3.png \n Your discord ID is ``"+str(message.author.id)+"``")
												if(await setState(message.author.id, 4, message) == False):
													await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
											else:
												await message.channel.send("File is too big or nonexistant! Image must be 8 MB or less!")
										elif(curState == 4):
											if(message.attachments[0].size > 0 and message.attachments[0].size <= 8000000):
												print("Image 2 Author: "+str(message.author.id))
												print("Image 2 URL: "+message.attachments[0].url)
												await saveImage(message.attachments[0].url, secretKey, message, True, ext)
												await message.channel.send("Verification Image received!\nFinally, please wait for a moderator to check that your image fits the rules and confirm your identity. I will respond back when your image has been accepted or denied. If your picture gets accepted, you will also be notified of your private key.")
												channel = client.get_channel(516126209139277834)
												if(await setState(message.author.id, 5, message) == False):
													await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
												msgOne = await channel.send("<@"+str(message.author.id)+">")
												try:
													msgTwo = await channel.send(file=discord.File("C:\\inetpub\\wwwroot\\FaceBot\\public\\Faces\\"+secretKey+await getExt(secretKey, False, message)),content="Face:")
												except Exception as e:
													print(e)
													await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
													print ("Failed to send face image to moderation!")
													python = sys.executable
													os.execl(python, python, * sys.argv)
												try:
													msgThree = await channel.send(file=discord.File("C:\\FaceBot\\private\\Verification\\"+secretKey+await getExt(secretKey, True, message)),content="Verification:")
													lmao = await channel.send("React with :white_check_mark: to approve the image or :x: to deny the image after confirming the people in the pictures look the same and that the image fits the image rules <@&516106024546074624> .")
												except Exception as e:
													print(e)
													await message.channel.send("It seems I fucked up! Give me 60 seconds while I restart myself, if I am not responding to commands after 60 seconds or more errors are thrown, Please DM <@143478947621896192> . The step you are at in the process has been saved.")
													print ("Failed to send verification image to moderation!")
													python = sys.executable
													os.execl(python, python, * sys.argv)
												if(await setModMsg(message.author.id, message, lmao)):
													await lmao.add_reaction('\U00002705')
													await lmao.add_reaction('\U0000274C')
													if(await checkExtMsgAccount(lmao.id, message)):
														if(await setExtMsg(lmao.id, message, lmao.id, msgOne.id, msgTwo.id, msgThree.id) == False):
															await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
													else:
														await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
												else:
													await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
											else:
												await message.channel.send("File is too big or nonexistant! Image must be 8 MB or less!")
										else:
											await message.channel.send("Wrong command! The step you are currently at requires a different action! You should currently be "+actionDict[curState])
									else:
										await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
							if not extfound:
								if(curState == 3 or curState == 4):
									await message.channel.send("Sent file was not an image or sent file was not an embeddable image (.png, .jpg, .jpeg)\nPlease send the image you would like to be placed in #cryogenic in an extension that embeds within discord")
						else:
							await message.channel.send("Sorry, but you have been banned by a moderator from using this bot.")
					else:
						await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
			if message.content.upper().startswith("!SENDFACE"):
				if isinstance(message.channel,discord.DMChannel):
					if(await checkDBAccount(message.author.id, message)):
						if(await getBan(message.author.id, message) == 0):
							curState = await getState(message.author.id, message)
							if(curState == 0):
								await message.channel.send("By using this bot you agree to the rules described in #cryo-rules on the discord server https://discord.gg/Fr6Vkrt , do you wish to proceed? reply with ``!next`` if you wish to proceed or ``!exit`` to exit the process. You may exit the process at any time if you decide against going into cryo.\nNOTE: ALL IMAGES IN CRYO ARE ANONYMOUS AND WILL NOT HAVE YOUR NAME TIED TO THEM")
								if(await setState(message.author.id, 1, message) == False):
									await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
							else:
								await message.channel.send("Wrong command! The step you are currently at requires a different action! You should currently be "+actionDict[curState])
						else:
							await message.channel.send("Sorry, but you have been banned by a moderator from using this bot.")
					else:
						await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
				else:
					await message.delete()
					await message.channel.send("Do not use this command in the server! Use this command in a private message to me instead!")
			if message.content.upper().startswith("!NEXT"):
				if isinstance(message.channel,discord.DMChannel):
					if(await checkDBAccount(message.author.id, message)):
						if(await getBan(message.author.id, message) == 0):
							curState = await getState(message.author.id, message)
							if(curState == 1):
								await message.channel.send("Now that the rules have been accepted, we will outline the things you will need to do to prove you are who you claim to be...\n\n**Steps**\nFirst: You will send the photo of yourself to be put in cryogenic storage\nSecond: You will send another photo of yourself holding a piece of paper That looks like the image below for verification of identity: (Text must be written in your own handwriting)\n https://opifexdev.net/facebot/public/template3.png \nFinally: Moderators will check the image and verification image to meet our rules and if accepted, the original photo will be placed in #cryogenic and your will be notified by me of your approval. If you are denied access by Moderators, a reason will be given.\nIf you are ready to start step one, reply with ``!next`` again and if you wish to exit the process, reply with ``!exit``\nNOTE: BOTH PICTURES MUST HAVE YOUR FACE LOOKING THE SAME AND IMAGES CANNOT BE EDITED BY A COMPUTER")
								if(await setState(message.author.id, 2, message) == False):
									await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
							elif(curState == 2):
								await message.channel.send("Please send the image you would like to be placed in #cryogenic in an extension that embeds within discord")
								if(await setState(message.author.id, 3, message) == False):
									await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
							else:
								await message.channel.send("Wrong command! The step you are currently at requires a different action! You should currently be "+actionDict[curState])
						else:
							await message.channel.send("Sorry, but you have been banned by a moderator from using this bot.")
					else:
						await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
				else:
					await message.delete()
					await message.channel.send("Do not use this command in the server! Use this command in a private message to me instead!")
			if message.content.upper().startswith("!EXIT"):
				if isinstance(message.channel,discord.DMChannel):
					if(await checkDBAccount(message.author.id, message)):
						if(await getBan(message.author.id, message) == 0):
							curState = await getState(message.author.id, message)
							if(curState == 1 or curState == 2 or curState == 3):
								await message.channel.send("Your progress has been reset. You may replay with !SendFace at any time to start the process again.")
								if(await setState(message.author.id, 0, message) == False):
									await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
							elif(curState == 4):
								if (await checkFaceAccount(message.author.id, message)):
									secretKey = await getPrivateKey(message.author.id, message)
									await removeImages(secretKey,message)
									await message.channel.send("Your progress has been reset. You may replay with !SendFace at any time to start the process again.")
									if(await setState(message.author.id, 0, message) == False):
										await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
							elif(curState == 0):
								await message.channel.send("No progress to reset!")
							else:
								await message.channel.send("Your canont reset your progress right now.")
						else:
							await message.channel.send("Sorry, but you have been banned by a moderator from using this bot.")
					else:
						await message.channel.send("Critical Failiure! You should never recieve this message, the SQL database must be malfunctioning! Please DM <@143478947621896192> with this error")
				else:
					await message.delete()
					await message.channel.send("Do not use this command in the server! Use this command in a private message to me instead!")
			if message.content.upper().startswith("!FORCEROLLOUT"):
				if isinstance(message.channel,discord.DMChannel):
					if message.author.id == 143478947621896192:
						await message.channel.send("Forcing a rollout...")
						#os.system('cd C:\\Users\\UltraTechX\\Documents\\FACE_BOT && python FACE_BOT_ROLLOUT.py')
						process = subprocess.Popen('cd C:\\Users\\UltraTechX\\Documents\\FACE_BOT && python FACE_BOT_ROLLOUT.py', shell=True, stdout=subprocess.PIPE)
					else:
						await message.channel.send("Woah there pal, you cant be here.")
				else:
					await message.delete()
					await message.channel.send("Do not use this command in the server! Use this command in a private message to me instead!")
		
client = MyClient()
client.run("token")