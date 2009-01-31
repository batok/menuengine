import wx
from breve.tags import custom_tag, flatten_tag
from breve.flatten import flatten

class MenuEngine(object):
	frame = None

menuengine = MenuEngine()

def flatten_menutag(val):
	msg = flatten_tag( val )
	label = val.children[0]
	mf = menuengine.frame
	enable = val.attrs.get("enable", True )
	try:
		if enable == "False":
			enable = False
	except:
		pass
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
		mi = wx.MenuItem( parentMenu = mf.am, id = wx.ID_ANY, text = label,  kind=wx.ITEM_NORMAL, subMenu = None)
		
		m = mf.am.AppendItem( mi ) 
		mi.Enable( enable )
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
		wx.Frame.__init__(self , None, -1, "Testing Menu Engine", size = ( 500,400))
		menuengine.frame = self
		self.panel = wx.Panel(self, -1)
		c = menubar[    menu[ "File",  menuitem( bind = "OnNotReady" )["Open"], menuitem["Save"] , menusep[""],  menuitem( bind = "OnExit" )["Exit"] ], 
			menu["Accounting" , menuitem["Chart of Accounts"], menuitem["General Ledger"] ],
			menu[ "Accounts Receivable", menuitem["Customers"], menusep[""], menucheck["Round Amounts"], menucheck["Log Activity"], menusep[""], menuradio["Dollars"], menuradio["Euros"]],
			menu["Color",[ menuitem(bind = "OnColor")[x] for x in "Red Green Blue Yellow Black Grey".split()  ] ],
			menu["Other", menuitem(enable = "False")["Disabled"], menuitem["Enabled"]]
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

if __name__ == "__main__":
	app = wx.PySimpleApp()
	f = MainFrame()
	f.CenterOnScreen()
	f.Show()
	app.MainLoop()

