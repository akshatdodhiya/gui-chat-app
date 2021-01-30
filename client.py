import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'  # localhost should be replaced with Public IP address of the server(If deployed online)
PORT = 9090  # Public port of server(If hosted online)


class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Create a socket of two types: internet and TCP
        self.sock.connect((host, port))

        msg = tkinter.Tk()  # Create a GUI window
        msg.withdraw()  # Hide the window

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)

        self.gui_done = False  # Pause the GUI till all the work is done
        self.running = True  # Set whether the program is running or not(Default=True & False when we want to stop)

        gui_thread = threading.Thread(target=self.gui_loop)  # Create thread for gui_loop function
        receive_thread = threading.Thread(target=self.receive)  # Create thread for receive function

        gui_thread.start()  # Start threading for gui_thread
        receive_thread.start()  # Start threading for receive_thread

    # Function used to build the GUI
    def gui_loop(self):
        # Designing the GUI
        self.win = tkinter.Tk()
        self.win.title('Chat Application by Akshat')
        self.win.configure(bg="darkgray")
        # Editing the looks of windows - with background color specified above
        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="darkgray")
        '''All elements should be individually specified with bg color because by default the
         color is white for all windows and elements'''
        self.chat_label.config(font=("Times", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')
        # Disabling the text area i.e chat history section so as to not allow user to edit the chat history

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="darkgray")
        self.msg_label.config(font=("Times", 12))
        self.msg_label.pack(padx=20, pady=5)

        # Textbox to input message
        self.input_area = tkinter.Text(self.win, height=5)
        self.input_area.pack(padx=20, pady=5)

        # Button which sends message on click
        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Times", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        # Close the program when window is closed by calling 'stop' function
        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    # Function that creates a perfect message format and sends to the server
    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        # Create a message that has message as well as nickname of the client
        # '1.0' means from the beginning & 'end' means till the ending (in-short it means get the whole text)
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    # Function to terminate program when window is closed
    def stop(self):
        self.running = False
        self.win.destroy()  # Destroy the Chat window
        self.sock.close()  # Close the socket connection
        exit(0)  # Exit the program with code 0

    # Function used to handle connections and receiving messages from server
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'Enter NICKNAME:':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')  # Convert chat history to editable format
                        self.text_area.insert('end', message)  # Append message at the end
                        self.text_area.yview('end')  # Keep scrolling automatically the view
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except Exception as err:
                print(err)  # Print error message
                self.sock.close()  # Close socket connection
                break


client = Client(HOST, PORT)  # Object of class Client
