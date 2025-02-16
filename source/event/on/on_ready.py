from disnake.ext import commands
import logging

class OnReadyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"Bot successfully logged in as {self.bot.user}")

def setup(bot):
    bot.add_cog(OnReadyCog(bot))