import os
import sys
import numpy as np 
import util
import h5py
import pickle
from plyfile import PlyData, PlyElement

def from_ply(split = "val", file = "E:\\基坑点云\\No3_LAS&PCD\\3_3_column_0\\columns-test.ply"):
    scene_ply = PlyData.read(file)
    scene_vertex = scene_ply['vertex']
    scene_data = np.stack((scene_vertex['x'], scene_vertex['y'],
                    scene_vertex['z'], scene_vertex['red'],
                    scene_vertex['green'], scene_vertex['blue']), axis = -1).astype(np.float32)
    
    scene_points_num = scene_data.shape[0]
    scene_data_id = np.array([c for c in range(scene_points_num)])

    if split == 'test':
        scene_label = np.zeros((scene_data.shape[0])).astype(np.int32)
    else:
        scene_label = scene_vertex['scalar_Scalar_field']#label
    # origin data structure has list outside
    # scene_data_test=[]
    # scene_data_test.append(scene_data)
    # print(scene_data_test,'\n\n',scene_label,'\n\n',scene_data_id, '\n\n', scene_points_num)

    pickle_out = open("scannet_%s_rgb.pickle"%(split),"wb")
    pickle.dump(scene_data, pickle_out, protocol=1)
    pickle.dump(scene_label, pickle_out, protocol=1)
    pickle.dump(scene_data_id, pickle_out, protocol=1)
    pickle.dump(scene_points_num, pickle_out, protocol=1)
    pickle_out.close()

if __name__ =='__main__':
    root = "E:\\基坑点云\\No3_LAS&PCD\\3_3_column_0\\"
    from_ply('val', file = root + 'columns-test.ply')