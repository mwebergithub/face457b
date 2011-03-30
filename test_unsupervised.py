from face_file_parser import FaceFileParser
from unsupervised_facial_classifier import UnsupervisedFacialClassifier
import sys
import os

if not len(sys.argv) > 2:
  print "Usage: python test_unsupervised [data-dir] [num-trials]"
  exit()

root_data_dir = sys.argv[1]
num_trials = int(sys.argv[2])

for data_dir in os.walk(root_data_dir):
  (dirname, subdirs, files) = data_dir
  if len(subdirs) == 0:
    ffp = FaceFileParser(verbose=False)
    ffp.add_dir(dirname)
    datalist = ffp.get_data()

    print "################################"
    print dirname
    for trial in range(num_trials):
      print "Trial #%i" % trial
      fc = UnsupervisedFacialClassifier(2,2, 0.01)
      train_perf = fc.train(datalist, 300, test_proportion=0.25, verbose=False)
      print train_perf

