import discord
from discord.ext import commands
from core.race_parsing import parse_race
from selenium.webdriver.common.by import By
from core.selenium_scraping_setup import login_with_selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException
from core.state_switch import switch_abbv_to_id, switch_abbv_to_id, switch_state_to_id, switch_id_to_state_name
import json

class Queue(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="queue", aliases=["q"])
    @commands.has_any_role("Admin","Treasurer","Chair","Vice Chair")
    async def queue(self, ctx, action: str = None, profile = None, amount: int = None):
        if action == None:
            driver = login_with_selenium()
            driver.get('https://www.battleforthehill.com/parties/1/admin')

            queue =  driver.find_elements(By.XPATH, "//table[@class='w-full bg-gray-900 text-gray-300']")[0]
            print(queue.text)
            embed = discord.Embed(title="Queue", description="Fund Transfer Queue", color=discord.Color.blue())
            n = 0
            rows = queue.find_elements(By.TAG_NAME, "tr")
            for transaction in rows:
                print(transaction.text)
                if n == 0:
                    pass
                else:
                    cells = transaction.find_elements(By.TAG_NAME, "td")
                    count = str(n)
                    
                    date = cells[0].text  # Text of the first cell
                    recip = cells[1].text  # Text of the second cell
                    amt = cells[2].text  # Text of the second cell
                    sender = cells[3].text  # Text of the second cell
                    joined = f"**Date:** {date} \n **Recipient:** {recip} \n **Amount:** {amt} \n **Sender:** {sender}"
                    embed.add_field(name=f"Transaction #{count}", value=joined, inline=False)
                n += 1
        if action in ["send","fund","funds"] and profile != None and amount!= None:
            embed = discord.Embed(title="Action", description="Action added to Fund Transfer Queue", color=discord.Color.blue())
            try:
               
                driver = login_with_selenium()
                wait = WebDriverWait(driver, 10)
                driver.get('https://www.battleforthehill.com/parties/1/admin')
                funds_input = wait.until(EC.element_to_be_clickable((By.ID, 'funds')))
                funds_input.send_keys(amount)  # The amount to send
                if profile.isdigit():
                    with open('data.json') as f:
                        data = json.load(f)
                    user_name = data[profile]['name']
                else:
                    user_name = profile
                embed.add_field(name="Funds sent!", value=f"You have sent {amount} to {user_name}!", inline=False)
                # Example: Select the recipient type from the dropdown menu
                # Select the recipient type from the dropdown menu
                recipient_type_dropdown = driver.find_element(By.ID, 'type')
                recipient_type_dropdown.click()
                # Specifically select "Politician" from the dropdown options
                politician_option = driver.find_element(By.XPATH, '//option[@value="user"]')
                politician_option.click()

                # Example: Enter the name of the recipient
                recipient_name_input = driver.find_element(By.ID, 'name')
                recipient_name_input.send_keys(user_name)
                # Get the total height of the page

    
                # Submit the form
               
                element = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@class, 'bg-gray-200') and contains(@class, 'cursor-pointer') and contains(@class, 'px-3') and contains(@class, 'py-1.5') and contains(@class, 'rounded') and contains(@class, 'shadow-sm') and contains(@class, 'text-white') and contains(@class, 'bg-green-700') and contains(@class, 'hover:bg-green-600')]")))
                driver.execute_script("arguments[0].click();", element)

            except Exception as e:
                raise e
        if action in ['approve','accept','confirm','a']:
            embed = discord.Embed(title="Approval", description=f"Transaction approved", color=discord.Color.blue())
            
            try:
                driver = login_with_selenium()
                
                wait = WebDriverWait(driver, 10)
                driver.get('https://www.battleforthehill.com/parties/1/admin')
                queue =  driver.find_elements(By.XPATH, "//table[@class='w-full bg-gray-900 text-gray-300']")[0]
                rows = queue.find_elements(By.TAG_NAME, "tr")
                index = 1
                transaction_to_approve = rows[index]
                print(f'Trans to approve: {transaction_to_approve.text}')
                element = transaction_to_approve.find_element(By.CSS_SELECTOR, '.px-3.py-1\\.5.rounded-md.text-white.bg-green-700')
                print(element.text)
                element.click()
                alert = driver.switch_to.alert
                alert.accept()
                embed.add_field(name="Transaction Approved!", value=f"Transaction #{index} has been approved!", inline=False)
            except Exception as e:
                embed.add_field(name="Error", value=f"Error: {e}", inline=False)
                print(f"Error: {e}")

                

        await ctx.send(embed=embed)


  

async def setup(bot):
    await bot.add_cog(Queue(bot))