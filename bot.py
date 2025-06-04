import json
import os
import discord
from discord.ext import commands
from dreamer import dreamer_response

# Load your Discord token from environment
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize conversation memory
conversation = []
memory = {}
# Create bot with command prefix
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Dreamer is now watching Discord as {bot.user}")

@bot.command()
async def ask(ctx, *, question):
    print(f"Received question: {question}")
    response = dreamer_response(question)

    # Save input/output to memory
    memory["last_input"] = question
    memory["last_response"] = response
    conversation.append({"role": "user", "content": question})
    conversation.append({"role": "assistant", "content": response})

    # Save conversation to file
    with open("conversation.json", "w") as f:
        json.dump(conversation, f, indent=2)

    await ctx.send(response)

bot.run(DISCORD_TOKEN)
