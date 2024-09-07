import discord
from discord.ext import commands
import os

from constants import SUGGEST_CHANNEL_ID, VOTE_CHANNEL_ID, READY_CHANNEL_ID, DONE_CHANNEL_ID

# Define channel names as variables
CHANNELS = {
    'suggest': SUGGEST_CHANNEL_ID,
    'vote': VOTE_CHANNEL_ID,
    'ready': READY_CHANNEL_ID,
    'done': DONE_CHANNEL_ID
}

# Intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True  # Enable reaction intents
intents.guilds = True  # Ensures the bot can fetch guilds and channels correctly
intents.members = True  # Required for counting members for reactions

# Bot setup
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    # Print all channels to verify access
    for guild in bot.guilds:
        for channel in guild.channels:
            print(f"Available channel: {channel.name} (ID: {channel.id}, Type: {channel.type})")


async def find_existing_song(song_name: str, youtube_url: str):
    """Checks if the song already exists in the vote, ready, or done channels."""
    for channel_id in [CHANNELS['vote'], CHANNELS['ready'], CHANNELS['done']]:
        try:
            # Use fetch_channel to get the latest channel object directly from Discord
            channel = await bot.fetch_channel(channel_id)
            print(f"Attempting to find channel: {channel_id} -> {channel}")  # Log channel information
        except discord.errors.NotFound:
            print(f"Error: Couldn't find the channel with ID {channel_id}. Make sure the bot has access.")
            continue
        except discord.errors.Forbidden:
            print(f"Error: Bot does not have permission to access the channel with ID {channel_id}.")
            continue

        # Proceed only if the channel exists
        async for message in channel.history(limit=100):  # Adjust the limit as needed
            if song_name.lower() in message.content.lower() or youtube_url in message.content:
                return message.jump_url
    return None


@bot.command(name='submit')
async def submit(ctx, youtube_url: str, *, song_name: str):
    """Handles the !submit command and sends the message to the 'vote' channel."""
    # Ensure the command is used in the 'suggest' channel
    if ctx.channel.id != int(CHANNELS['suggest']):
        await ctx.send("This command can only be used in the 'suggest' channel.")
        return

    # Check if the song already exists in any of the channels
    existing_song_url = await find_existing_song(song_name, youtube_url)
    if existing_song_url:
        await ctx.send(f"The song already exists in another channel: {existing_song_url}")
        return

    # Fetch the vote channel by ID
    try:
        vote_channel = await bot.fetch_channel(int(CHANNELS['vote']))
    except discord.errors.NotFound:
        await ctx.send("Couldn't find the vote channel. Please contact an admin.")
        return

    # Format the message to be sent
    message = f"**New Song Submission:**\n**Song Name:** {song_name}\n**YouTube URL:** {youtube_url}"
    sent_message = await vote_channel.send(message)  # Send the message to vote channel
    await ctx.send("Your song has been submitted for voting!")

    # Add a thumbs-up reaction to the message automatically
    await sent_message.add_reaction('👍')


@bot.event
async def on_raw_reaction_add(payload):
    """Handles reactions added to messages in the vote and ready channels."""

    # Handle thumbs-up reactions in the vote channel
    if payload.channel_id == int(CHANNELS['vote']) and str(payload.emoji) == '👍':
        try:
            channel = await bot.fetch_channel(payload.channel_id)
            print(f"Handling reaction in vote channel: {payload.channel_id} -> {channel}")  # Log channel info
        except discord.errors.NotFound:
            print(f"Error: Couldn't find the channel with ID {payload.channel_id}.")
            return
        message = await channel.fetch_message(payload.message_id)

        # Check if all users have reacted with thumbs-up
        reactions = [reaction for reaction in message.reactions if str(reaction.emoji) == '👍']
        if reactions and reactions[0].count >= len(message.guild.members):  # Exclude the bot itself
            # Move message to the ready channel
            ready_channel = await bot.fetch_channel(int(CHANNELS['ready']))
            if ready_channel:
                # Format and send the message to the ready channel
                formatted_message = f"**Song Approved**\n**Song Name:** {message.content.split('**Song Name:**')[1].strip()}"
                ready_message = await ready_channel.send(formatted_message)

                # Add a "done" reaction to the message automatically
                await ready_message.add_reaction('✅')

                # Delete the original message from the vote channel
                await message.delete()
            else:
                print("Couldn't find the ready channel.")

    # Handle "done" reactions in the ready channel
    elif payload.channel_id == int(CHANNELS['ready']) and str(payload.emoji) == '✅':
        try:
            channel = await bot.fetch_channel(payload.channel_id)
            print(f"Handling reaction in ready channel: {payload.channel_id} -> {channel}")  # Log channel info
        except discord.errors.NotFound:
            print(f"Error: Couldn't find the channel with ID {payload.channel_id}.")
            return
        message = await channel.fetch_message(payload.message_id)

        # Check if all users have reacted with "done" (✅)
        reactions = [reaction for reaction in message.reactions if str(reaction.emoji) == '✅']
        if reactions and reactions[0].count >= len(message.guild.members):
            # Move message to the done channel
            done_channel = await bot.fetch_channel(int(CHANNELS['done']))
            if done_channel:
                formatted_message = f"**Song Ready to Play**\n**Song Name:** {message.content.split('**Song Name:**')[1].strip()}"

                # Send the message to the done channel
                await done_channel.send(formatted_message)

                # Delete the original message from the ready channel
                await message.delete()
            else:
                print("Couldn't find the done channel.")


@bot.event
async def on_command_error(ctx, error):
    """Handles errors for commands."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Use `!help` to see the list of available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required arguments. Use `!help` to see the correct usage.")
    else:
        await ctx.send(f"An error occurred: {error}")


# Run the bot with the token
if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
