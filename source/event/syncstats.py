import disnake
from disnake.ext import commands

class SyncCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="sync", description="Update the stats category immediately.")
    async def sync(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        stats_cog = self.bot.get_cog("UpdateStatsCog")
        if not stats_cog:
            await inter.followup.send("❌ Stats system is not loaded.")
            return

        try:
            await stats_cog.manual_sync(inter.guild)
            await inter.followup.send("✅ Stats category updated.")
        except Exception as e:
            await inter.followup.send("❌ Error updating stats category.")

def setup(bot):
    bot.add_cog(SyncCommandCog(bot))