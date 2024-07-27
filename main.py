from discord.utils import MISSING
import config
import discord
from discord.ext import commands
import traceback
import asyncio

intents = discord.Intents.all()
bot=commands.Bot(intents=intents, command_prefix="!")

class NewTaskButton(discord.ui.View):
    def __init__(self):
        super().__init__()
    @discord.ui.button(label="New Task", style=discord.ButtonStyle.grey)
    async def button_1_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        button, interaction = interaction, button
        for role in interaction.user.roles:
            if role.id in config.roles.ALLOWED_CREATE:
                edit_modal = CreateModal()
                await interaction.response.send_modal(edit_modal)
                return None
        await interaction.response.send_message('You don\'t have permissions to do that!', ephemeral=True, delete_after=1)

class TaskButton(discord.ui.View):
    def __init__(self):
        super().__init__()
    @discord.ui.button(emoji="✅", label="", style=discord.ButtonStyle.green)
    async def button_1_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        button, interaction = interaction, button
        for role in interaction.user.roles:
            if role.id in config.roles.ALLOWED_COMPLETE_PROGRESS:
                embed = interaction.message.embeds[0] if interaction.message.embeds else None
                new_embed = discord.Embed(title=embed.title, description=embed.description, color=config.COMPLETED_COLOR)
                await interaction.message.edit(content=interaction.message.content, embed=new_embed)
                self.remove_item(button)
                await interaction.response.send_message('Task Completed!', ephemeral=True, delete_after=1)
                return None
        await interaction.response.send_message('You don\'t have permissions to do that!', ephemeral=True, delete_after=1)

    @discord.ui.button(emoji="☑️", label="", style=discord.ButtonStyle.grey)
    async def button_2_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        button, interaction = interaction, button
        for role in interaction.user.roles:
            if role.id in config.roles.ALLOWED_COMPLETE_PROGRESS:
                embed = interaction.message.embeds[0] if interaction.message.embeds else None
                new_embed = discord.Embed(title=embed.title, description=embed.description, color=config.PROGRESSING_COLOR)
                await interaction.message.edit(content=interaction.message.content, embed=new_embed)
                self.remove_item(button)
                await interaction.response.send_message('Task now in Progress!', ephemeral=True, delete_after=1)
                return None
        await interaction.response.send_message('You don\'t have permissions to do that!', ephemeral=True, delete_after=1)
    
    @discord.ui.button(emoji="✏️", label="", style=discord.ButtonStyle.blurple)
    async def button_3_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        button, interaction = interaction, button
        for role in interaction.user.roles:
            if role.id in config.roles.ALLOWED_EDIT:
                embed = interaction.message.embeds[0] if interaction.message.embeds else None
                await interaction.response.send_modal(EditorModal(interaction.message, embed.title, embed.description))
                return None
        await interaction.response.send_message('You don\'t have permissions to do that!', ephemeral=True, delete_after=1)

    @discord.ui.button(emoji="🗑️", label="", style=discord.ButtonStyle.red)
    async def button_4_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        button, interaction = interaction, button
        for role in interaction.user.roles:
            if role.id in config.roles.ALLOWED_DELETE:
                await interaction.message.delete()
                await interaction.response.send_message('Task removed!', ephemeral=True, delete_after=1)
                return None
        await interaction.response.send_message('You don\'t have permissions to do that!', ephemeral=True, delete_after=1)

class EditorModal(discord.ui.Modal):
    def __init__(self, msg: discord.Message, title, desc):
        self.msg = msg
        super().__init__(title="Task editor")

        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.short,
            label="Title",
            required=True,
            default=title
        ))

        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Description",
            required=True,
            default=desc,
            max_length=200
        ))

    async def on_submit(self, interaction: discord.Interaction) -> None:
        try:
            embed = discord.Embed(title=self.children[0].value, description=self.children[1].value, color=discord.Colour.blue())
            await self.msg.edit(embed=embed)
            await interaction.response.send_message('Task Edited!', ephemeral=True, delete_after=1)
        except:
            print(f'err: {traceback.format_exc()}')

    async def on_error(self, interaction: discord.Interaction, error) -> None:
        ...
    
    async def on_timeout(self, interaction: discord.Interaction) -> None:
        ...

class CreateModal(discord.ui.Modal, title="New Task"):
    task_title = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Title",
        required=True,
    )

    task_desc = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Description",
        required=False,
        max_length=200
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        try:
            channel = bot.get_channel(config.TASK_CHANNEL)
            embed = discord.Embed(title=self.task_title.value, description=self.task_desc.value, color=config.UNCOMPLETED_COLOR)
            await channel.send(embed=embed, view=TaskButton())
            await interaction.message.delete()
            await channel.send(view=NewTaskButton())
            await interaction.response.send_message('Task Created!', ephemeral=True, delete_after=1)
        except:
            print(f'err: {traceback.format_exc()}')

    async def on_error(self, interaction: discord.Interaction, error) -> None:
        ...
    
    async def on_timeout(self, interaction: discord.Interaction) -> None:
        ...


async def loop():
    while True:
        config.roles.load_roles()
        await asyncio.sleep(5)

def run_bot():
    @bot.event
    async def on_ready():
        print('bot is starting!')
        channel = bot.get_channel(config.TASK_CHANNEL)
        await channel.purge(limit=None)
        await channel.send(view=NewTaskButton())
        asyncio.create_task(loop())
        print('bot has started!')
        
    bot.run(config.BOT_TOKEN)

run_bot()