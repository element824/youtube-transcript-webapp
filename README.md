# YouTube Transcript Web App

A simple Flask web application that allows you to enter a YouTube URL, fetch the transcript (subtitles) for the video, and display it in your browser.

## Features
- Enter any YouTube video URL
- Fetches transcript using the latest [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- Displays transcript in a readable text area
- Handles errors (invalid URL, no transcript, unavailable video)

## How It Works
- The frontend (`index.html`) provides a user-friendly interface to input a YouTube URL and view the transcript.
- The backend (`app.py`) is a Flask server with an endpoint `/transcript` that extracts the video ID and fetches the transcript using `youtube-transcript-api`.

## Setup & Usage

1. **Clone the repository:**
   ```sh
   git clone https://github.com/element824/youtube-transcript-webapp.git
   cd youtube-transcript-webapp
   ```
2. **Install dependencies:**
   ```sh
   uv sync
   ```
3. **Run the app:**
   ```sh
   python app.py
   ```
4. **Open your browser:**
   Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) and use the app.

## Notes
- Some YouTube videos may not have transcripts available.
- Age-restricted or private videos may not work due to YouTube limitations.
- For production, use a proper WSGI server and secure deployment practices.

## License
MIT

Made by [Koushik Nagarajan](https://github.com/element824)

This repo was totally created by vibe coding by me.
