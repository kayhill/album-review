document.addEventListener('DOMContentLoaded', function() {
    // search menu options
    var select = document.querySelector('select');
    M.FormSelect.init(select);

    document.getElementById('custom-nom').addEventListener('click', () => loadNomForm());

    document.getElementById('search-query').addEventListener('submit', () => searchByArtist())

  });

async function searchByArtist() {
    try {        
        const response = await fetch('https://cors-anywhere.herokuapp.com/https://theaudiodb.com/api/v1/json/1/searchalbum.php?s=daft_punk');
        const albums = await response.json();        
        } catch(error) {
            alert(error);
        }
}     

function displayAlbums(albums) {
    const searchResult = document.getElementById('search-results');

    if (albums.count == 0) {
        searchResult.innerHTML = `<div class="text-field purple-text container">
        <h5>Sorry, your search returned 0 results.</h5>
          <ul id="nom-tips" class="browser-default flow-text">
            <li>Double check your spelling, including spaces</li>
            <li>Are you missing 'The'?</li>
            <li>Switch your search category: search for artist instead of album, or an album instead of an artist</li>
          </ul>
      </div>`
    } else if (albums.count > 0) {
        albums.forEach(album => {
            const markup = `<div class="col s12 m6 l4 album-result center border">
            <div class="album-art center">
              <a href=""><img class="z-depth-2" src="{{ album.strAlbumThumb }}" alt="album-cover"></a>
            </div>
            <div class="album-info center">
              <a href="albumview"><p class="album-title flow-text">{{ album.strAlbum }}</p></a>
              <a href="artistview"><p class="album-artist flow-text">{{album. strArtist }}</p></a>
              <div class="album-btns-small container">
                <a class="hover-btn"><i class="material-icons purple-text">stars</i> nominate</a>
                <a class="hover-btn"><i class="material-icons blue-text">music_note</i> view</a>
              </div>
            </div>
          </div>`;
          searchResult.insertAdjacentHTML('beforeend', markup);       
        });
    }
}

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