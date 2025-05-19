// Интерактивный скролл
const scrollContainer1 = document.querySelector('.scroll-container');

scrollContainer1.addEventListener('wheel', function(e) {
  // Если пользователь прокручивает колесико мыши вертикально
  if (e.deltaY !== 0) {
    // Перемещаем прокрутку по горизонтали
    scrollContainer1.scrollLeft += e.deltaY;
    // Отменяем стандартное вертикальное поведение прокрутки
    e.preventDefault();
  }
}, { passive: false });

const scrollContainer = document.querySelector('.scroll-container');
const buttons = scrollContainer.querySelectorAll('.oval-button');

buttons.forEach(button => {
  button.addEventListener('click', () => {
    // Если эта кнопка уже активна, ничего не делаем
    if (button.classList.contains('active')) return;

    // Убираем класс active у всех кнопок
    buttons.forEach(btn => btn.classList.remove('active'));

    // Добавляем active к нажатой кнопке
    button.classList.add('active');

    // Плавно скроллим контейнер к выбранной кнопке
    const buttonLeft = button.offsetLeft;
    const containerScrollLeft = scrollContainer.scrollLeft;
    const containerWidth = scrollContainer.clientWidth;
    const buttonWidth = button.offsetWidth;

    // Рассчитываем позицию для центрирования кнопки в контейнере
    const scrollTo = buttonLeft - (containerWidth / 2) + (buttonWidth / 2);

    scrollContainer.scrollTo({
      left: scrollTo,
      behavior: 'smooth'
    });
  });
});