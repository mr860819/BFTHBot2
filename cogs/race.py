import discord
from discord.ext import commands
from core.race_parsing import parse_race
from selenium.webdriver.common.by import By


from core.state_switch import switch_abbv_to_id, switch_abbv_to_id, switch_state_to_id, switch_id_to_state_name

class Race(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_path = "race_screenshot.png"

    @commands.command(name="race", aliases=["r"])
    async def race(self, ctx, state, race):
        if state.isdigit():
            state_var = state
        elif len(state) > 2:
            """State name"""""
            state_var = switch_state_to_id(state)
            print(state_var)
        else:
            """State abbv"""
            state_var = switch_abbv_to_id(state)
        
        state_name = switch_id_to_state_name(state_var)
        race_table, poll_close = parse_race(state_var, race)
        embed = discord.Embed(title=f"{state_name}, {race}", description=f"Polls Close(d):{poll_close.text}", color=discord.Color.blue())

          
        for row in race_table.find_elements(By.TAG_NAME, "tr"):
            # Find all 'td' elements within the row
            cells = row.find_elements(By.TAG_NAME, "td")
            
            # Ensure there are enough cells to avoid IndexError
            if len(cells) > 1:
                name = cells[0].text  # Text of the first cell
                value = cells[2].text  # Text of the second cell
                
                value2 = cells[1].text  # Text of the second cell
                joined = f"**Polling** \n{value}% \n **Stats** \n {value2}"
                embed.add_field(name=name, value=joined, inline=True)
            else:
                # Handle cases where there are not enough cells
                continue

        await ctx.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(Race(bot))