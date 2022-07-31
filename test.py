from operator import index
from datacrawling import Bot
import pandas as pd

bot = Bot()
data = bot.fetchData()
df = pd.DataFrame(data)
print(df['items'].loc[0])
