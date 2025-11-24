import mysql.connector
import random 
import time,sys

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
    "EHEH": "to remember who you are.",
    "EDDF": "But don’t get too excited, since I tricked you; the secret base, the key, my password - remember?",
}

## this is a function for defining random airports in r rows

def get_airport(db_conf): #random 30 airports for the game
    sql = """SELECT ident, name, municipality
             FROM airport
             WHERE continent = 'EU'
               AND type = 'large_airport'
             ORDER by RAND() LIMIT 30;"""
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
        fixed_name = {
            "LIRF": "Rome–Fiumicino Leonardo da Vinci Interna",
            "GCTS": "Tenerife Sur Airport",
            "LFPG": "Charles de Gaulle International Airport",
            "EHEH": "Eindhoven Airport",
            "EDDF": "Frankfurt am Main Airport"}
        
        # Ensure fixed airports are included
        for icao in FIXED_CODE_AIRPORTS:
            self.airport[icao] = {
                "ident": icao,
                "name": fixed_name.get(icao, ""),
                "municipality": fixed_municipalities.get(icao, "")
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
    
    def show_letter_so_far(self):
        parts = [letter_parts[i] for i in FIXED_CODE_AIRPORTS if i in self.found]
        if parts:
            print("\n>>> Letter so far:\n" + " ".join(parts) + "\n")

    def move(self, dest_ident):
        if dest_ident not in self.airport:
            return f'This airport {dest_ident} is not on the map!'
        if dest_ident == self.cur:
            return "You already at this place, please move to another destination."
        Coregame.show_letter_so_far(self)
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
            msg += "\n\n>>> The letter is now complete! <<<"
        return msg
    
    def win_condition(self):
        return len(self.found) == len(FIXED_CODE_AIRPORTS)
    
    def fmt(self, ident):
        row = self.airport[ident]
        return f"{ident} - {row['name']} - {row.get('municipality') or '' }"

# ----CLI runner----
def typing(text):
   for character in text:
      sys.stdout.write(character)
      sys.stdout.flush()
      time.sleep(0.05)

def run_cli(db_conf):
    from intro import show_intro
    show_intro()
    g = Coregame(db_conf)
    name = input("Type the player name: ").capitalize()
    input("\n\033[32mPress Enter to start the game...\033[0m")
    typing("\nThe world is falling apart, piece by piece.\n")
    time.sleep(0.8)
    typing("A strange new 'red hole' has opened somewhere out in the cosmos, quietly erasing the code that holds reality together.\n")
    time.sleep(0.8)
    typing("Languages grow simpler, memories fade, and entire systems vanish overnight. Nobody knows how to stop it.\n")
    time.sleep(0.8)
    typing(f"But somehow, {name}, you’ve woken up in the middle of it all—with nothing but a letter and a few cryptic clues that might lead to the last surviving computers.\n")
    time.sleep(0.8)
    typing("If there’s any hope left, the hope is you.")
    time.sleep(0.8)
    input("\n\033[32mPress Enter to continue...\033[0m")
    typing("\nYou need to find the computers at each airport to piece together the letter and remember who you are. Each computer you find will give you a part of the letter and a clue to the next location.\n")
    time.sleep(0.8)
    typing("Your journey begins now...\n")
    time.sleep(0.8)
    input("\n\033[32mPress Enter to accept the mission...\033[0m")
    print(f"{name}. You now are at {g.fmt(g.start)}")
    print("Commands: list (show airports) | go <IDENT> | quit")

    # ----Main loop----
    while not g.win_condition() and g.days_left > 0:
        print(f"Codes found: {len(g.found)}/5 | Days left: {g.days_left}/{g.max_days} | Current location: {g.fmt(g.cur)}")
        cmd = input("Choose your next destination: ").strip().upper().split()
        if not cmd:
            continue
        c = cmd[0].lower()
        if c == "list":
            remaining = [i for i in g.idents if i not in g.visited]
            count = len(remaining)
            if count > 0:
                print(f"You only have {count} airports remaining:")
                for ident in sorted(remaining): # show IDENT – NAME – MUNICIPALITY one per line
                    print("  " + g.fmt(ident))
            else:
                print("No more unvisited airports")
        elif c == "go" and len(cmd) >= 2:
            print(g.move(cmd[1]))
        elif c == "quit":
            break
        else:
            print("Invalid command.")
    if g.win_condition():
        from good import show_good_end
        show_good_end()
        show_good()
        print("You have visited:")
        for ident in sorted(g.visited):
            print("  " + g.fmt(ident))
    elif g.days_left <= 0:
        from bad import show_bad_end
        show_bad_end()
        show_bad()
    else:
        print(">>> GAME ENDED! <<<")

# Winning situation
def show_good():
    typing("\n--- MISSION COMPLETE ---\n")
    time.sleep(1)

    typing("You have visited all the airports and decoded every hint.\n")
    time.sleep(1)

    typing("The letter finally makes sense. You remember… it was you who caused the system error.\n")
    time.sleep(1)

    typing("You caused the Red Death, but you are the only one who could fix it.\n")
    time.sleep(1)

    typing("\n>>> Letter is now completed <<<\n")
    time.sleep(1)

    typing("\nIt’s painful, yes. But for the first time in weeks, you feel clarity.")
    time.sleep(1)

    typing("The Red Death recedes a little, just enough to stop immediate destruction.\n")
    time.sleep(1)

    typing("You sit on a bench in the empty airport lounge, reflecting.\n")
    time.sleep(1)

    typing("You have won not by reversing everything, but by understanding, remembering, and acting.\n")
    time.sleep(1)

    typing("\n>>> End of letter <<<\n")
    time.sleep(1)

# Losing situation
def show_bad():
    typing("\n--- TIME IS UP ---\n")
    time.sleep(1)

    typing("You didn’t manage to decode all the hints in time.\n")
    time.sleep(1)

    typing("The Red Death continues its work, erasing memories and simplifying everything.\n")
    time.sleep(1)

    typing("Fragments of the world you knew remain, but the full picture is lost.\n")
    time.sleep(1)

    typing("\n>>> Letter partially decoded <<<\n")
    time.sleep(1)

    typing("\nA familiar face appears—the ice cream seller from Italy.\n")
    time.sleep(1)

    typing("He hands you a cone and smiles gently.\n")
    time.sleep(1)

    typing('"Sometimes," he says, "there are battles you can’t win no matter how hard you try. But even then… there’s beauty in small moments."\n')
    time.sleep(1)

    typing("You take a bite, feeling the sweetness, and a quiet calm.\n")
    time.sleep(1)

    typing("On that bench, you rest, exhausted but alive.\n")
    time.sleep(1)
