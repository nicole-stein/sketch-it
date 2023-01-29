from flask import Flask, render_template, request, redirect, url_for, send_file
from utils import *
import subprocess
import os
from skimage import io
import matplotlib.pyplot as plt
import time

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
        io.imshow(img)
        plt.savefig("submissions/image")

        # TODO: Edit images
        time.sleep(1)

        # Return filenames
        image_filenames = [f"output/image{str(i+1)}.png" for i in range(9)]
        print(image_filenames)
        return render_template("draw.html", image_filenames=image_filenames)

    else:
        return redirect(url_for('index'))

@app.route("/temp", methods=["GET", "POST"])
def temp():
    image_filenames = [f"output/image{str(i+1)}.png" for i in range(9)]
    print(image_filenames)
    return render_template("draw.html", image_filenames=image_filenames)


@app.route('/database_download/<filename>')
def database_download(filename):
    return send_file(filename)

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
