# AOL_IM
AOL Style Instant Messenger that can communicate across two devices connected to the same local network.

## Overview
This project implements a **turn-based TCP Instant Messaging (IM) system**, following classic AOL-style chat behavior. Two users communicate across a network connection, taking turns typing messages until both exchange the `"Exit"` command.

This version includes a fully custom **Graphical User Interface (GUI)** for both users, which satisfies the assignment’s **GUI bonus requirement**.

---

## Features
- **Turn-based messaging** using `#` to switch turns  
- **Exit command** to end the chat only when *both* users send `"Exit"`  
- **TCP socket networking**  
- **Two different user programs (server + client)**  
- **Works across two separate computers on the same LAN**  
- **Full GUI** with styling, scrollback, and disabled/enabled typing  
- **AOL-themed look and feel**

---

## Files
### 1. `server_turn.py`
- Implements **User1**
- Acts as the server: listens for incoming TCP connections  
- Receives messages until `#`, then enables its own turn  
- Supports “Exit” logic and closes when both users exit

### 2. `client_turn.py`
- Implements **User2**
- Connects to User1’s LAN IP address  
- Starts the chat (first turn)  
- Sends messages until `#`, then waits  
- Supports “Exit” logic

### 3. `gui_turn.py`
- Builds the full AOL-style GUI  
- Text display with scrollback  
- Disabled input during other user’s turn  
- `insert_message()` for incoming messages  
- `set_send_enabled()` for turn enforcement  
- Sends text through `on_send_callback`

**`client.py`, `server.py`, and `gui.py` can be used instead for a more AOL Instant Messenger experience, without the need to use # or Exit, and allows for text editing and emoji menu. Add LAN IP in `client.py`.**
---

## Network Setup (Two Different Computers)
This system works on **any two devices** connected to the **same WiFi/LAN network**.

### 1. Find the server’s LAN IP
On macOS:
```bash
ifconfig
```
Look for something like:
```
inet 192.168.x.x
```
2. Set the client IP

In client_turn.py, edit:
```
SERVER_IP = "192.168.x.x"
```
3. Run the server
```
python3 server_turn.py
```
4. Run the client
```
python3 client_turn.py
```
Message Flow
End your turn:
```
#
```
End the conversation:
```
Exit
```