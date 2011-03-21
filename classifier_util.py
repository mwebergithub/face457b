from random                      import random

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
  def genRandomInputSet(cls):
    inputData = []
    for i in range(20):
      emo = int(random()*4)
      inputData.append((emo, tuple(cls.genRandomImg())))

    return inputData
