document.addEventListener('DOMContentLoaded', function() {
    var elem = document.querySelector('.sidenav');
    M.Sidenav.init(elem);
    var select = document.querySelector('select');
    M.FormSelect.init(select);

  });