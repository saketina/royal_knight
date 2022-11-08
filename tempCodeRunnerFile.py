game = discord.Game("with your feelings")
    await client.change_presence(activity=game, status=discord.Status.online)
