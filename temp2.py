import tkinter as tk
from tkinter import ttk, simpledialog

class NonInstantMessenger:
    def __init__(self, master):
        self.master = master
        self.master.title("Non-Instant Messenger")
        self.master.geometry("500x500")

        # Ask for username using a prompt
        self.username = simpledialog.askstring("Username", "Enter your username:")
        if not self.username:
            # If the user clicks cancel or enters an empty string, exit the program
            self.master.destroy()
            return

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # First tab for changing username
        self.username_tab = tk.Frame(self.notebook)
        self.notebook.add(self.username_tab, text="Change Username")
        self.create_username_tab()

        # Second tab for writing a message
        self.message_tab = tk.Frame(self.notebook)
        self.notebook.add(self.message_tab, text="Write a Message")
        self.create_message_tab()

        # Third tab for displaying messages
        self.display_tab = tk.Frame(self.notebook)
        self.notebook.add(self.display_tab, text="Display Messages")
        self.create_display_tab()

        # Sample messages
        self.messages = ["Hello", "How are you?", "Nice to meet you!"]
        self.update_display()

    def create_username_tab(self):
        # Label in the body of the tab
        label = tk.Label(self.username_tab, text=f"Current Username: {self.username}")
        label.pack(pady=10)

        # Text box to write the new username
        entry = tk.Entry(self.username_tab)
        entry.pack(pady=10)

        # Button to record the new username
        record_button = tk.Button(self.username_tab, text="Change Username", command=lambda: self.set_username(entry.get()))
        record_button.pack(pady=20)

    def create_message_tab(self):
        # Label in the body of the tab
        label = tk.Label(self.message_tab, text=f"Logged in as: {self.username}")
        label.pack(pady=10)

        # Text box to write the message
        text_box = tk.Text(self.message_tab, height=10, width=40)
        text_box.pack(pady=10)

        # Button to send the message
        send_button = tk.Button(self.message_tab, text="Send Message", command=lambda: self.send_message(text_box.get("1.0", tk.END)))
        send_button.pack(pady=20)

    def create_display_tab(self):
        # Listbox to display messages
        self.messages_listbox = tk.Listbox(self.display_tab, height=10, width=40)
        self.messages_listbox.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(self.display_tab, orient=tk.VERTICAL, command=self.messages_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.messages_listbox.config(yscrollcommand=scrollbar.set)

    def set_username(self, new_username):
        # Do something with the new username
        print(f"New username recorded: {new_username}")
        self.username = new_username
        # Update the label to display the current username
        self.username_tab.winfo_children()[0].config(text=f"Current Username: {self.username}")

    def send_message(self, message):
        # Do something with the message
        print(f"Message sent: {message}")
        self.messages.append(message.strip())  # Strip to remove newline characters
        self.update_display()

    def update_display(self):
        # Clear the listbox and insert messages
        self.messages_listbox.delete(0, tk.END)
        for message in self.messages:
            self.messages_listbox.insert(tk.END, message)

if __name__ == "__main__":
    root = tk.Tk()
    editor = NonInstantMessenger(root)
    root.mainloop()
