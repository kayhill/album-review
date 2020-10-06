document.addEventListener('DOMContentLoaded', function () {
  // side navigation menu  
  var sidenav = document.querySelector('.sidenav');
  M.Sidenav.init(sidenav);

  var carousel = document.querySelectorAll('.carousel');
  M.Carousel.init(carousel);

  // avatar img src
  const pics = document.querySelectorAll('.user_avatar');
  pics.forEach(geturl);
});

function geturl(pic) {  
    url = pic.attributes[0].nodeValue;
    url = url.replace('/resized/80/', '/');
    pic.attributes[0].nodeValue = url;
}