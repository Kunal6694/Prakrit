import pathway as pw
import pandas as pd

# 1. Create a standard Python list
data = [
    {"message": "Hello Prakrit!"},
    {"message": "Pathway Engine is Live"},
    {"message": "D-Drive setup successful"}
]

# 2. Convert to a Pandas DataFrame
df = pd.DataFrame(data)

# 3. Create the Pathway table from the DataFrame
table = pw.debug.table_from_pandas(df)

# 4. Run and print the results
pw.debug.compute_and_print(table)
