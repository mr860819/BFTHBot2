import discord
from discord.ext import commands
from datetime import datetime

from core.loadcarkeys import load_car_keys  # Assuming this is a custom module for loading bot tokens

prof_data = load_car_keys()

# Create a subclass of AutoShardedBot from discord.ext.commands module
class BFTHBot(commands.AutoShardedBot):
    def __init__(self, token):
        # Create an instance of discord.Intents to control which events the bot can receive
        intents = discord.Intents.default()
        intents.members = True  # Enable the GUILD_MEMBERS intent for member-related events
        intents.presences = True  # Optionally, enable the GUILD_PRESENCES intent for presence-related events
        intents.guilds = True  # Enable guild-related events; usually enabled by default
        intents.message_content = True  # Enable the MESSAGE_CONTENT intent for events like on_message
        intents.guild_messages = True  # Enable message-related events; usually enabled by default
        
        # Initialize the AutoShardedBot with the specified command prefix and intents
        super().__init__(command_prefix='!', intents=intents)
        self.token = token
       
        self.start_time = datetime.now()
        self.log_channel_id = 1224911777339543582
        self.coglist = ['cogs.profile','cogs.update','cogs.positions','cogs.race', 'cogs.queue']

    async def setup_hook(self):
        """Setup hook that runs after the bot is ready."""
        # Load each extension (cog) listed in self.coglist
        for extension in self.coglist:
            try:
                await self.load_extension(extension)
                print(f'Loaded extension {extension}')
            except Exception as e:
                print(f'Failed to load extension {extension}: {e}')
                raise e

    async def on_ready(self):
        # Called when the bot has successfully logged in and is ready to start receiving events
        print(f'Logged in as {self.user.name}')
        await self.change_presence(activity=discord.Game(name="!help for commands"))
        log_channel = self.get_channel(self.log_channel_id)
        if log_channel:
            log_embed = discord.Embed(title="Bot Started", description=f"Bot started at {self.start_time}", color=0x00ff00)
            await log_channel.send(embed=log_embed)

    async def on_command(self, ctx):
        # Called whenever a command is executed
        log_channel = self.get_channel(self.log_channel_id)
        if log_channel:
            log_message = f'Command executed: {ctx.command} by {ctx.author} in {ctx.channel}'
            log_embed = discord.Embed(title="Command Executed", description=log_message, color=0x00ff00)
            log_embed.set_footer(text=f"Command executed at {datetime.now()}")
            await log_channel.send(embed=log_embed)

    async def on_message(self, message):
        # Called whenever a message is received
        if message.author == self.user:
            return  # Ignore messages sent by the bot itself
        
        # Add your message processing logic here
        # Process the message
        
        await self.process_commands(message)

# Instantiate the bot with the token loaded from the custom module
bot = BFTHBot(token=prof_data['token'])

# Run the bot
try:
    bot.run(token=prof_data['token'])
except Exception as e:
    print(f"An error occurred while running the bot: {e}")
