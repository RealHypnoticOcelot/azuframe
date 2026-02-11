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
  raise Exception("File does not exist!")

files = []

for i in azudaioh.iterdir():
    if str(i).endswith(".mkv"):
        files.append(i)

output_dir = Path.cwd() / "daiohframes"
# Path to where thse frames will output to
# By default, a folder called "daiohframes" in the folder where the program was executed.

for input_file in files:
    outputpath = output_dir / input_file.stem
    outputpath.mkdir(parents=True, exist_ok=True)

    ffmpeg_command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"subtitles=\'{input_file}\',fps=5,mpdecimate=frac=1:hi=400:lo=400,scale=320:240,trim=start_frame=433",
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
