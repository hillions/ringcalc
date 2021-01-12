from decimal import Decimal

gamename = "Cash0111"
filename = "EventLog.txt"

def create_players(log):
    # Return a dictionary of player names with a 0 balance
    names = []
    players = {}

    for line in log:
        # Parse each line looking for player names
        # If "Account" appears in the line, 
        # a player's name follows who participated.
        if line.split("|")[1] == "Account" and gamename in line:
            names.append(line.split("|")[2].split(" ")[0])

    for name in set(names):
        # Set the initial balance to $0.00
        players[name] = 0

    return players

def balance_accounts(log, players):
    # Adjust from $0.00 each player's balance based on
    # account deposits and withdraws. Ignore tournament buy-ins.
    for line in log:
        if line.split("|")[1] == "Account" and gamename in line:
            name = line.split("|")[2].split(" ")[0]
            amount = Decimal(line.split(" ")[2].strip("+"))
            players[name] += amount

def print_totals(players):
    # Print player totals in a nicer format.
    p_view = [ (v,k) for k,v in players.items() ]
    p_view.sort()
    for item in p_view:
        print("%s\t%s" % item)
            
def check_totals(players):
    # Should be 0. A total other than 0 indicates log corruption.
    total = Decimal(0)
    for player in players:
        total += players[player]
    
    if int(total) == 0:
        print("Accounts total $0.00")
    else:
        print("Accounts off by %s" % total)

if __name__ == "__main__":
    with open(filename) as f:
        log = f.readlines()

    players = create_players(log)
    balance_accounts(log, players)
    print_totals(players)
    check_totals(players)