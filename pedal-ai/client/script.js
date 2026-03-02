let sessionId = null;

async function sendMessage() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  const userMessage = input.value;

  chat.innerHTML += `<p><strong>Anda:</strong> ${userMessage}</p>`;

  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "session-id": sessionId || ""
    },
    body: JSON.stringify({ message: userMessage })
  });

  const data = await response.json();
  sessionId = data.sessionId;

  chat.innerHTML += `<p><strong>AI:</strong> ${data.reply}</p>`;

  input.value = "";
  chat.scrollTop = chat.scrollHeight;
}