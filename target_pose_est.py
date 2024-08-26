import open3d as o3d
import numpy as np
from scipy.linalg import svd

def fit_plane_RANSAC(points, n_iterations=100, distance_threshold=0.01):
    best_plane = None
    best_inliers = []

    for _ in range(n_iterations):
        # Randomly sample three points
        sample_indices = np.random.choice(points.shape[0], 3, replace=False)
        sample = points[sample_indices, :]

        # Fit a plane to the sampled points
        normal = np.cross(sample[1] - sample[0], sample[2] - sample[0])
        normal /= np.linalg.norm(normal)
        d = -np.dot(normal, sample[0])

        # Compute distances from all points to the fitted plane
        distances = np.abs(points @ normal + d) / np.linalg.norm(normal)

        # Identify inliers
        inliers = distances < distance_threshold

        # Check if the current model is the best so far
        if np.sum(inliers) > np.sum(best_inliers):
            best_inliers = inliers
            best_plane = np.append(normal, d)
        
    return best_plane, best_inliers

def custom_kmeans(points, n_iterations=100):
    if len(points) == 0:
        return np.array([])

    # Initialize centroids
    centroid1 = points[np.random.choice(points.shape[0])]
    centroid2 = points[np.random.choice(points.shape[0])]

    for _ in range(n_iterations):
        # Assign each point to the nearest centroid
        distances1 = np.linalg.norm(points - centroid1, axis=1)
        distances2 = np.linalg.norm(points - centroid2, axis=1)

        labels = distances1 < distances2

        if np.sum(labels) == 0 or np.sum(~labels) == 0:
            return np.array([])

        # Update centroids
        centroid1 = np.mean(points[labels], axis=0)
        centroid2 = np.mean(points[~labels], axis=0)

    return labels

point_cloud = "cropped_pointcloud.ply"
pcd = o3d.io.read_point_cloud(point_cloud)
pcd_array = np.asarray(pcd.points)

pos = []
ha = 0
deg = 1
ii = 0
ransac_error = 0.03

while ha < 100:
    # Custom KMeans
    labels = custom_kmeans(pcd_array, n_iterations=10)

    if len(labels) == 0:
        continue

    cluster1 = pcd_array[labels]
    cluster2 = pcd_array[~labels]

    # RANSAC for cluster 1
    best_eq1, best_inliers1 = fit_plane_RANSAC(cluster1, 100, ransac_error)
    best_plane1 = cluster1[best_inliers1]

    # RANSAC for cluster 2
    best_eq2, best_inliers2 = fit_plane_RANSAC(cluster2, 100, ransac_error)
    best_plane2 = cluster2[best_inliers2]

    # SVD
    centroid1 = np.mean(best_plane1, axis=0)
    centered_points1 = best_plane1 - centroid1
    _, _, Vt1 = svd(centered_points1)
    normal_vector1 = Vt1[-1, :]
    D1 = -np.dot(normal_vector1, centroid1)

    centroid2 = np.mean(best_plane2, axis=0)
    centered_points2 = best_plane2 - centroid2
    _, _, Vt2 = svd(centered_points2)
    normal_vector2 = Vt2[-1, :]
    D2 = -np.dot(normal_vector2, centroid2)

    z_mean = (centroid1[2] + centroid2[2]) / 2
    d = np.array([[-D1 - z_mean * normal_vector1[2]], [-D2 - z_mean * normal_vector2[2]]])
    ab = np.array([normal_vector1[:2], normal_vector2[:2]])
    invab = np.linalg.inv(ab)
    xy = invab @ d

    # Check angle conditions
    n1 = np.linalg.norm(normal_vector1[:3])
    n2 = np.linalg.norm(normal_vector2[:3])
    deg1 = np.arccos(normal_vector1[2] / n1) * 180 / np.pi
    deg2 = np.arccos(normal_vector2[2] / n2) * 180 / np.pi
    deg3 = np.arccos(np.dot(normal_vector1[:3], normal_vector2[:3]) / (n1 * n2)) * 180 / np.pi

    if (abs(deg1 - 90) < deg) and (abs(deg2 - 90) < deg) and (abs(deg3 - 90) < deg):
        pos.append(xy)
        ha += 1
        print(ha)
        print(ii)
    ii += 1

# Calculate average and standard deviation
avg = np.mean(pos, axis=0) if len(pos) > 0 else np.array([])
std = np.std(pos, axis=0) if len(pos) > 0 else np.array([])
print("Estimated target pose:" + str(avg.T))
print("Standard Deviation:" +str(std.T))
