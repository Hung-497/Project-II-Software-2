import mysql.connector
import random
from flask import Flask, Response
import json

connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='demogame',
         user='root',
         password='Giahung@!497',
         autocommit=True,
         auth_plugin="mysql_native_password",
         use_pure=True
)

# ---- Fixed airports, hints and letter parts ----
FIXED_CODE_AIRPORTS = ["LIRF", "GCTS", "LFPG", "EHEH", "EDDF"]

FIXED_HINTS = {
    "LIRF": "Gelato can taste sweet. :)",
    "GCTS": "Les Fleurs du Petit Garçon",
    "LFPG": "Eheh :)",
    "EHEH": "ERROR 504: Data packet lost  Driver mismatch detected  Database access denied   File structure corrupted",
    # EDDF has no hint (final)
}

letter_parts = {
    "LIRF": "You have a great chance to save the world.",
    "GCTS": "Do what you can.",
    "LFPG": "There are still computers left, scattered around the EU that can help you",
    "EHEH": "To remember who you are.",
    "EDDF": "But don’t get too excited, since I tricked you; the secret base, the key, my password - remember?",
}

## this is a function for defining random airports in r rows
def get_airport(db_conf): #random 30 airports for the game
    sql = """SELECT ident, name, municipality, latitude_deg AS lat, longitude_deg AS lon
             FROM airport
             WHERE continent = 'EU'
               AND type = 'large_airport'
             ORDER by RAND() 
             LIMIT 30;"""
    con = mysql.connector.connect(**db_conf)
    cur = con.cursor(dictionary=True)
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    con.close()
    return {r["ident"]: r for r in rows}

# ----Coregame----
class Coregame:
    def __init__(self, db_conf):
        #Map
        self.airport = get_airport(db_conf)
        code_positions = {icao: FIXED_HINTS.get(icao, "") for icao in FIXED_CODE_AIRPORTS}
        fixed_municipalities = {
        "LIRF": "Rome",
        "GCTS": "Tenerife",
        "LFPG": "Paris",
        "EHEH": "Eindhoven",
        "EDDF": "Frankfurt"
        }
        fixed_name = {              #for messages
            "LIRF": "Rome–Fiumicino Leonardo da Vinci Interna",
            "GCTS": "Tenerife Sur Airport",
            "LFPG": "Charles de Gaulle International Airport",
            "EHEH": "Eindhoven Airport",
            "EDDF": "Frankfurt am Main Airport"}
        fixed_coords = {             #for markers on map
        "LIRF": (41.8003, 12.2389),
        "GCTS": (28.0445, -16.5725),       
        "LFPG": (49.0097, 2.5479),
        "EHEH": (51.4501, 5.3745),
        "EDDF": (50.0379, 8.5622),
        }
        # Ensure fixed airports are included
        for icao in FIXED_CODE_AIRPORTS:
            lat, lon = fixed_coords[icao]
            self.airport[icao] = {
                "ident": icao,
                "name": fixed_name.get(icao, ""),
                "municipality": fixed_municipalities.get(icao, ""),
                "lat": lat,
                "lon": lon,
            }
        self.idents = list(self.airport)
        # Player state
        self.start = random.choice(self.idents)
        self.cur = self.start
        self.found = set()
        self.visited = {self.start}
        self.days_left = 21
        self.max_days = 21
        self.code_positions = code_positions
        self.messages = []
        self.game_over = False
        self.outcome = None

    def built_message(self):
        remaining_airport = [{"code": code,
                              "name": self.airport[code]["name"] + " - " + self.airport[code]["municipality"],
                              "lat": self.airport[code]["lat"],
                              "lon": self.airport[code]["lon"] } 
                             for code in self.airport if code not in self.visited]
        random.shuffle(remaining_airport)
        curren_airport_infor = {
            "code": self.cur,
            "name": self.airport[self.cur]["name"] + " - " + self.airport[self.cur]["municipality"],
            "lat": self.airport[self.cur]["lat"],
            "lon": self.airport[self.cur]["lon"] 
        }
        return {
            "current_airport": self.cur,
            "current_airport_info": curren_airport_infor,
            "start_airport": self.start,
            "days_left": self.days_left,
            "max_days": self.max_days,
            "code_found": len(self.found),
            "visited_airports": list(self.visited),
            "game_over" : self.game_over,
            "outcome": self.outcome,
            "messages": self.messages,
            "reamaining_airport_count": len(remaining_airport),
            "remaining_airports": remaining_airport,
        }
  
    def reset_messages(self):
        self.messages = []

    def add_message(self, text):
        self.messages.append(text)

    def show_letter_so_far(self):
        parts = [letter_parts[i] for i in FIXED_CODE_AIRPORTS if i in self.found]
        if parts:
            text = "\n>>> Letter so far:\n" + " ".join(parts) + "\n"
            self.add_message(text)
            return text
        return ""

    def move(self, dest_ident):

        self.reset_messages()

        if dest_ident not in self.airport:
            msg = f'This airport {dest_ident} is not on the map!'
            self.add_message(msg)
            return msg
        
        if dest_ident == self.cur:
            msg = "You are already at this place, please move to another destination."
            self.add_message(msg)
            return msg
        
        self.days_left -= 1
        self.cur = dest_ident
        self.visited.add(dest_ident)
        
        msg = f"You are now at {self.fmt(dest_ident)}"

        if dest_ident in letter_parts and dest_ident not in self.found:
            part = letter_parts[dest_ident]
            msg += f"\n\n>>> Letter fragment discovered:\n\"{part}\" <<<"
            hint = self.code_positions.get(dest_ident, "")
            if hint:
                msg += f"\n\n>>> A computer flickers:\n\"{hint}\" <<<"
            self.found.add(dest_ident)

        # If all letter parts are found
        if len(self.found) == len(FIXED_CODE_AIRPORTS):
            self.game_over = True
            self.outcome = "win"

        if self.days_left <= 0 and not self.win_condition():
            self.game_over = True
            self.outcome = "lose"
        
        if self.game_over:
            if self.outcome == "win":
                pass
            else:
                pass

        self.add_message(msg)
        return msg
    
    def win_condition(self):
        return len(self.found) == len(FIXED_CODE_AIRPORTS)
    
    def fmt(self, ident):
        row = self.airport[ident]
        return f"{ident} - {row['name']} - {row.get('municipality') or '' }"

#-------- Flask App for interaction --------
db_conf = dict(
    host='127.0.0.1',
    port=3306,
    database='demogame',
    user='root',
    password='Giahung@!497',
    autocommit=True,
    auth_plugin="mysql_native_password",
    use_pure=True
)
app = Flask(__name__)
game = Coregame(db_conf)

@app.route('/move/<dest_ident>')
def move(dest_ident):
    try:
        game.move(dest_ident.upper().strip())
        state = game.built_message()
        json_response = json.dumps(state)
        return Response(response=json_response, status=200, mimetype="application/json")
    except ValueError:
        response = {
            "message": "Invalid",
            "status": 400
        }
        json_response = json.dumps(response)
        http_response = Response(response=json_response, status=400, mimetype="application/json")
        return http_response
    
@app.route('/state')
def state():
    try:
        if not game.messages:
            game.add_message(f"You are now at {game.fmt(game.cur)}")
        state = game.built_message()
        json_response = json.dumps(state)
        return Response(response=json_response, status=200, mimetype="application/json")
    except ValueError:
        response = {
            "message": "Invalid",
            "status": 400
        }
        json_response = json.dumps(response)
        http_response = Response(response=json_response, status=400, mimetype="application/json")
        return http_response

@app.route('/newgame')
def newgame():
    try:
        global game                                                 # global variable - use and modify the game variable
        game = Coregame(db_conf)
        state = game.built_message()
        json_response = json.dumps(state)
        return Response(response=json_response, status=200, mimetype="application/json")
    except ValueError:
        response = {
            "message": "Invalid",
            "status": 400
        }
        json_response = json.dumps(response)
        http_response = Response(response=json_response, status=400, mimetype="application/json")
        return http_response

@app.errorhandler(404)
def page_not_found(error_code):
    response = {
        "message": "Invalid endpoint",
        "status": 404
    }
    json_response = json.dumps(response)
    http_response = Response(response=json_response, status=404, mimetype="application/json")
    return http_response

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5501"
    return response # Enable CORS for local frontend because got errors

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)
