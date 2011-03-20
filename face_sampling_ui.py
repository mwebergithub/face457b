import wx
import os
from face_sampling import face_sampler

"""
class FaceStaticBitmap(wx.StaticBitmap):
    def __init__(self, parent, ID, img, pos,size):
        wx.StaticBitmap(parent,ID,wx.BitmapFromImage(img),pos=pos,size=size)
        self.pnl = FacePanel(self,pos=(0,0),size=size)
        self.Bind(wx.EVT_LEFT_DOWN,self.tst)
        
    def tst(self,event):
        print event.GetPosition()
"""


class FacePanel(wx.Panel):
    def __init__(self,parent,pos,size):
        wx.Panel.__init__(self,parent,pos=pos,size=size)
        
        self.state = 0
        self.px_ranges = {}
        self.px_ranges[1] = []
        self.px_ranges[2] = []
        self.px_ranges[3] = []
        
        self.bmp = wx.EmptyBitmap(640,480)
        self.Bind(wx.EVT_LEFT_DOWN,self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP,self.MouseUp)
        self.Bind(wx.EVT_ERASE_BACKGROUND,self.OnEraseBackground)
    
    def get_ranges(self):
        return self.px_ranges
    
    def set_bitmap(self,bmp):
        self.px_ranges[1] = []
        self.px_ranges[2] = []
        self.px_ranges[3] = []
        self.bmp = bmp
        self.Refresh()
        
    def set_state(self,state):
        self.state = state
        
    def MouseDown(self, event):
        if self.state != 0:
            self.px_ranges[self.state] = []
            self.px_ranges[self.state].append(event.GetPosition())
        print 'd' 
        print event.GetPosition()
        
    def MouseUp(self, event):
        if self.state != 0:
            self.px_ranges[self.state].append(event.GetPosition())
        print 'u'
        print event.GetPosition()
        
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
 
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        dc.DrawBitmap(self.bmp, 0, 0)
        
        print 'Drawing'


        
    
class FaceSamplerFrame(wx.Frame):
    def __init__(self,parent, title):
        wx.Frame.__init__(self, parent, title=title, size=wx.Size(665, 600))
        self.img_panel = FacePanel(self,pos=(5,5),size=(640,480))
        self.state = 0
        self.l_eye_coords = None
        self.r_eye_coords = None
        self.mouth_coords = None
        #self.refresh_img()
        
        self.typelist = ['Happy', 'Calm', 'Surprised', 'Sad']
        self.typebox = wx.RadioBox(self, label='Select the type of face this image represents',pos=(405,490),choices=self.typelist,majorDimension=2)
        
        self.l_eye_b = wx.Button(self,label='Left Eye',pos=(5,490))
        self.r_eye_b = wx.Button(self,label='Right Eye',pos=(85,490))
        self.mouth_b = wx.Button(self,label='Mouth',pos=(165,490))
        self.new_b = wx.Button(self,label='Select New Image',pos=(245,490))
        
        self.f_name_tb = wx.TextCtrl(self,pos=(5,520),size=(235,23))
        self.save_as_b = wx.Button(self,label='Save Data As',pos=(245,520))
        
        self.Bind(wx.EVT_BUTTON,self.select_new_image,self.new_b)
        self.Bind(wx.EVT_BUTTON,self.l_eye_evt,self.l_eye_b)
        self.Bind(wx.EVT_BUTTON,self.r_eye_evt,self.r_eye_b)
        self.Bind(wx.EVT_BUTTON,self.mouth_evt,self.mouth_b)
        self.Bind(wx.EVT_BUTTON,self.save_as,self.save_as_b)
        
        self.Show()
    
    def save_as(self, event):
        if self.f_name_tb.GetValue() != '':
            sets = self.img_panel.get_ranges()
            if (len(sets[1]) + len(sets[2]) + len(sets[3]) != 6):
                erwr = wx.MessageDialog(self,'Ranges are not properly selected.' 'Ranges Malformed', wx.OK)
                erwr.ShowModal()
                erwr.Destroy()
                return

            f_s = face_sampler()
            left_eye_range = (sets[1][0][0],sets[1][0][1],sets[1][1][0]-sets[1][0][0],sets[1][1][1]-sets[1][0][1])
            right_eye_range = (sets[2][0][0],sets[2][0][1],sets[2][1][0]-sets[2][0][0],sets[2][1][1]-sets[2][0][1])
            mouth_range = (sets[3][0][0],sets[3][0][1],sets[3][1][0]-sets[3][0][0],sets[3][1][1]-sets[3][0][1])
            p_s = f_s.gen_pixel_set(self.img,left_eye_range,right_eye_range,mouth_range)
            f_s.write_to_csv(p_s,self.typebox.GetSelection(),self.f_name_tb.GetValue())
    
    def l_eye_evt(self, event):
        self.state = 1
        self.img_panel.set_state(1)
        print 'State 1'
        
    def r_eye_evt(self, event):
        self.state = 2
        self.img_panel.set_state(2)
        print 'State 2'
    
    def mouth_evt(self, event):
        self.state = 3
        self.img_panel.set_state(3)
        print 'State 3'
    
    def select_new_image(self, event):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.img = wx.Image(os.path.join(self.dirname,self.filename))
            self.img = self.img.Scale(640,480,wx.IMAGE_QUALITY_NORMAL)
            #self.refresh_img()
            self.img_panel.set_bitmap(wx.BitmapFromImage(self.img))
        dlg.Destroy()

    def refresh_img(self):
        img = self.img.Scale(640,480,wx.IMAGE_QUALITY_NORMAL)
        self.bmp_img = wx.BitmapFromImage(img)
        self.st_bmp = wx.FaceStaticBitmap(self,-1,self.bmp_img,pos=(5,5),size=(640,480))
        self.Refresh()