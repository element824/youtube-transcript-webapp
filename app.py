from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import re

import os
app = Flask(__name__)

def extract_video_id(url):
    # Extracts video ID from various YouTube URL formats
    match = re.search(r'(?:v=|youtu\.be/|embed/|shorts/)([\w-]{11})', url)
    return match.group(1) if match else None

@app.route('/transcript', methods=['POST'])
def get_transcript():
    data = request.get_json()
    url = data.get('url', '')
    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id)
        text = '\n'.join([snippet.text for snippet in transcript])
        return jsonify({'transcript': text})
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return jsonify({'error': 'Transcript not available for this video.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    # Serve index.html from the root directory
    app.static_folder = os.path.dirname(os.path.abspath(__file__))
    app.run(debug=True)
