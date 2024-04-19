import time
from bs4 import BeautifulSoup
import discord
##
def fetch_page(response, session, url):
    """
    Fetches a web page using the provided session and URL.
    Returns the page content or None if an error occurs.
    """

    page = session.get(url, cookies=response.cookies, allow_redirects=False)
    print(f"Fetched page: {url}")
    return page

def scrape(response, session, url):
    """
    Scrapes a web page using the provided session and URL.
    Returns the parsed HTML content.
    """
    page = fetch_page(response, session, url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def scrape_state_positions(response, session, state_id):
    """
    Scrape a state profile from the specified URL.
    Retrieves: name, state_image, state_gdp, state_population, state_tax_rate, state_unemployment_rate, state_crime
    """
    url_constructor = f'https://battleforthehill.com/states/{state_id}'
    soup = scrape(response, session, url_constructor)
    social = soup.find('td', text='Social Stance:').find_next_sibling('td').text if soup.find('td', text='Social Stance:') else 'Not found'
    economic = soup.find('td', text='Economic Stance:').find_next_sibling('td').text if soup.find('td', text='Economic Stance:') else 'Not found'
    #state_name_element = soup.find('div', class_='text-center bg-gray-900 p-1 gap-1 uppercase font-bold').text
    embed = discord.Embed(title="placeholder", description=f'Social Stance: {social}\nEconomic Stance: {economic}', url=url_constructor, color=discord.Color.blue())
    print(soup.text)
    return embed

def scrape_profile(response, session, url):
    """
    Scrape a user profile from the specified URL.
    Retrieves: name, position, party, profile_image, campaign_strength, 
    state_reputation, national_reputation, social_stance, economic_stance,
    national_prestige, funds, pc, state, discord, last_online
    """

    soup = scrape(response, session, url)
    print(soup.text)

    # This is a simplified example. You'll need to adjust selectors based on the actual page structure.
    name = soup.find('p', class_='antialiased text-3xl font-semibold text-gray-500 px-2 pt-1 pb-0').get_text(strip=True)
    position = soup.find('p', class_="antialiased text-md italic text-gray-300 px-2 pb-1 pt-0").text if soup.find('p', class_="antialiased text-md italic text-gray-300 px-2 pb-1 pt-0") else '---'
    state_value = soup.find('td', text='State:').find_next_sibling('td').text if soup.find('td', text='State:') else 'Not found'
    campaign_value_td = soup.find('td', text='Campaign Strength:').find_next_sibling('td').text
    last_online_value = soup.find('td', text='Last Active:').find_next_sibling('td').text
    party_value_td = soup.find('td', text='Party:').find_next_sibling('td').text
    state_rep_value_td = soup.find('td', text='State Reputation:').find_next_sibling('td').text
    nat_rep_value_td = soup.find('td', text='National Reputation:').find_next_sibling('td').text
    pc_value_td = soup.find('td', text='Political Capital:').find_next_sibling('td').text
    funds_value_td = soup.find('td', text='Total Campaign Funds:').find_next_sibling('td').text
    social_stance_value = soup.find('td', text='Social Stance:').find_next_sibling('td').text if soup.find('td', text='Social Stance:') else 'Not found'
    discord_value = soup.find('td', text='Discord Username:').find_next_sibling('td').text if soup.find('td', text='Discord Username:') else 'Not found'
    national_prestige_value = soup.find('td', text='National Prestige:').find_next_sibling('td').text if soup.find('td', text='National Prestige:') else 'Not found'
    economic_stance_value = soup.find('td', text='Economic Stance:').find_next_sibling('td').text if soup.find('td', text='Economic Stance:') else 'Not found'
    profile_image = soup.find('img', class_='mr-2 inline-block w-24 h-24 sm:w-48 sm:h-48 rounded')['src']
    net_worth = soup.find('td', text='Total Net Worth').find_next_sibling('td').text if soup.find('td', text='Total Net Worth') else 'Not found'
    bond_value = soup.find('td', text='Bonds:').find_next_sibling('td').text if soup.find('td', text='Bonds:') else 'Not found'
    invested_pct = f"{int(bond_value.replace(',', '').replace('$','')) / int(net_worth.replace(',', '').replace('$','')) * 100:.2f}%"

    return {
        'name': name,
        'position': position,
        'party': party_value_td,
        'profile_image': profile_image,
        'campaign_strength': campaign_value_td,
        'state_reputation': state_rep_value_td,
        'national_reputation': nat_rep_value_td,
        'social_stance': social_stance_value,
        'economic_stance': economic_stance_value,
        'national_prestige': national_prestige_value,
        'funds': funds_value_td,
        'pc': pc_value_td,
        'state': state_value,
        'discord': discord_value,
        'last_online': last_online_value,
        'net_worth': net_worth,
        'bond_value': bond_value,
        'invested_pct': invested_pct
    }
    
