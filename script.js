const tg = window.Telegram.WebApp;
tg.expand();

const initDataUnsafe = Telegram.WebApp.initDataUnsafe;
const userPhoto = document.getElementById("user-photo");
const userName = document.getElementById("user-name");

function renderUser(user) {
  console.log("Rendering user:", user);

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

// Получаем пользователя из Telegram WebApp
const user = initDataUnsafe.user;
renderUser(user);

// Дальше работа с localStorage и авторизацией
const savedUser = localStorage.getItem("user");

if (savedUser) {
  const user = JSON.parse(savedUser);
  renderUser(user);
} else {
  fetch("https://giftcasebattle.onrender.com/auth/telegram", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(initDataUnsafe), // исправлено!
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