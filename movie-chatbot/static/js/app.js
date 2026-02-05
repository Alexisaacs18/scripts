const chatWindow = document.getElementById("chat-window");
const promptInput = document.getElementById("prompt-input");
const sendBtn = document.getElementById("send-btn");
const pageCountSelect = document.getElementById("page-count");
const scriptsInfo = document.getElementById("scripts-info");

document.addEventListener("DOMContentLoaded", loadScriptsInfo);

promptInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendPrompt();
    }
});

function addMessage(text, role) {
    const div = document.createElement("div");
    div.className = `message ${role}`;
    div.textContent = text;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return div;
}

async function sendPrompt() {
    const prompt = promptInput.value.trim();
    if (!prompt) return;

    const pageCount = parseInt(pageCountSelect.value);

    addMessage(prompt, "user");
    promptInput.value = "";

    sendBtn.disabled = true;
    sendBtn.textContent = "Generating...";

    const loadingMsg = addMessage("Writing your script...", "system");
    loadingMsg.classList.add("loading");

    try {
        const response = await fetch("/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt, page_count: pageCount }),
        });

        chatWindow.removeChild(loadingMsg);

        if (!response.ok) {
            const err = await response.json();
            addMessage(`Error: ${err.error || "Something went wrong."}`, "error");
            return;
        }

        const data = await response.json();
        addMessage(data.script, "assistant");
    } catch (err) {
        chatWindow.removeChild(loadingMsg);
        addMessage(`Error: ${err.message}`, "error");
    } finally {
        sendBtn.disabled = false;
        sendBtn.textContent = "Generate";
    }
}

async function loadScriptsInfo() {
    try {
        const response = await fetch("/api/scripts");
        const data = await response.json();
        if (data.scripts.length > 0) {
            scriptsInfo.textContent = `Reference scripts loaded: ${data.scripts.join(", ")}`;
        } else {
            scriptsInfo.textContent = "No reference scripts loaded. Add .txt or .fountain files to the scripts/ folder.";
        }
    } catch {
        scriptsInfo.textContent = "";
    }
}
