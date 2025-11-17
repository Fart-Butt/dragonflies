from mcrcon import MCRcon
import os
import MySQLdb
import datetime

killed=0
with MCRcon(os.environ['RCON_HOST'], os.environ['RCON_PASSWORD']) as mcr:
    resp=mcr.command("/kill @e[name='Dragonfly']")
    if resp.rstrip() == "No entity was found":
        killed=0
    elif resp.rstrip().split(" ")[0] == "Killed" and resp.rstrip().split(" ")[1] != "Dragonfly":
        killed=int(resp.rstrip().split(" ")[1])
    else:
        killed=1

if killed > 0:
    resp=mcr.command("/tell @a ZAP! buttbot zapped {} dragonflies".format(killed))

dbcon = MySQLdb.connect(host=os.environ['db_host'],
                        user=os.environ['db_username'],
                        passwd=os.environ['db_password'],
                        db=os.environ['db_name']
                        )
with dbcon.cursor() as cursor:
    cursor.execute("insert into `dragonflies` (`dt`, `killed`) VALUES (%s, %s)", (datetime.datetime.now(), killed))
dbcon.commit()