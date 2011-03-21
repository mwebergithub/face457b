import dircache
import os.path

class FaceFileParser:
    def __init__(self):
        self.dat_list = []
    
    def add_file(self,file):
        f = open(file,'r')
        vals = []
        emt = -1
        while f:
            f_l = f.readline()
            if ',' in f_l:
                vals.append(int(f_l.split(',')[1]))
            elif f_l != '':
                emt = int(f_l)
                break
        f.close()
        print 'Done with ' + file
        self.dat_list.append((emt,tuple(vals)))
        
    def add_files(self,files):
        for file in files:
            self.add_file(file)
    
    def get_data(self):
        return self.dat_list
        
    def add_dir(self,dir):
        dir_list = dircache.listdir(dir)
        files = []
        for f in dir_list:
            if os.path.isfile(os.path.join(dir,f)):
                files.append(os.path.join(dir,f))
                
        self.add_files(files)
        