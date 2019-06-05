from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint

# connect to MongoDB, TODO: Update to Alden's machine
client = MongoClient("mongodb://Anykze:Rajivisgay123@notifier-shard-00-00-wcy1w.azure.mongodb.net:27017,notifier-shard-00-01-wcy1w.azure.mongodb.net:27017,notifier-shard-00-02-wcy1w.azure.mongodb.net:27017/test?ssl=true&replicaSet=Notifier-shard-0&authSource=admin&retryWrites=true")
db=client.stockNotifier

# NOTE: Uncomment this for server status debugging
# serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)

# ------------------------------------------------------------
#                   Users table operations
#------------------------------------------------------------


# set up a user in the database
# takes a username, 3 128 byte fields for auth, and associated tickers
def newUser(username, loginData, tickers):
    if userExists(username):
        return False
    user = {
        'username' : username,
        'loginData' : loginData,
        'tickers' : tickers
    }
    result = db.users.insert_one(user)
    for symbol in tickers:
        addUserToTicker(symbol, username)
    # print the object id; basically if this runs, it went through.
    print('Registered user with id: {0}'.format(result.inserted_id))
    return True
# below is a test use case for newUser, to see how it works.
# newUser('Aldaddy',
#         [b'9hXxIRiqbWvnMC9o3y22H39VoviqdAmrYdo48Mw0xEc4S89W34y8unbaf1boIfdyalyoI5P71ftnh2uJuPsHHHhP741JT4HpBduppRIO7XnT399tSugvNL1gmKeSzq40',
#         b'jWGAOlw7Zgq12VRRa3Z56Tk8mWgdMFwi837XQBj6lcnUwaE5UKpqApxyT83ExcJ4gNhX0aj8ZXSq3R1wF8T0WsH2x3fLpxz9IKb50HoswIX7gwaaTjUNEjnnslDr4hqW',
#         b'6ghUn0TNggQla31n3c31uvgjJdLnage2KIoW1h3uyJ2QJpVRRZ11ue1z826WjPudIemUpzs7o84umeKFZFB34a18MfDpnNwqMSPf0xPgkWGt5i8oeWTWqho8bH1N4vFk'],
#         ['AMD', 'MSFT', 'SQ'])

def getUsers():
    col = db.users
    listOfUsers = list(col.find({}))
    for UserDict in listOfTickers:
        del userDict['loginData']
        del userDict['tickers']
        del userDict['sessions']
        del userDict['_id']
    return listOfUsers


# returns True if exists else false
def userExists(username):
    sessions = db.users.find(
        {'username' : username}
    )
    return sessions.count() > 0

def newSession(username, sessionID, a, b, b2, k, deviceID):
    col = db.users
    sessions = getSessionsFromUser(username)
    col.update_one(
        {'username' : username},
        {'$set' : 
            {'sessions' : sessions + [{'sessionID' : sessionID,
                                        'a' : a,
                                        'b' : b,
                                        'b2' : b2,
                                        'k' : k,
                                        'device': deviceID}] if sessions is not None else 
                                    [{'sessionID' : sessionID,
                                        'a' : a,
                                        'b' : b,
                                        'b2' : b2,
                                        'k' : k,
                                        'device' : deviceID}] 
            }
        }
    )
def deleteSession(username, sessionID):
    currentSessions = getSessionsFromUser(username)
    if currentSessions is None:
        return
    session = None
    for sessionDict in currentSessions:
        if sessionDict['sessionID'] == sessionID:
            session = sessionDict
    if session is None:
        return
    col = db.users
    col.update_one(
        {'username' : username},
        {'$set' : 
            {'sessions' : [s for s in currentSessions if not (s == session)]}
        }
    )

def editSessionInts(username, sessionID, a, b, b2):
    foundSessions = getSessionsFromUser(username)
    set = False
    col = db.users
    if foundSessions:
        for sessionDict in foundSessions:
            if sessionDict['sessionID'] == sessionID:
                sessionDict['a'] = a
                sessionDict['b'] = b
                sessionDict['b2'] = b2
                set = True
        col.update_one(
            {'username' : username},
            {'$set' : 
                {'sessions' : [s for s in foundSessions]}
            }
        )
        return set
    else:
        return False
    return False

def editSessionKey(username, sessionID, k, deviceID):
    foundSessions = getSessionsFromUser(username)
    set = False
    col = db.users
    if foundSessions:
        for sessionDict in foundSessions:
            if sessionDict['sessionID'] == sessionID:
                sessionDict['k'] = k
                sessionDict['device'] = deviceID
                set = True
        col.update_one(
            {'username' : username},
            {'$set' : 
             {'sessions' : [s for s in foundSessions]}
            }
        )
        return set
    else:
        return False
    return False

def getSessionInts(username, sessionID):
    foundSessions = getSessionsFromUser(username)
    if foundSessions:
        for sessionDict in foundSessions:
            if sessionDict['sessionID'] == sessionID:
                return sessionDict
    else:
        return None
    return None

def getSessionK(username, sessionID):
    foundSessions = getSessionsFromUser(username)
    if foundSessions:
        for sessionDict in foundSessions:
            if sessionDict['sessionID'] == sessionID:
                return sessionDict['k']
    else:
        return None
    return None

def getSessionsFromUser(username):
    sessions = db.users.find(
        {'username' : username}
    )
    try:
        foundSessions = sessions.next()['sessions']
    except:
        return None
    return foundSessions

# adds tickers to a user's list of tickers
# takes a string, and a list of string
def addTickersToUser(username, tickers):
    currentTickers = getTickersFromUser(username)
    col = db.users
    col.update_one(
        {'username' : username},
        {'$set' : 
            {'tickers' : list(set(currentTickers + tickers))}
        }
    )
    for symbol in tickers:
        addUserToTicker(symbol, username)
# below is a test case use for addTickersToUser, to see how it works.
# addTickersToUser('Aldaddy', ['BYND'])
# it assumes a run of the testcase for newUser

# removes tickers to a user's list of tickers
# takes a string, and a list of string
def removeTickersFromUser(username, tickers):
    currentTickers = getTickersFromUser(username)
    col = db.users
    col.update_one(
        {'username' : username},
        {'$set' : 
            {'tickers' : list(set(currentTickers) - set(tickers))}
        }
    )
    for symbol in tickers:
        removeUserFromTicker(symbol, username)
# below is a test case use for removeTickersFromUser, to see how it works.
# removeTickersFromUser('Aldaddy', ['BYND'])
# it assumes a run of the testcase for newUser, addTickersToUser

# prints out a user's tickers
# takes a string
def getTickersFromUser(username):
    tickers = db.users.find(
        {'username' : username}
    )
    foundTickers = tickers.next()['tickers']
    return foundTickers
    # print the tickers out for that user
    # pprint(foundTickers)
# below is a test case use for getTickersFromUser, to see how it works.
# getTickersFromUser('Aldaddy')
# it assumes a run of the testcase for newUser

def getLoginDataFromUser(username):
    tickers = db.users.find(
        {'username' : username}
    )
    foundData = tickers.next()['loginData']
    return foundData

# deletes a user account
# takes a string
# assumes all tickers that are in a users list exist in the tickers collection
def deleteUser(username):
    tickers = getTickersFromUser(username)
    for ticker in tickers:
        removeUserFromTicker(ticker, username)
    db.users.delete_one(
        {'username' : username}
    )
# below is a test case for deleteUser
# deleteUser('Aldaddy')
# it assumes a run of the testcase for newUser
# to see full results, also have the ticker existing


# ------------------------------------------------------------
#                 Tickers table operations
#------------------------------------------------------------

# adds a new ticker to the tickers table
# takes a string, and 3 lists of strings
# for first time addition of a new ticker, users is expected to be an empty list
def addTicker(symbol, name, supports, resistances, users, last):
    ticker = {
        'symbol' : symbol,
        'name' : name,
        'supports' : supports,
        'resistances' : resistances,
        'users' : users,
        'last' : last
    }
    result = db.tickers.insert_one(ticker)
    # print the object id; basically if this runs, it went through.
    print('Registered ticker with id: {0}'.format(result.inserted_id))
# below is a test use case for addTicker, to see how it works.
# addTicker(
#     'AMD',
#     'Advanced Micro Devices',
#     ['(20,4)', '(21,2)'],
#     ['(30,1)', '(37,5)'],
#     ['Aldaddy']
# )

def setLast(symbol, price):
    col = db.tickers
    col.update_one(
        {'symbol' : symbol},
        {'$set' : 
            {'last' : price}
        }
    )

def getLast(symbol, price):
    tickers = db.tickers.find(
        {'symbol' : symbol}
    )
    foundPrice = tickers.next()['last']
    return foundPrice

# updates the supports in the tickers table
# takes a symbol to be updates, and the new support levels as a list
def updateSupports(symbol, supports):
    col = db.tickers
    col.update_one(
        {'symbol' : symbol},
        {'$set' : 
            {'supports' : supports}
        }
    )
# below is a test use case for updateSupports, to see how it works.
# updateSupports(
#     'AMD',
#     ['30', '37']
# )
# this assumes a run of the testcase for addTicker

# similarly to updateSupports
def updateResistances(symbol, resistances):
    col = db.tickers
    col.update_one(
        {'symbol' : symbol},
        {'$set' : 
            {'resistances' : resistances}
        }
    )


# adds a user to a ticker symbol
# assumes the existence of the user in the database
def addUserToTicker(symbol, user):
    users = getUsersForTicker(symbol)
    col = db.tickers
    col.update_one(
        {'symbol' : symbol},
        {'$set' : 
            {'users' : users + [user]}
        }
    )
# below is a test use case for addUserToTicker, to see how it works.
# addUserToTicker(
#     'AMD',
#     'Deben'
# )
# this assumes a run of the testcase for addTicker

# removes a user from a ticker symbol
# assumes the existence of the user under the ticker
def removeUserFromTicker(symbol, user):
    users = getUsersForTicker(symbol)
    col = db.tickers
    col.update_one(
        {'symbol' : symbol},
        {'$set' : 
            {'users' : list(set(users) - set([user]))}
        }
    )
# below is a test case for removeUserFromTicker, to see how it works.
# removeUserFromTicker(
#     'AMD',
#     'Aldaddy'
# )
# this assumes a run of the testcase for addTicker

# get the user list associated with a certain ticker
def getUsersForTicker(symbol):
    tickers = db.tickers.find(
        {'symbol' : symbol}
    )
    try:
        foundUsers = tickers.next()['users']
        return foundUsers
    except StopIteration:
        return []
    # print the users out for that ticker
    # pprint(foundUsers)
# below is a test case for getUsersForTicker, to see how it works.
# getUsersForTicker('AMD')
# this assumes a symbol AMD with some associated users. 

# deletes a ticker symbol from the database
# takes a string
def deleteTicker(symbol):
    db.tickers.delete_one(
        {'symbol' : symbol}
    )
    for user in getUsersForTicker(symbol):
        removeTickersFromUser(user, [symbol])
# below is a test case for deleteTicker
# deleteTicker('AMD')
# it assumes a run of the testcase for addTicker

# gets a list of all tickers and their names
# in the form: 
# [{'name': 'Advanced Micro Devices', 'symbol': 'AMD'},
# {'name': 'Square', 'symbol': 'SQ'},
# {'name': 'Microsoft', 'symbol': 'MSFT'}]
# takes no arguments
def getTickers():
    col = db.tickers
    listOfTickers = list(col.find({}))
    for tickerDict in listOfTickers:
        del tickerDict['resistances']
        del tickerDict['supports']
        del tickerDict['users']
        del tickerDict['_id']
        del tickerDict['last']
    return listOfTickers
# output can be tested with
# pprint(getTickers())
# it assumes that tickers have been added

def getSupportsForTicker(symbol):
    tickers = db.tickers.find(
        {'symbol' : symbol}
    )
    foundSupports = tickers.next()['supports']
    return foundSupports

def getResistancesForTicker(symbol):
    tickers = db.tickers.find(
        {'symbol' : symbol}
    )
    foundResistances = tickers.next()['resistances']
    return foundResistances

def getRecordForTicker(symbol):
    cursor = db.tickers.find(
        {'symbol' : symbol}
    )
    try:
        return cursor.next()
    except StopIteration:
        return None
