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
      if (user.first_name) {
        userName.innerText = user.first_name;
      } else if (user.username) {
        userName.innerText = user.username;
      } else {
        userName.innerText = "Гость";
      }
    }
  }

  // Сначала отрисуем пользователя мгновенно из Telegram WebApp
  const webAppUser = initDataUnsafe.user;
  if (webAppUser) {
    renderUser(webAppUser);
  }

  // Затем отправим initData на сервер для авторизации
  fetch("https://giftcasebattle.onrender.com/auth/telegram", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: new URLSearchParams({ init_data: tg.initData }).toString()
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "ok") {
        // Можно сохранить серверную копию пользователя
        localStorage.setItem("user", JSON.stringify(data.user));

        // Если хочешь отрисовать именно серверного юзера — можешь перерендерить
        renderUser(data.user);
      } else {
        console.error("Auth failed", data);
      }
    })
    .catch(console.error);