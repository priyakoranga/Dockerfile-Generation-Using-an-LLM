# Dockerfile Generation Using an LLM 🐳

Generate Dockerfiles automatically from natural-language descriptions using a Large Language Model (LLM). This project provides a web interface where users can describe their application and receive a Dockerfile to help containerize it.

## 🚀 Features

- **AI-Powered Generation:** Uses an LLM through the Groq API to generate Dockerfiles.
- **Simple Web Interface:** Enter application requirements through an HTML-based frontend.
- **Automated Dockerfile Creation:** Generates Docker configuration based on the provided application details.
- **Frontend Integration:** Uses HTML, CSS, and JavaScript for the user interface.
- **Flask Backend:** Handles user requests and communicates with the LLM API.
- **Containerization Ready:** Includes a Dockerfile to package the application into a container.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Flask | Web application framework |
| Groq API | Access to the LLM |
| HTML | Web page structure |
| CSS | Frontend styling |
| JavaScript | Frontend interactions |
| Docker | Application containerization |
| Gunicorn | Production WSGI server |

## 📁 Project Structure

```text
Dockerfile-Generation-Using-an-LLM/
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
└── Frontend/
    ├── template/
    │   └── index.html
    └── static/
        ├── style.css
        └── script.js
```

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/priyakoranga/Dockerfile-Generation-Using-an-LLM.git
cd Dockerfile-Generation-Using-an-LLM
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Linux or GitHub Codespaces:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API Key

Create a Groq API key and configure it as an environment variable.

Linux / GitHub Codespaces:

```bash
export GROQ_API_KEY="your_actual_api_key"
```

Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_actual_api_key"
```

Replace the placeholder with your actual key. Never commit API keys to GitHub. For Codespaces, use **Codespaces Secrets** to manage sensitive credentials.

### 5. Run the Application

```bash
python app.py
```

Open the forwarded application port in your browser. Use the port configured in `app.py` (for example, `8000`).

## 🐳 Run with Docker

Build the Docker image from the directory containing the Dockerfile:

```bash
docker build -t dockerfile-generator .
```

Run the container:

```bash
docker run --rm -p 8080:8080 \
  -e GROQ_API_KEY="your_actual_api_key" \
  dockerfile-generator
```

Open the forwarded or mapped port `8080` in your browser.

**Note:** The Dockerfile uses Gunicorn with the entry point `app:app` and port `8080`. Ensure `requirements.txt` includes Gunicorn and that the Flask application exposes an object named `app`.

## 🔄 How It Works

1. The user enters an application description in the web interface.
2. JavaScript sends the request to the Flask backend.
3. Flask uses the Groq API to send the description to an LLM.
4. The LLM generates Dockerfile content based on the request.
5. The backend returns the generated content to the frontend.
6. The user can review and use the generated Dockerfile.

## 🔐 Security Considerations

- Store API keys in environment variables or Codespaces Secrets.
- Do not hardcode credentials in source code.
- Review generated Dockerfiles before building or deploying them.
- Avoid running generated commands or containers without checking their security implications.

## 🎯 Project Goal

The goal is to simplify Dockerfile creation, reduce repetitive configuration work, and help developers get started with containerizing applications more efficiently using LLMs.

## 👩‍💻 Author

Developed as a project exploring **Large Language Models, web development, and Docker containerization**.

