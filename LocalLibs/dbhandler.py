from replit import db

"""
Database handler to check player's currencies and other values.
"""
# All users will be added to the database under their discord ID.
def check_exist(user_id):
    """
    Checks for a user's ID in the database.
    """
    # If they user exists, return true. Otherwise return false
    if db.get(user_id):
        return True
    return False

def create_user(user_id):
    """
    Create a user with the starting values.
    """
    db[user_id] = {
        "Money": 500.00, # Total amount of money. 500 is the starting amount, for now.
        "Wins": 0, # Total wins
        "Losses": 0, # Total losses
        "Total Winnings": 0, # Amount of money won over every game played
    }
    
    db[user_id + "-Inventory"] = {
        
    }

    db[user_id + "-ActivePotions"] = {

    }

def remove_user(user_id):
    del db[user_id]

# This function is only for testing.
def wipe_database():
    amount = len(db.keys())
    for v in db.keys():
        del db[v]
    return ("Database Cleared.")