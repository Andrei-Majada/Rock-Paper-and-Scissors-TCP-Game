# -*- coding: utf-8 -*-
import socket
from _thread import *
import pickle
from game import Game

server = "IP ADDRESS"
port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((server, port))

s.listen(2)
print("Rodando na porta: ", port)

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Conexão perdida")
    try:
        del games[gameId]
        print("Fechando jogo", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connectado ao socket:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Criando partida: ", gameId)
    else:
        games[gameId].start = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))