Podcast Processor

Podcast Processor is a Flask-based web application that allows users to input a podcast transcript, which is then summarized and converted into a video with text-to-speech audio. The current version supports direct text input for transcripts. Future improvements aim to enhance the functionality with better voices, image generation, transcription from URLs, and more.

Features

Transcript Summarization: Analyzes and summarizes podcast transcripts.
Text-to-Speech: Converts summarized text into speech.
Video Creation: Generates a video with the speech audio and a placeholder image.
Web Interface: Simple web interface for pasting podcast transcripts.
Future Improvements

Image Generation: Integrate image generation for visual enhancement.
Better Voices: Utilize more natural and expressive voices.
Transcription: Add support for transcribing audio from URLs directly.
URL Support: Allow users to input podcast URLs instead of pasting transcripts.
Requirements

Python 3.7+
Flask
requests
anthropic
Pillow
openai
moviepy
gtts
Installation

Clone the repository:

sh
Copy code
git clone https://github.com/yourusername/podcast-processor.git
cd podcast-processor
Create and activate a virtual environment:

sh
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install the dependencies:

sh
Copy code
pip install -r requirements.txt
Create the static directory:

sh
Copy code
mkdir static
Set your API keys in app.py:

Replace your_anthropic_api_key and your_openai_api_key with your actual API keys.
Usage

Run the Flask app:

sh
Copy code
export FLASK_APP=app.py  # On Windows: set FLASK_APP=app.py
flask run
Open your web browser and navigate to http://localhost:5000/.

Paste your podcast transcript into the textarea and click the "Process Podcast" button.

Access the generated video via the provided URL.

Contributing

Feel free to fork the repository and submit pull requests. Contributions are welcome!

To Do
Implement image generation for better visuals.
Enhance text-to-speech with more natural voices.
Add support for transcribing audio from URLs.
Improve error handling and user experience.
License

This project is licensed under the MIT License.
