"""Find and save a template bot image."""

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

def find_template(filename):
    """Find template kilobot for matching. Currently hard-c"""

    kilobot_image = Image.from_file(filename)
    red_only = kilobot_image[:,:,0]

    edges = find_edges(red_only)
    blurred = gaussian_filter(edges, sigma=2)

    x1 = 135
    x2 = 185
    y1 = 485
    y2 = 535

    bot_template = blurred[135:185,485:535]

    return bot_template

def find_template_leader(filename):
    """Find template kilobot for matching. Currently hard-c"""

    kilobot_image = Image.from_file(filename)
    red_only = kilobot_image[:,:,0]

    edges = find_edges(red_only)
    blurred = gaussian_filter(edges, sigma=5)

    x1 = 255
    x2 = 325
    y1 = 650
    y2 = 710

    bot_template = blurred[x1:x2,y1:y2]

    return bot_template


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
    blurred = gaussian_filter(edges, sigma=2)

    # bot_template = blurred[135:185,485:535]

    # imsave('bot_template.png', bot_template)

    bot_template = load_bot_template('bot_template.png')

    match_result = skimage.feature.match_template(blurred, bot_template, pad_input=True)

    imsave('match_result.png', match_result)

    selected_area = match_result > 0.6

    imsave('selected_area.png', selected_area)

    ccs = find_connected_components(selected_area)
    centroids = component_centroids(ccs)

    return centroids
    #imsave(output_filename, centroids)


def generate_bot_template():
    bot_template = find_template('data/raw/output0001.png')
    imsave('bot_template.png', bot_template)

def do_dir():
    composite_image = np.zeros((480, 720, 3), dtype=np.uint8)
    #composite_image[:,:,] = 255, 255, 255
    for n, input_file in enumerate(os.listdir(args.directory)):
        full_input_filename = os.path.join(args.directory, input_file)
        output_filename = "output{}.png".format(n)
        kb_centroids = find_kilobots(full_input_filename, output_filename)

        centroid_locations = np.where(kb_centroids != 0)
        composite_image[centroid_locations] = 255, 255, 255
        print n

    imsave('composite_image.png', composite_image)

def main():

    parser = argparse.ArgumentParser(__doc__)
    #parser.add_argument('directory', help='Directory of still image files.')
    parser.add_argument('still_image', help='Still image from kilobot video.')

    args = parser.parse_args()

    bot_template = find_template_leader(args.still_image)
    imsave('bot_template.png', bot_template)


if __name__ == '__main__':
    main()
