import ffmpeg
from ffmpeg import Error
from pathlib import Path
import subprocess
import argparse

# You might have to do some tweaking if your videos have different subtitles/metadata/extension/whatever!

parser = argparse.ArgumentParser()
parser.add_argument("folder_path", type=Path)
export = parser.parse_args()

azudaioh = ""
if export.folder_path.exists():
  azudaioh = export.folder_path
else:
  raise Exception("Folder does not exist!")

files = []

for episode in azudaioh.iterdir():
  if episode.suffix == ".mkv":
      files.append(episode)
files.sort() # Puts the episodes in order (assuming your episode filenames are named in a way conducive to sorting)

output_dir = Path.cwd() / "daiohframes"
# Path to where thse frames will output to
# By default, a folder called "daiohframes" in the folder where the program was executed.

probe = ffmpeg.probe(files[0])
# Pick out the first video and get its metadata.
# For simplicity's sake, we're going to assume that all of the provided videos have the same subtitle track indices.
subtitle_streams = [
  stream for stream in probe["streams"]
  if stream["codec_type"] == "subtitle"
] # Get subtitle streams

subtitle_index = next(
  stream['index'] - (len(probe['streams']) - len(subtitle_streams)) for stream in subtitle_streams if stream['disposition']['default']
) # Set the default subtitle index to be the first subtitle stream marked as default

use_default_settings = (False if input("Use default settings? Y/n: ").lower() == "n" else True)
if not use_default_settings:
  subtitle_index = None
  while subtitle_index == None:
    subtitle_index = input("Select subtitle track number to use, or type \"list\" to view all available options: ")
    if subtitle_index == "list":
      print("\n")
      for index, stream in enumerate(subtitle_streams):
        print(f"""{"(default)" if stream['disposition']['default'] else ""} Track #{index+1}:
  language: {stream['tags']['language']}
  codec: {stream['codec_name']}
        """)
      subtitle_index = None
    else:
      try:
        subtitle_index = int(subtitle_index)
        subtitle_index = subtitle_index - 1 if subtitle_streams[subtitle_index - 1] else None
      except IndexError:
        print("Invalid track number!")
        subtitle_index = None
      except ValueError:
        print("Invalid input!")
        subtitle_index = None

for input_file in files:
  outputpath = output_dir / input_file.stem
  outputpath.mkdir(parents=True, exist_ok=True)

  ffmpeg_command = [
    "ffmpeg",
    "-i", input_file,
    "-vf", (
      f"subtitles=\'{input_file}\':si={subtitle_index},"
      f"fps=5,"
      f"mpdecimate=frac=1:hi=400:lo=400,"
      f"trim=start_frame=433," # Skip the intro for all episodes, which is around 433 frames
      f"scale=320:240"
    ),
    "-qscale:v", "4",
    "-an",
    "-fps_mode", "vfr",
    str(outputpath / "frame_%04d.png")
  ]
  # Execute the ffmpeg command
  try:
    subprocess.run(ffmpeg_command, check=True)
    print("Frames extracted successfully.")
  except subprocess.CalledProcessError as e:
    print("Error:", e)
