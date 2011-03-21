import wx
from face_sampling_ui import FaceSamplerFrame
from face_file_parser import FaceFileParser
from supervised_facial_classifier import SupervisedFacialClassifier


ffp = FaceFileParser()
ffp.add_dir("./inputData")
#ffp.add_dir("./normData")

datalist = ffp.get_data()
"""
print "Single Hidden Layer"
for i in range(2,20):
    fc = FacialClassifier()
    fc.alternateTrain(datalist, [(i)], 25)

print "Double Hidden Layer"
for i in range(2,20):
    fc = FacialClassifier()
    fc.alternateTrain(datalist, (i,i), 25)

print "Triple Hidden Layer"
for i in range(2,20):
    fc = FacialClassifier()
    fc.alternateTrain(datalist, (i,i,i), 25)
"""
fc = SupervisedFacialClassifier()
# alternateTrain(datalist, hiddenNodes, #epochs, log stats every X epochs)
fc.alternateTrain(datalist, (20,20), 500, 10);

"""
#Test a single input file
ffp2 = FaceFileParser()
ffp2.add_file("c:\\face457b\\inputData\\in01.csv")

datalist2 = ffp2.get_data()

emo,data = datalist2[0]
fc.classify(data)
"""
