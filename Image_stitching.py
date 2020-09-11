"""
The goal of this task is to stitch two images of overlap into one image.
To this end, you need to find feature points of interest in one image, and then find
the corresponding ones in another image. After this, you can simply stitch the two images
by aligning the matched feature points.
For simplicity, the input two images are only clipped along the horizontal direction, which
means you only need to find the corresponding features in the same rows to achieve image stiching.

"""
import cv2
import numpy as np
import random

def solution(left_img, right_img):
    """
    :param left_img:
    :param right_img:
    :return: you need to return the result image which is stitched by left_img and right_img
    """
    sift = cv2.xfeatures2d.SIFT_create()
    key_pt1, descriptor1 = sift.detectAndCompute(right_img, None)
    key_pt2, descriptor2 = sift.detectAndCompute(left_img, None)
    # matching the key points obtained above to find the best possible matches
    bf = cv2.BFMatcher()             #could also use FLANN based matcher
    matches = bf.knnMatch(descriptor1, descriptor2, k=2)   #here k is used to specify how many matches per descriptor we need
    best_match = []

    for i, j in matches:
        if i.distance < 0.5 * j.distance:      #tried changing the ratio and using simple distance comparison but 0.5 works best
            best_match.append(i)

    kp1_indices = np.float32([key_pt1[x.queryIdx].pt for x in best_match])          #queryIdx refers to indices of key_pt1
    kp2_indices = np.float32([key_pt2[x.trainIdx].pt for x in best_match])          #trainIdx refers to indices of key_pt2
    # print(kp1_indices.shape)
    kp1_indices = kp1_indices.reshape(-1, 1, 2)
    kp2_indices = kp2_indices.reshape(-1, 1, 2)
    HG, notUsed = cv2.findHomography(kp1_indices, kp2_indices, cv2.RANSAC, 5.0)                   #here 5.0 is the threshold given to RANSAC to classify inliers and outliers
    # print(HG)
    # print(left_img.shape[0])

    result = cv2.warpPerspective(right_img, HG, (right_img.shape[1] + left_img.shape[1], left_img.shape[0]))    #warp the Right img wrt to left so that it can be stitched according to matches
    result[0:left_img.shape[0], 0:left_img.shape[1]] = left_img                                                 #positioning left img so that it aligns perfectly with warped right img
    # cv2.imshow("Stitched_image.jpg", result)
    # cv2.waitKey()

    return result;
    # raise NotImplementedError

if __name__ == "__main__":
    left_img = cv2.imread('left.jpg')
    right_img = cv2.imread('right.jpg')
    result_image = solution(left_img, right_img)
    cv2.imwrite('results/task2_result.jpg',result_image)


