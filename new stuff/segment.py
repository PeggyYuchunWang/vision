import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image
import testcam

np.set_printoptions(threshold=np.nan)

def seg(box,imgstr):
    showImgs = False
    tl1 = box[0][0]
    tl2 = box[0][1]
    br1 = box[1][0]
    br2 = box[1][1]
    img = cv2.bilateralFilter(cv2.imread(imgstr),9,75,75)
    img = img[tl2:br2, tl1:br1]
    pil = Image.fromarray(img)
    w, h, channels = img.shape

    img2 = cv2.blur(img, (7, 7))
    img2 = (img2 * .8).astype(np.uint8)

    img3 = cv2.blur(img, (11, 11))
    img3 = (img3 * .5).astype(np.uint8)

    new_img = np.concatenate((img, img2, img3), axis=2)

    #displayImg(img, "Original Image", showImgs)
    labels = kmeans(new_img, 2, h, w)
    # img1, img2, img3 = generateThreeImages(labels, h, w)
    
    img1, img2, rgb, color = generateTwoImages(labels, h, w, img)

    return [img1, img2, rgb, pil, color]
    # plt.imsave('img3/test.png', img3)

def seg2(img):
    img = np.array(img)

    w, h, channels = img.shape

    img2 = cv2.blur(img, (7, 7))
    img2 = (img2 * .8).astype(np.uint8)

    img3 = cv2.blur(img, (11, 11))
    img3 = (img3 * .5).astype(np.uint8)

    new_img = np.concatenate((img, img2, img3), axis=2)

    #displayImg(img, "Original Image", showImgs)
    labels = kmeans(new_img, 2, h, w)
    # img1, img2, img3 = generateThreeImages(labels, h, w)
    
    img1, img2, img3 = generateThreeImages(labels, h, w)

    return[img1, img2, img3]

def generateTwoImages(labels,h,w,img):
    zeros = np.zeros((w, h), np.uint8)
    ones = np.zeros((w, h), np.uint8)
    ones.fill(255)

    img1 = np.zeros((w, h), np.uint8)
    img2 = np.zeros((w, h), np.uint8)

    labels = np.reshape(labels, (w, h))
    img1 = np.where(labels == 0, zeros, ones)
    
    img2 = np.where(labels == 1, zeros, ones)
    index = rav = gav = bav = 0
    for i in np.where(img2==0)[0]:
        b,g,r = img[i,np.where(img2==0)[1][index]]
        rav += r
        gav += g
        bav += b
        index+=1
    rav /= index
    gav /= index
    bav /= index
    im1 = Image.fromarray(np.uint8(img1))
    im2 = Image.fromarray(np.uint8(img2))
    im2.show()
    return im1, im2, [rav,gav,bav], minEuclideanDist(rav,gav,bav)

def minEuclideanDist(r,g,b):
    minNorm = 5000000
    color = ""
    norm = 0
    norm += (r-0)**2
    norm += (g-0)**2
    norm += (b-255)**2
    if norm <= minNorm:
        minNorm = norm
        color = "blue"
    norm = 0
    norm += (r-0)**2
    norm += (g-255)**2
    norm += (b-0)**2
    if norm <= minNorm:
        minNorm = norm
        color = "green"
    norm = 0
    norm += (r-255)**2
    norm += (g-0)**2
    norm += (b-0)**2
    if norm <= minNorm:
        minNorm = norm
        color = "red"
    norm = 0
    norm += (r-0)**2
    norm += (g-255)**2
    norm += (b-255)**2
    if norm <= minNorm:
        minNorm = norm
        color = "light blue"
    norm = 0
    norm += (r-255)**2
    norm += (g-255)**2
    norm += (b-0)**2
    if norm <= minNorm:
        minNorm = norm
        color = "yellow"
    norm = 0
    norm += (r-255)**2
    norm += (g-0)**2
    norm += (b-255)**2
    if norm <= minNorm:
        minNorm = norm
        color = "fuschia"
    norm = 0
    norm += (r-0)**2
    norm += (g-0)**2
    norm += (b-0)**2
    if norm <= minNorm:
        minNorm = norm
        color = "black"
    norm = 0
    norm += (r-255)**2
    norm += (g-255)**2
    norm += (b-255)**2
    if norm <= minNorm:
        minNorm = norm
        color = "white"
    norm = 0
    norm += (r-255)**2
    norm += (g-127)**2
    norm += (b-0)**2
    if norm <= minNorm:
        minNorm = norm
        color = "orange"
    return color


def generateThreeImages(labels,h,w):
    zeros = np.zeros((w, h), np.uint8)
    ones = np.zeros((w, h), np.uint8)
    ones.fill(255)

    img1 = np.zeros((w, h), np.uint8)
    img2 = np.zeros((w, h), np.uint8)
    img3 = np.zeros((w, h), np.uint8)

    labels = np.reshape(labels, (w, h))
    img1 = np.where(labels == 0, zeros, ones)
    img2 = np.where(labels == 1, zeros, ones)
    img3 = np.where(labels == 2, zeros, ones)
    img1 = Image.fromarray(np.uint8(img1))
    img2 = Image.fromarray(np.uint8(img2))
    img3 = Image.fromarray(np.uint8(img3))

    return img1, img2, img3
def cvtBinaryImage(img):
	mat1 = np.zeros((w, h), np.uint8)
	mat2 = np.zeros((w, h), np.uint8)
	mat2.fill(255)
	final = np.where(img, mat1, mat2);
	return final

def findLargestContour(contours):
    contourAreas = []
    for contour in contours:
        contourAreas.append(cv2.contourArea(contour))

    largestContour = contours[contourAreas.index(max(contourAreas))]
    return largestContour 


def calculateThreshold(centers):
    center1 = np.mean(centers[0])
    center2 = np.mean(centers[1])
    avg = np.mean([center1, center2])
    return int(avg)

def blackBackground(img):
    if img[1,1] != 0:
        return cv2.bitwise_not(img)
    else:
        return img

def displayImg(img, frameName, displayImg):
    plt.imshow(img)
    plt.show()

def kmeans(img, numClusters, h, w):
    #print img.shape
    Z = img.reshape((-1,3))

    #convert to np.float32
    Z = np.float32(Z)
    kmeans = KMeans(n_clusters=3, init="k-means++", random_state=0).fit(Z.reshape(w*h, 9))
    return kmeans.labels_

def get_neighborhood_variance(neighboorhood, mean):
    error = 0
    for i in range(neighboorhood.shape[0]):
        for j in range(neighboorhood.shape[1]):
            pixel = neighboorhood[i,j]
            error += np.linalg.norm(pixel - mean)
    error /= neighboorhood.size
    return error

def generate_rough_mask(image, threshold, radius):
    points = []
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            neighboorhood = image[x-radius:x+radius,y-radius:y+radius]
            if get_neighborhood_variance(neighboorhood, image[x,y]) < threshold:
                points.append((x,y))
    return points



if __name__ == "__main__":
    main()
