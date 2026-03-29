console.log("RideShare loaded");
function openLogin() {
  document.getElementById("loginModal").style.display = "block";
}

function closeLogin() {
  document.getElementById("loginModal").style.display = "none";
}

// Close when clicking outside
window.onclick = function(event) {
  let loginModal = document.getElementById("loginModal");
  let registerModal = document.getElementById("registerModal");

  if (event.target == loginModal) {
    loginModal.style.display = "none";
  }

  if (event.target == registerModal) {
    registerModal.style.display = "none";
  }
}
function openRegister() {
  document.getElementById("registerModal").style.display = "block";
}

function closeRegister() {
  document.getElementById("registerModal").style.display = "none";
}