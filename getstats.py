#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# masterserver parse from here: https://github.com/cwilkc/q3serverquery

import socket
import os
import re
import time

from tabulate import tabulate

DEBUG = False

test = b'\xff\xff\xff\xffgetserversResponse\\m\xe6\xef+\xad\x90\\\xd8\x0ep\xc8\xad\x99\\\x9fE \xac\xadp\\#\xf2\xff\xea\xadq\\[\xf0U\xd8\xad\x8e\\4\xc7\t4\xadr\\3\xc3\x8b\x07\xadp\\\x9fA\xa3\x95\xadq\\\xd8\x0ep\xc8\xadq\\N._\x9c\xadp\\\x03q\x1el\xadp\\\x9d\xf5\xe9"\xadq\\\xc3\x80g\xee\xadp\\4\xc7\t4\xadu\\\x9fA\xa3\x95\xads\\4\xc7\t4\xad\xa1\\4WdM\xad\xd5\\\xc3\xc9\xc5\x11\x13\x88\\Y\xa3\xf1*\xadp\\3\x0f-\x18\xad\xdf\\-O\x1e\xae\xadq\\m\xe6\xef\x87mo\\@5\xfd\xfd\xadp\\#\xee\x06c\xadp\\3\x0f-\x18\xad\xe1\\\xd8\x0ep\xc8\xadz\\\xc3\xc9\xc5\x11\x0f\xa0\\\xc3\xc9\xc5\x11\x1bX\\\xd8\x0ep\xc8\xadt\\\xd8\x0ep\xc8\xad\x7f\\\x9d\xf5\xe9"\xadr\\\xa1#JL\xadp\\3\xff\xaa\xa6\xadp\\M\xdd\x90\xf8\xadu\\t\xfb\xc0\xd4\xad\xb6\\Y\xcf\xdf\xca\xadq\\t\xfb\xc0\xd4\xd8\xd6\\\xd8\x0ep\xc8\xads\\t\xfb\xc0\xd4\xd8\xf4\\m\xe6\xef\x87l\xcf\\[\xf0U\xd8\xad\xd3\\\x03\x076\\\xadp\\m\xe6\xef+\xaf\xc7\\t\xfb\xc0\xd4\xd8\xe0\\\xd8\x0ep\xc8\xad\x80\\v\x1b\x1a]\xadp\\\xc3\xc9\xc5\x11\x17p\\t\xfb\xc0\xd4\xd8\xea\\\x97I\xd3h\xadp\\#\xf2\xff\xea\xadt\\\xc3\xc9\xc5\x11\x1f@\\\x0f\xce\xd0B\xadp\\-O\x1e\xae\xadp\\\xc3\xc9\xc5\x11\x07\xd0\\\xa0\x10\x82\xfa\xadp\\\xd8\x0ep\xc8\xady\\- \x90#\xadp\\YI\x13\x1f\xadp\\-O\x1e\xae\xadr\\\xd8\x0ep\xc8\xad\x81\\\x9fA\xa3\x95\xadp\\#\xf2\xff\xea\xads\\#\xee\x06c\xadq\\[\xf0U\xd8\xadt\\#\xee\x06c\xadr\\t\xcb>:\xadt\\[\xf0U\xd8\xadq\\3\x0f-\x18\xad\xde\\3\x0f-\x18\xad\xd9\\\xac\r\x84\xa7\xadp\\\xc3\xc9\xc5\x11#(\\\xc3\xc9\xc5\x11\'\x10\\t\xcb>:\xadq\\\xd8\x0ep\xc8\xadr\\\xad\xea\x1er\xadr\\t\xcb>:\xadp\\\x9fA\xa3\x95\xadt\\\xad\xea\x1er\xadq\\\x9fA\xa3\x95\xadv\\.e\xa5\x1d\xadp\\.e\xa5\x1d\xadq\\.e\xa5\x1d\xadr\\\xad\xea\x1er\xadp\\.e\xa5\x1d\xadt\\\xd8\x0ep\xc8\xadw\\.e\xa5\x1d\xadu\\\xd8\x0ep\xc8\xadx\\.e\xa5\x1d\xads\\\xd8\x0ep\xc8\xadu\\\xd8\x0ep\xc8\xadv\\\xd8\x0ep\xc8\xad|\\t\xcb>:\xadr\\M\xdd\x90\xf8\xadr\\t\xcb>:\xadu\\\xd8\x0ep\xc8\xad{\\t\xcb>:\xadv\\\x9fA\xa3\x95\xadu\\\xd8\x0ep\xc8\xad}\\t\xcb>:\xads\\\xd8\x0ep\xc8\xad\x82\\#\xf2\xff\xea\xadp\\t\xcbw\xd1\xadp\\#\xf2\xff\xea\xadr\\m\xe6\xef+\xad\xe9\\\x9d\xf5\xe9"\xadp\\\xd8\x0ep\xc8\xad~\\\x9d\xf5\rv\xadp\\\x9fA\xa3\x95\xadw\\M\xdd\x90\xf8\xadt\\M\xdd\x90\xf8\xads\\m\xe6\xef+\xadp\\M\xdd\x90\xf8\xadp\\EOT\x00\x00\x00'
testserver = b'\xff\xff\xff\xffstatusResponse\n\\challenge\\\\version\\2.10 x86_64 Jan  8 2020 Linux\\fs_game\\basewf\\g_antilag\\1\\g_gametypes_available\\\\g_instagib\\0\\g_match_score\\ OWLS: 6 RATS: 3\\g_match_time\\10:17\\g_needpass\\0\\g_race_gametype\\0\\gamedate\\Feb 10 2020\\gamename\\Warfork\\mapname\\cwM1\\protocol\\22\\sv_cheats\\0\\sv_hostname\\^0~^4~^0~^4~ ^7nightowl.pw | Clan Arena #1 ^0~^4~^0~^4~\\sv_http\\1\\sv_maxclients\\25\\sv_maxmvclients\\4\\sv_mm_enable\\0\\sv_mm_loginonly\\0\\sv_pps\\20\\sv_pure\\1\\sv_skilllevel\\1\\sv_skillRating\\0\\gametype\\nca\\clients\\6\n-9999 0 "^0Night^4Bot" 0\n-9999 20 "^8ph^0uck" 0\n6 21 "^2we^3ed" 3\n12 11 "Kry" 2\n16 9 "kmzu" 3\n5 37 "meh" 2\n'

INTERVAL = 1000

HOST = "master1.icy.gg"
HOST2 = "master1.forbidden.gg"
PORT = 27950

MYSERVER = '91.240.85.216'
MYPORT = 44401

challenge = ''

# master1.forbidden.gg master1.icy.gg (107.161.23.68) (27950)

def Debug(str):
    if (DEBUG):
        print(str)

class Forkstat:
    def __init__(self):
        self.status = {}
        self.servers = []

    def getserverinfo(self, servlist):
        message = ""
        cmd = b'\xFF\xFF\xFF\xFFgetstatus'
        for current in servlist:
            #print(current)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(1)
                s.sendto(cmd, current)
                try:
                    data, _ = s.recvfrom(4096)
                except socket.timeout:
                    continue
                s.close()
                Debug("received message: {}".format( (data) ))

            status_list = data[4:].split(b'\n')[1].split(b'\\')[1:]
            player_list = data[4:].split(b'\n')[2:-1]
            
            status_dct = {status_list[i]: status_list[i + 1] for i in range(0, len(status_list), 2)} 
            
            if ( int(status_dct[b"clients"].decode()) == 0 ):
                continue
            
            servername = re.sub('\^.','',status_dct[b"sv_hostname"].decode())
            gametype = ''
            if (int(status_dct[b"g_instagib"].decode())==1):
                gametype = 'i'
            player_table = []
            message += ("{}{} - `{}` - {} - {}/{}\n".format( 
                gametype, 
                status_dct[b"gametype"].decode(), 
                servername,
                status_dct[b"mapname"].decode(),
                status_dct[b"clients"].decode(),
                status_dct[b"sv_maxclients"].decode(),
                #status_dct[b"g_match_score"].decode(),
                ))
            #steam://connect/109.230.239.43:44521/privateowl
            message += ("steam://connect/{}:{}/\n".format(
                current[0],
                current[1]))
            
            #logfile.write("\tping\tscore\tname\n")
                
            for player in player_list:
                player_parse = player.decode().split(" ")
                # ignore 0 ping players
                # print("PING {}".format(player_parse[1]))
                if (int(player_parse[1]) == 0):
                    continue
                player_parse[0], player_parse[1] = player_parse[1], player_parse[0] 
                player_parse[2] = re.sub('\^.|\"','',player_parse[2])
                del player_parse[3]
                #logfile.write("\t{}\t{}\t{}\n".format(player_parse[1],
                #    player_parse[0],
                #    player_parse[2],
                #))
                player_table.append(player_parse)
            message += ("```C++\n" + tabulate(player_table, headers=['ping','score','name'], tablefmt="plain") + "```\n")
        with open("app.log", "w") as logfile:
            logfile.write(message)

    def getserverslist(self):
        cmd = b'\xFF\xFF\xFF\xFFgetservers Warfork 22 empty full'
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(1)
            s.sendto(cmd, (HOST2, PORT))
            try:
                data, _ = s.recvfrom(4096)
            except socket.timeout:
                return 1
            s.close()
            Debug("received message: {}".format( (data) ))
        for i in range(len(data)):
            try:
                if chr(data[i]) == '\\' and chr(data[i + 7]) == '\\':
                    ip_octets = []
                    for j in range(1, 5):
                        ip_octets.append(str(data[i + j]))

                    self.servers.append(
                        (
                            ".".join(ip_octets),
                            (data[i + 5]<<8) + data[i + 6]
                        )
                    )
            except IndexError:
                continue
        Debug(self.servers)
        return 0


if __name__ == "__main__":
    err = 0
    while(1):
        fs = Forkstat()
        err = fs.getserverslist()
        if (not err):
            fs.getserverinfo(fs.servers)
        time.sleep(10)


