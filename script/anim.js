document.addEventListener('DOMContentLoaded', function () {
  // Загружаем анимацию, но не запускаем сразу
  const animation = lottie.loadAnimation({
    container: document.getElementById('animation-container'),
    renderer: 'svg',
    loop: true,
    autoplay: false,  // отключаем автозапуск
    path: '../../jsons/Horror_Movie.json'
  });
  // Кнопка запуска анимации
  const playBtn = document.getElementById('play-btn');
  playBtn.addEventListener('click', function () {
    animation.play();  // запускаем анимацию по клику
  });
});