const tg = window.Telegram.WebApp;
tg.expand();

const initData = Telegram.WebApp.initData;
const userPhoto = document.getElementById("user-photo");
const userName = document.getElementById("user-name");

function renderUser(user) {
  console.log("Rendering user:", user);

  const userPhoto = document.getElementById("user-photo");
  const userName = document.getElementById("user-name");

  if (userPhoto) {
    if (user.photo_url) {
      userPhoto.src = user.photo_url;
    } else {
      userPhoto.src = "default_avatar.png";
    }
  }

  if (userName) {
    if (user.username) {
      userName.innerText = `@${user.username}`;
    } else if (user.first_name) {
      userName.innerText = user.first_name;
    } else {
      userName.innerText = "Anonymous";
    }
  }
}

const user = Telegram.WebApp.initDataUnsafe.user;
renderUser(user);

// дальше остальной код с localStorage и fetch
const savedUser = localStorage.getItem("user");

if (savedUser) {
  const user = JSON.parse(savedUser);
  renderUser(user);
} else {
  fetch("https://giftcasebattle.onrender.com/auth/telegram", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ init_data: initData }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "ok") {
        const user = data.user;
        localStorage.setItem("user", JSON.stringify(user));
        renderUser(user);
      } else {
        console.error("Auth failed", data);
      }
    })
    .catch(console.error);
}