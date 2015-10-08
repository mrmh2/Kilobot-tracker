"""Make composite image from video still and tracking data."""

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



def generate_composite_image(base_image, trajectory_image):
	still_image = Image.from_file(base_image)
	trajectories = Image.from_file(trajectory_image)[:,:,0]

	annotation_points = np.where(trajectories != 0)

	color = 255, 0, 0

	for x, y in zip(*annotation_points):
		still_image[x, y] = color
		still_image[x+1, y] = color
		still_image[x-1, y] = color
		still_image[x, y+1] = color
		still_image[x, y-1] = color								

	imsave('annotated_image.png', still_image)

def main():

	parser = argparse.ArgumentParser(__doc__)
	#parser.add_argument('directory', help='Directory of still image files.')
	parser.add_argument('base_image', help='Still image from kilobot video.')
	parser.add_argument('overlay_image', help='Image containing bot trajectories.')

	args = parser.parse_args()

	generate_composite_image(args.base_image, args.overlay_image)






if __name__ == '__main__':
	main()