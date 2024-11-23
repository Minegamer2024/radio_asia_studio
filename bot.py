import discord
from discord.ext import commands
import asyncio
import json
from art import text2art
from dotenv import load_dotenv
import os
load_dotenv()
token = os.getenv("TOKEN")
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)
@client.event
async def on_ready():
    art_ready = text2art("Asia studio")
    print(art_ready)
    print(f"ready {client.user}")
    await client.tree.sync()
@client.tree.command(name="radio",description="لأذاعة القرأن في روم صوتي")
async def join(interaction: discord.Interaction, channel: discord.VoiceChannel):
    try:
        if len(channel.members) != 0:
            with open("Quran.json", "r", encoding="utf-8") as Quran_radio:
                data = json.load(Quran_radio)
            option = [discord.SelectOption(label=i,value=i) for i in data.keys()]
            select = discord.ui.Select(placeholder="اختر الشيخ الذي تريد ان تسمعه", options=option)
            async def select_callback(interaction: discord.Interaction):
                if len(channel.members) != 0:
                    voice_client = discord.utils.get(client.voice_clients, guild=interaction.guild)
                    if voice_client is not None:
                        if  voice_client.channel != channel:
                            await voice_client.disconnect()
                    voice = await channel.connect()
                    await interaction.response.edit_message(content=f"تم بدء البث في روم {channel.mention}", view=None)
                    voice.play(discord.FFmpegPCMAudio(data[select.values[0]]))
                    for vc in client.voice_clients:
                        while True:
                            await asyncio.sleep(10)
                            if vc.channel == channel:
                                if len(channel.members) == 1:
                                    await voice.disconnect()
                                    break
                else:
                    await interaction.response.edit_message(content="اسف لكن لا يمكنني دخول روم بدون اي اعضاء", view=None)
            select.callback = select_callback
            view = discord.ui.View()
            view.add_item(select)
            if client.user not in channel.members:
                await interaction.response.send_message("يرجى اختيار الشيخ الذي سوف تسمع منه", view=view, ephemeral=True)
            else:
                await interaction.response.send_message("انا بالفعل موجود في هذه الروم", ephemeral=True)
        else:
            await interaction.response.send_message("يجب ان يكون في الروم اعضاء كي اتمكن من دخوله", ephemeral=True)
    except:
        await interaction.response.send_message("اسف لكن يوجد خطأ غريب لا يمكنني دخول الروم", ephemeral=True)  
client.run(token)