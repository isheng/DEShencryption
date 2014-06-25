#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import wx
import time
import wx.stc as stc
import os


class ColorTextBox(stc.StyledTextCtrl):
    """
    Subclass the StyledTextCtrl to provide  additions
    and initializations to make it useful to tag the text.

    """
    def __init__(self, parent, style=0):
        """
        Constructor
        
        """
        stc.StyledTextCtrl.__init__(self, parent, style=style)
        self._styles = [None]*32
        self._free = 1
        # self.SetMarginType(1, stc.STC_MARGIN_NUMBER)          
        # self.SetMarginWidth(1, 20)
    def getStyle(self, c='black'):
        """
        Returns a style for a given colour if one exists.  If no style
        exists for the colour, make a new style.
        
        If we run out of styles, (only 32 allowed here) we go to the top
        of the list and reuse previous styles.

        """
        free = self._free
        if c and isinstance(c, (str, unicode)):
            c = c.lower()
        else:
            c = 'black'

        try:
            style = self._styles.index(c)
            return style

        except ValueError:
            style = free
            self._styles[style] = c
            self.StyleSetForeground(style, wx.NamedColour(c))

            free += 1
            if free >31:
                free = 0
            self._free = free
            return style

    def write(self, text, c=None):
        """
        Add the text to the end of the control using colour c which
        should be suitable for feeding directly to wx.NamedColour.
        
        'text' should be a unicode string or contain only ascii data.
        """
        style = self.getStyle(c)
        lenText = len(text.encode('utf8'))
        #lenText=len(text)
        end = self.GetLength()
        self.AddText(text)
        self.StartStyling(end, 31)
        self.SetStyling(lenText, style)
        self.EnsureCaretVisible()


    __call__ = write

class MyPanel(wx.Panel):
    def __init__(self, parent, id=-1,image_file='background.png'):
        wx.Panel.__init__(self, parent, id=id)
        try:
            imagefile=image_file
            image = wx.Image(imagefile)
            temp = image.ConvertToBitmap()
            size = temp.GetWidth(),temp.GetHeight()
            wx.StaticBitmap(self, -1, temp)            
        except IOError:
            print 'Image file %s not found' % image_file
            raise SystemExi

class Frame(wx.Frame):   #2 wx.Frame

    def __init__(self, parent=None, style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX): #3
        """ 

        the Constructor wx.Frame(parent, id=-1, title="", pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE,
            name="frame")

        """
        title="Encrypt Your text"
        wx.Frame.__init__(self, parent, -1, title=title,size=(800,640),style=style)
        self.panel =MyPanel(self)
        # self.panel.SetBackgroundColour('cornflower blue')

        self.CreateTextBox()
        self.CreateButton()
        self.createLayout()
        self.BindButton()
        self.InitStatusBar()
        self.CreateMenuBar()

#init the Frame
    def CreateTextBox(self):
        '''
            create TextBox
            the contents2 is the ColorTextBox class which is the Subclass of the wx.stc.StyledTextCtrl
            we use its write function to tag the highlight words
        '''
        self.contents0=wx.TextCtrl(self.panel,pos=(635,37))
        self.contents1=wx.TextCtrl(self.panel,style=wx.TE_MULTILINE)  #add the texttctl componment
        self.contents2=ColorTextBox(self.panel)
        self.contents2.SetWrapMode(stc.STC_WRAP_WORD)

    def BindButton(self):
        '''
            bind the button
        '''
        self.analysisBuntton.Bind(wx.EVT_BUTTON, self.analysis)  #bind the event
        self.categoryBuntton.Bind(wx.EVT_BUTTON, self.category)
        # self.topicButton.Bind(wx.EVT_BUTTON,self.topic)
        # self.find_docButton.Bind(wx.EVT_BUTTON,self.Ondoc)

    def CreateButton(self):
        '''
            create the button
            use the BitmapButton as the button 
            use the Bitmap to convert pictures into bit
        '''
        pic= wx.Bitmap("encrypt.png"),wx.Bitmap("decrypt.png")#add list 
        self.analysisBuntton=wx.BitmapButton(self.panel,-1,pic[0])  
        self.categoryBuntton=wx.BitmapButton(self.panel,-1,pic[1])
        # self.topicButton=wx.BitmapButton(self.panel,-1,pic[2])
        # self.find_docButton=wx.BitmapButton(self.panel,-1,pic[3])

    def createLayout(self):
        '''
            BoxSizer is the Layout component 
            vbox is the Vertical
            hbox is the Horizontal
        '''
        self.hbox=wx.BoxSizer()
        self.hbox.Add(self.analysisBuntton,proportion=0,flag=wx.LEFT,border=30)
        self.hbox.Add(self.categoryBuntton,proportion=0,flag=wx.LEFT,border=20)
        # self.hbox.Add(self.topicButton,proportion=0,flag=wx.LEFT,border=20)
        # self.hbox.Add(self.find_docButton,proportion=0,flag=wx.LEFT,border=20)

        self.contents2Hbox=wx.BoxSizer()
        self.contents2Hbox.Add(self.contents2,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=30)

        self.contents1Hbox=wx.BoxSizer()
        self.contents1Hbox.Add(self.contents1,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=30)

        self.vbox=wx.BoxSizer(wx.VERTICAL)

        # self.vbox.Add(self.hbox1,proportion=0,flag=wx.TOP|wx.EXPAND,border=70)
        self.vbox.Add(self.contents1Hbox,proportion=1,flag=wx.EXPAND|wx.TOP,border=75)
        self.vbox.Add(self.hbox,proportion=0,flag=wx.EXPAND|wx.TOP|wx.BOTTOM,border=10 )
        self.vbox.Add(self.contents2Hbox,proportion=1,flag=wx.EXPAND|wx.BOTTOM,border=30)
        self.panel.SetSizer(self.vbox) 

    def InitStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-4,-1])  

    def statusBasPrint(self,strs):
        self.statusbar.SetStatusText(u''+strs, 0)

    def Printtime(self,strs):
        self.statusbar.SetStatusText(u'用时  '+strs,1)
    def MenuData(self):
        '''
                   menu data
        '''

        return [("&Menu", (                       
                           ("&Open", "Open paint file", self.OnOpen),
                           ("&About", "What About this program", self.Onabout),                                  #
                           ("&Quit", "Quit", self.OnCloseWindow)))
               ] 
    def CreateMenuBar(self):
        '''
        createMunBar
        '''
        menuBar = wx.MenuBar()
        for eachMenuData in self.MenuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1]
            menuBar.Append(self.CreateMenu(menuItems), menuLabel) 
        self.SetMenuBar(menuBar)
    def CreateMenu(self, menuData):
        '''
        create the munu
        '''
        menu = wx.Menu()
        for eachItem in menuData:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = self.CreateMenu(eachItem[1])
                menu.AppendMenu(wx.NewId(), label, subMenu) #
            else:
                self.CreateMenuItem(menu, *eachItem)
        return menu
    def CreateMenuItem(self, menu, label, status, handler, kind = wx.ITEM_NORMAL):
        '''topic
        create the item in the menu
        '''
        if not label:
            menu.AppendSeparator()
            return
        menuItem = menu.Append(-1, label, status, kind)
        self.Bind(wx.EVT_MENU, handler,menuItem)


#event handler of the menu
    def OnOpen(self, event):
        file_wildcard =" All files (*.*) |*.*"
        dlg = wx.FileDialog(self, "Open txt file...",
                            os.getcwd(), 
                            style = wx.OPEN,
                            wildcard = file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.ReadFile(filename)
        dlg.Destroy()

    def Onabout(self,event):
        mess='Encrypt Your Text Version 1.0 \nAuthor: \
        Wangjunsheng yoursheng@gmail.com'
        dlg = wx.MessageDialog(None,mess,
                      'What about !', wx.OK | wx.ICON_INFORMATION)
        result = dlg.ShowModal()
        dlg.Destroy()
    def OnCloseWindow(self, event):
        self.Destroy()
    def ReadFile(self,filename):
        try:
            f= open(filename, 'r')
            self.contents1.SetValue(f.read())
            f.close()
        except: 
            wx.MessageBox("%s is not a text file."
                          %filename, "error tip",
                          style = wx.OK | wx.ICON_EXCLAMATION)
     
#event handler of the button
    def analysis(self ,event):
        start = time.time()
        self.statusBasPrint(u'关键词提取中...')

        self.statusBasPrint(u'关键词提取 Successfully')
        self.contents2.SetReadOnly(True)  #set the contents2 readonly
        elapsed = (time.time() - start)
        self.Printtime(str(elapsed)+' s')

    def category(self,event):
        pass




class App(wx.App):  #5 wx.App
    """Application class."""

    def OnInit(self):
        self.frame = Frame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def main():  # main
    app = App()
    app.MainLoop()

if __name__ == '__main__':
     main()

