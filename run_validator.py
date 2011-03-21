import wx
from image_validation_frame import ImageValidationFrame

app = wx.App(False)
ImageValidationFrame(None,'Validation',r'./inputData')
app.MainLoop()
