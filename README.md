### Setup

1. Set up virtual environment

```bash
$ python3.12 -m venv .venv
```

2. Install requirements

```bash
(.venv) $ python3.12 -m pip install -r requirements.txt
```

### Usage

Ray trace default world (defined in ray\_tracer2/main.py) with default settings:
```bash
(.venv) $ python3.12 ray-tracer2.py
```

```bash
(.venv) $ python3.12 ray-tracer2.py --help
Ray Tracer in Python!
usage: ray-tracer2.py [-h] [-o OUTPUT_IMAGE] [-w IMAGE_WIDTH] [-a ANTI_ALIASING]

Ray Tracer in Python

options:
  -h, --help            show this help message and exit
  -o OUTPUT_IMAGE, --output-image OUTPUT_IMAGE
                        Path to the output image file
  -w IMAGE_WIDTH, --image-width IMAGE_WIDTH
                        Output image file width
  -a ANTI_ALIASING, --anti-aliasing ANTI_ALIASING
                        Anti-aliasing samples
```

### Performance

Currently this application is single-threaded and a single process. My laptop CPU is an 11th Gen Intel i5-1145G7 @ 2.60GHz.

```bash
(.venv) $ python3.12 ray-tracer2.py -w 400 -a 100
100%|███████████████████████████████████████████████████| 9000000/9000000 [18:09<00:00, 8259.10it/s]
```
![](output_image.png)
