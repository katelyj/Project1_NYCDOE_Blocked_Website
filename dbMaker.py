import sqlite3

f="database.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

q = "CREATE TABLE SavedSongs (songid INT, user TEXT, cityid INT)"
c.execute(q)

#q = "INSERT INTO SavedSongs VALUES(%d,'%s',%d)"%(0,michael,123)
#c.execute(q)


q = "CREATE TABLE weather (mode TEXT, genre TEXT)"
c.execute(q)

conditions = {"snowing": "seasonal and holiday", "cloudy": "alternative", "raining": "blues", "freezing": "classical", "cold": "rock", "nice": "rap", "warm": "folk", "hot" :"latin"}

for i in conditions:
    q = "INSERT INTO weather VALUES('%s','%s')"%(i,conditions[i])
    c.execute(q)

db.commit() #save changes
db.close()  #close database
