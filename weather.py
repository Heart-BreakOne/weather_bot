import discord
import requests
from discord.ext import commands, tasks

d_token = ''
ow_token = ''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='', intents=intents)

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={ow_token}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        weather_info = (
            f"**Weather in {city}:**\n"
            f"Temperature: **{temp}°C  -  {(temp * 9/5) + 32:.1f}°F**\n"
            f"Feels like: **{feels_like}°C  -  {(feels_like * 9/5) + 32:.1f}°F**\n"
            f"Condition: {weather_desc.capitalize()}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed * 3.6:.1f} km/h  -  {wind_speed * 2.23694:.1f} mph\n"
        )
        return weather_info
    else:
        return f"Could not fetch weather data for {city}."

@bot.command(name='weather')
async def weather(ctx):
    garca = get_weather('Garça, BR')
    fairport = get_weather('Fairport, US')
    await ctx.send(f"{garca}\n\n{fairport}")

@tasks.loop(minutes=5)
async def update_status():
    await bot.change_presence(activity=discord.Game("Monitoring weather..."))

@bot.event
async def on_ready():
    update_status.start()
    print(f'Logged in as {bot.user.name}')

bot.run(d_token)
