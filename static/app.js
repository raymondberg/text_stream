var socket = io();

function isMessageDisplayed(messageId){
  return $("#message_" + messageId).length
}

function isApprovalDisplayed(messageId){
  return $("#approval_request_" + messageId).length
}

function requestAllApprovals() {
  socket.emit("request_approvals")
}

function submitMessage() {
  console.log("Emitting: " + $("#message_input").val())
  socket.emit("submit_message", {content: $("#message_input").val()})

  $("#message_input").val("")
}

function deleteById(id) {
  console.log("removing " + id)
  $("#approval_request_" + id).remove()
}

function reject(id) {
  socket.emit("reject", { message_id: id })
  deleteById(id)
}

function approve(id) {
  socket.emit("approve", { message_id: id })
  deleteById(id)
}

var randomProperty = function (obj) {
  var keys = Object.keys(obj);
  return keys[ keys.length * Math.random() << 0];
};

