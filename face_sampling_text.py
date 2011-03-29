import wx
from face_sampling_ui import FaceSamplerFrame

app = wx.App(False)
FaceSamplerFrame(None,'Generate Face Training Data')
app.MainLoop()
