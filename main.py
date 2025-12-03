from mcrcon import MCRcon
import os
import MySQLdb
import datetime
import random

df_killed=0
with MCRcon(os.environ['RCON_HOST'], os.environ['RCON_PASSWORD']) as mcr:
    resp=mcr.command("/kill @e[name='Dragonfly']")
    if resp.rstrip() == "No entity was found":
        df_killed=0
    elif resp.rstrip().split(" ")[0] == "Killed" and resp.rstrip().split(" ")[1] != "Dragonfly":
        df_killed=int(resp.rstrip().split(" ")[1])
    else:
        df_killed=1

ms_killed=0
with MCRcon(os.environ['RCON_HOST'], os.environ['RCON_PASSWORD']) as mcr:
    resp=mcr.command("/kill @e[name='entity.reliquified_ars_nouveau.magic_shell']")
    if resp.rstrip() == "No entity was found":
        ms_killed=0
    elif resp.rstrip().split(" ")[0] == "Killed" and resp.rstrip().split(" ")[1] != "entities":
        ms_killed=int(resp.rstrip().split(" ")[1])
    else:
        ms_killed=1

#confuse 'em
stuff=[
    "trees",
    "trains",
    "contraptions",
    "diamond ore",
    "bees",
    "players"
]

if random.randint(1,3) == 3:
    zap = ("/tell @a ZAP! buttbot zapped {} dragonflies, {} magic shells and {} {}"
           .format(df_killed, ms_killed, random.choice(stuff),random.randint(1,10)))
else:
    zap = "/tell @a ZAP! buttbot zapped {} dragonflies and {} magic shells".format(df_killed, ms_killed)
if df_killed > 0 or ms_killed > 0:
    with MCRcon(os.environ['RCON_HOST'], os.environ['RCON_PASSWORD']) as mcr:
        resp=mcr.command(zap)





dbcon = MySQLdb.connect(host=os.environ['db_host'],
                        user=os.environ['db_username'],
                        passwd=os.environ['db_password'],
                        db=os.environ['db_name']
                        )
with dbcon.cursor() as cursor:
    cursor.execute("insert into `dragonflies` (`dt`, `killed`) VALUES (%s, %s)", (datetime.datetime.now(), df_killed))
    cursor.execute("insert into `magic_shells` (`dt`, `killed`) VALUES (%s, %s)", (datetime.datetime.now(), ms_killed))
dbcon.commit()


