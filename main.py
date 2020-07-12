#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord

HELPMESSAGE = "War**fork** game server **stat**istic (monitoring) \
    \n\t`!!stat` - show servers list\n\t*Note: 0 ping players and bots are not showed*"

DEBUG = False

def Debug(str):
    if (DEBUG):
        print(str)

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!!help'):
        await message.channel.send(HELPMESSAGE)

    if message.content.startswith('!!stat'):
        #TODO SPLIT CONTENT FILE, and send separate 2000
        serverinfo = ''
        try:
            with open("app.log", "r") as logfile:
                serverinfo += logfile.read(2000)
        except EnvironmentError as err:
            print(err)
        await message.channel.send(serverinfo)




client.run('TOKEN HERE')



