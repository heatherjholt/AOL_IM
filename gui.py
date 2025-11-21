#https://www.geeksforgeeks.org/python/python-gui-tkinter/
#https://realpython.com/python-gui-tkinter/
import tkinter as tk
from tkinter import scrolledtext

class AIMChatWindow:
    def __init__(self, master, screen_name="User"):
        self.buddy_name = None
        self.master = master
        master.title("Instant Message")
        master.geometry("460x450")
        master.minsize(460, 450)
        master.configure(bg="#C0C7D6")


        #load SEND icon
        try:
            self.send_icon = tk.PhotoImage(file="icons/send.png")
        except:
            self.send_icon = None

    #top/header blue bar
        self.title_bar = tk.Label(
            master,
            text=f"  {screen_name} - Instant Message",
            bg="#274CAA",
            fg="white",
            anchor="w",
            font=("Times New Roman", 11, "bold")
        )
        self.title_bar.pack(fill="x")



    #menu strip
        self.menu_bar = tk.Frame(master, bg="#C0C7D6")
        self.menu_bar.pack(fill="x")

        for label in ["File", "Edit", "View", "People"]:
            tk.Label(
                self.menu_bar, text=label,
                bg="#C0C7D6", fg="black",
                font=("Times New Roman", 12)
            ).pack(side="left", padx=6, pady=2)

        tk.Frame(self.menu_bar, bg="#C0C7D6").pack(side="left", expand=True)

    #warning level label on right
        self.warn_label = tk.Label(
            self.menu_bar,
            text=f"{screen_name}'s Warning Level 0%",
            bg="#C0C7D6",
            fg="black",
            font=("Times New Roman", 10)
        )
        self.warn_label.pack(side="right", padx=10)


    #chat area 
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

    #colors for messages
        self.chat_area.tag_config("me",   foreground="#CC0000", font=("Times New Roman", 10, "bold"))
        self.chat_area.tag_config("them", foreground="#000080", font=("Times New Roman", 10, "bold"))
        self.chat_area.tag_config("body", foreground="#000000", font=("Times New Roman", 10))

        def make_font_tag(size, bold=False, italic=False, underline=False):
            style = ""
            if bold: style += "bold"
            if italic: style += " italic"
            if underline: style += " underline"
            return ("Times New Roman", size, style.strip())

    #separator line
        tk.Frame(master, bg="#C0C7D6", height=2).pack(fill="x", pady=(2, 0))

    #toolbar
        self.toolbar = tk.Frame(master, bg="#C0C7D6", height=26)
        self.toolbar.pack(fill="x", padx=5, pady=(2, 0))

        #small font
        self.small_font_btn = tk.Button(
            self.toolbar, text="A↓", command=self.font_smaller,
            relief="flat", bg="#C0C7D6", activebackground="#C0C7D6", width=3
        )
        self.small_font_btn.pack(side="left", padx=2, pady=2)

        #big font
        self.big_font_btn = tk.Button(
            self.toolbar, text="A↑", command=self.font_bigger,
            relief="flat", bg="#C0C7D6", activebackground="#C0C7D6", width=3
        )
        self.big_font_btn.pack(side="left", padx=2, pady=2)

        #bold
        self.bold_btn = tk.Button(
            self.toolbar, text="B", command=self.toggle_bold,
            relief="raised", bg="#C0C7D6", activebackground="#C0C7D6", width=3
        )
        self.bold_btn.pack(side="left", padx=2, pady=2)

        #italic
        self.italic_btn = tk.Button(
            self.toolbar, text="I", command=self.toggle_italic,
            relief="raised", bg="#C0C7D6", activebackground="#C0C7D6", width=3
        )
        self.italic_btn.pack(side="left", padx=2, pady=2)

        #underline
        self.underline_btn = tk.Button(
            self.toolbar, text="U", command=self.toggle_underline,
            relief="raised", bg="#C0C7D6", activebackground="#C0C7D6", width=3
        )
        self.underline_btn.pack(side="left", padx=2, pady=2)

        #link
        self.link_btn = tk.Button(
            self.toolbar, text="link", command=self.insert_link,
            relief="flat", bg="#C0C7D6", activebackground="#C0C7D6", width=4
        )
        self.link_btn.pack(side="left", padx=4, pady=2)

        #picture emo
        self.static_emoji_btn = tk.Button(
            self.toolbar,
            text="🖼️",  
            font=("Segoe UI Emoji", 14),
            width=2,
            height=1,
            relief="flat",
            bg="#C0C7D6",
            activebackground="#C0C7D6",
            command=lambda: self.insert_emoji("🖼️")
        )
        self.static_emoji_btn.pack(side="left", padx=2, pady=2)

        #emo popup
        self.emoji_btn = tk.Button(
            self.toolbar,
            text="😊",
            font=("Times New Roman", 12),
            relief="flat",
            command=self.open_emoji_popup,
            bg="#C0C7D6", activebackground="#C0C7D6",
            width=3
        )
        self.emoji_btn.pack(side="left", padx=2, pady=2)


    #input box
        self.input_box = tk.Text(
            master,
            height=3,
            bg="white",
            font=("Times New Roman", 10),
            wrap=tk.WORD
        )
        self.input_box.bind("<KeyRelease>", self.apply_live_formatting)

        self.input_box.pack(fill="x", padx=5, pady=(0, 2))

    #fomatting system
        self.input_box.tag_config("bold", font=("Times New Roman", 10, "bold"))
        self.input_box.tag_config("italic", font=("Times New Roman", 10, "italic"))
        self.input_box.tag_config("underline", font=("Times New Roman", 10, "underline"))

        self.bold_on = False
        self.italic_on = False
        self.underline_on = False
        self.font_size = 12

    #bottom button bar 
        self.bottom_bar = tk.Frame(master, bg="#C0C7D6")
        self.bottom_bar.pack(fill="x", pady=(0, 6), side="bottom")


        #TALK and INFO icons
        try:
            self.talk_icon = tk.PhotoImage(file="icons/talk.png").subsample(3, 3)
        except:
            self.talk_icon = None

        try:
            self.info_icon = tk.PhotoImage(file="icons/info.png").subsample(3, 3)
        except:
            self.info_icon = None

        #SEND button
        if self.send_icon:
            self.send_icon = self.send_icon.subsample(3, 3)

        #TALK button
        if self.talk_icon:
            self.talk_btn = tk.Button(
                self.bottom_bar,
                image=self.talk_icon,
                bg="#C0C7D6",
                relief="flat",
                borderwidth=0,
                activebackground="#C0C7D6"
            )
        else:
            self.talk_btn = tk.Button(
                self.bottom_bar,
                text="Talk",
                bg="#C0C7D6",
                relief="raised"
            )
        self.talk_btn.pack(side="left", padx=20, pady=4)

        #INFO button
        if self.info_icon:
            self.info_btn = tk.Button(
                self.bottom_bar,
                image=self.info_icon,
                bg="#C0C7D6",
                relief="flat",
                borderwidth=0,
                activebackground="#C0C7D6"
            )
        else:
            self.info_btn = tk.Button(
                self.bottom_bar,
                text="Info",
                bg="#C0C7D6",
                relief="raised"
            )
        self.info_btn.pack(side="left", padx=20, pady=4)

        #SEND button right side
        if self.send_icon:
            self.send_btn = tk.Button(
                self.bottom_bar,
                image=self.send_icon,
                bg="#C0C7D6",
                relief="flat",
                borderwidth=0,
                activebackground="#C0C7D6",
                command=self.send_message
            )
        else:
            self.send_btn = tk.Button(
                self.bottom_bar,
                text="Send",
                width=9,
                bg="#C0C7D6",
                relief="raised",
                command=self.send_message
            )

        self.send_btn.pack(side="right", padx=20, pady=4)


    #messaging callback
        self.on_send_callback = None

    #AIM screenname
        self.screen_name = screen_name

    #newline
        master.bind("<Return>", self._on_enter)

    #message 
    def insert_message(self, sender, raw_text):
        self.chat_area.config(state=tk.NORMAL)

    #sender label 
        if sender == self.screen_name:
            self.chat_area.insert("end", f"{self.screen_name}: ", "me")
        else:
            self.chat_area.insert("end", f"{self.buddy_name}: ", "them")

    #message body with formatting
        self.parse_and_insert(sender, raw_text)

    #send message
    def send_message(self):
        msg = self.input_box.get("1.0", tk.END).strip()
        if msg == "":
            return

        formatted_msg = msg

        #formatting tags
        if self.bold_on:
            formatted_msg = f"<b>{formatted_msg}</b>"
        if self.italic_on:
            formatted_msg = f"<i>{formatted_msg}</i>"
        if self.underline_on:
            formatted_msg = f"<u>{formatted_msg}</u>"
        formatted_msg = f"<size={self.font_size}>{formatted_msg}</size>"

        self.insert_message(self.screen_name, formatted_msg)
        self.input_box.delete("1.0", tk.END)

        if self.on_send_callback:
            self.on_send_callback(formatted_msg)

    #newline handler
    def _on_enter(self, event):
        if event.state & 0x0001:  
            return
        self.send_message()
        return "break"
    
    def update_buddy_name(self, buddy):
        self.buddy_name = buddy
        self.warn_label.config(text=f"{buddy}'s Warning Level 0%")


#emo buttons :)
    def open_emoji_popup(self):
        #popup behaviors
        if hasattr(self, "emoji_window") and self.emoji_window.winfo_exists():
            return

        self.emoji_window = tk.Toplevel(self.master)
        self.emoji_window.title("Emojis")
        self.emoji_window.geometry("200x220")
        self.emoji_window.configure(bg="#ECECEC")
        self.emoji_window.resizable(False, False)

        emojis = [
            "😀", "😁", "😂", "🤣", "😅", "😊", 
            "😍", "😘", "😎", "🤓", "🤠", "😴",
            "😢", "😭", "😡", "🤬", "😱", "🤯",
            "👍", "👎", "🙏", "👏", "🔥", "💀",
        ]

        #grid
        row = 0
        col = 0
        for emo in emojis:
            btn = tk.Button(
                self.emoji_window,
                text=emo,
                font=("Times New Roman", 16),
                width=2,
                relief="flat",
                bg="#ECECEC",
                command=lambda e=emo: self.insert_emoji(e)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)

            col += 1
            if col == 4:  # 4 emojis per row
                col = 0
                row += 1

        #close popup behaviors
        self.emoji_window.transient(self.master)
        self.emoji_window.grab_set()

#insert emojis when mouse is over box
    def insert_emoji(self, emoji="🙂"):
        self.input_box.insert(tk.INSERT, emoji)

        #close popup behaviors
        if hasattr(self, "emoji_window") and self.emoji_window.winfo_exists():
            self.emoji_window.destroy()


#font editing functions
    #bold
    def toggle_bold(self):
        self.bold_on = not self.bold_on
        self.bold_btn.config(relief="sunken" if self.bold_on else "raised")
        self.apply_formatting()

    #italic
    def toggle_italic(self):
        self.italic_on = not self.italic_on
        self.italic_btn.config(relief="sunken" if self.italic_on else "raised")
        self.apply_formatting()

    #underline
    def toggle_underline(self):
        self.underline_on = not self.underline_on
        self.underline_btn.config(relief="sunken" if self.underline_on else "raised")
        self.apply_formatting()

    #big font
    def font_bigger(self):
        self.font_size += 1
        self.apply_formatting()

    #small font
    def font_smaller(self):
        if self.font_size > 3:
            self.font_size -= 1
        self.apply_formatting()

    #link
    def insert_link(self):
        self.input_box.insert(tk.INSERT, "http://")

    def apply_formatting(self):
        #font size update
        self.input_box.config(font=("Times New Roman", self.font_size))

        self.update_input_tags()

        #highlight buttons
        self.bold_btn.config(bg="#A0A0A0" if self.bold_on else "#C0C7D6")
        self.italic_btn.config(bg="#A0A0A0" if self.italic_on else "#C0C7D6")
        self.underline_btn.config(bg="#A0A0A0" if self.underline_on else "#C0C7D6")

    def apply_live_formatting(self, event=None):
        self.update_input_tags()
        #remove tags
        self.input_box.tag_remove("bold", "1.0", "end")
        self.input_box.tag_remove("italic", "1.0", "end")
        self.input_box.tag_remove("underline", "1.0", "end")

        #styles for current 
        if self.bold_on:
            self.input_box.tag_add("bold", "1.0", "end")
        if self.italic_on:
            self.input_box.tag_add("italic", "1.0", "end")
        if self.underline_on:
            self.input_box.tag_add("underline", "1.0", "end")

    def update_input_tags(self):
        size = self.font_size
        self.input_box.tag_config("bold", font=("Times New Roman", size, "bold"))
        self.input_box.tag_config("italic", font=("Times New Roman", size, "italic"))
        self.input_box.tag_config("underline", font=("Times New Roman", size, "underline"))

    #message parsing and inserting with formatting
    def parse_and_insert(self, sender, raw_text):
        self.chat_area.config(state=tk.NORMAL)

        pos = "end"

        #current formatting
        current_bold = False
        current_italic = False
        current_underline = False
        current_size = 12 

        i = 0
        while i < len(raw_text):

            # bold on
            if raw_text.startswith("<b>", i):
                current_bold = True
                i += 3
                continue

            # bold off
            if raw_text.startswith("</b>", i):
                current_bold = False
                i += 4
                continue

            # italic on
            if raw_text.startswith("<i>", i):
                current_italic = True
                i += 3
                continue

            # italic off
            if raw_text.startswith("</i>", i):
                current_italic = False
                i += 4
                continue

            # underline on
            if raw_text.startswith("<u>", i):
                current_underline = True
                i += 3
                continue

            # underline off
            if raw_text.startswith("</u>", i):
                current_underline = False
                i += 4
                continue

            # size on
            if raw_text.startswith("<size=", i):
                end = raw_text.find(">", i)
                current_size = int(raw_text[i+6:end])
                i = end + 1
                continue

            # size off
            if raw_text.startswith("</size>", i):
                current_size = 12
                i += 7
                continue

            # normal character
            ch = raw_text[i]

            #unique tag for custom format
            tag_name = f"f_{current_size}_{int(current_bold)}_{int(current_italic)}_{int(current_underline)}"

            #create tag if needed 
            if tag_name not in self.chat_area.tag_names():
                font_style = ""
                if current_bold:
                    font_style += "bold "
                if current_italic:
                    font_style += "italic "
                if current_underline:
                    font_style += "underline "

                self.chat_area.tag_config(
                    tag_name,
                    font=("Times New Roman", current_size, font_style.strip())
                )

            #insert character with tags
            self.chat_area.insert(pos, ch, tag_name)

            i += 1

        self.chat_area.insert(pos, "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview("end")
