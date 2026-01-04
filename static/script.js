// Connect to WebSocket server (auto-detects Render domain)
const socket = new WebSocket(
  (window.location.protocol === "https:" ? "wss://" : "ws://") +
  window.location.host
);

const chat = document.getElementById("chat");
const input = document.getElementById("msg");

// When message received
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  const p = document.createElement("p");
  p.textContent = data.message;
  chat.appendChild(p);

  // auto-scroll
  chat.scrollTop = chat.scrollHeight;
};

// Send message
function sendMsg() {
  if (input.value.trim() === "") return;

  socket.send(
    JSON.stringify({
      message: input.value
    })
  );

  input.value = "";
}

// Optional: send on Enter key
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMsg();
  }
});

// Connection status logs
socket.onopen = () => {
  console.log("✅ WebSocket connected");
};

socket.onclose = () => {
  console.log("❌ WebSocket disconnected");
};

socket.onerror = (err) => {
  console.error("WebSocket error:", err);
};
