document.addEventListener('DOMContentLoaded', function() {
    // search menu options
    var select = document.querySelector('select');
    M.FormSelect.init(select);

    document.getElementById('custom-nom').addEventListener('click', () => loadNomForm());

  });

  function loadNomForm() {
    document.getElementById('nom-form').innerHTML = `<div class="row">
    <form class="col s12" id="nomination-form">
     <div class="row">
        <div class="input-field col s8 offset-s2">
          <input id="artist-nom" type="text" class="validate">
          <label for="artist-nom">Artist</label>
        </div>
      </div>
      <div class="row">
        <div class="input-field col s8 offset-s2">
          <input id="album-nom" type="text" class="validate">
          <label for="album-nom">Album Title</label>
        </div>
      </div>
      <div class="row">
        <div class="input-field center">
          <input id="submit-nom" type="submit" class="submit btn" value="Nominate!">            
        </div>
      </div>
    </form>
  </div>`;  
  document.getElementById('custom-nom').style.display = "none"
  };