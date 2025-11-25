import socket   #tcp communication
import threading    #threading for concurrent receive/send
import tkinter as tk    #gui
from gui import AIMChatWindow

SERVER_IP = "192.168.1.164"  #set to local for now for testing
PORT = 1234
mode = "send"

# create tcp server socket and connect to client at ip address and port 
def start_server(chat_window, my_name):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, PORT))#set to local now for testing
    server_socket.listen(3)  #listen for incoming connections, max 3 queued connections

    print("Waiting for clients to connect........")
    connection, address = server_socket.accept()    #accept incoming connection from client
    buddy_name = connection.recv(1024).decode()  #receive buddy name from client
    chat_window.update_buddy_name(buddy_name)   #update chat window with buddy name
    connection.send(my_name.encode())
    print(f"Connected to IP:Port {address}")

    # receiving thread, listens for messages from client
    def receive_loop():
        while True:
            try:
                data = connection.recv(1024).decode()   #buffer size 1024 bytes, waits for data from client, decodes to string
                if not data:
                    break
                chat_window.insert_message(chat_window.buddy_name, data)  #display message in chat window
                if data == "Exit":                          #if client sent Exit, close connection    
                    break
            except:
                break                                       #on error, exit loop

    threading.Thread(target=receive_loop, daemon=True).start() #start receiving thread, closes when program is exited

    def send_message(msg):
        connection.send(msg.encode())   #send message to client, encoded to bytes
        if msg == "Exit":            #if Exit is sent, close connection
            connection.close()

    chat_window.on_send_callback = send_message    #set send callback for chat window when Send button is clicked


#run gui and server
root = tk.Tk()
window = AIMChatWindow(root, "xxHEATHERxx (Server)")

threading.Thread(       #start server in separate thread
    target=start_server,
    args=(window, "xxHEATHERxx (Server)"),  #my_name 
    daemon=True
).start()
root.mainloop() #start Tkinter event loop and wait for user to send messages or close window
