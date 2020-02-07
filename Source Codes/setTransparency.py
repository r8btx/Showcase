import wx, win32con, os

# Mainly from RobinDunn @https://wiki.wxpython.org/Transparent%20Frames
class AppFrame( wx.Frame )  :

    def __init__( self )  :

        wx.Frame.__init__( self, None, title="Am I transparent?",
                           style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP )
        self.SetClientSize( (300, 300) )

        self.alphaValue = 255
        self.alphaIncrement = -4

        pnl = wx.Panel( self )
        self.stTxt = wx.StaticText( pnl, -1, str( self.alphaValue ), (25, 25) )
        self.stTxt.SetFont( wx.Font( 18, wx.SWISS, wx.NORMAL, wx.NORMAL ) )

        self.changeAlpha_timer = wx.Timer( self )
        self.changeAlpha_timer.Start( 50 )       # 20 changes per second
        self.Bind( wx.EVT_TIMER, self.ChangeAlpha )

        self.Bind( wx.EVT_CLOSE, self.OnCloseWindow )

    #end AppFrame class

    #--------------------------------------------------------

    def ChangeAlpha( self, evt )  :
        """ The term "alpha" means variable transparency
              as opposed to a "mask" which is binary transparency.
              alpha == 255 :  fully opaque
              alpha ==   0 :  fully transparent (mouse is ineffective!)

            Only top-level controls can be transparent; no other controls can.
            This is because they are implemented by the OS, not wx.
        """

        self.alphaValue += self.alphaIncrement
        if (self.alphaValue) <= 0 or (self.alphaValue >= 255) :

            # Reverse the increment direction.
            self.alphaIncrement = -self.alphaIncrement

            if self.alphaValue <= 0 :
                self.alphaValue = 0

            if self.alphaValue > 255 :
                self.alphaValue = 255
        #end if

        self.stTxt.SetLabel( str( self.alphaValue ) )

        # Note that we no longer need to use ctypes or win32api to
        # make transparent windows, however I'm not removing the
        # MakeTransparent code from this sample as it may be helpful
        # to someone for other uses, someday.

        #self.MakeTransparent( self.alphaValue )

        # Instead, just call the SetTransparent() method
        self.SetTransparent( self.alphaValue )      # Easy !

    #end ChangeAlpha def

    #--------------------------------------------------------

    def OnCloseWindow( self, evt ) :

        self.changeAlpha_timer.Stop()
        del self.changeAlpha_timer       # avoid a memory leak
        self.Destroy()

    #-----------------------------------------------------
    # MakeTransparent from russelg @https://www.programcreek.com/python/example/62777/win32api.GetProcAddress

    def MakeTransparent(self, amount):
        if os.name == 'nt':  # could substitute: sys.platform == 'win32'
            hwnd = self.GetHandle()
            _winlib = win32api.LoadLibrary("user32")
            pSetLayeredWindowAttributes = win32api.GetProcAddress(
                _winlib, "SetLayeredWindowAttributes")
            if pSetLayeredWindowAttributes is None:
                return
            exstyle = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            if 0 == (exstyle & 0x80000):
                exstyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW | win32con.WS_EX_TRANSPARENT
                win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, exstyle)
            win32gui.SetLayeredWindowAttributes(hwnd, 0, amount, 2)
        else:
            print('####  OS Platform must be MS Windows')
            self.Destroy() 

#end AppFrame class

#=======================================================

if __name__ == '__main__' :

    app = wx.App( False )
    frm = AppFrame()
    frm.Show()
    app.MainLoop()