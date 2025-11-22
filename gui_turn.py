import tkinter as tk
from tkinter import scrolledtext

#gui for the instant messaging chat
class AIMTurnWindow:
    def __init__(self, master, screen_name="User", buddy_name="Buddy"):
        self.master = master
        self.screen_name = screen_name
        self.buddy_name = buddy_name

        self.on_send_callback = None  # set by server/client to send over socket

        master.title("Instant Message")
        master.geometry("460x450")
        master.minsize(460, 450)
        master.configure(bg="#C0C7D6")

#designs
        #top title bar
        self.title_bar = tk.Label(
            master,
            text=f"  {screen_name} - Instant Message",
            bg="#274CAA",
            fg="white",
            anchor="w",
            font=("Times New Roman", 11, "bold")
        )
        self.title_bar.pack(fill="x")

        #"file menu"
        self.menu_bar = tk.Frame(master, bg="#C0C7D6")
        self.menu_bar.pack(fill="x")

        for label in ["File", "Edit", "View", "People"]:
            tk.Label(
                self.menu_bar, text=label,
                bg="#C0C7D6", fg="black",
                font=("Times New Roman", 12)
            ).pack(side="left", padx=6, pady=2)

        tk.Frame(self.menu_bar, bg="#C0C7D6").pack(side="left", expand=True)

        self.warn_label = tk.Label(
            self.menu_bar,
            text=f"{screen_name}'s Warning Level 0%",
            bg="#C0C7D6",
            fg="black",
            font=("Times New Roman", 10)
        )
        self.warn_label.pack(side="right", padx=10)

        #chat display area 
        self.chat_frame = tk.Frame(master, bg="#C0C7D6")
        self.chat_frame.pack(padx=5, pady=(4, 2), fill="both", expand=True)

        self.chat_area = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            bg="white",
            fg="black",
            font=("Times New Roman", 12),
            height=10
        )
        self.chat_area.pack(fill="both", expand=True, padx=5, pady=(2, 0))
        self.chat_area.config(state=tk.DISABLED, relief="sunken", borderwidth=2)

        #colors for fonts and tags
        self.chat_area.tag_config("server",   foreground="#CC0000", font=("Times New Roman", 10, "bold"))
        self.chat_area.tag_config("client", foreground="#000080", font=("Times New Roman", 10, "bold"))
        self.chat_area.tag_config("system", foreground="#555555", font=("Times New Roman", 9, "italic"))
        self.chat_area.tag_config("body", foreground="#000000", font=("Times New Roman", 10))

        #separator line
        tk.Frame(master, bg="#C0C7D6", height=2).pack(fill="x", pady=(2, 0))

        #"toolbar"
        self.toolbar = tk.Frame(master, bg="#C0C7D6", height=26)
        self.toolbar.pack(fill="x", padx=5, pady=(2, 0))

        #just for looks 
        toolbar_buttons = [
            ("A↓", lambda: None),
            ("A↑", lambda: None),
            ("B",  lambda: None),
            ("I",  lambda: None),
            ("U",  lambda: None),
            ("link", lambda: None),
            ("🖼️", lambda: self.insert_text("🖼️")), 
            ("🙂", lambda: self.insert_text("🙂")),  
        ]

        for text, cmd in toolbar_buttons:
            tk.Button(
                self.toolbar,
                text=text,
                command=cmd,
                relief="flat",
                bg="#C0C7D6",
                activebackground="#C0C7D6",
                width=3
            ).pack(side="left", padx=2, pady=2)

        #text input box 
        self.input_box = tk.Text(
            master,
            height=3,
            bg="white",
            font=("Times New Roman", 10),
            wrap=tk.WORD
        )
        self.input_box.pack(fill="x", padx=5, pady=(0, 2))

        #bottom buttons bar 
        self.bottom_bar = tk.Frame(master, bg="#C0C7D6")
        self.bottom_bar.pack(fill="x", pady=(0, 6), side="bottom")

        #talk and info buttons just for looks 
        self.talk_btn = tk.Button(
            self.bottom_bar,
            text="Talk",
            bg="#C0C7D6",
            relief="raised",
            width=9
        )
        self.talk_btn.pack(side="left", padx=20, pady=4)

        self.info_btn = tk.Button(
            self.bottom_bar,
            text="Info",
            bg="#C0C7D6",
            relief="raised",
            width=9
        )
        self.info_btn.pack(side="left", padx=20, pady=4)

        #send button that is functional 
        self.send_btn = tk.Button(
            self.bottom_bar,
            text="Send",
            width=9,
            bg="#C0C7D6",
            relief="raised",
            command=self.send_message
        )
        self.send_btn.pack(side="right", padx=20, pady=4)

        #newlines
        master.bind("<Return>", self._on_enter)

        #enabling typing for whoever turn it is 
        # self.set_send_enabled(True)
        self.insert_message("System", "Type # to end your turn. Type Exit to end the chat.")


#functions

    #insert text in input box 
    def insert_text(self, text):
        self.input_box.insert(tk.INSERT, text)

    #enable/disable send button and input box
    def set_send_enabled(self, enabled: bool):
        print("[GUI] set_send_enabled?", enabled)   #testing

        state = tk.NORMAL if enabled else tk.DISABLED
        self.input_box.config(state=state)
        self.send_btn.config(state=state)

        if enabled:
            self.input_box.focus_set()  #attempt at fixing a bug 

    #insert message in chat area, how it looks depends on sender
    def insert_message(self, sender, text):
        self.chat_area.config(state=tk.NORMAL)

        if sender == "System":
            self.chat_area.insert("end", f"{text}\n", "system")
        else:
            if sender == self.screen_name:
                tag = "server"
                label = self.screen_name
            else:
                tag = "client"
                label = self.buddy_name if sender != self.screen_name else sender

            self.chat_area.insert("end", f"{label}: ", tag)
            self.chat_area.insert("end", text + "\n", "body")

        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview("end")

    #send message function
    def send_message(self):
        msg = self.input_box.get("1.0", "end").strip()
        if msg == "":
            return

        #show message locally
        self.insert_message(self.screen_name, msg)
        self.input_box.delete("1.0", "end")

        #send over connection
        if self.on_send_callback:
            self.on_send_callback(msg)

    #must not be empty, enter key sends message
    def _on_enter(self, event):
        msg = self.input_box.get("1.0", "end").strip()
        if msg != "":
            self.send_message()
        return "break"