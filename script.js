const tg = window.Telegram.WebApp;
tg.expand();

// fetch('https://myserver.com/api/save_user', {
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json',
//     },
//     body: JSON.stringify({ telegram_id: Telegram.WebApp.initDataUnsafe.user.id })
// });

const initData = Telegram.WebApp.initData;
const userPhoto = document.getElementById("user-photo");
const userName = document.getElementById("user-name");
    
const renderUser = (user) => {
  userPhoto.src = user.photo_url;
  userName.innerText = `@${user.username}`;
};

const savedUser = localStorage.getItem("user");

if (savedUser) {
  const user = JSON.parse(savedUser);
  renderUser(user);
} else {
  fetch("/auth/telegram", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ init_data: initData })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "ok") {
      const user = data.user;  // ✅ Теперь правильно
      localStorage.setItem("user", JSON.stringify(user));
      renderUser(user);
    } else {
      console.error("Auth failed", data);
    }
  })
  .catch(console.error);
}
