from src.client import Client
from src.server import Server
from src.message import createMessage
from pathlib import Path
import datetime
import argparse

import tkinter as tk
from tkinter import ttk, simpledialog

prompt = "\nWhat do you want to do? \n(1. sendmessage, 2. get all message, 3. get new (unread) messagges, 4. get convo, 5. exit): \n>"
prettyprint = "\n[>] From: {u} -> {t} \n[>] Time: {s} \n[>] Message: {m}"


class NonInstantMessenger:
    def __init__(self, master):
        self.master = master
        self.master.title("Non-Instant Messenger")
        self.master.geometry("1200x800")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Initialize username and recipient
        self.username = None
        self.recipient = None
        self.client = None
        self.partner = None
        self.address = "127.0.0.1"
        self.port = 8080

        self.all_messages = []

        # First tab for changing username
        self.username_tab = tk.Frame(self.notebook)
        self.notebook.add(self.username_tab, text="Change Username")
        self.create_set_username_tab()

        # Second tab for writing a message
        self.send_message_tab = tk.Frame(self.notebook)
        self.notebook.add(self.send_message_tab, text="Send message")
        self.create_send_message_tab()

        # Third tab for getting all messages
        self.get_all_messages_tab = tk.Frame(self.notebook)
        self.notebook.add(self.get_all_messages_tab, text="Get all messages")
        self.create_get_all_messages_tab()

        # Fourth tab for getting all unread messages
        self.get_unread_messages_tab = tk.Frame(self.notebook)
        self.notebook.add(self.get_unread_messages_tab, text="Get unread messages")
        self.create_get_unread_messages_tab()

        # Fifth tab for getting conversation by username
        self.get_conversation_tab = tk.Frame(self.notebook)
        self.notebook.add(self.get_conversation_tab, text="Get conversation messages")
        self.create_get_conversation_tab()


    def create_set_username_tab(self):
        # Label in the body of the tab
        label = tk.Label(self.username_tab, text="Plase enter your username:")
        label.pack(pady=10)

        # Text box to write the new username
        entry = tk.Entry(self.username_tab)
        entry.pack(pady=10)

        # Button to record the new username
        record_button = tk.Button(self.username_tab, text="Set Username", command=lambda: self.set_username(entry.get()))
        record_button.pack(pady=10)

    def create_send_message_tab(self):
        # Recipient label
        recipient_label = tk.Label(self.send_message_tab, text="Enter the recipient's username:")
        recipient_label.pack(pady=10)

        # Recipient text box
        recipient_entry = tk.Entry(self.send_message_tab)
        recipient_entry.pack(pady=10)

        # Button to record recipient username
        recipient_button = tk.Button(self.send_message_tab, text="Set Recipient", command=lambda: self.set_recipient(recipient_entry.get()))
        recipient_button.pack(pady=10)

        # Label in the body of the tab
        label = tk.Label(self.send_message_tab, text="Write your message:")
        label.pack(pady=10)

        # Text box to write the message
        text_box = tk.Text(self.send_message_tab, height=10, width=40)
        text_box.pack(pady=10)

        # Button to send the message
        send_button = tk.Button(self.send_message_tab, text="Send Message", command=lambda: self.send_message(text_box.get("1.0", tk.END)))
        send_button.pack(pady=20)


    def create_get_all_messages_tab(self):
        # Case 2: Get all messages
        # Label in the body of the tab
        self.all_messages_listbox = tk.Listbox(self.get_all_messages_tab, height=10, width=40)
        self.all_messages_listbox.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(self.get_all_messages_tab, orient=tk.VERTICAL, command=self.all_messages_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.all_messages_listbox.config(yscrollcommand=scrollbar.set)

        # Button to get all messages
        get_all_messages_button = tk.Button(self.get_all_messages_tab, text="Get all messages", command=lambda: self.get_all_messages())
        get_all_messages_button.pack(pady=20)


    def create_get_unread_messages_tab(self):
        # Case 3: Get all unread messages
        # Label in the body of the tab
        self.unread_messages_listbox = tk.Listbox(self.get_unread_messages_tab, height=10, width=40)
        self.unread_messages_listbox.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(self.get_unread_messages_tab, orient=tk.VERTICAL, command=self.unread_messages_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.unread_messages_listbox.config(yscrollcommand=scrollbar.set)

        # Button to get unread messages
        get_unread_messages_button = tk.Button(self.get_unread_messages_tab, text="Get unread messages", command=lambda: self.get_unread_messages())
        get_unread_messages_button.pack(pady=20)

    def create_get_conversation_tab(self):
        # Case 4: Get all conversation messages
        # Conversation partner label label
        convo_partner_label = tk.Label(self.get_conversation_tab, text="Enter the conversation partner's username:")
        convo_partner_label.pack(pady=10)

        # Partner entry
        partner_entry = tk.Entry(self.get_conversation_tab)
        partner_entry.pack(pady=10)

        # Button to record conversation partner username
        recipient_button = tk.Button(self.get_conversation_tab, text="Set Conversation Partner's Username", command=lambda: self.set_partner(partner_entry.get()))
        recipient_button.pack(pady=10)

        # Label in the body of the tab
        self.conversation_messages_listbox = tk.Listbox(self.get_conversation_tab, height=10, width=40)
        self.conversation_messages_listbox.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(self.get_conversation_tab, orient=tk.VERTICAL, command=self.conversation_messages_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.conversation_messages_listbox.config(yscrollcommand=scrollbar.set)

        # Button to get all messages
        conversation_messages_button = tk.Button(self.get_conversation_tab, text="Get conversation messages", command=lambda: self.get_conversation())
        conversation_messages_button.pack(pady=20)

    def set_username(self, new_username):
        # Record the new username
        if new_username.strip() == "":
            tk.messagebox.showwarning(title="Error", message="Please enter a username")
            return
        else:
            tk.messagebox.showinfo(title="Username recorded", message=f"New username recorded: {new_username}, initializing client...")
        self.username = new_username
        self.client = Client(self.username, self.address, self.port)
        self.client.connect()
        print(f"New username recorded: {new_username}")

    def set_recipient(self, recipient):
        # Record the new recipient
        if recipient.strip() == "":
            tk.messagebox.showwarning(title="Error", message="Please enter a recipient")
            return
        self.recipient = recipient
        tk.messagebox.showinfo(title="Recipient recorded", message=f"New recipient recorded: {recipient}")
        print(f"New recipient recorded: {recipient}")

    def set_partner(self, partner):
        # Record the new recipient
        if partner.strip() == "":
            tk.messagebox.showwarning(title="Error", message="Please enter a partner's username")
            return
        self.partner = partner
        tk.messagebox.showinfo(title="Partner recorded", message=f"New partner recorded: {partner}")
        print(f"New partner recorded: {partner}")


    def send_message(self, message):
        if not self.username:
            tk.messagebox.showwarning(title="Error", message="Please set your username first")
            return
        elif not self.recipient:
            tk.messagebox.showwarning(title="Error", message="Please set your recipient first")
            return
        elif not message.strip():
            tk.messagebox.showwarning(title="Error", message="Please enter a message")
            return
        self.client.sendMsg(createMessage(self.username, self.recipient, message))
        tk.messagebox.showinfo(title="Message sent", message=f"Message sent: {message}")
        print(f"Message sent: {message}")

    def get_all_messages(self):
        if not self.username:
            tk.messagebox.showwarning(title="Error", message="Please set your username first")
            return
        self.all_messages = self.client.requestAllMsg()
        self.all_messages_listbox.delete(0, tk.END)
        for message in self.all_messages:
            self.all_messages_listbox.insert(tk.END, prettyprint.format(
                u = message.fromUsr, 
                t = message.toUsr, 
                s = datetime.datetime.fromtimestamp(message.timeStamp), 
                m = message.msgData))
            
    def get_unread_messages(self):
        if not self.username:
            tk.messagebox.showwarning(title="Error", message="Please set your username first")
            return
        self.unread_messages = self.client.requestNewMsg()
        self.unread_messages_listbox.delete(0, tk.END)
        for message in self.unread_messages:
            self.unread_messages_listbox.insert(tk.END, prettyprint.format(
                u = message.fromUsr, 
                t = message.toUsr, 
                s = datetime.datetime.fromtimestamp(message.timeStamp), 
                m = message.msgData))
            
    def get_conversation(self):
        if not self.partner:
            tk.messagebox.showwarning(title="Error", message="Please set your partner username first")
            return
        elif not self.username:
            tk.messagebox.showwarning(title="Error", message="Please set your username first")
            return
        #self.convo_messages = self.client.requestConvo(self.partner)
        self.conversation_messages_listbox.delete(0, tk.END)

        for message in self.client.requestConvo(self.partner):

            if message.fromUsr == self.username:
                firstline = "[>] From: " + message.fromUsr + " -> " + message.toUsr + "\n"
                secondline = "[>] Time: " + str(datetime.datetime.fromtimestamp(message.timeStamp))
                thirdline = "[>] Message: " + message.msgData + "\n"
                if message.fromUsr == self.username:
                    secondline += "| READ On: " + str(datetime.datetime.fromtimestamp(message.firstRequested)) + "\n"
                else:
                    secondline += "\n"
                self.conversation_messages_listbox.insert(tk.END, firstline)
                self.conversation_messages_listbox.insert(tk.END, secondline)
                self.conversation_messages_listbox.insert(tk.END, thirdline)
                self.conversation_messages_listbox.insert(tk.END, "\n")
            else:
                firstline = "[<] From: " + message.fromUsr + " -> " + message.toUsr + "\n"
                secondline = "[<] Time: " + str(datetime.datetime.fromtimestamp(message.timeStamp)) + "\n"
                thirdline = "[<] Message: " + message.msgData + "\n"
                self.conversation_messages_listbox.insert(tk.END, firstline)
                self.conversation_messages_listbox.insert(tk.END, secondline)
                self.conversation_messages_listbox.insert(tk.END, thirdline)
                self.conversation_messages_listbox.insert(tk.END, "\n")


if __name__ == "__main__":
    root = tk.Tk()
    editor = NonInstantMessenger(root)
    root.mainloop()
