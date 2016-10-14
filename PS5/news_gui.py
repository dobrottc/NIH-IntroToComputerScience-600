import tkinter 
import time

#root = Tk()
#root.withdraw()

# The Popup class
class Popup:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.withdraw()
        """
        self.root.mainloop()
        def drawALot():
            self.root = Tk()
            self.root.withdraw()
            self.root.mainloop()
        thread.start_new_thread(drawALot, ())
        """
    def start(self):
        self.root.mainloop()

    def _makeTheWindow(self, item):
        """
        Private method that does the actual window drawing
        """
        root = tkinter.Toplevel()
        root.wm_title("News Alert")
        
        w = root.winfo_screenwidth()/20
        h = root.winfo_screenheight()/4
        
        title = tkinter.Text(root, padx=5, pady=5, height=3, wrap=tkinter.WORD, bg="white")
        title.tag_config("title", foreground="black", font=("helvetica", 12, "bold"))
        title.tag_config("subject", foreground="black", font=("helvetica", 12, "bold"))
        title.insert(tkinter.INSERT, "Title: %s" % item.get_title(), "title")
        title.insert(tkinter.INSERT, "\nSubject: ", "subject")
        title.insert(tkinter.INSERT, item.get_subject().rstrip(), "subject")    
        
        title.config(state=tkinter.DISABLED, relief = tkinter.FLAT)
        title.grid(sticky=tkinter.W+tkinter.E)
        
        summary = tkinter.Text(root, padx=10, pady=5, height=15, wrap=tkinter.WORD, bg="white")
        summary.tag_config("text", foreground="black", font=("helvetica", 12))
        summary.insert(tkinter.INSERT, item.get_summary().lstrip(), "text")
        
        summary.config(state=tkinter.DISABLED, relief = tkinter.FLAT)
        summary.grid(sticky=tkinter.W+tkinter.E)
        
        link = tkinter.Text(root, padx=5, pady=5, height=4, bg="white")
        link.tag_config("url", foreground="blue", font=("helvetica", 10, "bold"))
        link.insert(tkinter.INSERT, item.get_link(), "url")
        
        link.config(state=tkinter.DISABLED, relief=tkinter.FLAT)
        link.grid(sticky=tkinter.W+tkinter.E)

    def newWindow(self, item):
        """
        Displays a popup with the contents of the NewsStory newsitem
        """
        self.root.after(0, self._makeTheWindow, item)

        
       

