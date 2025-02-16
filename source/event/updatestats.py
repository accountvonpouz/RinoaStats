import disnake
import logging
import asyncio
from datetime import datetime, timedelta
from disnake.ext import commands, tasks

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UpdaterStatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category_name = "📊 Server Stats"
        self.total_channel_name = "👥 Total Members: {}"
        self.human_channel_name = "🙎 Humans: {}"
        self.bot_channel_name = "🤖 Bots: {}"

        # Start the loop when the cog is loaded
        self.update_stats.start()

    async def ShowIfCategoryExists(self, guild):
        # Check if the category exists
        category = disnake.utils.get(guild.categories, name=self.category_name)
        if category is not None:
            return category
        else:
            # Create the category if it doesn't exist
            category = await guild.create_category(self.category_name)
            return category

    async def GetNumbers(self, guild):
        total_members = sum(1 for member in guild.members)
        human_members = sum(1 for member in guild.members if not member.bot)
        bot_members = sum(1 for member in guild.members if member.bot)
        return total_members, human_members, bot_members

    async def CreateVoiceChannel(self, category, name):
        # Create a voice channel that no one can join (permission overwrite)
        overwrites = {
            category.guild.default_role: disnake.PermissionOverwrite(connect=False),  # Deny connect for @everyone
        }
        channel = await category.create_voice_channel(name, overwrites=overwrites)
        return channel

    async def schedule_next_run(self):
        # Calculate the next run time (on the next full hour or half hour)
        now = datetime.utcnow()
        if now.minute < 30:
            next_run = now.replace(minute=30, second=0, microsecond=0)
        else:
            next_run = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

        # Calculate the delay time (in seconds)
        delay = (next_run - now).total_seconds()
        logger.info(f"Next stats update scheduled for {next_run.strftime('%H:%M UTC')}")

        # Wait until the next scheduled time
        await asyncio.sleep(delay)
        await self.update_stats()

    @tasks.loop(seconds=1)
    async def update_stats(self):
        # This loop runs every second but will execute only at the scheduled time
        await self.schedule_next_run()

        for guild in self.bot.guilds:
            category = await self.ShowIfCategoryExists(guild)
            total_members, human_members, bot_members = await self.GetNumbers(guild)

            # Log that we are updating stats for the guild
            logger.info(f"Updating stats for guild: {guild.name} (ID: {guild.id})")

            # Check if voice channels exist, if not, create them
            total_channel = disnake.utils.get(category.voice_channels,
                                              name=self.total_channel_name.format(total_members))
            if not total_channel:
                total_channel = await self.CreateVoiceChannel(category, self.total_channel_name.format(total_members))
            else:
                await total_channel.edit(name=self.total_channel_name.format(total_members))

            human_channel = disnake.utils.get(category.voice_channels,
                                              name=self.human_channel_name.format(human_members))
            if not human_channel:
                human_channel = await self.CreateVoiceChannel(category, self.human_channel_name.format(human_members))
            else:
                await human_channel.edit(name=self.human_channel_name.format(human_members))

            bot_channel = disnake.utils.get(category.voice_channels, name=self.bot_channel_name.format(bot_members))
            if not bot_channel:
                bot_channel = await self.CreateVoiceChannel(category, self.bot_channel_name.format(bot_members))
            else:
                await bot_channel.edit(name=self.bot_channel_name.format(bot_members))

            # Log that the stats update has been completed
            logger.info(f"Stats updated for guild: {guild.name} (ID: {guild.id})")

    @update_stats.before_loop
    async def before_update_stats(self):
        # Wait until the bot is ready before starting the loop
        await self.bot.wait_until_ready()

        # Schedule the first run to occur immediately after the bot is ready
        await self.schedule_next_run()


def setup(bot):
    bot.add_cog(UpdaterStatsCog(bot))
