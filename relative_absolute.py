import numpy as np

def map_alignment(points_map1, points_map2):
    
    # Reshape arrays to have shape (num_points, 2)
    points_map1 = points_map1.reshape(-1, 2)
    points_map2 = points_map2.reshape(-1, 2)

    # Compute the center of mass for each set of points
    mean_point1 = np.mean(points_map1, axis=0)
    mean_point2 = np.mean(points_map2, axis=0)

    # Subtract the means to center the points
    centered_points1 = points_map1 - mean_point1
    centered_points2 = points_map2 - mean_point2

    # Compute the cross-covariance matrix
    cov_matrix = np.dot(centered_points1.T, centered_points2)

    # Perform Singular Value Decomposition (SVD) to find the rotation matrix
    U, _, V = np.linalg.svd(cov_matrix)
    rotation_matrix = np.dot(V.T, U.T)

    # Compute the translation vector
    translation_vector = mean_point2 - np.dot(rotation_matrix, mean_point1)

    # Calculate x, y, and theta
    x = translation_vector[0]
    y = translation_vector[1]
    theta = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])

    # Calculate distance error
    transformed_points1 = np.dot(points_map1, rotation_matrix.T) + translation_vector
    distance_error = np.mean(np.sqrt(np.sum((transformed_points1 - points_map2) ** 2, axis=1)))
    distance_errors = np.sqrt(np.sum((transformed_points1 - points_map2) ** 2, axis=1))
    # Convert theta to degrees
    theta = np.degrees(theta)

    return x, y, theta, distance_error, distance_errors

# Call map_alignment function with the provided points_map1 and points_map2
# GPS-based target pose [x1 y1 x2 y2 ...]
points_str1 = "-13.6460	-3.6600	-29.9110	-14.2090	-50.4380	-29.9460	-71.0430	-42.8770	-88.9730	-55.3930"
points_map1 = np.fromstring(points_str1, dtype=float, sep=' ')

# Map-based target pose [x1 y1 x2 y2 ...]
points_str2="-14.0814	-3.5197	-30.5827	-13.6769	-51.5332	-28.9985	-72.4392	-41.4736	-90.6130	-53.6343"
points_map2= np.fromstring(points_str2, dtype=float, sep=' ')
x, y, theta, distance_error, distance_errors = map_alignment(points_map1, points_map2)

# Print the results
print('------------------absolute error------------------')
print('x(m):', round(x,4))
print('y(m):', round(y,4))
print('theta:', round(theta,4), 'degrees')
print('Distance Errors(m):', np.round(distance_errors,4))
print('Distance Error(m):', np.round(distance_error,4))


points_map1 = points_map1.reshape(-1, 2)
points_map2 = points_map2.reshape(-1, 2)

target_distance = []
for i in range(4):
    for j in range(i + 1, 5):
        a1 = points_map1[i]
        b1 = points_map1[j]
        dist1 = np.linalg.norm(b1 - a1)
        
        a2 = points_map2[i]
        b2 = points_map2[j]
        dist2 = np.linalg.norm(b2 - a2)
        
        target_distance.append(abs(dist1 - dist2))

target_distance = np.array(target_distance)
distance_error = np.mean(target_distance)
print('------------------relative error------------------')
print("Target distance(m):", np.round(target_distance,4))
print("Distance error(m):", round(distance_error,4))
