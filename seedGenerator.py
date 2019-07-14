import random

def generateSeed():
    chars=u'9ABCDEFGHIJKLMNOPQRSTUVWXYZ' #27 characters - max number you can express by one Tryte - do you remember?
    rndgenerator = random.SystemRandom() #cryptographically secure pseudo-random generator

    NewSeed = u''.join(rndgenerator.choice(chars) for _ in range(81)) #generating 81-chars long seed. This is Python 3.6+ compatible
    return NewSeed

def mein():
    generateSeed()

if __name__ == "__main__":
    main()
