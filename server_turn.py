import socket   #tcp socket for server
import threading    #threading for receive loop in gui
import tkinter as tk
from gui_turn import AIMTurnWindow

HOST = ""   #listens on all interfaces on network
PORT = 1234

SERVER_NAME = "xxHEATHERxx(Server)"
CLIENT_NAME = "HTMLRulezD00d(Client)"


def start_server(chat_window: AIMTurnWindow):
    my_turn = False      #server starts as False and waits for '#' from client
    i_sent_exit = False     #tracking Exit messages
    they_sent_exit = False  #tracking Exit messages

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)   #listen for 1 connection for now

    chat_window.insert_message("System", f"Waiting for connection on port {PORT}...")
    chat_window.set_send_enabled(False)

    conn, addr = s.accept()
    chat_window.insert_message("System", f"Connected to {addr[0]}:{addr[1]}")   #display message when client connects
    print("[SERVER] accepted connection")   #testing

#receiving message loop function
    def receive_loop():

        nonlocal i_sent_exit, they_sent_exit, my_turn
        print("[DEBUG] receive_loop my_turn before:", my_turn)  #testing
        print("[SERVER] receive loop started")   #testing

        while True:
            try:
                data = conn.recv(1024)
                print("[SERVER] recv:", data)
                if not data:
                    break

                text = data.decode()
                print("[SERVER] decode:", text)

            #loop for # for turn taking or Exit to end chat 
                if text == "Exit":
                    they_sent_exit = True
                    chat_window.insert_message(CLIENT_NAME, "Exit")
                    
                    if i_sent_exit:
                        chat_window.set_send_enabled(False)
                        break
                    
                    my_turn = True
                    chat_window.set_send_enabled(True)
                    continue

                if text == "#":
                    chat_window.insert_message(CLIENT_NAME, "#")
                    my_turn = True
                    chat_window.set_send_enabled(True)
                    continue

                chat_window.insert_message(CLIENT_NAME, text)   #display received message after checking for # or Exit and decoding 

            except Exception as e:
                print("[SERVER ERROR]", e)   #testing
                break

        conn.close()
        chat_window.set_send_enabled(False)
        chat_window.insert_message("System", "Server listener stopped.")    #if connection closes message

    threading.Thread(target=receive_loop, daemon=True).start()

#sending message loop function
    def send_callback(msg):
        nonlocal i_sent_exit, they_sent_exit, my_turn

        #checking for empty message
        if msg == "":
            return

        if not my_turn and msg != "Exit":
            print("[SERVER] It's not your turn to send messages.")   #testing
            return

        print("[SERVER] sending:", msg)     #testing
        conn.send(msg.encode()) #sending encoded message

        #checking for # for turn taking or Exit to end chat
        if msg == "Exit":
            i_sent_exit = True
            chat_window.set_send_enabled(False)

        if msg == "#":
            my_turn = False
            chat_window.set_send_enabled(False)

    chat_window.on_send_callback = send_callback

#runs gui
if __name__ == "__main__":
    root = tk.Tk()
    window = AIMTurnWindow(root, SERVER_NAME, CLIENT_NAME)
    threading.Thread(target=start_server, args=(window,), daemon=True).start()
    root.mainloop()
