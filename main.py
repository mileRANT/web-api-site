# Project is going to be a basic website that pulls information to make a web api request
# will grab from daily quote

from flask import Flask, render_template, request
from PIL import Image, ImageOps
import numpy
app = Flask(__name__)


def give_most_hex(file_path, code):
    # resizing the image just incase image is too small
    # also retaining image colors because obviously that's important in this, so convert first
    my_image = Image.open(file_path).convert('RGB')
    size = my_image.size

    if size[0] >= 400 or size[1] >= 400:
        my_image = ImageOps.scale(image=my_image, factor=0.2)

    elif size[0] >= 600 or size[1] >= 600:
        my_image = ImageOps.scale(image=my_image, factor=0.4)

    elif size[0] >= 800 or size[1] >= 800:
        my_image = ImageOps.scale(image=my_image, factor=0.5)

    elif size[0] >= 1200 or size[1] >= 1200:
        my_image = ImageOps.scale(image=my_image, factor=0.6)

    my_image = ImageOps.posterize(my_image, 2)

    # Making the matrix of colours from our image.
    image_array = numpy.array(my_image)

    # create a dictionary of unique colors with each
    # color's count set to 0 increment count by 1 if it
    # exists in the dictionary
    unique_colors = {}  # (r, g, b): count
    for column in image_array:
        for rgb in column:
            t_rgb = tuple(rgb)
            if t_rgb not in unique_colors:
                unique_colors[t_rgb] = 1
            if t_rgb in unique_colors:
                unique_colors[t_rgb] += 1

    # get a list of top ten occurrences/counts of colors
    # from unique colors dictionary
    sorted_unique_colors = sorted(
        unique_colors.items(), key=lambda x: x[1], reverse=True)
    converted_dict = dict(sorted_unique_colors)

    # get only 10 highest values
    values = list(converted_dict.keys())
    top_10 = values[0:10]

    # code to convert rgb to hex
    print(code)
    if code == 'hex':
        hex_list = []
        for key in top_10:
            hex = rgb_to_hex(key)
            print(hex)
            hex_list.append(hex)
        return hex_list
    else:
        return top_10

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        colour_code = request.form['colour_code']
        hexes = give_most_hex(f.stream, colour_code)
        return render_template('index.html', colors_list=hexes, code=colour_code)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)