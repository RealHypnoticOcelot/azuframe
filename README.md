# Azuframes
###### Discord bot that outputs a random Azumanga Daioh frame

## How to use:

### (Optional: create a virtual environment)
Navigate to the directory the script was downloaded in, and run the following command:
```python
python3 -m venv env && source env/bin/activate
```
### (Install Dependencies)
Install the dependencies required with the following command:

```python
pip3 install -r requirements.txt
```

Install ffmpeg at [ffmpeg.org](https://www.ffmpeg.org/download.html), if you don't have it already.
If you're on MacOS and have `brew` installed, you can just run `brew install ffmpeg`.

If you want to generate a banner, you'll need to install imagemagick at [imagemagick.org](https://imagemagick.org/script/download.php).
If you're on MacOS and have `brew` installed, you can just run `brew install imagemagick`.

**For Nix users:**
Simply navigate to the application, run `nix develop`, and use the commands below!

### Usage

Extract the frames from your videos.
```python
python3 extract_frames.py /path/to/yourvideos
```
This script expects to be fed a folder containing all of your selected videos.
By default, it assumes all videos are in .mkv format.
Its options are tuned for Azumanga Daioh, so if you plan on doing something else, you might have to modify it.

### (Optional: Create a banner for the bot)
Create a banner for your Azumanga Daioh bot.
```python
python3 generate_banner.py /path/to/frames
```
This script expects to be fed the folder(called by default "daiohframes") containing the folders with your video frames.
It picks out 5,000 images(or less, if you didn't supply that many) and turns them into a montage.

### Running the program
Then, run the program!
```python
python3 main.py
```
You might have to tweak some paths if you change them.

###### If you have any issues, questions, concerns or suggestions, create an issue or pull request