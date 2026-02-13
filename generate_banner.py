from wand.image import Image
from pathlib import Path
import argparse
import random
import math

parser = argparse.ArgumentParser()
parser.add_argument("folder_path", type=Path, default="daiohframes")
export = parser.parse_args()

azudaioh = ""
if export.folder_path.exists():
  azudaioh = export.folder_path
else:
  raise Exception("Folder does not exist!")

files = []

for frame in azudaioh.glob('*/*.png'):
  if frame.suffix == ".png":
    files.append(frame)

maxfiles = 5000
if len(files) > maxfiles:
  files = random.sample(
    files,
    k=math.ceil(len(files) / (len(files) / maxfiles))
  )
# If we have more than the max amount of files, randomly pick out maxfiles files from the list.
# If our maxfiles is 5000, we'll pick out 5000 files to use.
random.shuffle(files)

with Image() as banner:
  for frame in files:
    with Image(filename=frame) as img:
      img.transform(resize="10%")
      banner.image_add(img)
    print(f"Added {frame}")
  banner.montage(
    thumbnail="+0+0"
  )
  banner.save(filename="generated_banner.png")
print("Successfully saved banner as generated_banner.png")