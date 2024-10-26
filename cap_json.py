import sqlite3
import json

conn = sqlite3.connect('mydb.sqlite')
if conn:
    print("Successfully Connected...")

cursor = conn.cursor()

sqlstr = '''select strftime('%Y', mod_date) as Year, count() as Mod_Ct
from WikiChange GROUP by Year  ORDER by Year
'''

cursor.execute(sqlstr)

rows = cursor.fetchall()
columns = [col[0] for col in cursor.description]
data = [dict(zip(columns, row)) for row in rows]

to_json = json.dumps(data, indent=2)
print(to_json)

with open('cap_wikichg.json', 'w') as file:
    file.write(to_json)

conn.commit()
cursor.close()
conn.close()

