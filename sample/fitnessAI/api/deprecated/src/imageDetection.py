from transformers import pipeline

checkpoint = 'google/owlv2-base-patch16-ensemble'
detector = pipeline(model=checkpoint, task="zero-shot-object-detection")

# import numpy as np
import os
from os.path import join, dirname
from PIL import Image

image_path = join(dirname(__file__), '..', 'content', 'parsed_outputs', '2024_04_11_GYM_ADAM', '2024_04_11_GYM_ADAM_frame00-06.png')
image = Image.open(image_path)


# Try using the model to detect -- 