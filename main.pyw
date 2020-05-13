# -*- coding: utf-8 -*-
# python 3 only !
# ubuntu : sudo apt-get install python3-minimal
#          sudo apt-get install python3-tk

import tkinter, tkinter.ttk, tkinter.filedialog, binascii, hashlib, time

class MyNotebook(tkinter.Frame):
    def loadFileAndCompute(self):
        self.filename = tkinter.filedialog.askopenfilename(initialdir = "C:\\", title = "choose a file", filetypes = [("All files","*.*")])
        if self.filename != None: 
            try: 
                # read file
                filedata = None
                #print ("Open file OK: %s" % self.filename)
                self.tab1txtfile.delete('1.0', tkinter.END)
                self.tab1txtfile.insert(tkinter.INSERT, "%s" % self.filename)
                with open(self.filename, "rb") as f:
                    filedata = f.read()
                # crc32
                crcval = binascii.crc32(filedata)
                # md5 
                m = hashlib.md5(filedata)
                # sha256
                sha1 = hashlib.sha1(filedata)
                # clear & show
                self.tab1txtcrc32.delete('1.0', tkinter.END)
                self.tab1txtmd5.delete('1.0', tkinter.END)
                self.tab1txtsha1.delete('1.0', tkinter.END)
                self.tab1txtcrc32.insert(tkinter.INSERT, "0x%08X" % crcval)
                self.tab1txtmd5.insert  (tkinter.INSERT, "%s" % m.hexdigest().upper())
                self.tab1txtsha1.insert (tkinter.INSERT, "%s" % sha1.hexdigest().upper())
            except: 
                print ("Failed to read file '%s'" % self.filename)

    def tab2cb(self):
        val = 0;
        # clear
        self.tab2txtbin.delete(1.0, tkinter.END)
        self.tab2txtoct.delete(1.0, tkinter.END)
        self.tab2txtdec.delete(1.0, tkinter.END)
        self.tab2txthex.delete(1.0, tkinter.END)
        # compute
        for x in range(0, 32):
            if self.tab2chkvals[x].get():
                val += (1 << x)
        # show    
        self.tab2txtbin.insert(tkinter.INSERT, "%s" % (bin(val).replace("0b", "")))
        self.tab2txtoct.insert(tkinter.INSERT, "%s" % (oct(val).replace("0o", "")))
        self.tab2txtdec.insert(tkinter.INSERT, "%d" % val)
        self.tab2txthex.insert(tkinter.INSERT, "%s" % (hex(val).replace("0x", "")))
    
    def tab3update_time(self):
        self.tab3timeval.set("%.3f" % (((time.time() * 1000) - self.tab3now)/1000))
        self._tab3job = self.master.after(10, self.tab3update_time)
        
    def tab3cb(self):
        if self.tab3btnstart == 1:
            self.tab3now = int(time.time() * 1000)
            self.tab3update_time()
            self.tab3btn.config(text="Stop")
            self.tab3btnstart = 0
        else:
            self.tab3btn.config(text="Start")
            self.master.after_cancel(self._tab3job)
            self._tab3job = None
            self.tab3btnstart = 1
        
    def createWidgets(self, master):
        # create notebook
        self.note = tkinter.ttk.Notebook(master)
        
        #######     
        # tab1: Hash Values
        #######
        self.tab1 = tkinter.Frame(self.note)
        self.tab1str = "Hash Values"
        self.tab1btn = tkinter.Button(self.tab1, text='Open File', command=self.loadFileAndCompute)
        
        tkinter.Label(self.tab1, text="File").grid(row=0, column=0, sticky=tkinter.W)
        tkinter.Label(self.tab1, text="CRC32").grid(row=1, column=0, sticky=tkinter.W)
        tkinter.Label(self.tab1, text="MD5").grid(row=2, column=0, sticky=tkinter.W)
        tkinter.Label(self.tab1, text="SHA1").grid(row=3, column=0, sticky=tkinter.W)
        
        self.tab1txtfile  = tkinter.Text(self.tab1, height=1, width=72); self.tab1txtfile.grid(row=0, column=1)
        self.tab1txtcrc32 = tkinter.Text(self.tab1, height=1, width=72); self.tab1txtcrc32.grid(row=1, column=1)
        self.tab1txtmd5   = tkinter.Text(self.tab1, height=1, width=72); self.tab1txtmd5.grid(row=2, column=1)
        self.tab1txtsha1  = tkinter.Text(self.tab1, height=1, width=72); self.tab1txtsha1.grid(row=3, column=1)
        self.tab1btn.grid(row=0, column=2)
        
        #######
        # tab2
        #######
        self.tab2 = tkinter.Frame(self.note)
        self.tab2str = "Bits Values"
        # LabelFrame:Bits
        lftab2input = tkinter.ttk.Labelframe(self.tab2, text='Bits')
        lftab2input.grid(row=0, sticky=tkinter.W)
        self.tab2chkvals = [None] * 32
        self.tab2btn = [None] * 32
        for x in range(0,32):
            #tkinter.Label(lftab2input, text="%d\n%d"%((31-x)/10, (31-x)%10), padx=0, width=0).grid(row=0, column=x)
            tkinter.Label(lftab2input, text="%s\n%s"%( (str(int((31-x)/10)), "")[int((31-x)/10) == 0], str((31-x)%10))).grid(row=0, column=x)
            self.tab2chkvals[x] = tkinter.IntVar()
            self.tab2btn[x] = tkinter.Checkbutton(lftab2input, text="", variable = self.tab2chkvals[x], command=self.tab2cb, padx=0, pady=0)
            self.tab2btn[x].grid(row=1, column=31-x)
        
        # LabelFrame:Values
        lftab2output = tkinter.ttk.Labelframe(self.tab2, text='Values')
        lftab2output.grid(row=1, sticky=tkinter.W)
        tkinter.Label(lftab2output, text="Binary" ).grid(row=0, column=0, sticky=tkinter.W)
        tkinter.Label(lftab2output, text="Octal"  ).grid(row=1, column=0, sticky=tkinter.W)
        tkinter.Label(lftab2output, text="Decimal").grid(row=2, column=0, sticky=tkinter.W)
        tkinter.Label(lftab2output, text="Hex"    ).grid(row=3, column=0, sticky=tkinter.W)
        
        self.tab2txtbin = tkinter.Text(lftab2output, height=1, width=72); self.tab2txtbin.grid(row=0, column=1)
        self.tab2txtoct = tkinter.Text(lftab2output, height=1, width=72); self.tab2txtoct.grid(row=1, column=1)
        self.tab2txtdec = tkinter.Text(lftab2output, height=1, width=72); self.tab2txtdec.grid(row=2, column=1)
        self.tab2txthex = tkinter.Text(lftab2output, height=1, width=72); self.tab2txthex.grid(row=3, column=1)
        
        #######
        # tab3: Stopwatch
        #######
        self.tab3 = tkinter.Frame(self.note)
        self.tab3str = "Stopwatch"
        self.tab3timeval = tkinter.StringVar()
        self.tab3timeval.set("-" * 10)
        self.tab3btnstart = 1
        self.tab3qqq = 1
        tkinter.Label(self.tab3, textvariable=self.tab3timeval, font=("Courier New", 24), width=10).pack()
        self.tab3btn = tkinter.Button(self.tab3, text="Start", command=self.tab3cb, font=("Courier New", 24), width=5)
        self.tab3btn.pack()
        
        #######
        # notebook 
        #######
        self.note.add(self.tab1, text = self.tab1str)
        self.note.add(self.tab2, text = self.tab2str)
        self.note.add(self.tab3, text = self.tab3str)
        self.note.pack()

    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master.title('RD Gadgets')
        self.pack()
        self.createWidgets(master)


if __name__=='__main__':
    root = tkinter.Tk()
    app = MyNotebook(master=root)
    app.mainloop()
    