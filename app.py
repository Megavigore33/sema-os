from flask import Flask, request, redirect, url_for
from views.fragments import nomClient, pingResult, debitResult, netscanResult, pingHistory, publicIPFile
from scripts.network_scanner import scan, translate_result
import subprocess
import datetime

server = Flask(__name__)

@server.route('/', methods=['GET'])
def rootpath():
    return redirect('/home')

@server.route('/home', methods=['GET'])
@server.route('/home/<typeToShow>', methods=['GET'])
def index(typeToShow = ""):
    
    clName = nomClient()
    
    if request.method == "GET":
        
        if typeToShow == "home":
            dl = bytes()
            up = bytes()
        
        if typeToShow == "debit":
            open("output/debit.txt", "w").truncate(0)
            subprocess.run(["python3 scripts/testdebit.py"], shell=True)
            
            #return redirect(url_for('index', typeToShow = "debit"))
        
        if typeToShow == "ping":
            open("output/pinglist.txt", "w").truncate(0)
            ping = subprocess.check_output("ping -c 5 8.8.8.8 | tail -1 | awk '{print $4}' | cut -d '/' -f 2", shell=True)
            goodping = ping.decode()
            firstnow = datetime.datetime.now()
            now = (firstnow.strftime("%Y-%m-%d %H:%M:%S"))

            filename = "output/pinglist.txt"

            with open(filename, 'a') as f:
                f.write(f'Date : {now} \n')
                f.write(f'| Ping : {goodping} \n')
                
        if typeToShow == "iprefresh":
            open("output/publicip.txt", "w").truncate(0)
            ip = subprocess.check_output("curl -s http://monip.org | sed -n 's/.*IP : \([0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\).*/\1/p'")
            filename = "output/publicip.txt"

            with open(filename, 'a') as f:
                f.write(f'{ip} \n')
                
            #return redirect(url_for('index',typeToShow = "ping"))

    # if request.method == "POST":
    #     if typeToShow == "Ping":
    #         ping = subprocess.check_output("ping -c 5 8.8.8.8 | tail -1 | awk '{print $4}' | cut -d '/' -f 2", shell=True)
    #         goodping = ping.decode()
    #         firstnow = datetime.datetime.now()
    #         now = (firstnow.strftime("%Y-%m-%d %H:%M:%S"))

    #         filename = "./output/pinglist.txt"

    #         with open(filename, 'a') as f:
    #             f.write(f'Date : {now} \n')
    #             f.write(f'Ping : {goodping} \n')
                
    #         return redirect('/',typeToShow = "ping")
    
    pingString = pingResult()
    debitString = debitResult()
    publicIP = publicIPFile()
    
    html = '''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="style.css">
            <title>Tableau de bord</title>
        </head>
        <body>
            <div>
                <h1>SemaBox - ''' + clName + '''</h1>
                <h4><a class="c" href="/home/iprefresh">IP Publique</a> : </h4><p>''' + publicIP + '''</p><br>
                <button><a class="c" href="/netscan">Scan</a></button>
                <button><a class="c" href="/home/debit">Débit</a></button>
                <button><a class="c" href="/home/ping">Ping</a></button>
                <h5><a class="c" href="/ping-history">Historique de ping</a></h5>
                <p> Ping : ''' + pingString + '''
                <p> Débit : ''' + debitString + '''
            <div>
        </body>
    </html>
    ''' 
    return html


@server.route('/netscan', methods=['GET', 'POST'])
def netscanPage():
    if request.method == "POST":
        open("output/netscan.txt", "w").truncate(0)
        portsString = request.form['portsInput'].split()
        portsInt = []
        for i in portsString:
            portsInt.append(int(i))
        ipaddr = request.form['IPInput']
        result = scan(ipaddr, portsInt)
        # netscanData = create_result(result)
        translate_result(result)
        
        return redirect(url_for('netscanPage'))
    
    
    data = netscanResult()
    
    html = '''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tableau de bord - Netscan</title>
        </head>
        <body>
            <div>
                <h1>NetScan</h1>
                <form action = "http://localhost:5000/netscan" method = "post">
                    <p>Saisir votre IP et un ou des ports à vérifier (séparés par des espaces) :</p>
                    <p><input type = "text" placeholder = "IP" name = "IPInput" /></p>
                    <p><input type = "text" name = "portsInput" /></p>
                    <p><input type = "submit" value = "Lancer scan" /></p>
                    <p>Résultat :</p>
                    <textarea name="result" rows="8", cols="66"> ''' + data + ''' </textarea>
                    <br><br>
                    <p><a class="c" href="/home">Revenir à l'accueil</a></p>
                </form>
            <div>
        </body>
    </html>
    ''' 
    return html

@server.route('/ping-history', methods=['GET'])
def pingHistoryPage():
    
    data = pingHistory()
    
    html = '''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tableau de bord</title>
        </head>
        <body>
            <div>
                <h3>Historique de ping :</h3>
                <textarea rows="12", cols="88">''' + data + ''' </textarea>
                </form>
            <div>
        </body>
    </html>
    ''' 
    return html
    