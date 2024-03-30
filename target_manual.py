import open3d as o3d
import numpy as np

# Load pcd
point_cloud_path = "automotive_3.pcd"
pcd = o3d.io.read_point_cloud(point_cloud_path)
pcd_array = np.asarray(pcd.points)

#crop pcl, gps base
target_array = []
target_pos = [-9, -20]
for point in pcd_array:
    if(np.linalg.norm(point[0:2]-target_pos)<5):
        target_array.append(point)

target = o3d.geometry.PointCloud()
target.points = o3d.utility.Vector3dVector(target_array)

#cropping code
o3d.visualization.draw_geometries_with_editing([target])



