#!/usr/bin/env python

import configparser
import discord
from collections import Counter
from os import path
import hashlib

configFileName = "astria.config.ini"

config = configparser.ConfigParser()
if path.isfile(configFileName):
    config.read(configFileName)
else:
    print("No config found")
    exit(1)

client = discord.Client()

@client.event
async def on_ready():
    print('Online as {0.user}'.format(client))
    if len(client.guilds) > 1:
        print('Too many servers, please run with only one connected server')
    byUser = Counter()
    byChannel = Counter()
    for channel in client.guilds[0].channels:
        if type(channel) == discord.TextChannel:
            try:
                async for message in channel.history(limit=None):
                    byChannel += Counter({channel.name})
                    userHash = hashlib.md5(bytes(str(message.author.id) + config.get("core", "salt"), "utf-8")).hexdigest()
                    byUser += Counter({userHash})
            except:
                pass
            finally:
                pass
    with open(config.get("core", "channelfile"), 'w') as channelFile:
        for channel in byChannel.most_common():
            channelFile.write("{0},{1}\n".format(channel[0], channel[1]))
    with open(config.get("core", "userfile"), 'w') as userfile:
        for channel in byUser.most_common():
            userfile.write("{0},{1}\n".format(channel[0], channel[1]))      
    print("Files outputed")
    await client.close()

client.run(config.get("core", "token"))