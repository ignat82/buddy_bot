import telepot # module to cope telegramm API

def readtoken(pathtotokenfile):
    """function reading bot token from txt file"""
    token = input('input bot token or press ENTER to read it from {}: '\
                 .format(pathtotokenfile))
    if token == '': #if input is empty - reading token from file
        with open(pathtotokenfile, "r") as tokenfile:
            print('reading token from {}...'.format(pathtotokenfile))
            token = tokenfile.read()
    print('using token {}'.format(token))
    return token

def getmessages(last_upd_id):
    """ function to recieve updates and extract messages from them"""
    chat = 0
    inp =  None
    messages = []
    updates = TGbot.getUpdates(last_upd_id+1)
    for update in updates:
        last_upd_id = update['update_id']
        # if received update contains NOT a message, going to next update
        if not ('message' in update.keys()) \
                or not ('text' in update['message'].keys()): continue
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

def readdict(filepatch):
    """ function reading dictionary in format 'misspeled word':'correct one'\
    from csv file"""
    words = {}
    with open(filepatch, "r") as dictfile:
        for line in dictfile:
            #saving first word in line as key, and second without last symbol
            # (that is just \n) as value
            words[line.split(',')[0]] = line[:-1].split(',')[1]
        return words

def wearing(somemessage, wear):
    """function for 'misspelling joke' """
    for word in somemessage.split():
        #looking for misspelling and returning correct word
        if word.lower() in wear.keys(): return wear[word.lower()]
    return None   #or returning None otherwise


bottoken = readtoken('token.txt')
TGbot = telepot.Bot(bottoken) # creating bot object
weardict = readdict("telebotdict.csv") #reading misspelling dictionary from csv file
lastmessageid, chatid = 0, 0
while True: #continiously checking for new updates
    messageslist, lastmessageid, chatid = getmessages(lastmessageid)
    if messageslist != []: #if an update contains a message
        # - iterating trough them, trying to joke
        for message in messageslist:
            # trying to make 'dog joke'
            if you_d(message):
                TGbot.sendMessage(chatid, you_d(message))
            # truing to make 'misspelling joke'
            elif wearing(message, weardict):
                TGbot.sendMessage(chatid, wearing(message, weardict))
