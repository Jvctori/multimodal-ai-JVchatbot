# 🤖 AI Multifunction Chatbot

A powerful chatbot that leverages state-of-the-art AI models to perform multiple tasks through a simple command interface.

## ✨ Features

- 🎨 **Image Generation**: Create images from text descriptions
- 🌐 **Text Translation**: Support for multiple languages
- 💻 **Code Generation**: Generate code snippets in various programming languages
- 📝 **Text Summarization**: Create concise summaries of long texts

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- pip package manager
- A Hugging Face account with API access

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Jvctori/multimodal-ai-JVchatbot.git
cd multimodal-ai-JVchatbot
```

2. **Set up a virtual environment**

Windows:
```bash
python -m venv . 
venv\Scripts\activate
```

Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:
```env
FLASK_APP=app.py
FLASK_ENV=development
HUGGINGFACE_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_flask_secret_key_here
```

## 💫 Usage

### Starting the Server

```bash
flask run
```
The server will start at `http://localhost:5000` by default.

### Available Commands

| Command | Syntax | Description | Example |
|---------|--------|-------------|----------|
| Image Generation | `$imagem <prompt>` | Generates an image based on text description | `$imagem A sunset over mountains` |
| Code Generation | `$codigo <description>` | Generates code based on description | `$codigo Function to calculate Fibonacci sequence` |
| Text Summarization | `$resumo <text>` | Creates a summary of provided text | `$resumo [Your long text here]` |
| Translation | `$traduzir.<lang> <text>` | Translates text to specified language | `$traduzir.pt Hello world` |

### Available Languages for Translation

| Language Code | Language Name |
|--------------|---------------|
| pt | Portuguese |
| en | English |
| es | Spanish |
| fr | French |
| de | German |
| it | Italian |
| ru | Russian |
| ja | Japanese |
| zh-CN | Chinese (Simplified) |

Example: `$traduzir.es Hello, how are you?` (translates to Spanish)

## 🔑 API Keys

1. Create a Hugging Face account at [huggingface.co](https://huggingface.co/)
2. Generate an API key in your account settings
3. Add the key to your `.env` file

## 📚 Documentation

For more detailed information, visit:
- [Hugging Face Documentation](https://huggingface.co/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
