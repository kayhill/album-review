document.addEventListener('DOMContentLoaded', function () {
  // side navigation menu  
  var sidenav = document.querySelector('.sidenav');
  M.Sidenav.init(sidenav);

  var carousel = document.querySelectorAll('.carousel');
  M.Carousel.init(carousel);

  geturl();
});

function geturl() {
  const pics = document.querySelectorAll('.user_avatar');
  for (let pic in pics) {
    url = pic.src;
    url.replace('/resized/80/', '/');
  }
}