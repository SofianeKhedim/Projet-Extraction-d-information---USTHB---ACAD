import re
import sqlite3 as sq3
from sys import argv

# Vérifier si un chemin de fichier est fourni en tant qu'argument de ligne de commande
if(len(argv) == 2):
	path = argv[1]
else:  # Chemin de fichier par défaut s'il n'est pas fourni
	path = 'concord.html'

phase3_results = open(path, 'r', encoding="UTF-8").read()
posologies = re.findall('<a href="[0-9 ]+?">(.*?)</a>', phase3_results)
db = sq3.connect("extraction.db")
control = db.cursor()
control.execute("DROP TABLE IF EXISTS Treatment")
control.execute("CREATE TABLE IF NOT EXISTS Treatment (id INT PRIMARY KEY NOT NULL, posologie TEXT NOT NULL )")
control.executemany("INSERT INTO Treatment VALUES (?,?)", enumerate(posologies, start=1))
print("Insertion terminée.")
db.commit()
db.close()
