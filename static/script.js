const socket = new WebSocket(
  "wss://websocket-chat-app-1-vx88.onrender.com"
);

const messagesDiv = document.getElementById("messages");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

// When connection opens
socket.onopen = () => {
  console.log("Connected to WebSocket server");
};

// When message comes from server
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  const msg = document.createElement("div");
  msg.textContent = `${data.user}: ${data.message}`;
  messagesDiv.appendChild(msg);
};

// When connection closes
socket.onclose = () => {
  console.log("Disconnected from server");
};

// Send message
sendBtn.onclick = () => {
  if (input.value.trim() !== "") {
    socket.send(
      JSON.stringify({
        message: input.value
      })
    );
    input.value = "";
  }
};
