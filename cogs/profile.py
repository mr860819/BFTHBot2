import discord
from discord.ext import commands
from datetime import datetime
import json
"""import local modules"""
try:
    from core.login import login_with_csrf
    from core.scrape import scrape_profile
    from core.state_switch import switch_state_to_id
except ImportError as e:
    print(str(e))

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Initialize session and response with login_with_csrf
        
        # Load user data
        with open('data.json', 'r') as file:
            self.data = json.load(file)

    async def find_user_id(self, username):
        """Utility function to find user ID by username."""
        return next((key for key, value in self.data.items() if value['name'].lower() == username.lower()), None)

    @commands.command(name='scrape_profile', aliases=['profile', 'p', 'user'])
    async def scrape_profile_command(self, ctx, *, ids: str = None):
        response, session = login_with_csrf()
        try:
            start_time = datetime.now()
            
            if ids is None:
                disc = f"{ctx.author.name}#{ctx.author.discriminator}"
                id = next((key for key, value in self.data.items() if value['discord'] == disc), None)
            elif ids.isdigit():
                id = ids
            else:
                print(str(ids))
                id = await self.find_user_id(ids)

            if id is None:
                await ctx.send("User not found.")
                return

            try:
                url = f'https://www.battleforthehill.com/politician/{id}'
                profile_data = scrape_profile(response, session, url)
                print(str(profile_data))
                embed = discord.Embed(title=profile_data['name'], description=profile_data['position'],url=url, color=discord.Color.blue())
                embed.add_field(name='Last Online', value=profile_data['last_online'], inline=True)
                embed.add_field(name='Party', value=profile_data['party'], inline=True)
                
                embed.add_field(name='State', value=profile_data['state'], inline=True)
                embed.add_field(name='PC', value=profile_data['pc'], inline=True)
                embed.add_field(name='Funds', value=profile_data['funds'], inline=True)
                embed.set_thumbnail(url=profile_data['profile_image'])
                embed.add_field(name='Campaign Strength', value=profile_data['campaign_strength'], inline=True)
                embed.add_field(name='State Reputation', value=profile_data['state_reputation'], inline=True)
                embed.add_field(name='National Reputation', value=profile_data['national_reputation'], inline=True)
                embed.add_field(name='Social Stance', value=profile_data['social_stance'])
                embed.add_field(name='Economic Stance', value=profile_data['economic_stance'])
                embed.add_field(name='National Prestige', value=profile_data['national_prestige'])
                embed.add_field(name='Net Worth', value=profile_data['net_worth'])
                embed.add_field(name='Bond Value', value=profile_data['bond_value'])
                embed.add_field(name='Invested %', value=profile_data['invested_pct'])
                embed.add_field(name='Discord', value=profile_data['discord'])
                # Assuming `execution_time` is of interest for debugging or info purposes
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds() * 1000  # milliseconds
                embed.set_footer(text=f"Command executed in {execution_time:.2f} ms")

                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"An error occurred: {str(e)}")
                raise e
        except Exception as e:
            print(f'Error in scrape_profile_command: {str(e)}')
            raise e

async def setup(bot):
    await bot.add_cog(Profile(bot))
