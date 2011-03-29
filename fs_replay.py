from face_sampling import face_sampler
import os
import wx

class fs_replay:
    def __init__(self,replay_file):
        self.f_s = face_sampler()
        self.replays = []
        rf = open(replay_file,'r')
        while True:
            rp_file = rf.readline().strip()
            if rp_file == None or rp_file == '':
                break
            l_e = rf.readline().strip().split(',')
            r_e = rf.readline().strip().split(',')
            mouth = rf.readline().strip().split(',')
            type = rf.readline().strip()
            ofile = rf.readline().strip()
            self.replays.append((rp_file,(int(l_e[1]),int(l_e[2]),int(l_e[3]),int(l_e[4])),
            (int(r_e[1]),int(r_e[2]),int(r_e[3]),int(r_e[4])),
            (int(mouth[1]),int(mouth[2]),int(mouth[3]),int(mouth[4])),
            type,ofile))
        
            
    
    def replay(self):
        for (rp_file,l_e,r_e,mouth,type,ofile) in self.replays:
            img = wx.Image(rp_file)
            img = img.Scale(640,480,wx.IMAGE_QUALITY_HIGH)
            p_s = self.f_s.gen_pixel_set(img,l_e,r_e,mouth)
            self.f_s.write_to_csv(p_s,type,ofile)