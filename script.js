const tg = window.Telegram.WebApp;
tg.expand();

// fetch('https://myserver.com/api/save_user', {
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json',
//     },
//     body: JSON.stringify({ telegram_id: Telegram.WebApp.initDataUnsafe.user.id })
// });

const initData = Telegram.WebApp.initData;  // Данные из Telegram WebApp
const userPhoto = document.getElementById("user-photo");
const userName = document.getElementById("user-name");

const renderUser = (user) => {
  if (user.photo_url) {
    userPhoto.src = user.photo_url;
  } else {
    userPhoto.src = "default_avatar.png"; // или любой запасной аватар
  }

  if (user.username) {
    userName.innerText = `@${user.username}`;
  } else if (user.first_name) {
    userName.innerText = user.first_name;
  } else {
    userName.innerText = "Anonymous";
  }
};

const savedUser = localStorage.getItem("user");

if (savedUser) {
  const user = JSON.parse(savedUser);
  renderUser(user);
} else {
  fetch("/auth/telegram", {
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
