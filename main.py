import discord
import emojis

#variables
#configuring client
client = discord.Client()

#shortcut for color methods
colors = discord.Color

poll_color = colors.blurple()

#helpme - bot is playing this so there is access
helpme = discord.Game("*poll.helpme/*poll.helpus")

#help embed
poll_help = discord.Embed(description='This is the help message for @Poll bot#2205.\n\n*poll(posts a poll with the given title, options, and emojis or default emojis):\n```\n*poll "{title}" "(emoji 1){option 1}" "(emoji 2){option 2}" "(emoji n){option n}"\n\nExample:\n*poll "This is a title" "👌 This is an ok hand "This will display 🇦"\n```No options require emojis and you may include emojis with any number of options, otherwise a default emoji will be provided.\n\n*poll.invite(sends an invite link): \n```\n*poll.invite\n```\n**KEY**\n```\n{}: required\n(): optional\n```\nThanks for using this bot!', color=poll_color)

#error embed
poll_error = discord.Embed(description="It seems like there was an error processing this. Please check again that you have formatted the message correctly. Sadly, this bot is dumb so unless the message is formatted correctly it will not be understood. If you need any help formatting please send ``*poll.helpme`` or ``*poll.helpus``. If there are any more issues fell free to join the support discord, which isn't actully a thing yet...sry.", color=colors.red())

#invite link embed and string
invite_link = 'https://discordapp.com/api/oauth2/authorize?client_id=579350634000678922&permissions=85056&scope=bot'

#function definitions
#def print_help():

#function to parse message from user to create post off of
def parse_poll(message):
    poll = message.content.split('"')
    poll_options = ""
    emoji = iter('🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿'.split())
    emoji_opt = []
    i = 1
    del poll[0]
    poll[0] = poll[0].strip()
    poll_title = "**:bar_chart:" + str(poll[0]) + "**"
    while i < len(poll)-1:
        del poll[i]
        poll[i] = poll[i].strip()
        if poll[i].startswith("<"):
            poll_options = poll_options + poll[i] + "\n"
            emoji_opt.append(poll[i].split(">")[0])
            emoji_opt[-1] = emoji_opt[-1] + ">"
        elif emojis.get(poll[i][0]) != set():
            poll_options = poll_options + poll[i] + "\n"
            emoji_opt.append(emojis.get(poll[i][0]).pop())
        else:
            current_emoji = next(emoji)
            poll_options = poll_options + current_emoji + ' ' + poll[i] + '\n'
            emoji_opt.append(current_emoji)
        i += 1
    poll_options = discord.Embed(description=poll_options, color=poll_color)
    poll = [poll_title, poll_options, emoji_opt]
    return poll

#readying client
@client.event
async def on_ready():
    global creator
    #grabs user id from file "creator_id.txt"
    with open("creator_id.txt") as f_obj:
        creator = client.get_user(int(f_obj.read().rstrip()))
    await client.change_presence(activity=helpme)
    print("I'm ready!")
    print(client.user)
    print(discord.version_info)
    print(discord.__version__)
    print(creator)

@client.event
async def on_message(message):
    global poll
    if message.author != client.user:
        if message.content.startswith('*poll.helpme'):
            await message.author.send(content='**poll.help**', embed=poll_help)
        elif message.content.startswith('*poll.helpus'):
            await message.channel.send(content='**poll.help**', embed=poll_help)
        elif message.content.startswith('*poll.invite'):
            await message.author.send(invite_link)
        elif message.content.startswith("*poll"):
            try:
                poll = parse_poll(message)
            except:
                poll = ['**ERROR**', discord.Embed(description=poll_error, color=colors.red()),]
                await creator.send(message)
                await creator.send(message.content)
            await message.channel.send(content=poll[0], embed=poll[1])
    if message.author == client.user and message.content.startswith('**:bar_chart:'):
        for emoji in poll[2]:
            await message.add_reaction(emoji)
            
#grabs bot token from file "bot_token.txt"
with open("bot_token.txt") as f_obj:
    token = f_obj.read().rstrip()
client.run(token)
