import numpy as np
import matplotlib.pyplot as plt
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

def _weight_mean_color(graph, src, dst, n):
    diff = graph.nodes[dst]['mean color'] - graph.nodes[n]['mean color']
    diff = np.linalg.norm(diff)
    return {'weight': diff}

def merge_mean_color(graph, src, dst):
    graph.nodes[dst]['total color'] += graph.nodes[src]['total color']
    graph.nodes[dst]['pixel count'] += graph.nodes[src]['pixel count']
    graph.nodes[dst]['mean color'] = (graph.nodes[dst]['total color'] /
                                      graph.nodes[dst]['pixel count'])

sliders = {}
sliders_vals = []
def slide(label, valmin, valmax, valinit=None):
    if sliders.get(label):
        # Get slider value
        return sliders.get(label).val
    else:
        # Create slider and return value
        if not valinit:
            valinit = round((valmin+valmax)/2)
        vals = {
            "label": label,
            "valmin": valmin,
            "valmax": valmax,
            "valinit": valinit
        }
        sliders_vals.append(vals)
        return valinit

def make_sliders():
    for i, vals in enumerate(sliders_vals):
        h = (0.40 / len(sliders_vals) * i) + 0.05
        slider = Slider(
            ax=fig.add_axes([0.25, h, 0.65, 0.03]),
            label=vals['label'],
            valmin=vals['valmin'],
            valmax=vals['valmax'],
            valinit=vals['valinit']
        )
        sliders[vals['label']] = slider
        slider.on_changed(update)
    sliders_vals.clear()

img_paths = [
    "dog.jpg",
    "mountain.png",
    "car.png",
    "selfie.png",
    "selfie2.jpg"
]

original_imgs = []
for img in [io.imread(x) for x in img_paths]:
    fixed_height = 150
    new_width = round(img.shape[1] * (fixed_height / img.shape[0]))
    img = resize(img, (fixed_height, new_width), anti_aliasing=True)
    original_imgs.append(img)

fig, ax = plt.subplots(3, len(original_imgs))
fig.subplots_adjust(left=0.25, bottom=0.45)

def update(val):
    for i, original_img in enumerate(original_imgs):

        # # RAG Mean
        # img = original_img
        # labels = segmentation.slic(
        #     img,
        #     compactness=slide('compactness', 1, 40),
        #     n_segments=slide('n_segments', 1, 20, 5),
        #     start_label=1
        # )
        # g = graph.rag_mean_color(img, labels)
        # labels2 = graph.merge_hierarchical(labels, g, thresh=slide('thresh'), rag_copy=False,
        # in_place_merge=True, merge_func=merge_mean_color, weight_func=_weight_mean_color)
        # out = color.label2rgb(labels2, img, kind='avg', bg_label=0)
        # rag = segmentation.mark_boundaries(out, labels2, (0, 0, 0))
        # ax[1][i].imshow(rag)

        # Canny
        img = ndi.gaussian_filter(rgb2gray(original_img), slide('gaussian_blur', 0, 5, 3))
        canny = feature.canny(img, sigma=slide('sigma', 0, 5, 3.5))
        ax[0][i].imshow(canny)
        
        # # Remove small objects
        # img = remove_small_objects(img, min_size=slide('rag_min_size', 1, 100), connectivity=slide('rag_connectivity', 1, 100))
        # ax[2][i].imshow(img)

        # Threshold otsu
        val = threshold_otsu(rgb2gray(original_img))
        mask = rgb2gray(original_img) < val
        ax[1][i].imshow(mask)

        # # Threshold mutliotsu
        # thresholds = threshold_multiotsu(rgb2gray(original_img), classes=round(slide("multiotsu_classes", 2, 5, 2)))
        # regions = np.digitize(rgb2gray(original_img), bins=thresholds)
        # ax[2][i].imshow(regions)

        # # Subdivide polygon
        # img = subdivide_polygon(rgb2gray(original_img), degree=round(slide('degree', 0, 5)), preserve_ends=True)
        # ax[2][i].imshow(img)

        # # Skeletonize
        # img = skeletonize(canny)
        # ax[2][i].imshow(img, cmap=plt.cm.gray)

        # # Probabilistic Hough
        # lines = probabilistic_hough_line(canny, threshold=round(slide("hough_threshold", 1, 100)), line_length=round(slide("hough_line_length", 1, 100)), line_gap=round(slide("hough_line_gap", 1, 100)))
        # ax[2][i].cla()
        # ax[2][i].imshow(img * 0)
        # for line in lines:
        #     p0, p1 = line
        #     ax[2][i].plot((p0[0], p1[0]), (p0[1], p1[1]))
        # ax[2][i].set_xlim((0, img.shape[1]))
        # ax[2][i].set_ylim((img.shape[0], 0))
        
        # Circular Hough Transform
        hough_radii = np.arange(20, 100, 2)
        hough_res = hough_circle(canny, hough_radii)
        accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
            total_num_peaks=round(slide('n_circles', 1, 5))
        )
        img = gray2rgb(rgb2gray(original_img))
        for center_y, center_x, radius in zip(cy, cx, radii):
            circy, circx = circle_perimeter(center_y, center_x, radius,
                                            shape=img.shape)
            img[circy, circx] = (220, 20, 20)
        ax[2][i].imshow(img)

        make_sliders()
        fig.canvas.draw_idle()

update(0)
plt.show()

# level_1 = [
#     connectivity 3.7764423076922995
#     min_size 23.052884615384606
#     Gaussian Blur 1.5096153846153844
#     Sigma 3.573717948717949
# ]