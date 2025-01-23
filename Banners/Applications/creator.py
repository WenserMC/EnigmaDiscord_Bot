import discord
import traceback
import asyncio
import os
from .embed import banner_grinder, banner_cmp, banner_builder, banner_faq
from .config import config

async def applications_creator(client: discord.Client, loop: bool = False) -> None:
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
                    await channel.send(embed=banner_grinder())
                    await channel.send(embed=banner_cmp())
                    await channel.send(embed=banner_builder())
                    await channel.send(embed=banner_faq())
                else:
                    if len(messages) >= 4:
                        await messages[0].edit(embed=banner_grinder())
                        await messages[1].edit(embed=banner_cmp())
                        await messages[2].edit(embed=banner_builder())
                        await messages[3].edit(embed=banner_faq())
                    else:
                        await channel.purge(limit=10)
                        await applications_creator(client, loop=False)

            except:
                print(f"Error:\n{traceback.format_exc()}")

            if loop:
                await asyncio.sleep(24 * 60 * 60)

    except:
        print("Error when accessing the channel or trying to send messages.")
