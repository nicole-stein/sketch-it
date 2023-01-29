from flask import Flask, render_template, request, redirect, url_for, send_file
from utils import *
import subprocess
import os
from skimage import io
import matplotlib.pyplot as plt
import time


import importlib 
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import feature, io, segmentation, color
from skimage.color import rgb2gray, gray2rgb
from skimage.transform import probabilistic_hough_line, resize
from time import time
FRAMES = [
    (5, 5),
    (5, 4.5),
    (4.5,4.2),
    (4.4,4),
    (4,3.8),
    (3.8,3.6),
    (3.8,3.2),
    (3.2,3.2),
    (3,2.9),
    (2.7,2.7),
    (2.4,2.4),
    (2,2.1),
    (1.8,1.7),
    (1.5,1.2),
    (1.5,0.5),
]



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
UPLOAD_FOLDER = 'submissions'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit_photo", methods=["GET", "POST"])
def submit_photo():
    if request.method == "POST":
        
        # For now, save the photo down into the "submissions" folder
        imgfile = request.files.get('submitted_photo')
        img = io.imread(imgfile)
        image_filenames = process_img(img)
        return render_template("draw.html", image_filenames=image_filenames)

    else:
        return redirect(url_for('index'))

@app.route("/temp", methods=["GET", "POST"])
def temp():
    image_filenames = [f"output/image{str(i+1)}.png" for i in range(9)]
    return render_template("draw.html", image_filenames=image_filenames)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# Make filenames work in both production and development
def filepath(path):
    if is_production():
        return "/home/sketchit/sketch-it/" + path
    else:
        return path

def is_production():
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url != developer_url


if __name__ == "__main__":
    try:
        current = subprocess.check_output(["lsof", "-t", "-i:5000"])
        current = max(current.decode("utf-8").split("\n"))
        print(f"kill {current}")
        os.system(f"kill {current}")
    except Exception as e:
        print(e)
    os.system("flask run")


def process_img(img):
    original_img = set_new_size(img)
    t = str(time())
    filenames = []
    last_image = None
    for i, frame in enumerate(FRAMES):
        print(i)
        img = ndi.gaussian_filter(rgb2gray(original_img), frame[0])
        img = feature.canny(img, sigma=frame[1])
        img = 255 - img
        plt.axis('off')
        plt.legend().remove()
        filename = "submissions/" + t + "_" + str(i) + ".png"
        filenames.append(filename)
        io.imsave(filepath('static/' + filename), img)

        # if i > 0:
        #     print("IN1")
        #     print("LAST IMG", last_image, "CURRENT", img)
        #     # io.imshow(last_image)
        #     # io.imshow(img)
        #     last_image = img.copy()
        # else:
        #     print("IN2")
        #     last_image = img.copy()

    return filenames


    
def set_new_size(img):
    fixed_height = 150
    new_width = round(img.shape[1] * (fixed_height / img.shape[0]))
    img = resize(img, (fixed_height, new_width), anti_aliasing=True)
    return img