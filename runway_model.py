import runway
import numpy as np
import shutil
import os
import os.path as osp
import platform
import argparse
import time
import sys
import subprocess
from subprocess import call
from PIL import Image
import shutil

os.chdir("./tool/")


def run_cmd(command):
    try:
        print(command)
        call(command, shell=True)
    except KeyboardInterrupt:
        print("Process interrupted")
        sys.exit(1)
    

@runway.command('removal', inputs={'source': runway.image, 'target': runway.image}, outputs={'image': runway.image})
def removal(models, inputs):
  os.makedirs('./images', exist_ok=True)
  os.makedirs('./mask', exist_ok=True)

  inputs['source'].save('./images/00000.png')
  inputs['target'].save('./mask/00000.png')
  
  


  stage_1_command = ("python video_completion.py"
            + " --mode object_removal"
            + " --path ../images"
            + " --path_mask ../mask"
            + " --outroot ../result/temp_removal"
  )          
  run_cmd(stage_1_command)
  path = "../result/temp_removal/frame_comp_final/00000.png"
  img = Image.open(open(path, 'rb'))
  return img

@runway.command('extrapolation', inputs={'source': runway.image,}, outputs={'image': runway.image})
def extrapolation(models, inputs):
  os.makedirs('./images', exist_ok=True)

  inputs['source'].save('./images/00000.png')

  stage_1_command = ("python video_completion.py"
            + " --mode video_extrapolation"
            + " --path ../images"
            + " --outroot ../result/temp_extrapolation"
            + " --H_scale 2"
            + " --W_scale 2"
  )          
  run_cmd(stage_1_command)
  path = "../result/temp_extrapolation/frame_comp_final/00000.png"
  img = Image.open(open(path, 'rb'))
  return img


if __name__ == '__main__':
    runway.run()