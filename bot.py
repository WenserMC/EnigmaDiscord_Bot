import discord
import asyncio
from discord.ext import commands
from config import BOT_TOKEN
from Banners.ServerInfo.creator import server_creator
from Banners.Applications.creator import applications_creator
from Banners.DiscordFriends.creator import friends_creator
from Banners.Honeypot.creator import honeypot_creator
from Banners.MemberInfo.creator import members_creator
from Commands.Restart.restart import Restart
from Commands.Send.send import SendCommand
from Commands.Clear.clear import ClearCommand
from Functions.OnMemberJoin import on_member_join
from Functions.OnMemberRemove import on_member_remove
from Functions.Honeypot import honeypot
from Functions.Translate import chinese, english, spanish

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

initial_status = discord.Activity(
    type=discord.ActivityType.playing,
    name="Managing Enigma"
)

@bot.event
async def on_ready():
    print("Bot loaded")

    # Cargar embeds
    tasks = [
        ("Embed ServerInfo", server_creator, {"loop": True}),
        ("Embed Applications", applications_creator, {"loop": True}),
        ("Embed Friends", friends_creator, {}),
        ("Embed Honeypot", honeypot_creator, {"loop": True}),
        ("Embed MemberInfo", members_creator, {}),
    ]
    for name, task, kwargs in tasks:
        try:
            asyncio.create_task(task(bot, **kwargs))
        except Exception as e:
            print(f"       ✖︎ Error en {name}: {e}")
    
    # Cargar funciones
    functions = [
        ("Function Honeypot", honeypot.Honeypot(bot)),
        ("Function On_Member_Join", on_member_join.OnMemberJoin(bot)),
        ("Function On_Member_Remove", on_member_remove.OnMemberRemove(bot)),
        ("Function Translate_To_Spanish", spanish.translate_to_spanish(bot)),
        ("Function Translate_To_English", english.translate_to_english(bot)),
        ("Function Translate_To_Chinese", chinese.translate_to_chinese(bot)),
    ]
    for name, func in functions:
        try:
            await bot.add_cog(func)
        except Exception as e:
            print(f"       ✖︎ Error en {name}: {e}")

    # Cargar comandos
    print("   ➡︎ Loading Modules")
    await load_commands()

    try:
        await bot.tree.sync()
    except Exception as e:
        print(f"     ✖︎ Error al sincronizar comandos de barra: {e}")

    await bot.change_presence(
        activity=initial_status,
        status=discord.Status.online
    )

    # Mostrar todos los mensajes al final
    print("       ✔ Embeds cargados correctamente")
    print("       ✔ Funciones cargadas correctamente")
    print("       ✔ Comandos cargados correctamente")

async def load_commands():
    commands_to_load = [
        ("Command Restart", "Commands.Restart.restart"),
        ("Command Send", "Commands.Send.send"),
        ("Command Clear", "Commands.Clear.clear"),
    ]
    for name, path in commands_to_load:
        try:
            await bot.load_extension(path)
        except Exception as e:
            print(f"      ✖︎ Error en {name}: {e}")
    
    print("       ✔ Comandos cargados correctamente")

async def main():
    async with bot:
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"      ✖︎ Error al ejecutar el bot: {e}")
