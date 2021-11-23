import telepot # module to cope telegramm API
token = '2133949865:AAHxfsbCt0HlKD5QocwR7l2SW17cKpyxp1s' # bot token
TGbot = telepot.Bot(token) # creating bot object

def getmessages(last_upd_id):
    """ function to recieve updates and extract messages from them"""
    chat = 0
    inp =  None
    messages = []
    updates = TGbot.getUpdates(last_upd_id+1)
    for update in updates:
        last_upd_id = update['update_id']
        # condition below checks if received update contains NOT a message
        if not ('message' in update.keys()) \
                or not ('text' in update['message'].keys()):
            return [], last_upd_id, 0
        chat = update['message']['chat']['id']
       # messageid = update['message']['message_id'] going to use later for
                            # answering messages with citation
        messages.append(update['message']['text'])
    return messages, last_upd_id, chat

def you_d(message):
    """ function for 'dog-kidding' """
    verbsends = ['ил', 'ул', 'ел', 'ал'] # list of possible verbends
    if message.lower().find("я бы") != -1:  # cheking if user talkes about
                                                    #"something he'd do"
        cutmessage = message[message.lower().find("я бы"):]
        for word in cutmessage.split():
            if word[-2:] in verbsends: #finding in message the verb, defining
                                            # what exactly the user would do
                return 'ты бы и собаку {}'.format(word) #and returning the
                               # message, that user'll do it even with the dog
    return None # and returning None othervise

def wearing(message):
    """function for 'misspelling joke' """
    #dictionary of misspelling and correct spelling
    wear = {'одел' : 'надел', 'одену' : 'надену', 'одевать' : 'надевать', \
           'одевал' : 'надевал', 'одеваю' : 'надеваю', 'одето' : 'надето', \
           'одевала' : 'надевала', 'одела' : 'надела', 'одеть' : 'надеть'\
            }
    for word in message.split():
        #looking for misspelling and returning correct word
        print(word)
        print(wear[word])
        if word.lower() in wear.keys(): return wear[word.lower()]
    return None   #or returning None otherwise

lastmessageid, chatid = 0, 0
while True: #continiously checking for new updates
    messageslist, lastmessageid, chatid = getmessages(lastmessageid)
    if messageslist != []: #if an update contains a message
        # - iterating trough them, trying to joke
        for message in messageslist:
            # trying to make 'dog joke'
            print(message)
            if you_d(message): TGbot.sendMessage(chatid, you_d(message))
            # truing to make 'misspelling joke'
            elif wearing(message): TGbot.sendMessage(chatid, wearing(message))
