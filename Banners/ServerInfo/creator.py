import discord
import traceback
import asyncio
import os
from .embed import banner_server_info, banner_host_information, banner_enigma_map
from .config import config

async def server_creator(client: discord.Client, loop: bool = False) -> None:
    try:
        channel = await client.fetch_channel(config['Serverinfo ID'])
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
                    await channel.send(embed=banner_server_info())
                    await channel.send(embed=banner_host_information())
                    await channel.send(embed=banner_enigma_map())
                    await channel.send(f'**Invitation Link:**\n {config["Discord Invite"]}')
                else:
                    if len(messages) >= 4:
                        await messages[0].edit(embed=banner_server_info())
                        await messages[1].edit(embed=banner_host_information())
                        await messages[2].edit(embed=banner_enigma_map())
                        await messages[3].edit(content=f'**Invitation Link:**\n {config["Discord Invite"]}')
                    else:
                        await channel.purge(limit=10)
                        await server_creator(client, loop=False)

            except:
                print(f"Error:\n{traceback.format_exc()}")

            if loop:
                await asyncio.sleep(24 * 60 * 60)

    except:
        print("Error when accessing the channel or trying to send messages.")
