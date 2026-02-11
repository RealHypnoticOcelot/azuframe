# Jarvis
###### Jarvis, become a Discord bot

## How to use:

### (Optional: create a virtual environment)
Navigate to the directory the script was downloaded in, and run the following command:
```python
python3 -m venv env && source env/bin/activate
```
### (Required Steps)
Install the dependencies required with the following command:

```python
pip3 install -r requirements.txt
```

Extract the frames from your Azumanga Daioh videos.
```python
python3 frameextract.py
```
This command isn't well-tested, and probably won't work out of the box! It's a throwaway script I made ages ago.


### (Optional: Create a banner for the bot)
Create a banner for your Azumanga Daioh bot.
First, install imagemagick at [imagemagick.org](https://imagemagick.org/script/download.php).
If you're on MacOS and have brew installed, you can just run `brew install imagemagick`.
Navigate to one of the directories where the frames outputted to(you have to navigate to a specific episode), and run this command!
```
montage $(shuf -e *.png) -geometry +0+0 tiles.png && convert tiles.png -resize 10% resized_tiles.png
```

Then, run the program! You might have to tweak some paths if they're not what's expected.
```python
python3 main.py
```

###### If you have any issues, questions, concerns or suggestions, create an issue or pull request
