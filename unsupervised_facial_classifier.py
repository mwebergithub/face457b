from random import random
from scipy.ndimage import maximum_position
from scipy import zeros, array 
from numpy import mean
from custom_kohonen import KohonenMap
from classifier_util import Emotion, EPOCHS, IMG_SIZE, RandomFaceGen

class UnsupervisedFacialClassifier:
  som = None
  emo_clusters = []

  def __init__(self, nNeurons, mNeurons, learningrate=0.01, neighbourdecay=0.9999):
    # KohonenMap of IMG_SIZE dimensions and a 2x2 grid. (try 4x1 later)
    self.som = KohonenMap(IMG_SIZE, nNeurons, mNeurons);
    self.som.learningrate = learningrate
    self.som.neighbourdecay = neighbourdecay

    self.emo_clusters = [ [-1]*mNeurons for x in range(nNeurons)]
    
  def train(self, inputData, epochs, test_proportion=0.25, verbose=True):
    # Sort the known emotions into image piles, to assosciate a cluster with an
    # emotion after training, store that assosciation in emo_cluster
    cluster_identification_images = {
      Emotion.SAD: [],
      Emotion.SMILING: [],
      Emotion.CALM: [],
      Emotion.ASTONISHED: []
    }

    # Dictionary to return with performance metrics etc.
    train_perf = {}

    train_faces = []
    test_faces = []
    for entry in inputData:
      if (random() > test_proportion):
        # Build training set with 75% of inputData
        (emotion, img) = entry
        cluster_identification_images[emotion].append(img)
        train_faces.append(img)
      else:
        # Build test set with the other 25%
        test_faces.append(entry)

    i = 0
    #while (self.som.neighbours > 0.5 or i < epochs):
    while (i < epochs):
      for img in train_faces:
        # Not sure if this can be done with som.activateOnDataset()
        self.som.activate(img)
        self.som.backward()

      i += 1

      if verbose:
        if not (i % 20):
          print "SOM neighbors: %f" % self.som.neighbours
          print "SOM winner err: %f" % self.som.winner_error

    # Finished training SOM
    train_perf['epochs'] = i
    train_perf['final_som_winner_err'] = self.som.winner_error

    # Correlate N SOM clusters with N emotions
    training_error = []
    for emotion in cluster_identification_images.keys():
      emo_count = zeros((self.som.nNeurons, self.som.mNeurons))

      for img in cluster_identification_images[emotion]:
        self.som.activate(img)
        emo_count[self.som.winner[0]][self.som.winner[1]] += 1
      dominant_node = maximum_position(emo_count)
      training_error.append( 1.0 - 
        (1.0*emo_count[dominant_node[0]][dominant_node[1]]/
        len(cluster_identification_images[emotion]))
      )
      self.emo_clusters[dominant_node[0]][dominant_node[1]] = emotion

    # Record training error
    train_perf['training_error'] = training_error
    train_perf['avg_training_error'] = mean(training_error)

    train_perf['emo_clusters'] = self.emo_clusters

    # Start the testing set
    if verbose: print "Testing:"
    error_count = 0

    for entry in test_faces:
      (expectd_emo, img) = entry

      determined_emo = self.classify(img, verbose=False)
      if (expectd_emo != determined_emo):
        error_count += 1

        if verbose: print "{>_<} Expected %s, got %s" % \
            (Emotion.to_s[determined_emo], Emotion.to_s[expectd_emo])
      else:
        if verbose: print "{^-^} Classified a %s face correctly." % \
            Emotion.to_s[determined_emo]

    train_perf['avg_testing_error'] = (1.0*error_count / len(test_faces))

    if verbose: print train_perf
    return train_perf


  def classify(self, facialData, verbose=True ):
    self.som.activate(facialData)
    emotion = self.emo_clusters[self.som.winner[0]][self.som.winner[1]]

    if verbose:
      print "This face looks %s to me" % Emotion.to_s[emotion]

    return emotion


########## SMOKE TEST

if __name__ == '__main__':
  f = UnsupervisedFacialClassifier(2,2)
  t = RandomFaceGen.genGaussClusteredInputSet(50)
  f.train(t)

  #just for kicks
  img = RandomFaceGen.genRandomImg()
  f.classify(img)
