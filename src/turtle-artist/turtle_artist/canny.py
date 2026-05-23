import numpy as np

def convolve(img, kernel):
    img_h, img_w = img.shape
    ker_h, ker_w = kernel.shape

    pad_h = ker_h // 2
    pad_w = ker_w // 2

    padded = np.pad(
        img,
        ((pad_h, pad_h), (pad_w, pad_w)),
        mode='constant'
    )
    
    kernel = np.flipud(np.fliplr(kernel))
    
    output = np.zeros((img_h, img_w))

    for i in range(img_h):
        for j in range(img_w):
            region = padded[i:i+ker_h, j:j+ker_w]
            output[i, j] = np.sum(region * kernel)
            
    return output

def gaussian_kernel(size=5, sigma=1.0):
    ax = np.arange(-size // 2 + 1, size // 2 + 1)
    xx, yy = np.meshgrid(ax, ax)

    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    kernel = kernel / np.sum(kernel)
    
    return kernel

def gaussian_blur(img, sigma=1.0):
    size = 6 * sigma + 1
    if size % 2 == 0:
        size += 1

    kernel = gaussian_kernel(size, sigma)
    return convolve(img, kernel)

def sobel(img):
    kernel_sobel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])

    kernel_sobel_y = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ])

    gx = convolve(img, kernel_sobel_x)
    gy = convolve(img, kernel_sobel_y)

    magnitude = np.hypot(gx, gy)
    magnitude = magnitude / magnitude.max() * 255
    theta = np.arctan2(gy, gx)

    return magnitude, theta

def non_max_suppression(img, theta):
    img_w, img_h = img.shape
    output = np.zeros((img_w,img_h))
    angle = theta * 180. / np.pi
    angle[angle < 0] += 180
    
    for i in range(1,img_w-1):
        for j in range(1,img_h-1):
            try:
                q = 255
                r = 255
                
               # 0*
                if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                    q = img[i, j+1]
                    r = img[i, j-1]
                # 45*
                elif (22.5 <= angle[i,j] < 67.5):
                    q = img[i+1, j-1]
                    r = img[i-1, j+1]
                # 90*
                elif (67.5 <= angle[i,j] < 112.5):
                    q = img[i+1, j]
                    r = img[i-1, j]
                # 135*
                elif (112.5 <= angle[i,j] < 157.5):
                    q = img[i-1, j-1]
                    r = img[i+1, j+1]

                if (img[i,j] >= q) and (img[i,j] >= r):
                    output[i,j] = img[i,j]
                else:
                    output[i,j] = 0

            except IndexError as e:
                pass
    
    return output

def threshold(img, lowThresholdRatio=0.2, highThresholdRatio=0.3):
    
    highThreshold = img.max() * highThresholdRatio
    lowThreshold = highThreshold * lowThresholdRatio
    
    img_w, img_h = img.shape
    res = np.zeros((img_w, img_h))
    
    weak = np.int32(25)
    strong = np.int32(255)
    
    strong_i, strong_j = np.where(img >= highThreshold)
    weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))
    
    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak
    
    return (res, weak, strong)

def hysteresis(img, weak, strong=255):
    M, N = img.shape  
    for i in range(1, M-1):
        for j in range(1, N-1):
            if (img[i,j] == weak):
                try:
                    if ((img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
                        or (img[i, j-1] == strong) or (img[i, j+1] == strong)
                        or (img[i-1, j-1] == strong) or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError as e:
                    pass
    return img

def edge_detector(img, sigma, live_viewer=True):
    if live_viewer:
        try:
            import matplotlib.pyplot as plt
        except: 
            print("Failed to import matplotlib!")
            return False
        plt.ion()
        if plt.get_fignums():  # if any figure already exists
            plt.close('all')
        
    img = np.mean(img, axis=2)

    if live_viewer:
        fig, ax = plt.subplots()
        im = ax.imshow(img, cmap='gray')
        ax.set_title(f"Canny Edge Detection (σ = {sigma})")
        plt.axis("off")
        plt.show()
        plt.pause(0.5)

    def update(img):
        if live_viewer:
            im.set_data(img)
            plt.draw()
            plt.pause(0.1)
    
    update(img)

    img = gaussian_blur(img, sigma)
    update(img)

    img, theta = sobel(img)
    update(img)

    img = non_max_suppression(img, theta)
    update(img)

    img, weak, strong = threshold(img)
    update(img)

    img = hysteresis(img, weak, strong)
    update(img)

    return img