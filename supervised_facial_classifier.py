from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from random                      import random

from pybrain.datasets            import SupervisedDataSet
from pybrain.structure           import FeedForwardNetwork
from pybrain.structure           import LinearLayer, SigmoidLayer
from pybrain.structure           import FullConnection

from classifier_util import Emotion, EPOCHS, IMG_SIZE, RandomFaceGen
 
class SupervisedFacialClassifier:

  fnn = None;

  """
  classify(facialData) returns an int [0..3] from the Emotion class
    facialData is a IMG_SIZE-tuple with the color values of the eyes and mouth
  """
  def classify(self, facialData, verbose=True):
    if(self.fnn):
      emotion = self.fnn.activate(facialData)
      emotion = emotion.argmax()

      if verbose:
        print "This face looks %s to me" % Emotion.to_s[emotion]

      return emotion
    

  """ 
  train(inputData, verbose=True) train the network
    inputData is a parsed CSV file, each array entry is a tuple of tuples:
    (Emotion.SOMETHING, (d,a,t,a,..,200))
    Where emotion is an int [1..4]
   """
  def train(self, inputData, verbose=True):

    # Set of data to classify:
    # - IMG_SIZE input dimensions per data point
    # - 1 dimensional output
    # - 4 clusters of classification
    all_faces = ClassificationDataSet(IMG_SIZE, 1, nb_classes=4)

    for entry in inputData:
      (emotion, data) = entry
      all_faces.addSample(data, [emotion])
     
    # Generate a test and a train set from our data
    test_faces, train_faces = all_faces.splitWithProportion(0.25)

    # Hack to convert a 1-dimensional output into 4 output neurons
    test_faces._convertToOneOfMany()   
    train_faces._convertToOneOfMany()
    
    # Set up the actual network. These are the tunable params
    self.fnn = buildNetwork( 
      train_faces.indim, 
      20, 
      train_faces.outdim, 
      outclass=SoftmaxLayer
    )
    
    # Set up the network trainer. Also nice tunable params
    trainer = BackpropTrainer(
      self.fnn, 
      dataset=train_faces, 
      momentum=0.1, 
      verbose=False,
      weightdecay=0.01
    )
    
    tabledata = []     

    # Train this bitch. 
    if verbose:
      # Report after every epoch if verbose
      for i in range(EPOCHS):
        trainer.trainEpochs(1)

        trnresult = percentError( trainer.testOnClassData(),
                                  train_faces['class'] )
        tstresult = percentError( trainer.testOnClassData(
               dataset=test_faces ), test_faces['class'] )

        tabledata.append((trainer.totalepochs,trnresult,tstresult))
    else:
      trainer.trainEpochs(EPOCHS)

    if verbose:
      print "Epoch\tTrain Error\tTest Error"
      for line in tabledata:
         print "%4d\t" % line[0], \
               "%5.2f%%\t\t" % line[1], \
               "%5.2f%%" % line[2]
    


  """ 
  alternateTrain(inputData, hiddenLayers, numEpochs, logFreq=1, verbose=True)
    trains the network
    inputData is a parsed CSV file, each array entry is a tuple of tuples:
    (Emotion.SOMETHING, (d,a,t,a,..,200))
    Where emotion is an int [1..4]
    hiddenLayers is a list of the hidden layer sizes (supports up to 3 hidden layers)
    numEpochs is the number of training epochs to perform
    logFreq is the frequency of epochs to output error data
   """
  def alternateTrain(self, inputData, hiddenLayers, numEpochs, logFreq=1, verbose=True):


    # Set of data to classify:
    # - IMG_SIZE input dimensions per data point
    # - 1 dimensional output
    # - 4 clusters of classification
    all_faces = ClassificationDataSet(IMG_SIZE, 1, nb_classes=4)

    for entry in inputData:
      (emotion, data) = entry
      all_faces.addSample(data, [emotion])
     
    # Generate a test and a train set from our data
    test_faces, train_faces = all_faces.splitWithProportion(0.25)

    # Hack to convert a 1-dimensional output into 4 output neurons
    test_faces._convertToOneOfMany()   
    train_faces._convertToOneOfMany()

    self.fnn = self.buildCustomNetwork(hiddenLayers,train_faces)
    
    # Set up the network trainer. Also nice tunable params
    trainer = BackpropTrainer(
      self.fnn, 
      dataset=train_faces, 
      momentum=0.1, 
      verbose=False,
      weightdecay=0.01
    ) 

    # Train this bitch. 
    if verbose:
      print "Epoch\tTrain Error\tTest Error\t%d Nodes" % hiddenLayers[0]
      # Report after every epoch if verbose
      for i in range(numEpochs):
        trainer.trainEpochs(1)
        
        if trainer.totalepochs % logFreq == 0 :
          trnresult = percentError( trainer.testOnClassData(),
                                    train_faces['class'] )
          tstresult = percentError( trainer.testOnClassData(
                 dataset=test_faces ), test_faces['class'] )

          print "%4d\t" % trainer.totalepochs, \
                 "%5.2f%%\t\t" % trnresult, \
                 "%5.2f%%" % tstresult
    else:
      trainer.trainEpochs(EPOCHS)

  """
  Builds a ff network with various numbers of hiddenLayer/nodes
  """
  @classmethod
  def buildCustomNetwork(self, hiddenLayers, train_faces):
      myfnn = None
      if len(hiddenLayers) == 1:
          myfnn = buildNetwork( 
            train_faces.indim, 
            hiddenLayers[0],
            train_faces.outdim, 
            outclass=SoftmaxLayer
          )
      elif len(hiddenLayers) == 2:
          myfnn = buildNetwork( 
            train_faces.indim, 
            hiddenLayers[0],
            hiddenLayers[1],
            train_faces.outdim, 
            outclass=SoftmaxLayer
          )
      elif len(hiddenLayers) == 3:
          myfnn = buildNetwork( 
            train_faces.indim, 
            hiddenLayers[0],
            hiddenLayers[1],
            hiddenLayers[2],
            train_faces.outdim, 
            outclass=SoftmaxLayer
          )
      return myfnn


##### SMOKE TEST
if __name__ == '__main__':

  f = SupervisedFacialClassifier()
  t = RandomFaceGen.genRandomInputSet()
  f.train(t)
  for i in xrange(10):
    img = RandomFaceGen.genRandomImg()
    f.classify(img)
