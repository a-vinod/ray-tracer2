#!/usr/bin/env python3

import argparse

from ray_tracer2.main import main

print("Ray Tracer in Python!")
parser = argparse.ArgumentParser(description='Ray Tracer in Python')
parser.add_argument('-o', '--output-image',
                    help='Path to the output image file')
parser.add_argument('-w', '--image-width', help='Output image file width')
parser.add_argument('-a', '--anti-aliasing', help='Anti-aliasing samples')
args = parser.parse_args()

output_image = "output_image.png"
image_width = 400
anti_aliasing = 10

if args.output_image:
    output_image = args.output_image
if args.image_width:
    image_width = int(args.image_width)
if args.anti_aliasing:
    anti_aliasing = int(args.anti_aliasing)

exit(main(output_image, image_width, anti_aliasing))
