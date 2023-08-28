from flask import Flask, request, render_template
from pytube import YouTube
from transformers import pipeline
import os
import subprocess
import nltk
import re

nltk.download('punkt')

app = Flask(__name__)

# Initializing models outside the route
stt_pipe = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-large-960h-lv60-self")
summarizer_pipe = pipeline("summarization", model="facebook/bart-large-cnn")

def split_audio(file_name, chunk_length=30):
    command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_name]
    total_duration = float(subprocess.check_output(command).decode('utf-8').strip())
    
    chunks = []
    for i in range(0, int(total_duration), chunk_length):
        output_file = f"chunk_{i}.wav"
        command = ['ffmpeg', '-ss', str(i), '-t', str(chunk_length), '-i', file_name, '-q:a', '0', '-map', 'a', output_file]
        subprocess.call(command)
        chunks.append(output_file)
    
    return chunks

def sentence_case(text):
    return '. '.join(i.capitalize() for i in text.split('. '))

def split_and_summarize(text, tokenizer_kwargs):
    sentences = nltk.sent_tokenize(text)
    sections = [' '.join(sentences[i:i+10]) for i in range(0, len(sentences), 10)]
    summarized_sections = [summarizer_pipe(section, min_length=200, do_sample=False, **tokenizer_kwargs)[0]["summary_text"] for section in sections]
    return ' '.join(summarized_sections)

@app.route('/', methods=['GET', 'POST'])
def index():
    original_text = None
    summary = None

    if request.method == 'POST':
        video_url = request.form['video_url']

        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
        audio_stream.download()

        downloaded_file_name = audio_stream.default_filename
        new_file_name = "video.wav"  
        if os.path.exists(new_file_name):
            os.remove(new_file_name)
        os.rename(downloaded_file_name, new_file_name)

        # Convert audio to text in chunks
        chunks = split_audio(new_file_name)
        texts = []
        for chunk in chunks:
            text_chunk = stt_pipe(chunk, chunk_length_s=10)
            texts.append(text_chunk["text"])
            os.remove(chunk)

        original_text = sentence_case(" ".join(texts))

        # Summarize the text in sections
        tokenizer_kwargs = {'truncation': True, 'max_length': 512}
        summary = sentence_case(split_and_summarize(original_text, tokenizer_kwargs))



    return render_template('upload.html', original_text=original_text, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
