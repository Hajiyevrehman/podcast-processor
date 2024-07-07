from flask import Flask, request, jsonify, send_from_directory, render_template_string
import requests
from anthropic import Anthropic
from PIL import Image
import openai
import os
from moviepy.editor import ImageClip, AudioFileClip
from gtts import gTTS
app = Flask(__name__)


# Set your API keys here
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def summarize_transcript(transcript):
    anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
    response = anthropic.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": f"""Analyze the following podcast transcript and create a structured summary. The summary should be in this format:


[Parties, [[Party1: 'brief description of who this person is'], [Party2: 'brief description of who this person is'], ...]],
[Topic 1, 'summary of what was discussed and each party's stance on this topic'],
[Topic 2, 'summary of what was discussed and each party's stance on this topic'],
...
]

For the 'Parties' section:
- Identify all participants in the podcast.
- Provide a brief, one-sentence description of who each person is.

For each subsequent topic:
- Identify the main topics discussed in the podcast.
- For each topic, summarize the key points of discussion.
- Include the stance or opinion of each party on the topic, if applicable.

Ensure that:
1. The topics are listed in the order they appear in the podcast.
2. Each topic summary is concise but comprehensive, capturing the essence of the discussion.
3. The stances of each party are clearly differentiated within the topic summaries.
4. If a topic has subtopics, include them under the main topic.
The goal is to cover most of podcast in summarized manner.
Here's the podcast transcript:

:\n\n{transcript}"""}
        ]
    )
    return response.content[0].text

# def generate_image(summary):
#     openai.api_key = OPENAI_API_KEY
#     response = openai.Image.create(
#         prompt=f"An image representing: {summary}",
#         n=1,
#         size="1024x1024"
#     )
#     image_url = response['data'][0]['url']
#     img_data = requests.get(image_url).content
#     img_path = "generated_image.png"
#     with open(img_path, 'wb') as handler:
#         handler.write(img_data)
#     return img_path

def text_to_speech(text):
    audio_path = os.path.join('static', 'audio.mp3')
    tts = gTTS(text)
    tts.save(audio_path)
    # Debugging statement to verify audio file creation
    if os.path.exists(audio_path):
        print(f"Audio file created successfully at {audio_path}")
    else:
        print("Failed to create audio file")
    return audio_path

def create_video(summary, audio_path):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # Create a blank image as a placeholder
    image_path = os.path.join('static', 'blank.png')
    if not os.path.exists(image_path):
        from PIL import Image
        img = Image.new('RGB', (1024, 1024), color = (73, 109, 137))
        img.save(image_path)

    audio = AudioFileClip(audio_path)
    print(f"Audio duration: {audio.duration} seconds")  # Debugging statement for audio duration
    image_clip = ImageClip(image_path).set_duration(audio.duration)
    video = image_clip.set_audio(audio)
    video_path = os.path.join('static', 'output.mp4')  # Save video in static directory
    video.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac')

    # Debugging statement to verify video file creation
    if os.path.exists(video_path):
        print(f"Video file created successfully at {video_path}")
    else:
        print("Failed to create video file")

    audio.close()
    image_clip.close()
    video.close()

    return video_path

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Podcast Processor</title>
        </head>
        <body>
            <h1>Podcast Processor</h1>
            <form id="podcast-form">
                <textarea id="transcript" rows="10" cols="50" placeholder="Paste your podcast transcript here"></textarea><br>
                <button type="button" onclick="processPodcast()">Process Podcast</button>
            </form>
            <div id="result"></div>
            <script>
                function processPodcast() {
                    const transcript = document.getElementById('transcript').value;
                    console.log('Transcript:', transcript);
                    fetch('/process_podcast', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ transcript: transcript }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Response:', data);
                        const resultDiv = document.getElementById('result');
                        if (data.videoUrl) {
                            resultDiv.innerHTML = `<p>Video URL: <a href="${data.videoUrl}" target="_blank">${data.videoUrl}</a></p>`;
                        } else {
                            resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
                        }
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                }
            </script>
        </body>
        </html>
    ''')

@app.route('/process_podcast', methods=['POST'])
def process_podcast():
    try:
        data = request.get_json()
        transcript = data['transcript']
        summary = summarize_transcript(transcript)
        # image_path = generate_image(summary)  # Commented out image generation
        audio_path = text_to_speech(summary)
        video_path = create_video(summary, audio_path)  # Updated to only use audio_path

        response = {
            "videoUrl": f"/static/output.mp4"
        }
        return jsonify(response)
    except Exception as e:
        print(f"Error processing podcast: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
