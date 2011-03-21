import wx
from face_file_parser import FaceFileParser

class ImageValidationFrame(wx.Frame):
    def __init__(self,parent,title,dir):
        ffp = FaceFileParser()
        ffp.add_dir(dir)
        data_imgs = ffp.get_data()
        wx.Frame.__init__(self,parent,title=title,size=(300,650))
        
        self.imgs = [[],[],[],[]]
        self.images = [[], [], [], []]
        
        for img in data_imgs:
            self.imgs[img[0]].append(img)
        
        for a in range(0,4):
            self.images[a] = self.make_images(self.imgs[a])
            
        for a in range(0,4):
            for b in range(0,len(self.images[a])):
                i = self.images[a][b].ConvertToBitmap()
                wx.StaticBitmap(self,-1,i,(5 + (70 * a), 5 + (30 * b)))
            
        #i = self.images[0].Scale(240,80,wx.IMAGE_QUALITY_NORMAL)
        #self.show_img = wx.StaticBitmap(self,-1,i.ConvertToBitmap(),(5,5))
        #self.img_c = 0
        #self.next_b = wx.Button(self,label='Next',pos=(5,90))
        #self.Bind(wx.EVT_BUTTON,self.next_img,self.next_b)
        
        self.Show()
        
    #def next_img(self,event):
    #    self.img_c += 1
    #    self.img_c = self.img_c % len(self.images)
    #    i = self.images[self.img_c].Scale(240,80,wx.IMAGE_QUALITY_NORMAL)
    #    self.show_img = wx.StaticBitmap(self,-1,i.ConvertToBitmap(),(5,5))
    #    self.Refresh()
        
    def make_images(self,src_data):
        ret_images = []
        
        for img in src_data:
            i = wx.EmptyBitmap(width=60,height=20).ConvertToImage()
            data = list(img[1])
            l_e = data[:50]
            r_e = data[50:100]
            mo = data[100:]
            #Create the typestrip which tells us the class of the face
            for x in range(0,2):
                for y in range(0,20):
                    if img[0] == 0:
                        i.SetRGB(x,y,0,0,0)
                    elif img[0] == 1:
                        i.SetRGB(x,y,255,0,0)
                    elif img[0] == 2:
                        i.SetRGB(x,y,0,255,0)
                    elif img[0] == 3:
                        i.SetRGB(x,y,0,0,255)
            ct = 0
            for x in range(5,10):
                for y in range(5,15):
                    i.SetRGB(x,y,l_e[ct],l_e[ct],l_e[ct])
                    ct += 1
            ct = 0
            for x in range(15,20):
                for y in range(5,15):
                    i.SetRGB(x,y,r_e[ct],r_e[ct],r_e[ct])
                    ct += 1
            ct = 0
            for x in range(25,55):
                for y in range(5,15):
                    i.SetRGB(x,y,mo[ct],mo[ct],mo[ct])
                    ct += 1
            ret_images.append(i)
        
        return ret_images