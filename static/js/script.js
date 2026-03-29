console.log("RideShare loaded");
function openLogin() {
  document.getElementById("loginModal").style.display = "block";
}

function closeLogin() {
  document.getElementById("loginModal").style.display = "none";
}

// Close when clicking outside
window.onclick = function(event) {
  let modal = document.getElementById("loginModal");
  if (event.target == modal) {
    modal.style.display = "none";
  }
}