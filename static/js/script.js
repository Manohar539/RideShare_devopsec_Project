console.log("RideShare loaded");

// ================= LOGIN MODAL =================
function openLogin() {
  document.getElementById("loginModal").style.display = "block";
}

function closeLogin() {
  document.getElementById("loginModal").style.display = "none";
}

// ================= REGISTER MODAL =================
function openRegister() {
  document.getElementById("registerModal").style.display = "block";
}

function closeRegister() {
  document.getElementById("registerModal").style.display = "none";
}

// ================= CLOSE MODALS ON OUTSIDE CLICK =================
window.onclick = function(event) {
  let loginModal = document.getElementById("loginModal");
  let registerModal = document.getElementById("registerModal");

  if (event.target == loginModal) {
    loginModal.style.display = "none";
  }

  if (event.target == registerModal) {
    registerModal.style.display = "none";
  }
};

// ================= REGISTER FORM AJAX =================
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("registerForm");

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      let formData = new FormData(form);

      fetch("/users/register/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
        },
      })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Registration successful!");

          // close popup
          closeRegister();

          // reload page to update navbar (logged in)
          location.reload();
        } else {
          let errorMsg = "";

          for (let field in data.errors) {
            errorMsg += field + ": " + data.errors[field].join(", ") + "\n";
          }

          alert(errorMsg);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    });
  }
});