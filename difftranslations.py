#!/bin/env python
import wx, imgs
from wx.lib.wordwrap import wordwrap
from wx.lib.pdfwin import PDFWindow
import wx.lib.buttons as buttons
import  wx.lib.scrolledpanel as scrolled
import hexagram as hx
from pathutils import get_main_dir

coinmethod = True 
stattext = [
        "I Ching: The Book of Change by John Blofeld",
        "The Taoist I Ching by Lui I-Ming translated by Thomas Cleary",
        "Total I Ching: Myths for Change by Stephen Karcher",
        "The I Ching: The Book of Changes by James Legge",
        "The Classic of Changes: A New Translation of the I Ching as Interpreted by Wang Bi by Richard John Lynn",
        "The Original I Ching: An Authentic Translation of the Book of Changes by Margaret Pearson",
        "Zhouyi: A New Translation with Commentary of the Book of Changes by Richard Rutt",
        "I Ching: Classics of Ancient China by Edward Shaughnessy",
        "The Authentic I-Ching by Henry Wei",
        "Rediscovering the I Ching by Gregory Whincup",
        "The I Ching or Book of Changes by Richard Wilhelm and Cary Baynes",
        ] 
hnms = [
    "Title page",
    "Copyright Information",
    ]
hnms += [ "Hexagram " + str(i) for i in xrange(1,65)]
foldernames = [
    'Blofeld/',
    'Cleary_T/',
    'Karcher/',
    'Legge/',
    'Lynn/',
    'Pearson/',
    'Rutt/',
    'Shaughnessy/',
    'Wei/',
    'Whincup/',
    'Wilhelm/',
    ]
if len(stattext) != len(foldernames):
    print "Warning the lists of books are not equal in size."

files = ['titlepage.pdf', 'copyright.pdf']
files += [ '%.2d.pdf' % j for j in xrange(1,65)]
maindir = get_main_dir()
pages = [[maindir+'/pages/' + folder+file for file in files] for folder in foldernames]

whichbook = hx.random.choice(range(len(stattext)))
whichchapter = 0
## These are the 2-dimensional list indexes

class MainWindow(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, size=(790,650))
        self.status = self.CreateStatusBar()
        self.Centre()
        self.SetSizeHints(425,375,-1,-1)
        self.pgch_win = wx.SashLayoutWindow(self,
                                        -1,
                                        wx.DefaultPosition,
                                        (150, 30),
                                        wx.NO_BORDER|wx.SW_3D
                                        )
        self.pgch_win.SetDefaultSize((150, 1000))
        self.pgch_win.SetOrientation(wx.LAYOUT_VERTICAL)
        self.pgch_win.SetAlignment(wx.LAYOUT_LEFT)
        self.pgch_win.SetSashVisible(wx.SASH_RIGHT, True)
        self.pgch_win.SetMinimumSizeX(95)


        ## The list chooser
        self.pagechooser = wx.ListBox(self.pgch_win, -1, 
                                choices=hnms, # the list of pages
                                style=wx.LB_SINGLE
                                )
        
        self.pagechooser.SetMinSize((150, -1))
        self.Bind(wx.EVT_LISTBOX, self.OnListSelect, self.pagechooser)
        self.Bind(wx.EVT_SASH_DRAGGED_RANGE, self.OnSashDrag)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        ## This is the parent for the panel where all right side material is
        self.RemainingSize = wx.SashLayoutWindow(self, -1,
                                                 wx.DefaultPosition,
                                                 (600, 1000),
                                                 )
        self.RemainingSize.SetOrientation(wx.LAYOUT_VERTICAL)
        self.RemainingSize.SetAlignment(wx.LAYOUT_LEFT)

        ## The panel for non-listchooser material (right side)
        pp = wx.Panel(self.RemainingSize, -1)

        ## The panel for book selection buttons
        bookpanel = scrolled.ScrolledPanel(pp, -1, size=(len(stattext)*50, 80))
        bookpanel.SetupScrolling(scroll_y=False)
        bookpanel.SetMinSize((-1, 90))
        self.books = range(len(stattext))
        bookimgs = range(11)
        bookimgs[0]=imgs.blofeld.GetBitmap()
        bookimgs[1]=imgs.clearytaoist.GetBitmap()
        bookimgs[2]=imgs.karcher.GetBitmap()
        bookimgs[3]=imgs.legge.GetBitmap()
        bookimgs[4]=imgs.lynn.GetBitmap()
        bookimgs[5]=imgs.pearson.GetBitmap()
        bookimgs[6]=imgs.rutt.GetBitmap()
        bookimgs[7]=imgs.shaughnessy.GetBitmap()
        bookimgs[8]=imgs.wei.GetBitmap()
        bookimgs[9]=imgs.whincup.GetBitmap()
        bookimgs[10]=imgs.wilhelmbaynes.GetBitmap()
        if len(bookimgs) != len(self.books):
            print "Warning: array of button bitmaps 'bookimgs' is not the "
            print "same length as the array of buttons 'frame.buttons'."
            
        for i in range(len(self.books)):
            self.books[i] = buttons.GenBitmapButton(
                bookpanel, -1, bookimgs[i], size=(50, 70)
                ) #Creates the buttons with names 'self.books[0 - n]
            
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        for i in xrange(len(self.books)):
            hsizer.Add(self.books[i], 0, wx.LEFT | wx.RIGHT, 3)
        bookpanel.SetSizer(hsizer)

        for i in xrange(len(self.books)):
            self.Bind(wx.EVT_BUTTON, self.OnBookSelect, self.books[i])
            self.books[i].Bind(wx.EVT_ENTER_WINDOW, self.OnBook )
            self.books[i].Bind(wx.EVT_LEAVE_WINDOW, self.OnClear )

        ## Book reader window        
        self.bookwin = PDFWindow(pp, -1)
        self.bookwin.LoadFile(pages[whichbook][whichchapter])

        ## Panel for hexagram generate buttons
        ctrlpanel = wx.Panel(pp, -1)
        throw = wx.Button(ctrlpanel, -1, "Consult the Yijing")
        self.Bind(wx.EVT_BUTTON, self.OnThrow, throw)
        throw.Bind(wx.EVT_ENTER_WINDOW, self.OnThrowStatus )
        throw.Bind(wx.EVT_LEAVE_WINDOW, self.OnClear )

        space = wx.StaticText(ctrlpanel, -1, "")
        ## Textbox to read the hexagram number
        self.inform = wx.TextCtrl(
                                  ctrlpanel, 
                                  -1, 
                                  "", 
                                  size=(150, 45), 
                                  style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.inform.Bind(wx.EVT_ENTER_WINDOW, self.OnHexTextStatus )
        self.inform.Bind(wx.EVT_LEAVE_WINDOW, self.OnClear )

        #Sizer for the bottom area of the program
        ctrlsizer = wx.BoxSizer(wx.HORIZONTAL)
        ctrlsizer.Add(throw, 0, wx.EXPAND | wx.ALL, 1)
        ctrlsizer.Add(space, 1, wx.EXPAND | wx.ALL, 1)
        ctrlsizer.Add(self.inform, 0, wx.EXPAND | wx.ALL, 1)
        ctrlpanel.SetSizer(ctrlsizer)

        ## Sizer for the whole right side
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(bookpanel, 0, wx.EXPAND | wx.ALL, 3)
        s.Add(self.bookwin, 5, wx.EXPAND | wx.ALL, 3)
        s.Add(ctrlpanel, 0, wx.EXPAND |wx.ALL, 3)
        pp.SetSizer(s)

        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)

    def OnClear(self, event):
        self.SetStatusText("")
        event.Skip()

    def OnBook(self, event):
        self.SetStatusText(
            stattext[
                self.books.index(
                    event.GetEventObject()
                    )
                ]
            )
        event.Skip()

    def OnThrow(self, event):
        dialogue = wx.TextEntryDialog(
            self, "Use the space below to state your query.",
                "Consult the Yijing")
        if dialogue.ShowModal() == wx.ID_OK:
            self.inform.SetValue(self.GetHexText(coinmethod))
        dialogue.Destroy()

    def OnThrowStatus(self, event):
        self.SetStatusText("Generates a random hexagram with changing lines.")
        event.Skip()

    def OnHexTextStatus(self, event):
        self.SetStatusText("Any changing lines belong to the initial hexagram. A secondary hexagram indicates the situation's conclusion.")

    def GetHexText(self, coinmethod=False):
        global whichchapter
        booleanhex = hx.generatehex(coinmethod)
        number = hx.hvals[hx.getbinvalue(booleanhex)]
        whichchapter = number + 1
        self.bookwin.LoadFile(pages[whichbook][whichchapter])
        self.pagechooser.SetSelection(whichchapter)

        topline="Hexagram %d" % number
        middleline = "Changing lines: "
        static = True
        for i in xrange(6):
            if booleanhex[i][1]:
                if static == False:
                    middleline += ", "
                static = False
                middleline += str(i+1)
        if static:
            middleline += "None"
            bottomline = ""
        else: 
            bottomline = "Hexagram %d" % hx.hvals[hx.getbinvalue(hx.changehex(booleanhex))]
        return topline + '\n' + middleline + '\n' + bottomline
        
        
    def OnSashDrag(self, event):
        self.pgch_win.SetDefaultSize((event.GetDragRect().width, 1000))
        wx.LayoutAlgorithm().LayoutWindow(self, self.RemainingSize)
        self.RemainingSize.Refresh()

    def OnSize(self, event):
        wx.LayoutAlgorithm().LayoutWindow(self, self.RemainingSize)

    def OnListSelect(self, event):
        global whichbook
        global whichchapter
        whichchapter = event.GetSelection()
        self.bookwin.LoadFile(pages[whichbook][whichchapter])

    def OnBookSelect(self, event):
        global whichbook
        global whichchapter
        whichbook = self.books.index(
            event.GetEventObject()
            )
        self.bookwin.LoadFile(pages[whichbook][whichchapter])

    def OnContextMenu(self, event):
        self.popupID1 = wx.NewId()
        self.popupID2 = wx.NewId()
        self.popupID3 = wx.NewId()
        self.popupID4 = wx.NewId()
        self.popupID5 = wx.NewId()
        self.popupID6 = wx.NewId()
        self.popupID7 = wx.NewId()
        self.popupID8 = wx.NewId()
        self.popupID9 = wx.NewId()
        self.popupID10 = wx.NewId()
        self.popupID11 = wx.NewId()
        self.popupID12 = wx.NewId()
        self.popupID13 = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.popupID1)
        self.Bind(wx.EVT_MENU, self.OnLegal, id=self.popupID2)
        self.Bind(wx.EVT_MENU, self.OnWhatIs, id=self.popupID3)
        self.Bind(wx.EVT_MENU, self.OnDiv, id=self.popupID4)
        self.Bind(wx.EVT_MENU, self.OnCoin, id=self.popupID6)
        self.Bind(wx.EVT_MENU, self.OnMilfoil, id=self.popupID7)
        self.Bind(wx.EVT_MENU, self.OnSysRand, id=self.popupID9)
        self.Bind(wx.EVT_MENU, self.OnMT, id=self.popupID10)
        self.Bind(wx.EVT_MENU, self.OnWH, id=self.popupID11)
        self.Bind(wx.EVT_MENU, self.OnCMWC, id=self.popupID12)
        self.Bind(wx.EVT_MENU, self.OnExit, id=self.popupID13)
        # right click menu
        menu = wx.Menu()
        menu.Append(self.popupID1, "About")
        menu.Append(self.popupID2, "Legal")
        menu.Append(self.popupID3, "What is the Yijing?")
        menu.Append(self.popupID4, "What is divination?")
        # submenus
        sm1 = wx.Menu()
        sm1.Append(self.popupID6, "Coins")
        sm1.Append(self.popupID7, "Milfoil")
        menu.AppendMenu(self.popupID5, "Probability", sm1)
        if wx.Platform == '__WXMSW__':
            sysrand = "CryptGenRandom"
        else:
            sysrand = "/dev/urandom"
        sm2 = wx.Menu()
        sm2.Append(self.popupID9, sysrand)
        sm2.Append(self.popupID10, "Mersenne Twister")
        sm2.Append(self.popupID11, "Wichmann-Hill")
        sm2.Append(self.popupID12, "Multiply-with-carry")
        menu.AppendMenu(self.popupID8, "Randomness", sm2)
        menu.Append(self.popupID13, "Exit")
        self.PopupMenu(menu)
        menu.Destroy()

    def OnWhatIs(self, event):
        what = wx.MessageDialog(self,
                                wordwrap(
                                    "The Yijing, or I Ching, is an ancient "
                                    "Chinese text over three thousand years "
                                    "old, which was used throughout its "
                                    "history as a handbook for divination. It "
                                    "was used by peasants as well as "
                                    "imperial courts. For centuries, it "
                                    "was taught as mandatory reading in all "
                                    "Chinese schools. \n\n"
                                    "To use the Yijing, one first forms a "
                                    "question in mind. Then through an "
                                    "ancient form of random number generation, "
                                    "one creates a six-line figure called a "
                                    "hexagram. Each line has the quality of "
                                    "being either broken or solid. In addition, "
                                    "each line also has the quality of being "
                                    "either static or changing. Changing lines "
                                    "have additional text associated with them, "
                                    "and will transform the hexagram into a "
                                    "different, second hexagram. The text of "
                                    "the indicated hexagrams and lines will "
                                    "pertain to the question originally asked."
                                    "\n\nIf you would like more information "
                                    "about the history of the Yijing, how it "
                                    "works, or how it can be used, please "
                                    "consider purchasing whichever of the "
                                    "books featured here you find useful. "
                                    "Each book contains much "
                                    "valuable information that this small "
                                    "program does not display.",
                                    400, wx.ClientDC(self)),
                                "What is the Yijing?",
                                wx.OK 
                                )
        what.ShowModal()
        what.Destroy()

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "Yijing in Translation"
        info.Version = "1.0.0"
        info.Copyright = "(C) 2012 Matt Pagan\n"
        info.WebSite = ("http://yijingintranslation.com", "Yijing in Translation")
        info.Description = wordwrap(            
            "Yijing in Translation is written using wxPython. This program "
            "provides access to several different translations of the Yijing. "
            "This program can be used for divination, for semantic analysis, or as an e-reader for this ancient text."
            "\n\nThis work is dedicated with gratitude to my former "
            "professor Robert Ford Campany, who revealed to me the pernicious "
            "issue of translating ancient Chinese into modern English.\n",
            350, wx.ClientDC(self))
        info.License = wordwrap(
            "This program is free software: you can redistribute it and/or "
            "modify it under the terms of the GNU General Public License as "
            "published by the Free Software Foundation, either version 3 of "
            "the License, or (at your option) any later version. \n\nThis "
            "program is distributed in the hope that it will be useful, but "
            "WITHOUT ANY WARRANTY; without even the implied warranty of "
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU "
            "General Public License for more details. ",
            350, wx.ClientDC(self))
        wx.AboutBox(info)

    def OnDiv(self, event):
        dlg2 = wx.MessageDialog(self, wordwrap(
            "Divination is the use of randomness and human interpretation to answer questions. "
            "Although it remains unclear how divination works, the skillful use of divination has the potential to benefit anyone who uses it by reducing the doubt and uncertainty concerning whatever topic the user bears. \n\n"
            "Divination involves forming a question, selecting one symbol out of a set of symbols with defined meanings, and interpreting the selected symbol in some way that pertains to the original question. "
            "The potency of divination is not reduced if the questioner is unfamilar with the symbolic language from which he or she will read. "
            "Divination seems equally effective for questions concerning past events, present conditions, and the conjectured future.\n",
            500, wx.ClientDC(self)),
                               "What is divination?",
                               wx.OK
                               )
        
        dlg2.ShowModal()
        dlg2.Destroy()
        

    def OnLegal(self, event):
        dlg = wx.MessageDialog(self, wordwrap(
            "This program uses copyrighted material under fair use guidlines. "
            "This program is an artistic work, and it uses all published "
            "material in a significantly different way than it is used "
            "in any currently copyrighted work. For more information you "
            "can contact the author of this program at matthew.a.pagan@"
            "gmail.com.\n\n",
            450, wx.ClientDC(self)),
                               "Legal Information",
                               wx.OK
                               )
        
        dlg.ShowModal()
        dlg.Destroy()

    def OnMilfoil(self, event):
        global coinmethod
        coinmethod = False

    def OnCoin(self, event):
        global coinmethod
        coinmethod = True

    def OnSysRand(self, event):
        global hx
        hx.rand = hx.random.SystemRandom()
        
    def OnMT(self, event):
        global hx
        hx.rand = hx.random

    def OnWH(self, event):
        global hx
        hx.rand = hx.random.WichmannHill()

    def OnCMWC(self, event):
        global hx
        hx.rand = hx.CMWC()

    def OnExit(self, event):
        self.Close()
        

############################## End MainWindow ########################

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow(None, -1, "Yijing in Translation")
    frame.SetIcon(imgs.hexico2.GetIcon())
    frame.Show()
    app.MainLoop()
