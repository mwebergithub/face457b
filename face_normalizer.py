from face_file_parser import FaceFileParser
import os.path

eye_c = 50
total_c = 400
mouth_c = total_c - 2*eye_c

class FaceNormalizer:
    def __init__(self,src_dir,dest_dir):
        ffp = FaceFileParser()
        ffp.add_dir(src_dir)
        data_imgs = ffp.get_data()
        self.img_lists = [[],[],[],[]]
        self.dest_dir = dest_dir
        
        for img in data_imgs:
            self.img_lists[img[0]].append(list(img[1]))
        
    def proc_blocks(self):
        
        self.norm_data  = [[],[],[],[]]
        
        for j in range(0,len(self.img_lists[0])):
            l_eyes = []
            r_eyes = []
            mouths = []
            for i in range(0,4):
                l_eyes += (self.img_lists[i][j][0:eye_c])
                r_eyes += (self.img_lists[i][j][eye_c:2*eye_c])
                mouths += (self.img_lists[i][j][2*eye_c:total_c])
            l_fact = float(128.0)/float((sum(l_eyes)/len(l_eyes)))
            r_fact = float(128.0)/(sum(r_eyes)/len(r_eyes))
            mouths_fact = float(128.0)/(sum(mouths)/len(mouths))
            for i in range(0,4):
                vals = []
                for k in range(0,eye_c):
                    vals.append(min(255,int(round(self.img_lists[i][j][k]*l_fact))))
                for k in range(eye_c,2*eye_c):
                    vals.append(min(255,int(round(self.img_lists[i][j][k]*r_fact))))
                for k in range(2*eye_c,total_c):
                    vals.append(min(255,int(round(self.img_lists[i][j][k]*mouths_fact))))
                self.norm_data[i].append(vals)
                
    def write_to_csv(self):
        for i in range(0,len(self.norm_data[0])):
            for j in range(0,4):
                f = None
                try:
                    f = open(os.path.join(self.dest_dir,'normdata' + str(i) + '-' + str(j) + '.csv'),'w')
                except IOError:
                    return -1
                for k in range(0,eye_c):
                    f.write('1,' + str(self.norm_data[j][i][k]) + '\n')
                for k in range(eye_c,2*eye_c):
                    f.write('1,' + str(self.norm_data[j][i][k]) + '\n')
                for k in range(2*eye_c,total_c):
                    f.write('1,' + str(self.norm_data[j][i][k]) + '\n')
                f.write(str(j))
                f.close()