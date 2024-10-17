document.addEventListener("DOMContentLoaded", function() {
  const logo = document.querySelector('.logo');

  logo.addEventListener('click', function(event) {
      event.preventDefault();
      window.location.href = '/';
  });
});
