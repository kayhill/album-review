document.addEventListener('DOMContentLoaded', function() {
  // search menu options
  var select = document.querySelector('select');
  M.FormSelect.init(select);

  document.getElementById('custom-nom').addEventListener('click', () => loadNomForm());
});


function loadNomForm() {
  document.getElementById('nom-form').style.display = "block";
  document.getElementById('custom-nom').style.display = "none";
}
