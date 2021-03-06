import sqlite3, urllib2, spotipy, random, json, os, requests


special = ['Snow','Rain','Clouds']
genreList = ["christmas","pop", "blues", "classical", "rock", "rap", "folk", "latin"]


#returns the temperature condition given the current temperature
#if there is an issue w/temp, just return "nice" by default
def tempCondition(temp):
    if temp < 0:
        return "freezing"
    if temp < 40:
        return "cold"
    if temp < 60:
        return "nice"
    if temp < 80:
        return "warm"
    return "hot"


def getTrack(givenGenre):

    #if there is an error, you have to listen to blues
    #b/c you make me sad
    if givenGenre not in genreList:
        givenGenre = "blues"

    spotify = spotipy.Spotify()

    #picked b/c # spotify songs/genre not available, but big number
    n = random.randrange(10000)
    searchRet = spotify.search("genre:" + givenGenre, limit=1, offset=n, type='track')

    ret = {}

    ret['url'] = searchRet['tracks']['items'][0]['preview_url']
    ret['title'] = searchRet['tracks']['items'][0]['name']
    ret['artist'] = searchRet['tracks']['items'][0]['artists'][0]['name']
    ret['genre'] = givenGenre
    return ret

def main(condition, temp):
    if condition in genreList:
        genre = condition
    else:
        if condition not in special:
            condition = tempCondition(temp)
        #db stuff
        f="database.db"
        db = sqlite3.connect(f) #open if f exists, otherwise create
        c = db.cursor()    #facilitate db ops

        query = "SELECT genre FROM weather WHERE mode='%s'"%(condition)
        genre = c.execute(query).fetchall()
        genre = genre[0][0]

        db.close()  #close database

    return getTrack(genre)

def get_saved_songs(username):
    f = "database.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    song_count = 0
    song_str = ""
    query = "SELECT * FROM SavedSongs where user = \'%s\'"%(username)
    dbSavedSongs = c.execute(query)
    for entry in dbSavedSongs:
        song_str+= "<a href=%s> %s by %s </a>"%(entry[0], entry[2], entry[3])
        song_str+= "<form method=\"POST\"><input type=\"submit\" value=\"Remove\" name=\"remove_song\">"
        song_str+="<input type=\"hidden\" name=\"url\" value=\"%s\"></form><br><br>"%(entry[0])
        song_count+=1
    if (song_count == 0): song_str+= "You currently have no songs saved."
    return song_str

def get_loc_coords():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return lat,lon
