import discord
import traceback
import asyncio
import os
from .embed import banner_honeypot
from .config import config

async def honeypot_creator(client: discord.Client, loop: bool = False) -> None:
    try:
        channel = await client.fetch_channel(config['Applications ID'])
        if not isinstance(channel, discord.TextChannel):
            print("Error: The configured channel is not a text channel.")
            os._exit(0)
        
        first_iteration = True

        while loop or first_iteration:
            first_iteration = False

            try:
                messages = [
                    msg async for msg in channel.history(limit=10, oldest_first=True)
                    if msg.author.id == client.user.id
                ]

                if len(messages) == 0:
                    await channel.send(embed=banner_honeypot())
                else:
                    if len(messages) >= 1:
                        await messages[0].edit(embed=banner_honeypot())
                    else:
                        await channel.purge(limit=10)
                        await honeypot_creator(client, loop=False)

            except:
                print(f"Error:\n{traceback.format_exc()}")

            if loop:
                await asyncio.sleep(24 * 60 * 60)

    except:
        print("Error when accessing the channel or trying to send messages.")
