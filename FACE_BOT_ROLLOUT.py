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
import pprint

async def setPosted(id, newPosted):
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("UPDATE fb_faces SET posted = '"+ str(newPosted) +"' WHERE id = '" + str(id) + "'")
		mydb.commit()
		mycursor.execute("SELECT posted FROM fb_faces WHERE id = '" + str(id) + "'")
		data = mycursor.fetchone()
		if data is not None:
			mydb.close()
			mycursor.close()
			if(int(data[0]) == int(newPosted)):
				print("Updated posted for "+str(id) + " to " + str(newPosted))
				return True
			else:
				print("FAILED updating posted for "+str(id))
		else:
			print("FAILED updating posted for "+str(id))
			return False
	except Exception as e:
		print(e)
		print ("Database Connection Failed! (3)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def getAllCompleted():
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT id FROM fb_states WHERE state = '6'")
		data = mycursor.fetchall()
		if data is not None:
			print("Completed (state 6) members found")
			mydb.close()
			mycursor.close()
			iter = 0
			newdata = []
			for id in data:
				newdata.append(str(id[0]))
				#print(newdata[iter])
				iter = iter + 1
			return newdata
		else:
			print("FAILED finding completed (state 6) members")
			return False
	except Exception as e:
		print(e)
		print ("Database Connection Failed! (4)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def getAllUnposted():
	try:
		mydb = mysql.connector.connect(host="127.0.0.1", user="FaceBot", passwd="password", database="facebot")
		mycursor = mydb.cursor(buffered=True)
		mycursor.execute("SELECT id FROM fb_faces WHERE posted = '0'")
		data = mycursor.fetchall()
		if data is not None:
			print("Unposted members found")
			mydb.close()
			mycursor.close()
			iter = 0
			newdata = []
			for id in data:
				newdata.append(str(id[0]))
				#print(newdata[iter])
				iter = iter + 1
			return newdata
		else:
			print("FAILED finding unposted members")
			return False
	except Exception as e:
		print(e)
		print ("Database Connection Failed! (4)")
		python = sys.executable
		os.execl(python, python, * sys.argv)
		
async def getBan(id):
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
		print ("Database Connection Failed! (6)")
		python = sys.executable
		os.execl(python, python, * sys.argv)

async def getPrivateKey(id):
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
		print ("Database Connection Failed! (2)")
		python = sys.executable
		os.execl(python, python, * sys.argv)

async def getExt(secretKey, veri):
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
		
class MyClient(discord.Client):
	async def on_ready(self):	
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
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
				
				fchannel = client.get_channel(516108282390380565)
				#await fchannel.send("Sup niggas")
				
				allUnposted = await getAllUnposted()
				allCompleted = await getAllCompleted()
				
				postList = []
				
				for id in allUnposted:
					for sid in allCompleted:
						if id == sid:
							postList.append(int(id))
				
				await fchannel.send("**BEGIN CRYOGEN ROLLOUT FOR "+str(datetime.datetime.today().strftime('%m/%d/%Y'))+"**")
				
				if postList:
					for id in postList:
						if await getBan(str(id)) == False:
							print("Discord user with id "+str(id)+" is now being placed in cryogen")
							secretKey = await getPrivateKey(str(id))
							#print(secretKey)
							await fchannel.send(file=discord.File("C:\\inetpub\\wwwroot\\FaceBot\\public\\Faces\\"+secretKey+await getExt(secretKey, False)))
							await setPosted(str(id),1)
							fuser = fchannel.guild.get_member(int(id))
							role = discord.utils.get(fchannel.guild.roles, name="In Cryo")
							await fuser.add_roles(role)
							
				newdate = datetime.datetime.today() + datetime.timedelta(days=14)
				await fchannel.send("**END OF "+str(datetime.datetime.today().strftime('%m/%d/%Y'))+" CRYOGEN ROLLOUT. NEXT ROLLOUT WILL BE ON "+str(newdate.strftime('%m/%d/%Y'))+" @everyone **")
				print("Next rollout date will be - "+str(newdate.strftime('%m/%d/%Y')))
				
				os._exit(0)
			else:
				print ("Database Connection Failed! (0)")
				python = sys.executable
				os.execl(python, python, * sys.argv)
		else:
			print ("Database Connection Failed! (-1)")
			python = sys.executable
			os.execl(python, python, * sys.argv)

client = MyClient()
client.run("token")