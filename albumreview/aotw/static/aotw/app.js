document.addEventListener('DOMContentLoaded', function() {
  // side navigation menu  
    var sidenav = document.querySelector('.sidenav');
    M.Sidenav.init(sidenav);

    var carousel = document.querySelectorAll('.carousel');
    M.Carousel.init(carousel);

    var scrollspy = document.querySelectorAll('.scrollspy');
    M.ScrollSpy.init(scrollspy);

  });