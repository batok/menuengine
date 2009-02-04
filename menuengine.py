import wx
from breve.tags import custom_tag, flatten_tag
from breve.flatten import flatten

class MenuEngine(object):
	user = ""
	groups = []
	frame = None
	prebind = None
	_d_prebinds = dict()

menuengine = MenuEngine()

def prebind_wrapper( event = None ):
	met = menuengine._d_prebinds[ event.GetId() ]
	if menuengine.prebind:
		menuengine.prebind( met )
	
	method = getattr( menuengine.frame, met )( event )


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
	prebind = val.attrs.get("prebind", False )
	try:
		if prebind == "True":
			prebind = True
	except:
		pass
	help = val.attrs.get("help", "")
	user = val.attrs.get("user", "")
	group = val.attrs.get("group", "")
	
	if user and menuengine.user not in [ x.strip() for x in user.split(",")]:
		return msg
	
	if group:
		found = False
		for g in menuengine.groups:
			if g in [gr.strip() for gr in group.split(",")]:
				found = True
				break
		if not found:
			return msg
	
	try:
		mf.mb
	except:
		mf.CreateStatusBar()
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
		id = wx.NewId()
		mi = wx.MenuItem( parentMenu = mf.am, id = id , text = label,  help = help , kind = wx.ITEM_NORMAL, subMenu = None)
		m = mf.am.AppendItem( mi ) 
		mi.Enable( enable )
		if val.attrs.get("bind", ""):
			if prebind:
				menuengine._d_prebinds[ id ] = val.attrs.get("bind")
				mf.Bind( wx.EVT_MENU, prebind_wrapper, id = id )
			else:
				mf.Bind( wx.EVT_MENU, getattr( mf, val.attrs.get("bind")), m )

	if val.name == "menucheck":
		mf.am.AppendCheckItem( -1 , label) 

	if val.name == "menuradio":
		mf.am.AppendRadioItem( -1 , label )

	return msg

menubar, menu, menusep, menuitem, menucheck, menuradio = [ custom_tag( x, flattener = flatten_menutag) for x in "menubar menu menusep menuitem menucheck menuradio".split() ]

class MainFrame( wx.Frame ):
	def __init__(self):
		wx.Frame.__init__(self , None, -1, "Testing Menu Engine", size = ( 500,400 ))

		menuengine.frame = self
		menuengine.prebind = self.Logger
		c = menubar[  menu[ "File",  menuitem( bind = "OnNotReady" )["Open"], menuitem( prebind = "True", bind = "OnNotReady" )["Save"] , menusep[""],  menuitem( bind = "OnExit" )["Exit"] ] ]
		flatten( c )

	def OnExit( self, event ):
		self.Close()

	def OnNotReady(self, event):
		wx.MessageBox("Not ready", "Hey" )

	def Logger( self, met ):
		print "I am  here before %s" %  met

if __name__ == "__main__":
	app = wx.PySimpleApp()
	f = MainFrame()
	f.CenterOnScreen()
	f.Show()
	app.MainLoop()

