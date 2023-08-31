# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils ffmpeg

# Install the required packages using pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt


# Download the models during the build process
RUN python -c "from transformers import pipeline; \
               pipeline('automatic-speech-recognition', model='facebook/wav2vec2-large-960h-lv60-self'); \
               pipeline('summarization', model='facebook/bart-large-cnn')"




# Make port 5000 available to the world outside this container
EXPOSE 5000


# Run the application when the container launches
CMD ["python", "app.py"]
