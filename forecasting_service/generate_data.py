import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create 90 days of daily data
end_date = datetime.now()
df = pd.DataFrame({
    "date": [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(90)][::-1],
    "value": np.random.randint(100, 200, size=90) + np.arange(90) * 0.5
})

df.to_csv("data.csv", index=False)
print("Created data.csv with 90 rows.")