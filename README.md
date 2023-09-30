Certainly, here's the content for your README:

```
# YouTube Video Transcription and Summarization

This application is designed to transcribe and summarize YouTube videos using the [pytube](https://pytube.io/) library for downloading, [Hugging Face Transformers](https://huggingface.co/transformers/) for text summarization, and [NLTK](https://www.nltk.org/) for sentence tokenization. The application allows users to provide a YouTube video URL, transcribe the audio content, and generate a summary of the transcript.

## Prerequisites

Before running the application, ensure you have the required Python libraries installed:

```bash
pip install Flask pytube transformers nltk
```

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Set up your environment:

   - Open the `app.py` file and replace the placeholder API keys for `bee_key` and `openai_key` with your actual keys.

3. Run the application:

   ```bash
   python app.py
   ```

4. Access the application:

   Open a web browser and navigate to `http://127.0.0.1:5000/`. You'll see a form where you can enter the URL of the YouTube video you want to transcribe and summarize.

5. Transcribe and Summarize:

   Enter the YouTube video URL and click the "Submit" button. The application will transcribe the audio content, summarize it, and display both the original transcription and the summary.

## Notes

- The application splits the audio into chunks, transcribes each chunk, and then summarizes the complete transcript.
- Summarization can be adjusted by modifying parameters in the `summarizer_pipe` initialization.
- Make sure to review the YouTube terms of use and API usage guidelines before using the application extensively.

Feel free to customize the application further based on your needs.

## Disclaimer

This application is provided for educational purposes and may require additional fine-tuning and error handling for production use. Be mindful of API usage limits and ensure compliance with API terms and conditions.
