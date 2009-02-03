"""
This script needs python 2.6 or above because uses the "with" statement.
"""
import wx
from  menuengine import *
import wx.lib.sized_controls as sc
from contextlib import contextmanager

TEST_USER = "JOE"
TEST_PASSWORD = "pass"
TEST_GROUPS = dict( joe = ["average"])

class User(object):
	username = None
	password = None

class MainFrame( wx.Frame ):
	def __init__(self, user):
		wx.Frame.__init__(self , None, -1, "Testing Menu Engine", size = ( 500,400))
		menuengine.frame = self
		self.panel = wx.Panel(self, -1)
		menuengine.user = user.username.lower()
		#getting test related groups for user. In real life this comes from a database
		for group in TEST_GROUPS[ user.username.lower() ]:
			menuengine.groups.append( group )
		c = menubar[    menu[ "File",  menuitem( bind = "OnNotReady" )["Open"], menuitem["Save"] , menusep[""],  menuitem( bind = "OnExit" )["Exit"] ], 
			menu["Accounting" , menuitem["Chart of Accounts"], menuitem["General Ledger"] ],
			menu[ "Accounts Receivable", menuitem["Customers"], menusep[""], menucheck["Round Amounts"], menucheck["Log Activity"], menusep[""], menuradio["Dollars"], menuradio["Euros"]],
			menu["Color",[ menuitem(bind = "OnColor")[x] for x in "Red Green Blue Yellow Black Grey".split()  ] ],
			menu["Other", menuitem(enable = "False")["Disabled"], menuitem["Enabled"], menuitem( user = "joe")["Only for Joe"], menuitem( group = "average")["Only for Average group"] ]
			]
		flatten( c )

	def OnExit( self, event ):
		self.Close()

	def OnNotReady(self, event):
		wx.MessageBox("Not ready", "Hey" )

	def OnColor(self, event):
		menu = event.GetEventObject()
		name = menu.GetLabel( event.GetId())
		color = wx.NamedColour(name.lower()) 
		self.panel.SetBackgroundColour( color )

class NonEmptyValidator( wx.PyValidator):
	def __init__( self, name, data):
		wx.PyValidator.__init__(self)
		self.name = name
		self.data = data
		
	def Clone( self):
		return NonEmptyValidator(self.name, self.data)

	def Validate(self, win):
		textCtrl = self.GetWindow()
		text = textCtrl.GetValue()
		# a warning.  setting SetBackgroundColour in mac os x is useless, because the background color of the TextCtrl can not change.
		if len(text) == 0:
			wx.MessageBox("{0} can't be empty!".format(self.name), caption="Validation Error")
			textCtrl.SetBackgroundColour("pink")
			textCtrl.SetFocus()
			textCtrl.Refresh()
			return False
		else:
			textCtrl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
			textCtrl.Refresh()
			return True

	def TransferToWindow( self):
		return True

	def TransferFromWindow( self):
		tc = self.GetWindow()
		value = tc.GetValue()
		setattr( self.data, self.name.lower(), value) 
		return True


class LoginDialog( sc.SizedDialog ):
	def __init__( self , user=""):
		sc.SizedDialog.__init__(self, None, -1 , "Pseudo-Login Dialog", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
		self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY) # Tks to Robin Dunn for his advice on this...when using SizedDialog
		pane = self.GetContentsPane()
		pane.SetSizerType("form")
		self.user = user
	        self.ID_USERNAME = wx.NewId()	
		wx.StaticText(pane, -1, "User")
		user = wx.TextCtrl(pane, self.ID_USERNAME ,"", validator = NonEmptyValidator("username", self.user))
		user.SetSizerProps(expand=True)
		
		wx.StaticText(pane, -1, "Password")
		password = wx.TextCtrl(pane, -1 ,"", style=wx.TE_PASSWORD, validator = NonEmptyValidator("password", self.user))
		password.SetSizerProps(expand=True)
		self.Bind( wx.EVT_TEXT, self.OnText, id = self.ID_USERNAME)
		
		self.SetButtonSizer( self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))
		self.Fit()
		self.SetMinSize(self.GetSize())
		user.SetFocus()

	def OnText(self,event):
		id = event.GetId()
		if id == self.ID_USERNAME:
			t = self.FindWindowById( id )
			v = t.GetValue()
			v = v.upper()
			t.SetValue(v)
			lastposition = t.GetLastPosition()
			t.SetInsertionPoint(lastposition)

@contextmanager
def dialog( params ):
	#@contextmanager restricts this function to receive one argument, that's why we place everything in a dict
	DialogClass = params["dialog"]
	params.pop("dialog")
	try:
		dlg = DialogClass(**params)
		dlg.CenterOnScreen()
		val = dlg.ShowModal()
		yield val
	except:
		raise
	else:
		dlg.Destroy()

if __name__ == "__main__":
	app = wx.PySimpleApp()
	user = User()
	#using "with" which is new in python 2.6 and above.  You submit an object as a carrier of returned data from the Dialog
	with dialog( dict(dialog = LoginDialog, user = user ) ) as val:
		#in this case for testing purposes trying to validate against to variables. In real life this is against a database
		if user.username == TEST_USER and user.password == TEST_PASSWORD:
			f = MainFrame( user )
			f.CenterOnScreen()
			f.Show()
	app.MainLoop()
