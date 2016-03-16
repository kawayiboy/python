import wx
import wx.lib.masked as masked
# import datetime
from datetime import datetime
import sys
sys.path.append('../')
import selfCommon

########################################################################
class TimeCtrlPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.parent = parent

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        timestr = datetime.strftime(datetime.now(), '%H:%M:%S')

        text1 = wx.StaticText( self, -1, "12-hour format:", size=(150,-1))
        self.time12 = masked.TimeCtrl( self, -1, value = timestr,name="12 hour control" )
        h = self.time12.GetSize().height
        spin1 = wx.SpinButton( self, -1, wx.DefaultPosition, (-1,h), wx.SP_VERTICAL )
        self.time12.BindSpinButton( spin1 )
        self.addWidgets([text1, self.time12, spin1])

        text2 = wx.StaticText( self, -1, "24-hour format:")
        spin2 = wx.SpinButton( self, -1, wx.DefaultPosition, (-1,h), wx.SP_VERTICAL )
        self.time24 = masked.TimeCtrl(
                        self, -1, value = timestr, name="24 hour control", fmt24hr=True,
                        spinButton = spin2
                        )
        self.addWidgets([text2, self.time24, spin2])

        text3 = wx.StaticText( self, -1, "No seconds\nor spin button:")
        self.spinless_ctrl = masked.TimeCtrl(
                                self, -1, value = timestr,name="spinless control",
                                display_seconds = False
                                )
        self.addWidgets([text3, self.spinless_ctrl])

        saveButton = wx.Button(self, label='Save')
        saveButton.Bind(wx.EVT_BUTTON, self.OnSave)
        self.addWidgets([saveButton])


        self.SetSizer(self.mainSizer)

    def call_program(self):
        outs, errs = selfCommon.exec_cmd(['python','../seleniumTest/selenium_bing.py',self.time24.GetValue()])
        print outs

    def OnSave(self, event):
        # print self.time24.GetValue()
        # self.Close()
        self.call_program()
        self.parent.Destroy()

    #----------------------------------------------------------------------
    def addWidgets(self, widgets):
        """"""
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for widget in widgets:
            if isinstance(widget, wx.StaticText):
                sizer.Add(widget, 0, wx.ALL|wx.CENTER, 5),
            else:
                sizer.Add(widget, 0, wx.ALL, 5)
        self.mainSizer.Add(sizer)

########################################################################

class DatePickerPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        dpc = wx.DatePickerCtrl(self, size=(120,-1),
                                style = wx.DP_DROPDOWN
                                      | wx.DP_SHOWCENTURY
                                      | wx.DP_ALLOWNONE )
        self.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged, dpc)
        sizer.Add(dpc, 0, wx.ALL, 50)

        # In some cases the widget used above will be a native date
        # picker, so show the generic one too.            
        dpc = wx.GenericDatePickerCtrl(self, size=(120,-1),
                                       style = wx.TAB_TRAVERSAL
                                       | wx.DP_DROPDOWN
                                       | wx.DP_SHOWCENTURY
                                       | wx.DP_ALLOWNONE )
        self.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged, dpc)
        sizer.Add(dpc, 0, wx.LEFT, 50)


    def OnDateChanged(self, evt):
        print("OnDateChanged: %s\n" % evt.GetDate())

class MyFrame(wx.Frame):
    """"""
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Spinner Demo")
        panel = TimeCtrlPanel(self)
        self.Show()

    # def __init__(self):
    #     """Constructor"""
    #     wx.Frame.__init__(self, None, title="Spinner Demo")
    #     panel = DatePickerPanel(self)
    #     self.Show()

if __name__ == "__main__":        
    app = wx.App(False)
    f = MyFrame()
    app.MainLoop()