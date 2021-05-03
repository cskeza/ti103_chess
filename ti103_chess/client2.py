import json

import socketio
import board
sio = socketio.Client(engineio_logger=True)
start_timer = None
partie = board.nouvelle_partie("2")

@sio.on('server response')
def handle_json(data):
    print('received data from broadcast: ' + data)
    print("TYPE OF RECEIVED DATA = ", type(data))
    update_move = json.loads(data)

    #Si l'autre client a envoyé les données, mettre à jour l'écran de déplacement et d'actualisation
    # sid ne sera pas égal si l'autre client l'a envoyé
    print("sio.sid",sio.sid)
    print("update_move[sid]", update_move["sid"])
    #Mettre à jour le déplacement -> si l'autre client l'a envoyé. c'est-à-dire que le sid ne sera pas égal
    if update_move["sid"] != sio.sid:
       partie.make_auto_move(update_move["move"])
       partie.update_screen()

if __name__ == '__main__':
    sio.connect('http://127.0.0.1:3000')
    print(sio.sid,"connected to server")
    while True:
        partie.jouer("Noir")
        print("played ")
        if partie.make_move:
            print("move made !!! ")
            data = partie.last_move + partie.move_coord
            sid_client = sio.sid
            print("SENDING SID ", sid_client)
            x = {"sid": sid_client, "move": str(data)}
            x_json = json.dumps(x)
            sio.emit('connected', x_json)




