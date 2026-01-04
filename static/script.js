// Get elements
const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("send");

// Create WebSocket connection to /ws
const socket = new WebSocket(
  (location.protocol === "https:" ? "wss://" : "ws://") +
  location.host +
  "/ws"
);

// When connection opens
socket.onopen = () => {
  console.log("✅ Connected to WebSocket server");
};

// When message received
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message");
  msgDiv.innerHTML = `<b>${data.user}:</b> ${data.message}`;
  chatBox.appendChild(msgDiv);

  chatBox.scrollTop = chatBox.scrollHeight;
};

// On error
socket.onerror = (error) => {
  console.error("❌ WebSocket error:", error);
};

// Send message
sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

function sendMessage() {
  const message = messageInput.value.trim();
  if (message === "") return;

  socket.send(JSON.stringify({
    user: "User",
    message: message
  }));

  messageInput.value = "";
}
