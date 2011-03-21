from face_normalizer import FaceNormalizer

fn = FaceNormalizer(r'./inputData',r'./normData')
fn.proc_blocks()
fn.write_to_csv()