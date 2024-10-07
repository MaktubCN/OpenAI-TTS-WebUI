# OpenAI-TTS-WebUI
This is a simple OpenAI TTS Web built by MaktubCN, you are welcome to use it 👏!

A web-based Text-to-Speech (TTS) application that allows users to convert text into audio using various voices and output formats.

## Features

- Text-to-Speech conversion with multiple voice options
- Supports various audio formats (mp3, opus, aac, flac, pcm)
- Web-based interface built with Gradio
- Can be deployed via Python or Docker

## Installation

### Option 1: Using Python

#### Requirements

- Python 3.8 or higher
- pip (Python package installer)

#### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/tts-web.git
    cd tts-web
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python app.py
    ```

4. Access the web application:

    Open your browser and navigate to `http://localhost:7860`.

### Option 2: Using Docker

#### Prerequisites

- Docker installed on your system

#### Steps

1. Pull the Docker image:

    ```bash
    docker pull maktubcn/tts-web:1.2
    ```

2. Run the Docker container:

    ```bash
    docker run -d -p 7860:7860 --name tts-web maktubcn/tts-web:1.2
    ```

3. Access the web application:

    Open your browser and navigate to `http://localhost:7860`.

## Configuration

If you need to modify the base URL or API key, you can either set them via the interface or by editing the relevant variables in the `app.py` file.

### Customizing the Theme

If you'd like to use a custom theme, modify the `app.py` to point to the custom CSS file or JSON configuration for the theme. You can reference your downloaded themes by using the `css` parameter in the `gr.Blocks()` method.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
