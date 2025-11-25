import socket   #tcp communication
import threading    #threading for concurrent receive/sendS
import tkinter as tk    #gui
from gui import AIMChatWindow

SERVER_IP = "192.168.1.164"  #set to local for now for testing, change to server ip to connect over lan network
PORT = 1234
mode = "send"

# create tcp client socket and connect to server at ip address and port 
def start_client(chat_window, my_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))    
    client_socket.send(my_name.encode())    #send my name to server for display
    server_name = client_socket.recv(1024).decode()
    chat_window.update_buddy_name(server_name)


    # receiving thread loop, listens for messages from server
    def receive_loop():
        while True:
            try:
                data = client_socket.recv(1024).decode()    #buffer size 1024 bytes, waits for data from server, decodes to string
                if not data:
                    break
                chat_window.insert_message(chat_window.buddy_name, data)  #display message in chat window
                if data == "Exit":                          #if server sent Exit, close connection
                    break
            except:
                break                                       #on error, exit loop

    threading.Thread(target=receive_loop, daemon=True).start()  #start receiving thread, closes when program is exited

    def send_message(msg):
        client_socket.send(msg.encode())     #send message to server, encoded to bytes
        if msg == "Exit":                   #if Exit is sent, close connection
            client_socket.close()

    chat_window.on_send_callback = send_message    #set send callback for chat window when Send button is clicked


#run gui and client 
root = tk.Tk()
window = AIMChatWindow(root, "HTMLRulezd00d (Client)")

threading.Thread(
    target=start_client,
    args=(window, "HTMLRulezD00d (Client)"),
    daemon=True
).start()
root.mainloop()  #start Tkinter event loop and wait for user to send messages or close window
