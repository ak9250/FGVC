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


def run_cmd(command):
    try:
        print(command)
        call(command, shell=True)
    except KeyboardInterrupt:
        print("Process interrupted")
        sys.exit(1)
    

@runway.command('imitate', inputs={'source': runway.image, 'target': runway.image}, outputs={'image': runway.image})
def imitate(models, inputs):
  os.makedirs('images', exist_ok=True)
  inputs['source'].save('images/temp1.jpg')
  inputs['target'].save('images/temp2.jpg')

  paths1 = os.path.join('images','temp1.jpg')
  paths2 = os.path.join('images','temp2.jpg')

  
  os.chdir("./tool/")
  src_path = "/model/images/temp1.jpg"

  ref_path = "/model/images/temp2.jpg"
  stage_1_command = ("python video_completion.py"
            + " --mode object_removal"
            + " --path src_path"
            + " --path_mask ref_path"
            + " --outroot /model/result/temp_removal"
            + " --seamless"
  )      
  run_cmd(stage_1_command)
  path = "/model/result/temp_removal/frame_seamless_comp_final/00000.png"
  img = Image.open(open(path, 'rb'))
  return img

if __name__ == '__main__':
    runway.run()