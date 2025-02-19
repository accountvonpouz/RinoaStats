import disnake
import logging
import asyncio
from datetime import datetime, timedelta
from disnake.ext import commands, tasks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UpdateStatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category_name = "📊 Server Stats"
        self.total_channel_name = "👥 Total Members: {}"
        self.human_channel_name = "🙎 Humans: {}"
        self.bot_channel_name = "🤖 Bots: {}"

        self.create_stats_channels.start()

    def cog_unload(self):
        self.create_stats_channels.cancel()

    def get_next_half_hour(self):
        now = datetime.now()
        next_half_hour = (now + timedelta(minutes=30)).replace(second=0, microsecond=0)
        if now.minute >= 30:
            next_half_hour = next_half_hour.replace(minute=0) + timedelta(hours=1)
        else:
            next_half_hour = next_half_hour.replace(minute=30)
        return (next_half_hour - now).total_seconds()

    async def update_stats(self, guild):
        total_members = len(guild.members)
        human_members = len([m for m in guild.members if not m.bot])
        bot_members = len([m for m in guild.members if m.bot])

        category = disnake.utils.get(guild.categories, name=self.category_name)
        if not category:
            category = await guild.create_category(self.category_name)

        if category.position != 0:
            await category.edit(position=0)

        channels_info = [
            (self.total_channel_name.format(total_members), total_members),
            (self.human_channel_name.format(human_members), human_members),
            (self.bot_channel_name.format(bot_members), bot_members)
        ]

        overwrites = {
            guild.default_role: disnake.PermissionOverwrite(connect=False, view_channel=True)
        }

        for name, _ in channels_info:
            channel = disnake.utils.get(category.channels, name=name)
            if not channel:
                await category.create_voice_channel(name, overwrites=overwrites)
            else:
                await channel.edit(name=name, overwrites=overwrites)

    @tasks.loop(minutes=30)
    async def create_stats_channels(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(self.get_next_half_hour())

        for guild in self.bot.guilds:
            try:
                await self.update_stats(guild)
            except Exception as e:
                logger.error(f"Error updating stats: {e}")

    async def manual_sync(self, guild):
        await self.update_stats(guild)

def setup(bot):
    bot.add_cog(UpdateStatsCog(bot))