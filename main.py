import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from fuzzywuzzy import process

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client) #This tree contains all the commands written, not super necessary right now but scalable.

#Notification that the bot is online and running
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=246483365832687619))
    print(f'We have logged in as {client.user}')

#Makes sure the bot doesn't respond to istelf
@client.event
async def on_message(message):
    if message.author == client.user:
        return

@tree.command(name = "ammo", description = "search for an ammo type", guild=discord.Object(id=246483365832687619)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def ammo_command(ctx, search: str):
    ammo = find_ammo_type(search)
    if ammo is None:
        await ctx.send("No matching ammo found")
    else:
        response_embed = generate_embed(ammo)
        await ctx.response.send_message(embed=response_embed)

class Ammo:
    def __init__(self, name, damage, penetration, fragmentation, recoil, accuracy, eff_dist, max_hs_dist, speed, pen_array):
        self.name = name
        self.damage = damage
        self.penetration = penetration
        self.fragmentation = fragmentation
        self.recoil = recoil
        self.accuracy = accuracy
        self.eff_dist = eff_dist
        self.max_hs_dist = max_hs_dist
        self.speed = speed
        self.pen_array = pen_array

#Uses fuzzy wuzzy string comparison to find the closest match.
def find_ammo_type(search):
    confidence = process.extractOne(search, ammo_types.keys())
    if confidence[1] >= 70:
        return ammo_types[confidence[0]]
    else:
        return None

 #Dictionary containing all ammunition. Missing some elements.   
ammo_types = {
    #Shotgun shells
    '12/70 5.25mm Buckshot': Ammo('12/70 5.25mm Buckshot', '8x37', 1, 0, 0, 0, 108, 9, 330, [3, 3, 3, 3, 3, 3]),
    '12/70 8.5mm Magnum Buckshot': Ammo('12/70 8.5mm Magnum Buckshot', '8x50', 2, 0, 115, -15, 80, 116, 385, [3, 3, 3, 3, 3, 3]),
    '12/70 6.5mm Express Buckshot': Ammo('12/70 6.5mm Express Buckshot', '9x35', 3, 0, 0, 15, 71, 'Never', 430, [3, 3, 3, 3, 3, 3]),
    '12/70 7mm Buckshot': Ammo('12/70 7mm Buckshot', '8x39', 3, 0, 0, 0, 39, 3, 415, [3, 3, 3, 3, 3, 3]),
    '12/70 Piranha': Ammo('12/70 Piranha', '10x25', 24, 0, 0, -5, '-', '-', 310, [6, 6, 5, 4, 4, 4]),
    '12/70 Flechette': Ammo('12/70 Flechette', '8x25', 31, 0, 0, -10, '>1Km', 'Never', 320, [6, 6, 6, 5, 5, 5]),
    #Slugs
    '12/70 RIP': Ammo('12/70 RIP', 265, 2, 100, 35, 80, 188, '>1Km', 410, [0, 0, 0, 0, 0, 0]),
    '12/70 Superformance HP Slug': Ammo('12/70 Superformance HP Slug', 220, 5, 39, -15, 170, 344, '>1Km', 594, [0, 0, 0, 0, 0, 0]),
    '12/70 Grizzly 40 Slug': Ammo('12/70 Grizzly 40 Slug', 190, 12, 12, 20, 80, 840, '>1Km', 594, [6, 2, 0, 0, 0, 0]),
    '12/70 Copper Sabot HP Slug': Ammo('12/70 Copper Sabot HP Slug', 206, 14, 38, 10, 150, 305, '>1Km', 442, [6, 3, 1, 0, 0, 0]),
    '12/70 Lead Slug': Ammo('12/70 Lead Slug', 167, 15, 20, 0, 120, 487, '>1Km', 370, [6, 4, 1, 0, 0, 0]),
    '12/70 Dual Sabot Slug': Ammo('12/70 Dual Sabot Slug', '2x85', 17, 10, 15, 110, 251, '>1Km', 415, [6, 5, 2, 0, 0, 0]),
    '12/70 \'Poleva-3\' Slug': Ammo('12/70 \'Poleva-3\' Slug', 140, 17, 20, -15, 100, 406, '>1Km', 410, [6, 5, 1, 0, 0, 0]),
    '12/70 FTX Custom Lite Slug': Ammo('12/70 FTX Custom Lite Slug', 183, 20, 10, -25, 135, 498, '>1Km', 480, [6, 6, 2, 0, 0, 0]),
    '12/70 \'Poleva-6u\' Slug': Ammo('12/70 \'Poleva-6u\' Slug', 150, 20, 15, -10, 115, 181, '>1Km', 430, [6, 6, 2, 0, 0, 0]),
    '12/70 Makeshift .50 BMG Slug': Ammo('Makeshift .50 BMG Slug', 197, 26, 5, 25, 90, '>1Km', '>1Km', 410, [6, 6, 5, 3, 1, 0]),
    '12/70 AP-20 Armor-Piercing Slug': Ammo('12/70 AP-20 Armor-Piercing Slug', 164, 37, 3, 50, 80, 905, '>1Km', 510, [6, 6, 6, 5, 4, 3]),
    #20 Gauge
    '20/70 5.6mm Buckshot': Ammo('20/70 5.6mm Buckshot', '8x26', 1, 0, 10, -10, 124, 'Never', 340, [3, 3, 3, 3, 3, 3]),
    '20/70 6.2mm Buckshot': Ammo('20/70 6.2mm Buckshot', '8x22', 2, 0, 0, 0, 100, 'Never', 475, [3, 3, 3, 3, 3, 3]),
    '20/70 7.5mm Buckshot': Ammo('20/70 7.5mm Buckshot', '8x25', 3, 0, 0, 0, 181, 'Never', 475, [3, 3, 3, 3, 3, 3]),
    '20/70 7.3mm Buckshot': Ammo('20/70 7.3mm Buckshot', '9x23', 3, 0, 15, 0, 86, 'Never', 430, [3, 3, 3, 3, 3, 3]),
    '20/70 Devastator Slug': Ammo('20/70 Devastator Slug', 198, 5, 100, 30, 125, 109, '>1Km', 405, [1, 0, 0, 0, 0, 0]),
    '20/70 \'Poleva-3\' Slug': Ammo('20/70 \'Poleva-3\' Slug', 120, 14, 20, -15, 110, 517, '>1Km', 425, [6, 2, 0, 0, 0, 0]),
    '20/70 Star Slug': Ammo('20/70 Star Slug', 154, 16, 10, 5, 130, 416, '>1Km', 415, [6, 5, 1, 0, 0, 0]),
    '20/70 \'Poleva-6u\' Slug': Ammo('20/70 \'Poleva-6u\' Slug', 135, 17, 15, -10, 110, 438, '>1Km', 445, [6, 5, 1, 0, 0, 0]),
    #23x75mm
    '\'Zvezda\' Flashbang Round': Ammo('\'Zvezda\' Flashbang Round', 0, 0, 20, 0, 0, 0, 0, 0, [0, 0, 0, 0, 0, 0]),
    '\'Shrapnel-25\' Buckshot': Ammo('\'Shrapnel-25\' Buckshot', '8x78', 10, 0, 10, 20, 83, '>1Km', 375, [6, 4, 3, 3, 3, 3]),
    '\'Shrapnel-10\' Buckshot': Ammo('\'Shrapnel-10\' Buckshot', '8x87', 11, 0, 0, 0, 106, '>1Km', 270, [6, 4, 3, 3, 3, 3]),
    '\'Barrikada\' Slug': Ammo('\'Barrikada\' Slug', 192, 39, 20, 25, -5, 974, '>1Km', 420, [6, 6, 6, 6, 4, 4]),
    #9x18mm
    #5.49x39
    '5.45x39 BS GS': Ammo('5.45x39 BS GS', 40, 52, 17, 10, -3, 363, 179, 830, [6, 6, 6, 6, 6, 5]),
    '5.45x39 PPBS GS \'Igolnik\'': Ammo('5.45x39 PPBS GS \'Igolnik\'', 37, 62, 2, 15, 0, 430, 85, 905, [6, 6, 6, 6, 6, 6])
}

#Generates the embed
def generate_embed(ammo: Ammo):
    embed = discord.Embed(title=ammo.name,
                          description =
                          '**Damage:**                  ' + f'{ammo.damage}' +
                          '\n**Penetration:**           ' + f'{ammo.penetration}' +
                          '\n**Fragmentation:**         ' + f'{ammo.fragmentation}' + '%' +
                          '\n**Recoil:**                ' + f'{ammo.recoil}' +
                          '\n**Accuracy:**              ' + f'{ammo.accuracy}' + '%' +
                          '\n**Effective Distance:**    ' + f'{ammo.eff_dist}' +
                          '\n**Max Headshot Distance:** ' + f'{ammo.max_hs_dist}' +
                          '\n**Speed:**                 ' + f'{ammo.speed}' + 'm/s' +
                          '\n**Pen Chart:**             ' + f'{ammo.pen_array}', color=0xff0000)
    return embed

TOKEN = os.getenv('TOKEN')
client.run(TOKEN)