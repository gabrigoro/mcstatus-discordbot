import discord
from mcstatus import MinecraftServer
import asyncio

# Crea una conexión al servidor
server = MinecraftServer("tu.ip.del.server", 25565) # reemplaza con la dirección y el puerto de tu servidor

# Crea una instancia de cliente de Discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(check_players())

async def check_players():
    old_players = []
    while True:
        status = server.status()
        new_players = status.players.sample if status.players.sample else []
        new_players_names = [player.name for player in new_players]

        channel = client.get_channel(int('9913484423487234986'))  # Recuerda reemplazar 'Discord_channel_id' con el ID de tu canal de Discord.

        for player in new_players_names:
            if player not in old_players:
                await channel.send(f"{player} se ha conectado.")
        for player in old_players:
            if player not in new_players_names:
                await channel.send(f"{player} se ha desconectado.")

        old_players = new_players_names
        await asyncio.sleep(60)  # espera un minuto antes de verificar de nuevo

@client.event
async def on_message(message):
    if message.content.startswith("conectados"):
        status = server.status()
        if status.players.sample:
            player_names = ', '.join([player.name for player in status.players.sample])
            await message.channel.send(f"Jugadores conectados: {player_names}")
        else:
            await message.channel.send("No hay jugadores conectados.")

client.run('Tu_Token_aca')  # Recuerda reemplazar 'Tu_Token_aca' con el token de tu bot.
