let menuBtn = document.querySelector('.menu-btn');
let menu = document.querySelector('.menu');

document.getElementById('hotel_link').addEventListener('click', function(event) {
 // Отменяем стандартное действие ссылки
  window.location.href = '/hotels';  // Перенаправляем на /hotels
});

menuBtn.addEventListener('click', function () {
  menuBtn.classList.toggle('active');
  menu.classList.toggle('active');
});
