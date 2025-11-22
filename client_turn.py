import socket
import threading
import tkinter as tk
from gui_turn import AIMTurnWindow

SERVER_IP = "192.168.1.164" #change to SERVER's ip address
PORT = 1234

SERVER_NAME = "xxHEATHERxx(Server)"
CLIENT_NAME = "HTMLRulezD00d(Client)"


def start_client(chat_window: AIMTurnWindow):
    my_turn = True           #client starts as True and can send messages immediately
    i_sent_exit = False     #tracking Exit messages
    they_sent_exit = False  #tracking Exit messages

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #create socket then connect
    s.connect((SERVER_IP, PORT))    #connecting to server

    chat_window.insert_message("System", f"Connected to server {SERVER_IP}:{PORT}")    #display message when connected
    chat_window.set_send_enabled(True)      #enable sending messages immediately

#receiving message loop function
    def receive_loop():

        nonlocal i_sent_exit, they_sent_exit, my_turn
        print("[CLIENT] receive loop started")  #testing

        while True:
            try:
                data = s.recv(1024)
                print("[CLIENT] recv:", data)   #testing
                if not data:
                    print("[CLIENT] server disconnected")   #testing
                    break

                text = data.decode()
                print("[CLIENT] decode :", text)    #testing

            #loop for # for turn taking or Exit to end chat
                if text == "Exit":
                    they_sent_exit = True
                    chat_window.insert_message(SERVER_NAME, "Exit")
                    if i_sent_exit:
                        chat_window.set_send_enabled(False)
                        break
    

                    my_turn = True
                    chat_window.set_send_enabled(True)  #if server exits, client can still send until client Exit
                    continue

                if text == "#":
                    chat_window.insert_message(SERVER_NAME, "#")
                    my_turn = True
                    chat_window.set_send_enabled(True)
                    continue

                chat_window.insert_message(SERVER_NAME, text)   #display received message after checking for # or Exit and decoding 

            except Exception as e:
                print("[CLIENT ERROR]", e)   #testing   
                break

        s.close()
        chat_window.insert_message("System", "Client listener stopped.")    #if connection closes message   

    threading.Thread(target=receive_loop, daemon=True).start()  #threading for receive loop to not block gui

#sending message loop function
    def send_callback(msg):
        nonlocal i_sent_exit, they_sent_exit, my_turn

        #check for empty message
        if msg == "":
            return

        if not my_turn and msg != "Exit":
            print("[CLIENT] It's not your turn to send messages.")  #testing
            return

        print("[CLIENT] sending:", msg)  #testing
        s.send(msg.encode())    #sending encoded message

        #checking for # for turn taking or Exit to end chat
        if msg == "Exit":
            i_sent_exit = True
            chat_window.set_send_enabled(False)

        if msg == "#":
            my_turn = False
            chat_window.set_send_enabled(False)

    chat_window.on_send_callback = send_callback    #setting send callback for gui so message can be sent thru socket

#runs gui
if __name__ == "__main__":
    root = tk.Tk()
    window = AIMTurnWindow(root, CLIENT_NAME, SERVER_NAME)
    threading.Thread(target=start_client, args=(window,), daemon=True).start()
    root.mainloop()
