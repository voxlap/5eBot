import discord
import nltk
import time
import json
import random
from googleapiclient.discovery import build

client = discord.Client()
with open('discordToken.txt', 'r+') as myfile:
    token = str(myfile.read())
with open('commands.json', encoding='UTF-8') as fh:
    commands_file = json.load(fh)
commands = list(commands_file['commands'])
with open('test_messages.json', encoding='UTF-8') as fh:
    test_messages_file = json.load(fh)
test_messages = list(test_messages_file['messages'])
with open('emojis.json', encoding='UTF-8') as fh:
           emojis = json.load(fh)
           
class Search(object):
    def __init__(self, query, command, channel):
        
        self.command = command
        with open(self.command + '.json', encoding='UTF-8') as fh:
           self.data = json.load(fh)
        with open('types.json', encoding='UTF-8') as fh:
           self.types = json.load(fh)
        self.emojis = emojis['emojis']
        self.query = query
        self.parsed = ''
        self.url = ''
        self.item = {}
        self. dmg = ''
        self.itemTypes = []
        self.iter = 0
        self.parseQuery()
        #self.image_search()
        self.parseItem()
        self.channel = channel
        
    def parseQuery(self):
        for i in range(len(self.query)):
            if i == len(self.query) - 1 or '\'' in self.query[i + 1]:
                self.parsed += self.query[i]
            else:
                self.parsed += self.query[i] + ' '

        
    def parseItem(self):
        tokens = []
        if str(type(self.data['compendium'])) == '<class \'dict\'>':
            for i in range(len(self.data['compendium'][self.command])):
                if self.parsed.lower() == self.data['compendium'][self.command][i][list(self.data['compendium'][self.command][i].keys())[0]].lower():
                    self.item = self.data['compendium'][self.command][i]
        else:
            for i in range(len(self.data['compendium'])):
                mydict = {}
                mydict = self.getToDict(self.data['compendium'][i])
                if self.parsed.lower() == mydict[list(mydict.keys())[0]].lower():
                    self.item = mydict
    def image_search (self):
        service = build("customsearch", "v1",
               developerKey="AIzaSyB27BaTCo7TQmdX1lGglsfRD9GBZVIUBGw")
        res = service.cse().list(
             q='d&d ' + self.parsed,
             cx='013493964073211676985:xukairzvkiy"',
             searchType='image',
             rights='cc_publicdomain cc_attribute cc_sharealike cc_noncommercial cc_nonderived',
           ).execute()
        urls = [item['link'] for item in res['items']]
        self.url = urls[0]

    def message(self):
        misc = str()
        tokens = []
        embedFields = []
        description = str()
        types = str()
        embed=discord.Embed(title='**'+ self.item[list(self.item.keys())[0]] + '**', color=0x0ee796)
        #embed.set_thumbnail(url=self.url)
        for i in range(len(self.item)):
            if list(self.item.keys())[i] == 'text':
                embedFields.append(list(self.item.keys())[i])
                for j in range(len(self.item[list(self.item.keys())[i]])):
                    if str(self.item[list(self.item.keys())[i]][j]) != 'None':
                        if self.command == 'item' and messageTokenizor(str(self.item[list(self.item.keys())[i]][j]))[0] == 'Source':
                            description += '\n :notebook_with_decorative_cover:' + self.item[list(self.item.keys())[i]][j] + '\n'
                        else:
                            if self.item[list(self.item.keys())[i]][j] != '':
                                description += ':small_orange_diamond:' + self.item[list(self.item.keys())[i]][j].replace('<i>', '*').replace('</i>', '*') + '\n'
            if list(self.item.keys())[i] == 'type':
                embedFields.append(list(self.item.keys())[i])
                embedFields.append('misc')
                tokens = messageTokenizor(self.item['type'])
                for j in range(len(tokens)):
                    if tokens[j] in list(self.types.keys()):
                        if tokens[j] != ',':
                            types += self.types[tokens[j]]
                if self.command == 'monster':
                    types = self.item['type']   
            if list(self.item.keys())[i] == 'value':
                embedFields.append(list(self.item.keys())[i])
                embedFields.append('misc')
                misc += ':moneybag:' + self.item['value'] + ', '
            if list(self.item.keys())[i] == 'weight':
                embedFields.append(list(self.item.keys())[i])
                misc += ':scales:' + self.item['weight'] + 'lb(s), '
            if i != 0 and list(self.item.keys())[i] not in embedFields:
                embedFields.append('misc')
                if i != len(self.item) - 1:
                    misc += ':small_red_triangle:' + str(self.item[list(self.item.keys())[i]]) + ', '
                else:
                    misc += ':small_red_triangle:' + str(self.item[list(self.item.keys())[i]])
            if i != 0 and list(self.item.keys())[i] not in embedFields and self.command != 'item':
                if str(type(self.item[list(self.item.keys())[i]])) == '<class \'str\'>':
                    if list(self.item.keys())[i] in list(self.emojis.keys()):
                        embed.add_field(name=self.getEmoji(list(self.item.keys())[i]) + list(self.item.keys())[i].capitalize(), value=self.item[list(self.item.keys())[i]].capitalize(), inline=True)    
                    else:
                        embed.add_field(name=list(self.item.keys())[i].capitalize(), value=self.item[list(self.item.keys())[i]].capitalize(), inline=True)
                else:
                    for j in range(len(self.item[list(self.item.keys())[i]])):
                        mydict = {}
                        mydict = self.getToDict(self.item[list(self.item.keys())[i]][j])
                        if mydict != None:
                            for k in range(0, len(list(mydict.keys())), 2):
                                dmg = str()
                                if self.command == 'monster':
                                    if k != len(list(mydict.keys())) - 1:
                                        embed.add_field(name=self.getToStr(mydict[list(mydict.keys())[k]]), value=self.getToStr(mydict[list(mydict.keys())[k + 1]]), inline=True)
                                else:
                                    embed.add_field(name=self.getToStr(mydict[list(mydict.keys())[k]]), value=self.getToStr(mydict[list(mydict.keys())[k + 1]]), inline=True)  
                        else:
                            embed.add_field(name=list(self.item.keys())[i], value=self.getToStr(self.item[list(self.item.keys())[i]]), inline=True)
        if 'type' in embedFields:
            embed.add_field(name='Types', value=types, inline=False)
        if 'misc' in embedFields and self.command == 'item': 
            embed.add_field(name='Misc.', value=misc, inline=True)
        if 'text' in embedFields:
            embed.add_field(name='Description :notepad_spiral:', value=description, inline=True)
        return embed   

    def getToStr(self, thing):
        if str(type(thing)) == '<class \'dict\'>':
            return self.getToStr(thing[list(thing.keys())[self.iter]])
            self.iter += 1
        if str(type(thing)) == '<class \'list\'>':
            return self.getToStr(thing[0])
        if str(type(thing)) == '<class \'str\'>':
            self.iter = 0
            return thing
                                       
    def getToDict(self, thing):
        if str(type(thing)) == '<class \'dict\'>':
            self.iter = 0
            return thing
        if str(type(thing)) == '<class \'list\'>':
            return thing[self.iter]
            self.iter += 1
            
    def getEmoji(self, emoji):
        for i in range(len(self.emojis)):
            if emoji == list(self.emojis.keys())[i]:
                return self.emojis[list(self.emojis.keys())[i]]
        
def messageTokenizor(message):
    tokens = nltk.word_tokenize(message)
    return tokens

def getRandomInvite():
    with open('invites.json', encoding='UTF-8') as fh:
               invites = json.load(fh)
    return invites[str(random.randrange(1, 790, 1))]

@client.event
#Console Feedback
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name=' D&D 5e'))
    for i in range(len(client.servers)):
        if list(client.servers)[i].id == '419162890503847937':
            for j in range(len(list(list(client.servers)[i].channels))):
                if list(list(client.servers)[i].channels)[j].id == '479537541847056384':
                    for k in range(len(test_messages)):
                        await client.send_message(list(list(client.servers)[i].channels)[j], content=test_messages[k])

                    
        

@client.event
#Messages channel when given certain commands
async def on_message(message):
    if message.content.startswith('&test'):
        print(message.channel.id)
        #for i in range(len(test_messages)):
            #await client.send_message(message.channel, content=test_messages[i])
    if message.content.startswith('&') and messageTokenizor(message.content)[1] in commands:
        text = messageTokenizor(message.content)
        search = Search(text[2:], text[1], message.channel)
        await client.send_message(message.channel, embed=search.message())
    if message.content.startswith('&random invite'):
        await client.send_message(message.channel, content=getRandomInvite())        
#Discord Bot Authentication data
client.run(token)
