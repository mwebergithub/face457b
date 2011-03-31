from face_file_parser import FaceFileParser
from unsupervised_facial_classifier import UnsupervisedFacialClassifier
import sys
import os
import numpy

# Ensure the correct number of commandline params
if not len(sys.argv) > 3:
  print "Usage: python test_unsupervised [data-dir | 'manual'] [num-trials] [outfile-name]"
  exit()

root_data_dir = sys.argv[1]
num_trials = int(sys.argv[2])
outfile_name = "%s.csv" % sys.argv[3] # Append .csv extension for excel

#learningrates_to_test = [0.05, 0.025, 0.01, 0.005]
learningrates_to_test = [0.01]

#neighbourdecays_to_test = [0.9990, 0.9995, 0.9999, 0.99995]
neighbourdecays_to_test = [0.9999]

epochs_to_test = [10, 25, 50, 100, 150, 200, 250, 300, 350]
#epochs_to_test = [200]

dirs_to_test = []
if root_data_dir == "manual":
  dirs_to_test = [ "./data/data_narrow/data_fcs_mouth_norm",
                 "./data/data_narrow/data_std_norm",
                 "./data/data_medium/data_std_mdplus_norm"]
else: 
  # For all leaf-node directories under the specified path we run trials
  for data_dir in os.walk(root_data_dir):
    (dirname, subdirs, files) = data_dir
    dirs_to_test.append(dirname)

# Write the trial data out to a file
outfile = open(outfile_name, 'w')
outfile.write("DIRNAME, LEARNINGRATE, DECAY, EPOCHS, TRAINING_ERR, TRAINING_ERR_STD, TESTING_ERR, TESTING_ERR_STD\n")

for dirname in dirs_to_test:
  for learningrate in learningrates_to_test:
    for neighbourdecay in neighbourdecays_to_test:
      for epochs in epochs_to_test:

        ffp = FaceFileParser(verbose=False)
        ffp.add_dir(dirname)
        datalist = ffp.get_data()

        print "################################"
        print " %s, learningrate: %s, decay: %s, epochs: %s" %\
          (dirname, learningrate, neighbourdecay, epochs)
        trial_avg_testing_err = []
        trial_avg_training_err = []

        # Run trials
        for trial in range(num_trials):
          print "Trial #%i" % trial
          fc = UnsupervisedFacialClassifier(2,2, 0.01)
          train_perf = fc.train(datalist, epochs, test_proportion=0.25, verbose=False)

          trial_avg_training_err.append(train_perf['avg_training_error'])
          trial_avg_testing_err.append(train_perf['avg_testing_error'])

          print "Average Training Error: %5.3f%%" % (train_perf['avg_training_error']*100.0)
          print "Average Testing Error: %5.3f%%" % (train_perf['avg_testing_error']*100.0)
          print "Emo Cluster Map: %s" % train_perf['emo_clusters']
          print "Final SOM Winner Error: %s" % train_perf['final_som_winner_err']

        print "\nSummary for %s, learningrate: %s, decay: %s" % \
          (dirname, learningrate, neighbourdecay)

        overall_training_error = numpy.mean(trial_avg_training_err)
        overall_training_error_std = numpy.std(trial_avg_training_err)

        overall_testing_error = numpy.mean(trial_avg_testing_err)
        overall_testing_error_std = numpy.std(trial_avg_testing_err)

        print "Overall Training Error and StDev: %5.3f%%, %5.4f" % (
          overall_training_error*100.0, overall_training_error_std)

        print "Overall Testing Error and StDev: %5.3f%%, %5.4f" % (
          overall_testing_error*100.0, overall_testing_error_std)

        outfile.write("%s, %s, %s, %s, %5.3f, %5.4f, %5.3f, %5.4f\n"% (
          dirname, learningrate, neighbourdecay, epochs,
          overall_training_error, overall_training_error_std, 
          overall_testing_error, overall_testing_error_std)
        )

        ffp.reset_data()

outfile.close()
