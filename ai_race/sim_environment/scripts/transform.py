
import cv2
import numpy as np


def display_cv_image(image):
    cv2.imshow('gray', image)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()

def add_edge(img):
    H, W = img.shape
    WID = int(np.max(img.shape) * 2**0.5)
    e_img = np.zeros((WID, WID))
    e_img[int((WID-H)/2):int((WID+H)/2),
          int((WID-W)/2):int((WID+W)/2)] = img
    return e_img


def translation_matrix(tx, ty):
    return np.array([[1, 0, -tx],
                     [0, 1, -ty],
                     [0, 0, 1]])


def rotation_matrix(a):
    return np.array([[np.cos(a), -np.sin(a), 0],
                     [np.sin(a),  np.cos(a), 0],
                     [        0,          0, 1]])


def shear_matrix(mx, my):
    return np.array([[1, -mx, 0],
                     [-my, 1, 0],
                     [0,  0, 1]])    


def scaling_matrix(sx, sy):
    return np.array([[1/sx, 0, 0],
                     [0, 1/sy, 0],
                     [0,  0, 1]])


def affin(img, m):
    WID = np.max(img.shape)
    x = np.tile(np.linspace(-1, 1, WID).reshape(1, -1), (WID, 1))
    y = np.tile(np.linspace(-1, 1, WID).reshape(-1, 1), (1, WID))
    p = np.array([[x, y, np.ones(x.shape)]])
    dx, dy, _ = np.sum(p * m.reshape(*m.shape, 1, 1), axis=1)
    u = np.clip((dx + 1) * WID / 2, 0, WID-1).astype('i')
    v = np.clip((dy + 1) * WID / 2, 0, WID-1).astype('i')
    return img[v, u]

img_path = "/home/jetson/Pictures/Screenshot.png"
#img = cv2.imread(img_path)
img = np.ones((480,620))
img[145:155, 315:325] = 0
e_img = add_edge(img)
m1 = rotation_matrix(-np.pi*3 / 4)
#m2 = scaling_matrix(0.5, 1.0)
#m3 = translation_matrix(0.5, 0)
m2 = shear_matrix(0.25, 0)
m = np.dot(m1, m2)
display_cv_image(affin(e_img, m))