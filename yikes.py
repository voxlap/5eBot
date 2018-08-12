import discord
import nltk
import time
import json


client = discord.Client()
with open('discordToken.txt', 'r+') as myfile:
    token = str(myfile.read())

class Search(object):
    def __init__(self, query, command):
        self.command = command
        with open(self.command + '.json', encoding='UTF-8') as fh:
           self.data = json.load(fh)
        with open(self.command + '_types.json', encoding='UTF-8') as fh:
           self.types = json.load(fh)
        self.query = query
        self.parsed = ''
        self.item = {}
        self.itemTypes = []
        self.parseQuery()
        self.parseItem()
        #print(self.item)
        print(self.types)
    def parseQuery(self):
        for i in range(len(self.query)):
            if i == len(self.query) - 1:
                self.parsed += self.query[i]
            else:
                self.parsed += self.query[i] + ' '
        
    def parseItem(self):
        tokens = []
        for i in range(len(self.data['compendium'][self.command])):
            '''
            for j in range(len(self.data['compendium'][self.command][i])):
                if list(self.data['compendium'][self.command][i].keys())[j] == 'type':
                    tokens = messageTokenizor(self.data['compendium'][self.command][i]['type'])
                    for k in range(len(tokens)):
                        if tokens[k] not in self.itemTypes:
                            self.itemTypes.append(tokens[k])
            #print(self.data['compendium'][command][i][list(self.data['compendium'][command][i].keys())[0]])
                            '''
            if self.parsed.lower() == self.data['compendium'][self.command][i][list(self.data['compendium'][self.command][i].keys())[0]].lower():
                self.item = self.data['compendium'][self.command][i]

    def message(self):
        tokens = []
        embed=discord.Embed(title='**'+ self.item[list(self.item.keys())[0]] + '**', color=0x0ee796)
        for i in range(len(self.item)):
            if list(self.item.keys())[i] == 'text':
                description = str()
                for j in range(len(self.item[list(self.item.keys())[i]])):
                    if str(self.item[list(self.item.keys())[i]][j]) != 'None':
                        description += ':small_orange_diamond:' + self.item[list(self.item.keys())[i]][j] + '\n'
                embed.add_field(name='Description', value=description, inline=True)
            if list(self.item.keys())[i] == 'type':
                types = str()
                tokens = messageTokenizor(self.data['compendium'][self.command][i]['type'])
                for j in range(len(tokens)):
                    if token[j] in list(self.types.keys()):
                        types += self.types[token[j]]
                print('######HERE########')
                print(types)
                print('######HERE########')
                embed.add_field(name='Types', value=types, inline=False)
            if i != 0 and list(self.item.keys())[i] != 'text' and list(self.item.keys())[i] != 'type':
                embed.add_field(name=list(self.item.keys())[i], value=':crossed_swords:' + str(self.item[list(self.item.keys())[i]]), inline=True)
        return embed   

def messageTokenizor(message):
    tokens = nltk.word_tokenize(message)
    return tokens

@client.event
#Console Feedback
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name=' around, ig'))
    
@client.event
#Messages channel when given certain commands
async def on_message(message):
    if message.content.startswith('!item'):
        text = messageTokenizor(message.content)
        search = Search(text[2:], text[1])
        await client.send_message(message.channel, embed=search.message())
#Discord Bot Authentication data
client.run(token)
