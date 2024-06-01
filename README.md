<center>
<img alt="Logo of the project" src="https://raw.githubusercontent.com/jehna/webcam-song/master/logo.png" width="200">
</center>

# Webcam Song
> Use your mood to control the music

This project uses your webcam to take an image, then asks AI what the perfect
song for your mood is. It then plays that song from Spotify.

## Getting started

First you need to install the required dependencies:
```shell
# Create a virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then you need to set up the environment variables:
```shell
cp .env-example .env
```

To use this app you need to set up a Spotify app and an OpenAI API key and save
the required values to `.env`file.

Then you can run the project:
```shell
python -m webcam_song
```

The first time you run the project, you need to authenticate with Spotify.

## Contributing

This was intended to be a super simple solo project. If you'd like to extend on
the work, pull requests are warmly welcome! Please fork the repository and use a
feature branch.

## Licensing

The code in this project is licensed under MIT license.
