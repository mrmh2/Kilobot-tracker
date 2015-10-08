"""Track kilobots from a video."""

import os
import argparse

import numpy as np
from scipy.misc import imsave

import skimage.feature

from jicbioimage.core.image import Image

from protoimg2.transform import (
    find_edges,
    gaussian_filter,
    find_connected_components,
    component_centroids
)

def load_bot_template(template_filename):
    """Load bot template from file."""

    bot_template = Image.from_file(template_filename)

    return bot_template

def find_kilobots(image_filename, output_filename):
    """Find kilobots in a still image file."""

    kilobot_image = Image.from_file(image_filename)
    red_only = kilobot_image[:,:,0]

    imsave('red.png', red_only)
    edges = find_edges(red_only)
    blurred = gaussian_filter(edges, sigma=5)

    bot_template = load_bot_template('bot_template.png')

    match_result = skimage.feature.match_template(blurred, bot_template, pad_input=True)

    imsave('match_result.png', match_result)

    selected_area = match_result > 0.7

    imsave('selected_area.png', selected_area)

    ccs = find_connected_components(selected_area)
    centroids = component_centroids(ccs)

    return centroids
    #imsave(output_filename, centroids)


def generate_bot_template():
    bot_template = find_template('data/raw/output0001.png')
    imsave('bot_template.png', bot_template)

def do_dir(directory):
    composite_image = np.zeros((972, 1296, 3), dtype=np.uint8)
    #composite_image[:,:,] = 255, 255, 255
    for n, input_file in enumerate(os.listdir(directory)):
        full_input_filename = os.path.join(directory, input_file)
        output_filename = "output{}.png".format(n)
        kb_centroids = find_kilobots(full_input_filename, output_filename)

        centroid_locations = np.where(kb_centroids != 0)
        composite_image[centroid_locations] = 255, 255, 255
        print n

    imsave('composite_image.png', composite_image)

def main():

    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('directory', help='Directory of still image files.')

    args = parser.parse_args()

    do_dir(args.directory)



if __name__ == '__main__':
    main()
