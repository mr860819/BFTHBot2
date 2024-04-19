import discord
from discord.ext import commands
import discord
from discord.ext import commands
from core.login import login_with_csrf
from core.scrape import scrape_state_positions
from core.scrape import fetch_page
from core.selenium_scraping_setup import login_with_selenium
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from shutil import which
from core.state_switch import switch_state_to_id
import json

class Positions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('data.json', 'r') as file:
            self.data = json.load(file)

    @commands.command(name='positions', help='Returns the Social and Economic Position of a given state', aliases=['pos'])
    async def scrape_state_positions(self, ctx, *, state_var: str = None):
        if state_var is None:
            disc = f"{ctx.author.name}#{ctx.author.discriminator}"
            id = next((key for key, value in self.data.items() if value['discord'] == disc), None)
            state_id = self.data[id]['state']
        elif state_var.isdigit() == False:
            try:
                state_id = switch_state_to_id(state_var)
            except Exception as e:
                await ctx.send(f"Error: {e}")
        else:
            state_id = state_var
        
        original_message = await ctx.send(f"Scraping positions for state ID {state_id}...")
        driver = login_with_selenium()
        driver.get(f'https://www.battleforthehill.com/states/{state_id}')
        time.sleep(2)  # Adjust as necessary

        # Scrape Social and Economic Stances
        try:
            state_name = driver.find_element(By.XPATH, '/html/body/div/main/div/div/div[1]/div/div[2]/p').text
            social_stance = driver.find_element(By.XPATH, '/html/body/div/main/div/div/div[4]/div[2]/div/div/form[2]/div/div[14]').text
            economic_stance = driver.find_element(By.XPATH, '/html/body/div/main/div/div/div[4]/div[2]/div/div/form[2]/div/div[14]').text
            await original_message.edit(content=f'***{state_name}*** \n Social Stance: {social_stance} \n Economic Stance: {economic_stance}')
        except Exception as e:
            print(f'Error scraping state ID {state_id}: {e}')
  

async def setup(bot):
    await bot.add_cog(Positions(bot))