from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from random                      import random

# Most obviously tunable params
EPOCHS = 50
IMG_SIZE = 5

# Emotion "enums"
class Emotion:
  SAD = 0
  SMILING = 1
  CALM = 2
  ASTONISHED = 3
  to_s = {
    0: "sad",
    1: "smiling",
    2: "calm",
    3: "astonished",

  }
  
class FacialClassifier:

  fnn = None;

  """
  classify(facialData) returns an int [0..3] from the Emotion class
    facialData is a IMG_SIZE-tuple with the color values of the eyes and mouth
  """
  def classify(self, facialData):
    if(self.fnn):
      emotion = self.fnn.activate(facialData)
      emotion = emotion.argmax()

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
      5, 
      train_faces.outdim, 
      outclass=SoftmaxLayer
    ) 
    # Set up the network trainer. Also nice tunable params
    trainer = BackpropTrainer(
      self.fnn, 
      dataset=train_faces, 
      momentum=0.1, 
      verbose=True,
      weightdecay=0.01
    ) 

    # Train this bitch. 
    if verbose:
      # Report after every epoch if verbose
      for i in range(EPOCHS):
        trainer.trainEpochs(1)

        trnresult = percentError( trainer.testOnClassData(),
                                  train_faces['class'] )
        tstresult = percentError( trainer.testOnClassData(
               dataset=test_faces ), test_faces['class'] )

        print "epoch: %4d" % trainer.totalepochs, \
              "  train error: %5.2f%%" % trnresult, \
              "  test error: %5.2f%%" % tstresult
    else:
      trainer.trainEpochs(EPOCHS)

  @classmethod
  def genRandomImg(cls):
      img = []
      for j in range(IMG_SIZE):
        img.append(int(random()*256))
      return img

  @classmethod
  def genRandomInputSet(cls):
    inputData = []
    for i in range(10):
      emo = int(random()*3)
      inputData.append((emo, tuple(cls.genRandomImg())))

    return inputData

      

    


