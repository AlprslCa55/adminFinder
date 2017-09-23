# coding: utf-8
# Author: notesoftware
# version: 1.0
# work on python2

from Tkinter import *
import ScrolledText
from tkFileDialog import askopenfilename
import urllib as r
from threading import Thread
from Queue import Queue
import sys
import webbrowser as w

class Admin:
    def __init__(self):
        self.window = Tk()
        self.window.title("Admin Finder")
        self.window.geometry("400x400")
        self.window.resizable(width=FALSE, height=FALSE)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.filePath = 0
        self.que = Queue()

        self.logoBar = Frame(self.window)
        self.logoBar.pack(side = BOTTOM)

        self.github = Label(self.logoBar,text = "http://github.com/notesoftware")
        self.github.pack(side = LEFT)
        self.github.bind("<Button-1>",lambda event = None:w.open_new_tab("http://github.com/notesoftware"))
        self.github.bind("<Enter>",lambda event = None:self.github.config(cursor="hand2"))
        self.website = Label(self.logoBar,text = "https://savecoder.blogspot.com")
        self.website.pack(side = RIGHT)
        self.website.bind("<Button-1>",lambda event = None:w.open_new_tab("https://savecoder.blogspot.com"))
        self.website.bind("<Enter>",lambda event = None:self.website.config(cursor="hand2"))
        self.label = Label(self.window, text="select wordlist,entry web adress and press Find!")
        self.label.place(x=10, y=0)

        self.webAdress = Entry(self.window)  # input web adress
        self.webAdress.place(x=10, y=20, width=200, height=20)

        self.searchButton = Button(self.window,
                                   text="Find!",
                                   command=lambda:Thread(target = self.conf,args = (),).start(),
                                   state = "disable")

        self.searchButton.place(x=210, y=20, width=90, height=20)

        self.fileSelect = Button(self.window,text = "Select Worlist",command = self.dialog)
        self.fileSelect.place(x = 300,y = 20,width = 90,height = 20)

        self.result = ScrolledText.ScrolledText(self.window,
                                                wrap="word",
                                                fg = "red",
                                                bg = "black")

        self.result.place(x=10, y=60, width=200, height=300)

        self.resultFind = ScrolledText.ScrolledText(self.window,
                                                    fg = "green",
                                                    bg = "black",
                                                    wrap = "word")
        self.resultFind.place(x=210, y=60, width=180, height=300)

        self.window.mainloop()

    def conf(self):
        if(self.filePath):
            if(self.webAdress.get()):
                try:
                    adress = self.webAdress.get()
                    if(adress.startswith("http://") or adress.startswith("https://")):
                        self.searchButton["state"] = "disable"
                        self.fileSelect["state"] = "disable"
                        self.result.config(state = "normal")
                        self.result.delete(1.0,END)
                        self.resultFind.config(state = "normal")
                        self.resultFind.delete(1.0,END)
                        self.label["text"] = "please wait..."
                        for i in self.adminList:
                            i = i.strip("\n")
                            i = "/"+i
                            site = adress+str(i)
                            try:
                                connection = r.urlopen(site)
                            except:
                                code = 404
                                connection = False
                            
                            if(connection):
                                code = connection.getcode()
                                if(code == 200):
                                    self.write(site,1)
                                else:
                                    self.write(site,0)
                            else:
                                self.write(site,0)
                            
                        self.searchButton["state"] = "normal"
                        self.fileSelect["state"] = "normal"
                        self.label["text"] = "End!"
                    else:
                        self.label["text"] = "Please entry web adress startswith 'http://' or 'https://'"
                
                except ValueError:
                    self.label["text"] = "Please entry web adress startswith 'http://' or 'https://'"
                except Exception as e:
                    pass
                    
            else:
                self.label["text"] = "entry web adress..."
                
        else:
            self.label["text"] = "File isn't select"


    def dialog(self):
        self.filePath = askopenfilename()
        if(self.filePath):
            self.searchButton["state"] = "normal"
            self.file = open(self.filePath.encode("cp1254"),"r")
            self.adminList = self.file.readlines()
            self.file.close()
         

    def write(self,variable,flag):
        if(flag):
            self.resultFind.configure(state = "normal")
            self.resultFind.insert(END,"\n[+]{}".format(variable))
            self.resultFind.configure(state = "disable")
            self.resultFind.yview(END)
        else:
            self.result.configure(state = "normal")
            self.result.insert(END,"\n[-]{}".format(variable))
            self.result.configure(state = "disable")
            self.result.yview(END)            

    def close(self):
        self.window.destroy()
        sys.exit(0)

if __name__ == "__main__":
    Admin()
