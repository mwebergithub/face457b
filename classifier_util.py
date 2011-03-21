from random import random
from numpy.random import multivariate_normal
from scipy import diag

# Most obviously tunable params
EPOCHS = 200
IMG_SIZE = 400

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
  
class RandomFaceGen:
    
  @classmethod
  def genRandomImg(cls):
      img = []
      for j in range(IMG_SIZE):
        img.append(int(random()*256))
      return img

  @classmethod
  def genRandomInputSet(cls, size=10):
    inputData = []
    for i in range(size):
      emo = int(random()*4)
      inputData.append((emo, tuple(cls.genRandomImg())))

    return inputData

  @classmethod
  def genGaussClusteredInputSet(cls, size=10):

    means = [
      tuple([10]*IMG_SIZE), 
      tuple([70]*IMG_SIZE), 
      tuple([130]*IMG_SIZE),
      tuple([200]*IMG_SIZE)
    ]
    cov = diag([1]*IMG_SIZE)
    inputData = []
    for i in range(size):
      emo = i % 4
      inputData.append((emo, multivariate_normal(means[emo], cov)))

    return inputData
