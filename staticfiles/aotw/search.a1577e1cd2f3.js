document.addEventListener('DOMContentLoaded', function() {
  // search menu options
  var select = document.querySelector('select');
  M.FormSelect.init(select);


  document.getElementById('custom-nom').addEventListener('click', () => loadNomForm());
  document.getElementById('new-search').addEventListener('click', () => loadSearchForm());
  
});


function loadNomForm() {
  document.getElementById('nom-form').classList.toggle("hidden");
}

function loadSearchForm() {
  document.getElementById('new-search-form').classList.toggle("hidden");
}

