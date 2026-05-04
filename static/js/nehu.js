// Flash message auto-hide
setTimeout(() => {
  const flashBox = document.getElementById("flashMessage");
  if (flashBox) {
    flashBox.style.transition = "opacity 1s";
    flashBox.style.opacity = "0";
    setTimeout(() => flashBox.remove(), 1000);
  }
}, 5000);

// Login modal logic
const modal = document.getElementById("loginModal");
const loginBtn = document.getElementById("loginBtn");
const closeBtn = document.getElementsByClassName("close")[0];

loginBtn.onclick = () => modal.style.display = "block";
closeBtn.onclick = () => modal.style.display = "none";
window.onclick = (event) => { if (event.target == modal) modal.style.display = "none"; }

