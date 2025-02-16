# Discord Server Stats Bot
A Discord bot that tracks server statistics such as total members, human members, and bot members. The bot updates the stats and displays them in voice channels every hour at xx:00 and xx:30 UTC.

# Features

- Server Stats: Tracks the total number of members, human members, and bot members in your server.
- Scheduled Updates: Stats are updated automatically every hour at xx:00 and xx:30 UTC.
- Logging: logs for each stats update to monitor changes.

# How It Works

- The bot listens for changes in the server and updates stats every hour at xx:00 and xx:30 UTC.
- It checks if the necessary categories and voice channels exist. If they don't, it creates them.
- Each voice channel represents a specific stat (total members, human members, and bot members) and is updated accordingly.
<br>

  Example:

- 👥 Total Members: 123
- 🙎 Humans: 100
- 🤖 Bots: 23

# License
This project is licensed under the MIT License
