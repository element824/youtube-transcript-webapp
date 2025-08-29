from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import re
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
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
        text = summarize_text(text)
        return jsonify({'transcript': text})
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return jsonify({'error': 'Transcript not available for this video.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

 
def summarize_text(transcript):
    """
    Summarize text using OpenAI's GPT model.
    
    Args:
        text (str): Text to summarize
        
    Returns:
        Optional[str]: Summary if successful, None otherwise
    """
    try:
        prompt = """
        Please provide a comprehensive summary of the following video transcript. 
        Focus on:
        1. Main topics and key points discussed
        2. Important insights or conclusions
        3. Any actionable advice or recommendations
        4. Key statistics, facts, or data mentioned
        
        Format the summary with clear headings and bullet points for easy reading.
        
        Transcript:
        """
        
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_name = "gpt-4o-mini"
        deployment = "gpt-4o-mini"
        subscription_key = os.getenv("AZURE_OPENAI_KEY")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION")

        client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=subscription_key,
        )
        response = client.chat.completions.create(
            model= "gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates clear, structured summaries of video content."},
                {"role": "user", "content": f"{prompt}\n\n{transcript}"}
            ],
            max_tokens=1000,
            temperature=0.3 
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return None
    

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    # Serve index.html from the root directory
    app.static_folder = os.path.dirname(os.path.abspath(__file__))
    app.run(debug=True)
