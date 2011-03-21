from random                      import random

from scipy.ndimage import maximum_position
from scipy import zeros, array 
from custom_kohonen              import KohonenMap
from classifier_util import Emotion, EPOCHS, IMG_SIZE, RandomFaceGen

class UnsupervisedFacialClassifier:
  som = None
  emo_clusters = []

  def __init__(self, nNeurons, mNeurons):
    # KohonenMap of IMG_SIZE dimensions and a 2x2 grid. (try 4x1 later)
    self.som = KohonenMap(IMG_SIZE, nNeurons, mNeurons);
    #self.som.neighbourdecay = 0.990

    self.emo_clusters = [ [-1]*mNeurons for x in range(nNeurons)]
    
  def train(self, inputData, verbose=True):
    # Sort the known emotions into image piles, to assosciate a cluster with an
    # emotion after training, store that assosciation in emo_cluster
    cluster_identification_images = {
      Emotion.SAD: [],
      Emotion.SMILING: [],
      Emotion.CALM: [],
      Emotion.ASTONISHED: []
    }

    train_faces = []
    test_faces = []
    for entry in inputData:
      if (random() > 0.25):
        # Build training set with 75% of inputData
        (emotion, img) = entry
        cluster_identification_images[emotion].append(img)
        train_faces.append(img)
      else:
        # Build test set with the other 25%
        test_faces.append(entry)

    i = 0
    # Should the number of epochs be consistent with supervised?
    while self.som.neighbours > 0.5:
    #for epoch in range(EPOCHS):
      for img in train_faces:
        # Not sure if this can be done with som.activateOnDataset()
        self.som.activate(img)
        self.som.backward()


      i += 1
      if not (i % 10):
        print "SOM neighbors: %f" % self.som.neighbours


    for emotion in Emotion.to_s.keys():
      emo_count = zeros((self.som.nNeurons, self.som.mNeurons))
      for img in cluster_identification_images[emotion]:
        self.som.activate(img)
        emo_count[self.som.winner[0]][self.som.winner[1]] += 1
      dominant_node = maximum_position(emo_count)
      print self.emo_clusters
      self.emo_clusters[dominant_node[0]][dominant_node[1]] = emotion
      
      print emo_count
      print "Emo-Training Error: %f" % (1.0 - (emo_count[dominant_node[0]][dominant_node[1]] / 
                                    len(cluster_identification_images[emotion])))

    print "Final emo-map:"
    print self.emo_clusters

    error_count = 0
    print "Testing:"
    for entry in test_faces:
      (expectd_emo, img) = entry

      determined_emo = self.classify(img, verbose=False)
      if (expectd_emo != determined_emo):
        error_count += 1
        print "{>_<} Expected %s, got %s" % \
          (Emotion.to_s[determined_emo], Emotion.to_s[expectd_emo])
      else:
        print "{^-^} Classified a %s face correctly." % Emotion.to_s[determined_emo]

    print "Error rate on test-set: %f" %(error_count / len(test_faces))

    return False

  def classify(self, facialData, verbose=True ):
    self.som.activate(facialData)
    emotion = self.emo_clusters[self.som.winner[0]][self.som.winner[1]]

    if verbose:
      print "This face looks %s to me" % Emotion.to_s[emotion]

    return emotion


#################### TEST

f = UnsupervisedFacialClassifier(2,2)
t = RandomFaceGen.genRandomInputSet()
f.train(t)
for i in xrange(10):
  img = RandomFaceGen.genRandomImg()
  f.classify(img)
