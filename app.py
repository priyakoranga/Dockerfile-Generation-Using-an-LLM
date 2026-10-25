
import os
import re

import requests
from flask import Flask, jsonify, render_template, request
app = Flask(
    __name__,
    template_folder="./Frontend/template",
    static_folder="./Frontend/static",
    static_url_path="/static"
)


API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
You are an experienced Docker and DevOps engineer.

Generate a secure, practical Dockerfile based on the user's requirements.

Rules:
- Return only the Dockerfile, without Markdown fences or explanations.
- Use a suitable official base image.
- Prefer pinned versions when the version is known.
- Use a non-root user where practical.
- Avoid embedding credentials or secrets.
- Use appropriate working directories and dependency caching.
- Do not invent application files or dependencies.
- If important details are missing, use sensible, clearly documented defaults.
- Do not include commands that download or execute untrusted scripts.
- Do not use privileged mode or expose unnecessary ports.
- Include an appropriate CMD or ENTRYPOINT when possible.
"""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if not API_KEY:
        return jsonify({
            "error": "GROQ_API_KEY is not configured on the server."
        }), 500

    data = request.get_json(silent=True) or {}
    description = str(data.get("description", "")).strip()
    language = str(data.get("language", "")).strip()
    port = str(data.get("port", "")).strip()

    if not description:
        return jsonify({"error": "Please describe your application."}), 400

    if len(description) > 4000:
        return jsonify({"error": "Description must be under 4000 characters."}), 400

    if language not in {"Python", "Node.js", "Java", "Go", "PHP", "Other"}:
        return jsonify({"error": "Please select a valid technology."}), 400

    if port and not re.fullmatch(r"\d{1,5}", port):
        return jsonify({"error": "Port must be a number between 1 and 65535."}), 400

    if port and not 1 <= int(port) <= 65535:
        return jsonify({"error": "Port must be between 1 and 65535."}), 400

    user_prompt = (
        f"Application technology: {language}\n"
        f"Application description: {description}\n"
        f"Application port: {port or 'Not specified'}\n\n"
        "Generate a Dockerfile for this application."
    )

    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "temperature": 0.2,
                "max_tokens": 1800,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
            },
            timeout=60,
        )

        response.raise_for_status()
        result = response.json()
        dockerfile = result["choices"][0]["message"]["content"].strip()

        # Remove Markdown fences if the model adds them.
        dockerfile = re.sub(
            r"^```(?:dockerfile|Dockerfile)?\s*",
            "",
            dockerfile,
            flags=re.IGNORECASE,
        )
        dockerfile = re.sub(r"\s*```$", "", dockerfile).strip()

        if not dockerfile:
            return jsonify({"error": "The model returned an empty Dockerfile."}), 502

        return jsonify({"dockerfile": dockerfile})

    except requests.Timeout:
        return jsonify({"error": "The LLM request timed out. Please try again."}), 504

    except requests.RequestException:
        app.logger.exception("LLM API request failed")
        return jsonify({
            "error": "The LLM service request failed. Check the API key, quota, and model."
        }), 502

    except (KeyError, IndexError, TypeError, ValueError):
        app.logger.exception("Unexpected LLM response")
        return jsonify({"error": "The LLM returned an unexpected response."}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
