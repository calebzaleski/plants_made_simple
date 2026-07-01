import pandas as pd
from backend.endpoints import engine
from backend import models

df = pd.read_sql("select * from plants", con=engine)
print(df.head())
