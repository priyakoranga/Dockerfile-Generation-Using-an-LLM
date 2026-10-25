
const form = document.getElementById("generatorForm");
const description = document.getElementById("description");
const language = document.getElementById("language");
const port = document.getElementById("port");

const generateBtn = document.getElementById("generateBtn");
const buttonText = document.getElementById("buttonText");
const status = document.getElementById("status");
const output = document.getElementById("output");

const copyBtn = document.getElementById("copyBtn");
const downloadBtn = document.getElementById("downloadBtn");

let generatedDockerfile = "";

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const appDescription = description.value.trim();

  if (!appDescription) {
    showStatus("Please describe your application.", true);
    return;
  }

  if (port.value &&
      (!Number.isInteger(Number(port.value)) ||
       Number(port.value) < 1 ||
       Number(port.value) > 65535)) {
    showStatus("Enter a valid port from 1 to 65535.", true);
    return;
  }

  generateBtn.disabled = true;
  buttonText.textContent = "Generating...";
  showStatus("Asking the LLM to generate your Dockerfile...");
  generatedDockerfile = "";
  output.textContent = "# Generating Dockerfile...";
  copyBtn.disabled = true;
  downloadBtn.disabled = true;

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        description: appDescription,
        language: language.value,
        port: port.value
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Generation failed.");
    }

    generatedDockerfile = data.dockerfile;
    output.textContent = generatedDockerfile;

    copyBtn.disabled = false;
    downloadBtn.disabled = false;

    showStatus("Dockerfile generated successfully. Review it before use.");
  } catch (error) {
    output.textContent = "# Generation failed.\n# Check the error message and try again.";
    showStatus(error.message || "Something went wrong.", true);
  } finally {
    generateBtn.disabled = false;
    buttonText.textContent = "✦ Generate Dockerfile";
  }
});

copyBtn.addEventListener("click", async () => {
  if (!generatedDockerfile) return;

  try {
    await navigator.clipboard.writeText(generatedDockerfile);
    showStatus("Dockerfile copied to clipboard.");
  } catch {
    showStatus("Copy failed. Select and copy the output manually.", true);
  }
});

downloadBtn.addEventListener("click", () => {
  if (!generatedDockerfile) return;

  const file = new Blob([generatedDockerfile], {
    type: "text/plain;charset=utf-8"
  });

  const url = URL.createObjectURL(file);
  const link = document.createElement("a");

  link.href = url;
  link.download = "Dockerfile";
  document.body.appendChild(link);
  link.click();
  link.remove();

  URL.revokeObjectURL(url);
  showStatus("Dockerfile download started.");
});

function showStatus(message, isError = false) {
  status.textContent = message;
  status.classList.toggle("error", isError);
}
