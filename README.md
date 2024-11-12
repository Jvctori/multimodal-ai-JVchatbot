# AI Chatbot - Image Generation, Translation, Code Generation, and Text Summarization

This project is a chatbot that leverages multiple AI models to perform the following tasks:

- Generate images from text prompts
- Translate text
- Generate code
- Summarize text

## How to Use

### 1. **Set Up a Virtual Environment**

It is recommended to use a virtual environment to manage dependencies. To create and activate one, follow these steps:

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate


2. Environment Setup
Create a .env file with the necessary API keys and other variables:


FLASK_APP = app.py
FLASK_ENV = development
HUGGINGFACE_API_KEY = <your_api_key>
FLASK_SECRET_KEY = <your_flask_secret_key>

3. Install Dependencies
Once the virtual environment is activated, install the required libraries:
pip install -r requirements.txt

4. Run the Flask Server
Start the Flask server:
flask run

5. Chatbot Commands
Send the following commands to the chatbot:

Image Generation: $imagem <prompt>
Code Generation: $codigo <description>
Text Summarization: $resumo <text>
Translation: $traduzir.<language> <text>
Example:

$imagem A cat sitting on a chair
$codigo Write a function that reverses a string
$resumo This is a long text that needs to be summarized
$traduzir Hello, how are you?
$traduzir.ru Oi, como você esta? (to translate to russian)

Useful Links:
Create an account on Hugging Face
https://huggingface.co/
Hugging Face API Documentation
https://huggingface.co/docs
