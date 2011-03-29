import random
from wx import Image

class face_sampler:
    def __init__(self):
        self.eye_p_count = 50
        self.mouth_p_count = 400 - 2*self.eye_p_count
        self.mouth_st_d = 6.0
        self.eye_st_d = 2.0

    def sample_pixels(self,top_x,top_y,width,height,num_nodes,st_d):
        stdev_w = float(width) / st_d
        mean_w = float(width) / 2.0
        stdev_h = float(height) / st_d
        mean_h = float(height) / 2.0
        ret_nodes = []
        while len(ret_nodes) < num_nodes:
            x = top_x + random.gauss(mean_w,stdev_w)
            y = top_y + random.gauss(mean_h,stdev_h)
            if x > top_x and x < top_x + width and y > top_y and y < top_y + height:
                if not (x,y) in ret_nodes:
                    ret_nodes.append((x,y))
        return sorted(ret_nodes)
        
    #left_eye, right_eye and mouth are 4-tuples of (x,y,width,height)
    def gen_pixel_set(self,pic,left_eye,right_eye,mouth):
        l_eye_p = self.sample_pixels(left_eye[0],left_eye[1],left_eye[2],left_eye[3],self.eye_p_count,self.eye_st_d)
        r_eye_p = self.sample_pixels(right_eye[0],right_eye[1],right_eye[2],right_eye[3],self.eye_p_count,self.eye_st_d)
        mouth_p = self.sample_pixels(mouth[0],mouth[1],mouth[2],mouth[3],self.mouth_p_count,self.mouth_st_d)
        pic.ConvertToGreyscale()
        px_set = []
        for px in l_eye_p:
            print '1:' + str(px)
            px_set.append((1,pic.GetGreen(px[0],px[1])))
        for px in r_eye_p:
            print '2:' + str(px)
            px_set.append((2,pic.GetGreen(px[0],px[1])))
        for px in mouth_p:
            print '3:' + str(px)
            px_set.append((3,pic.GetGreen(px[0],px[1])))
        return px_set
        
    def write_to_csv(self,px_set,f_class,fname):
        f = None
        try:
            f = open(fname,'w')
        except IOError:
            return -1
        for px in px_set:
            print px
            f.write(str(px[0]) + ',' + str(px[1]) + '\n')
        f.write(str(f_class))
        f.close()
        return 0
