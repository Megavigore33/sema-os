COLOR_CLASSES="wb"

def nomClient():
    with open("./output/nomClient.txt") as file:
        clName = file.read()
    return clName

def pingResult():
    with open("./output/pinglist.txt") as file:
        pingString = file.read()
    return pingString

def debitResult():
    with open("./output/debit.txt") as file:
        debitString = file.read()
    return debitString

def netscanResult():
    with open("./output/netscan.txt") as file:
        netscanString = file.read()
    return netscanString

def pingHistory():
    with open("/home/theo/pinglist.txt") as file:
        pinghString = file.read()
    return pinghString

def publicIPFile():
    with open("./output/publicip.txt") as file:
        publicIPString = file.read()
    return publicIPString