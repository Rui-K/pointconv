import os
import sys
import numpy as np 
import util
import h5py
import pickle
from plyfile import PlyData, PlyElement

def from_ply(split = "val", root = "E:\\基坑点云\\No3_LAS&PCD\\3_3_column_0\\columns-test.ply"):
    files = os.listdir(root)
    scene_data = []
    scene_data_labels = []
    scene_data_id = []
    scene_data_num = []
    for i in range(len(files)):
        file = os.path.join(root, files[i])
        scene_ply = PlyData.read(file)
        # print("reading...",file)
        scene_vertex = scene_ply['vertex']
        scene_data_tmp = np.stack((scene_vertex['x'], scene_vertex['y'],
                        scene_vertex['z'], scene_vertex['red'],
                        scene_vertex['green'], scene_vertex['blue']), axis = -1).astype(np.float32)
        
        scene_points_num = scene_data_tmp.shape[0]
        if (scene_points_num < 10000):
            print("data %s set too small, skip!", i)
            continue
        scene_data_id_tmp = np.array([c for c in range(scene_points_num)])

        if split == 'test':
            scene_label_tmp = np.zeros((scene_data_tmp.shape[0])).astype(np.int32)
        else:
            scene_label_tmp = scene_vertex['scalar_Scalar_field']#label

        scene_data.append(scene_data_tmp)
        scene_data_labels.append(scene_label_tmp)
        scene_data_id.append(scene_data_id_tmp)
        scene_data_num.append(scene_points_num)
    # origin data structure has list outside
    # scene_data_test=[]
    # scene_data_test.append(scene_data)

    if split == 'test':
        print(scene_data[0:3],'\n\n',scene_data_labels[0:3],'\n\n',scene_data_id[0:3], '\n\n', scene_data_num[0:3])

    print("writing "+split+" file...")
    # pickle_out = open("scannet_%s_rgb.pickle"%(split),"wb")
    pickle_out = open("scannet_%s_rgb.pickle"%(split),"wb")
    pickle.dump(scene_data, pickle_out, protocol=1)
    pickle.dump(scene_data_labels, pickle_out, protocol=1)
    pickle.dump(scene_data_id, pickle_out, protocol=1)
    pickle.dump(scene_data_num, pickle_out, protocol=1)
    pickle_out.close()

if __name__ =='__main__':
    root = "E:\\基坑点云\\No3_LAS&PCD\\3_3_total\\"
    # from_ply('val', file = root + 'Validation.ply')
    # from_ply('test', file = root + 'Test.ply')
    # from_ply('train', file = root + 'Train.ply')
    from_ply('val', root = root + 'validation')
    from_ply('test', root = root + 'test')
    from_ply('train', root = root + 'train')

    print("Done!")