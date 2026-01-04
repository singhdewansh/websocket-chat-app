const socket = new WebSocket("ws://localhost:8765");
const messagesDiv = document.getElementById("messages");

const username = prompt("Enter your name");

socket.onopen = () => {
  socket.send(JSON.stringify({
    type: "join",
    user: username
  }));
};

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const msg = document.createElement("div");

  if (data.type === "system") {
    msg.innerHTML = `<i>${data.text}</i>`;
  } else {
    msg.innerHTML = `<b>${data.user}:</b> ${data.text}`;
  }

  messagesDiv.appendChild(msg);
};

function sendMessage() {
  const input = document.getElementById("messageInput");
  socket.send(JSON.stringify({
    type: "message",
    user: username,
    text: input.value
  }));
  input.value = "";
}
