import wx
from breve.tags import custom_tag, flatten_tag
from breve.flatten import flatten

class MenuEngine(object):
	frame = None
	counter = 0

menuengine = MenuEngine()

def flatten_menutag(val):
	msg = flatten_tag( val )
	label = val.children[0]
	mf = menuengine.frame
	try:
		mf.mb
	except:
		mf.mb = wx.MenuBar()
		mf.am = wx.Menu()

	if val.name == "menubar":
		mf.SetMenuBar( mf.mb )

	if val.name == "menu":
		mf.mb.Append( menuengine.frame.am, label )
		mf.am = wx.Menu()

	if val.name == "menusep":
		mf.am.AppendSeparator()

	if val.name == "menuitem":
		m = mf.am.Append( -1 , label) 
		if val.attrs.get("bind", ""):
			mf.Bind( wx.EVT_MENU, getattr( mf, val.attrs.get("bind")), m )

	if val.name == "menucheck":
		mf.am.AppendCheckItem( -1 , label) 

	if val.name == "menuradio":
		mf.am.AppendRadioItem( -1 , label )

	return msg

menubar, menu, menusep, menuitem, menucheck, menuradio = [ custom_tag( x, flattener = flatten_menutag) for x in "menubar menu menusep menuitem menucheck menuradio".split() ]

class MainFrame( wx.Frame ):
	def __init__(self):
		wx.Frame.__init__(self , None, -1, "Testing Menu Engine", size = ( 300,300))
		menuengine.frame = self
		self.panel = wx.Panel(self, -1)
		c = menubar[    menu[ "File",  menuitem( bind = "OnNotReady" )["Open"], menuitem["Save"] , menusep[""],  menuitem( bind = "OnExit" )["Exit"] ], 
			menu["Accounting" , menuitem["Chart of Accounts"], menuitem["General Ledger"] ],
			menu[ "Accounts Receivable", menuitem["Customers"], menusep[""], menucheck["Round Amounts"], menucheck["Log Activity"], menusep[""], menuradio["Dollars"], menuradio["Euros"]],
			menu["Color",[ menuitem(bind = "OnColor")[x] for x in "Red Green Blue Yellow Black Grey".split()  ] ]
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
		self.panel.Refresh()

if __name__ == "__main__":
	app = wx.PySimpleApp()
	MainFrame().Show()
	app.MainLoop()

