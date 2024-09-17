#!/usr/bin/env python3

import argparse

from ray_tracer2.main import main

print("Ray Tracer in Python!")
parser = argparse.ArgumentParser(description='Ray Tracer in Python')
parser.add_argument('-o', '--output-image', help='Path to the output image file')
args = parser.parse_args()

if args.output_image:
    exit(main(args.output_image))
else:
    exit(main("output_image.png"))