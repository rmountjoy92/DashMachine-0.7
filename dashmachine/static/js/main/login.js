let loginForm = document.getElementById("loginForm");
loginForm.addEventListener("submit", function (e) {
  e.preventDefault();
  fetch(checkLoginUrl, {
    method: "post",
    body: new FormData(loginForm),
  })
    .then((r) => r.text())
    .then(function (r) {
      if (r == "success") {
        window.location.href = mainUrl;
      } else {
        let loginError = document.getElementById("loginError");
        loginError.classList.remove("d-none");
        loginError.innerText = r;
      }
    });
});
