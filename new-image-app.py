import importlib 
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import meijering, sato, frangi, hessian
from scipy import ndimage as ndi
from skimage import feature, io, segmentation, color
from skimage.future import graph
from skimage.morphology import remove_small_objects
from skimage.color import rgb2gray, gray2rgb
from matplotlib.widgets import Slider
from skimage.filters import sobel
from skimage import segmentation
from skimage.color import label2rgb
from skimage.transform import probabilistic_hough_line, resize
from skimage.measure import find_contours, approximate_polygon, subdivide_polygon
from skimage.filters import threshold_otsu, threshold_local, threshold_multiotsu
from skimage.morphology import skeletonize
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte

# #import image file
# pic = plt.imread("dog.jpg")
# #display image
# fig  = plt.figure()
# ax = fig.subplots()
# f = ax.imshow(pic[:,:,1], cmap = 'gray', vmin =0, vmax = 100)
# plt.show

def _weight_mean_color(graph, src, dst, n):
    diff = graph.nodes[dst]['mean color'] - graph.nodes[n]['mean color']
    diff = np.linalg.norm(diff)
    return {'weight': diff}


def merge_mean_color(graph, src, dst):
    graph.nodes[dst]['total color'] += graph.nodes[src]['total color']
    graph.nodes[dst]['pixel count'] += graph.nodes[src]['pixel count']
    graph.nodes[dst]['mean color'] = (graph.nodes[dst]['total color'] /
                                      graph.nodes[dst]['pixel count'])

# sliders = {}
# sliders_vals = []
# def slide(label, valmin, valmax, valinit=None):
#     if sliders.get(label):
#         # Get slider value
#         return sliders.get(label).val
#     else:
#         # Create slider and return value
#         if not valinit:
#             valinit = round((valmin+valmax)/2)
#         vals = {
#             "label": label,
#             "valmin": valmin,
#             "valmax": valmax,
#             "valinit": valinit
#         }
#         sliders_vals.append(vals)
#         return valinit

# def make_sliders():
#     for i, vals in enumerate(sliders_vals):
#         h = (0.40 / len(sliders_vals) * i) + 0.05
#         slider = Slider(
#             ax=fig.add_axes([0.25, h, 0.65, 0.03]),
#             label=vals['label'],
#             valmin=vals['valmin'],
#             valmax=vals['valmax'],
#             valinit=vals['valinit']
#         )
#         sliders[vals['label']] = slider
#         slider.on_changed(update)
#     sliders_vals.clear()

img_paths = [
    "dog.jpg",
    "mountain.png",
    "car.png",
    "selfie2.jpg"
]
original_imgs = []
for img in [io.imread(x) for x in img_paths]:
    fixed_height = 150
    new_width = round(img.shape[1] * (fixed_height / img.shape[0]))
    img = resize(img, (fixed_height, new_width), anti_aliasing=True)
    original_imgs.append(img)

fig, ax = plt.subplots(15, len(original_imgs))
fig.subplots_adjust(left=0.25, bottom=0.45)
# ax = plt.gca()
# ax.get_xaxis().set_visible(False)
# ax.get_yaxis().set_visible(False)

def frame1(img):
    img = ndi.gaussian_filter(rgb2gray(img), 5)
    img = feature.canny(img, sigma=5)
    img = 255-img #inverts colors from white line black bckg to black line white bckg
    return img

def frame2(img):
    img = ndi.gaussian_filter(rgb2gray(img),5)
    img = feature.canny(img, sigma=4.5)
    img = 255-img #inverts colors from white line black bckg to black line white bckg
    return img

def frame3(img):
    img = ndi.gaussian_filter(rgb2gray(img), 4.5)
    img = feature.canny(img, sigma=4.2)
    img = 255-img #inverts colors from white line black bckg to black line white bckg
    return img

def frame4(img):
    img = ndi.gaussian_filter(rgb2gray(img), 4.2)
    img = feature.canny(img, sigma= 4)
    img = 255-img #inverts colors from white line black bckg to black line white bckg
    return img

def frame5(img):
    img = ndi.gaussian_filter(rgb2gray(img), 4)
    img = feature.canny(img, sigma=3.8)
    img = 255-img #inverts colors from white line black bckg to black line white bckg
    return img

def frame6(img):
    img = ndi.gaussian_filter(rgb2gray(img), 3.8)
    img = feature.canny(img, sigma=3.6)
    img = 255-img #inverts colors from white line black bckg to black line white bckg
    return img

def frame7(img):
    img = ndi.gaussian_filter(rgb2gray(img), 3.8)
    img = feature.canny(img, sigma=3.2)
    img = 255-img #inverts colors from white line black bckg to black line white bckg
    return img

def frame8(img):
    img = ndi.gaussian_filter(rgb2gray(img), 3.2)
    img = feature.canny(img, sigma=3.2)
    img = 255-img #inverts colors from white line black bckg to black line white bckg
    return img

def frame9(img):
    img = ndi.gaussian_filter(rgb2gray(img), 3)
    img = feature.canny(img, sigma=2.9)
    img = 255-img 
    return img

def frame10(img):
    img = ndi.gaussian_filter(rgb2gray(img), 2.7)
    img = feature.canny(img, sigma=2.7)
    img = 255-img 
    return img

def frame11(img):
    img = ndi.gaussian_filter(rgb2gray(img), 2.4)
    img = feature.canny(img, sigma=2.4)
    img = 255-img 
    return img

def frame12(img):
    img = ndi.gaussian_filter(rgb2gray(img),2)
    img = feature.canny(img, sigma=2.1)
    img = 255-img 
    return img

def frame13(img):
    img = ndi.gaussian_filter(rgb2gray(img), 1.8)
    img = feature.canny(img, sigma= 1.7)
    img = 255-img 
    return img

def frame14(img):
    img = ndi.gaussian_filter(rgb2gray(img), 1.5)
    img = feature.canny(img, sigma=1.2)
    img = 255- img
    return img 

def frame15(img):
    img = ndi.gaussian_filter(rgb2gray(img), 1.5)
    img = feature.canny(img, sigma=0.5)
    img = 255-img 
    return img

    # labels = segmentation.slic(img, compactness=30, n_segments=4, start_label=1)
    # g = graph.rag_mean_color(img, labels)

    # labels2 = graph.merge_hierarchical(labels, g, thresh=35, rag_copy=False,
    #                                in_place_merge=True,
    #                                merge_func=merge_mean_color,
    #                                weight_func=_weight_mean_color)

    # out = color.label2rgb(labels2, img, kind='avg', bg_label=0)
    # out = segmentation.mark_boundaries(out, labels2, (0, 0, 0))
    # val = threshold_otsu(rgb2gray(img))
    # mask = rgb2gray(img) < val
    # img = 255- mask
    # img1 = ndi.gaussian_filter(img, 1)
    # img2 = ndi.gaussian_filter(rgb2gray(img), 1)
    # img2 = feature.canny(img2, sigma=1)
    # B = 255-img #inverts colors from white line black bckg to black line white bckg
    # img3 = np.ubyte(0.7*img1 + 0.3*img2)


#start process at stage 0, press next to advance

def update(val):
    stage = 1
    while stage <= 15: 
        for i, original_img in enumerate(original_imgs):
            if stage == 1: 
                img1 = frame1(original_img)
                ax[0][i].imshow(img1, cmap = 'gray')
                plt.savefig(f"img{str(i)}.png")# saves to desktop, should save to gallery on website 
            
            #elif stage == 2: 
                img2 = frame2(original_img)
                ax[1][i].imshow(img2, cmap = 'gray')
            
            #elif stage == 3: 
                img3 = frame3(original_img)
                ax[2][i].imshow(img3, cmap = 'gray')
            
            #elif stage == 4: 
                img4 = frame4(original_img)
                ax[3][i].imshow(img4, cmap = 'gray')
            
            #elif stage == 5: 
                img5 = frame5(original_img)
                ax[4][i].imshow(img5, cmap = 'gray')
            
            #elif stage == 6: 
                img6 = frame6(original_img)
                ax[5][i].imshow(img6, cmap = 'gray')

            #elif stage == 7: 
                img7 = frame7(original_img)
                ax[6][i].imshow(img7, cmap = 'gray')

            #elif stage == 8: 
                img8 = frame8(original_img)
                ax[7][i].imshow(img8, cmap = 'gray')

            #elif stage == 9: 
                img9 = frame9(original_img)
                ax[8][i].imshow(img9, cmap= 'gray')

            #elif stage == 10: 
                img10 = frame10(original_img)
                ax[9][i].imshow(img10, cmap= 'gray')

            #elif stage == 11: 
                img11 = frame11(original_img)
                ax[10][i].imshow(img11, cmap= 'gray')

            #elif stage == 12: 
                img12 = frame12(original_img)
                ax[11][i].imshow(img12, cmap= 'gray')

            #elif stage == 13: 
                img13 = frame13(original_img)
                ax[12][i].imshow(img13, cmap= 'gray')

            #elif stage == 14: 
                img14 = frame14(original_img)
                ax[13][i].imshow(img14, cmap= 'gray')

            #elif stage == 15: 
                img15 = frame15(original_img)
                ax[14][i].imshow(img15, cmap= 'gray')
            
            

            
                
        
            # # Canny
            # img = ndi.gaussian_filter(rgb2gray(original_img), slide('gaussian_blur', 0, 5, 3))
            # canny = feature.canny(img, sigma=slide('sigma', 0, 5, 3.5))
            # ax[0][i].imshow(canny)
    

            # # Threshold otsu
            # val = threshold_otsu(rgb2gray(original_img))
            # mask = rgb2gray(original_img) < val
            # ax[1][i].imshow(mask)

            #make_sliders()
            #fig.canvas.draw_idle()
            #button1 = input(print("Next"))
            # print(stage)
            # if button1 == "y":
            #     stage+=1
            #if buttonPressed = True, while loop continues 
        if stage ==1:
            plt.tight_layout()

            plt.show()
        else:
            fig.canvas.draw_idle()

        stage+=1
        
        
 

update(0)
plt.tight_layout()
plt.show()
