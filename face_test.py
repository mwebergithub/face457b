from facial_classifier import FacialClassifier, Emotion

f = FacialClassifier()
t = f.genRandomInputSet()
f.train(t)
for i in xrange(10):
  img = f.genRandomImg()
  f.classify(img)
