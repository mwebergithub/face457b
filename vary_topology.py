from face_file_parser import FaceFileParser
from supervised_facial_classifier import SupervisedFacialClassifier

max_hn = 400
min_hn = 50
step_size = 25
epochs = 750
output = 50

ffp = FaceFileParser()
sfc = SupervisedFacialClassifier()
ffp.add_dir('./normData')
d_s = ffp.get_data()

csv_out = open('./vary_topology.csv','w')
csv_out.write('topology,min test error,at epoch,avg test error,avg train error\n')

l1 = min_hn
while l1 <= max_hn:
    print 'Topology :' + str(l1) + '\n'
    results = sfc.alternateTrain(d_s,[(l1)],epochs,logFreq=output)
    min_err = min(results['testing_error'])
    at_e = results['epochs'][results['testing_error'].index(min_err)]
    avg_tst = results['avg_testing_error']
    avg_trn = results['avg_training_error']
    csv_out.write(str(l1) + ';' + ',' + str(min_err) + ','
    + str(at_e) + ',' + str(avg_tst) + ',' + str(avg_trn) + '\n')
    print 'Minimum error of ' + str(min_err) + ' at epoch ' + str(at_e)

    l2 = min_hn
    while l2 <= max_hn:
        print 'Topology :' + str(l1) + ';' + str(l2) + '\n'
        results = sfc.alternateTrain(d_s,(l1,l2),epochs,logFreq=output)
        min_err = min(results['testing_error'])
        at_e = results['testing_error'].index(min_err)
        avg_tst = results['avg_testing_error']
        avg_trn = results['avg_training_error']
        csv_out.write(str(l1) + ';' + str(l2) + ',' + str(min_err) + ','
        + str(at_e) + ',' + str(avg_tst) + ',' + str(avg_trn) + '\n')
        print 'Minimum error of ' + str(min_err) + ' at epoch ' + str(at_e)
        
        l3 = min_hn
        while l3 <= max_hn:
            print 'Topology :' + str(l1) + ';' + str(l2) + ';' + str(l3) + '\n'
            results = sfc.alternateTrain(d_s,(l1,l2,l3),epochs,logFreq=output)
            min_err = min(results['testing_error'])
            at_e = results['testing_error'].index(min_err)
            avg_tst = results['avg_testing_error']
            avg_trn = results['avg_training_error']
            csv_out.write(str(l1) + ';' + str(l2) + ';' + str(l3) + ',' + str(min_err) + ','
            + str(at_e) + ',' + str(avg_tst) + ',' + str(avg_trn) + '\n')
            print 'Minimum error of ' + str(min_err) + ' at epoch ' + str(at_e)
            l3 += step_size
        l2 += step_size
    l1 += step_size
    
csv_out.close()