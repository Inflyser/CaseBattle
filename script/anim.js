document.addEventListener('DOMContentLoaded', function () {
  lottie.loadAnimation({
    container: document.getElementById('animation-container'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: '../jsons/Horror_Movie.json'
  });
});