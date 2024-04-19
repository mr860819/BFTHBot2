import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import discord
from discord.ext import commands
import json
import os


"""import local modules"""
try:
    from core.login import login_with_csrf
    from core.scrape import scrape_profile
except ImportError as e:
    print(str(e))

class UpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        intents = discord.Intents.default()

    @commands.command(name='updateusers', help='Scrapes all users from the battle for the hill website', aliases=['update'])
    async def update_users(self, ctx, x, y):
        if y > x:
            await ctx.send("The first argument must be less than the second argument.")
        else:
            pass
        await ctx.send(f"Updating users... with a worker pool of  workers. This may take a while.")
        response, session = login_with_csrf()
        executor = ThreadPoolExecutor(max_workers=10)
        loop = asyncio.get_event_loop()
        start_time = datetime.now()
        for user_id in range(int(x), int(y)):  # Assuming user IDs are numeric and sequential
            profile_url = f'https://www.battleforthehill.com/politician/{user_id}'

            # Wrap scrape_profile call to pass it without executing
            def scrape_with_args():
                return scrape_profile(response, session, profile_url)

            try:
                profile_data = await loop.run_in_executor(executor, scrape_with_args)

                discord_user = profile_data.get('discord', 'N/A')

                # Check if the JSON file exists
                if not os.path.exists('data.json'):
                    data = {}  # Create an empty dictionary if the file doesn't exist
                else:
                    with open('data.json', 'r') as file:
                        data = json.load(file)  # Load the existing data

                # Update the dictionary with the new data
                data[user_id] = {
                    'discord': discord_user,
                    'name': profile_data['name'],
                    'party': profile_data['party'].strip().replace("\u00a0", " "),
                    'funds': int(profile_data['funds'].replace("$", "").replace(",", "")),
                    'net_worth': int(profile_data['net_worth'].replace("$", "").replace(",", "")),
                    'national_prestige': float(profile_data['national_prestige'].replace(',', '')),
                    'state': profile_data['state'],
                }

                # Save the updated data back to the JSON file
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)

                # Update the loading bar
                embed = discord.Embed(title="Bot DB User Update", description=f"User ID {user_id} has been updated", color=discord.Color.green())
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"An error occurred with user ID {user_id}: {str(e)}")
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000  # Convert to milliseconds
        minutes, seconds = divmod(int(execution_time / 1000), 60)
        embed = discord.Embed(title="Update Users", description="All users have been updated", color=discord.Color.green())
        embed.add_field(name="Execution Time", value=f"{minutes} minutes, {seconds} seconds", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UpdateCog(bot))
