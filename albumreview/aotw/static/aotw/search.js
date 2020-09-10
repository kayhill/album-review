document.addEventListener('DOMContentLoaded', function() {
    // search menu options
    var select = document.querySelector('select');
    M.FormSelect.init(select);

    document.getElementById('custom-nom').addEventListener('click', () => loadNomForm());

    const searchForm = document.getElementById('search-query');
    searchForm.addEventListener('submit', e => {
      e.preventDefault();

      if (searchForm.elements["search-option"].value === '1') {
        let artistName = searchForm.elements["search"].value;
        searchByArtist(artistName);
      } else {
        let albumName = searchForm.elements["search"].value;
        searchByAlbum(albumName);      }
      
    });
  });

async function searchByArtist(artistName) {
    try {        
        const response = await fetch(`https://www.theaudiodb.com/api/v1/json/523532/searchalbum.php?s=${artistName}`);
        const json = await response.json();       
        const albums = await JSON.parse(JSON.stringify(json));
          displayAlbums(albums);
          console.log(albums);      
            
        } catch(error) {
            alert(error);
        }
}     


async function searchByAlbum(albumName) {
  try {        
      const response = await fetch(`https://www.theaudiodb.com/api/v1/json/1/searchalbum.php?a=${albumName}`);
      const json = await response.json();  
      const albums = await JSON.parse(JSON.stringify(json));

      //TESTING
      console.log(albums);
      displayAlbums(albums);      
      } catch(error) {
          alert(error);
      }
}     

function displayAlbums(albums) {
    const searchResult = document.getElementById('search-results');
    searchResult.innerHTML='';
    const albumResults = albums.album.length;
    albums = albums.album;        

    if (albumResults == 0) {     

        searchResult.innerHTML = `<div class="text-field purple-text container">
        <h5>Sorry, your search returned 0 results.</h5>
          <ul id="nom-tips" class="browser-default flow-text">
            <li>Double check your spelling, including spaces</li>
            <li>Are you missing 'The'?</li>
            <li>Switch your search category: search for artist instead of album, or an album instead of an artist</li>
          </ul>
      </div>`
    } else if (albumResults > 0) {
      let li = document.createElement('div')
      document.querySelector('ul').appendChild(li)
      
        for (const album of albums) {
          let albumPhoto;

          if (album.strAlbumThumb) {
            albumPhoto = album.strAlbumThumb;
          } else {
            albumPhoto = 'https://i.ibb.co/VVFSqNk/music-album-icon-2.jpg'
          };

          const markup = `
          <div class="col s12 m6 l4 album-result center border">
            <div class="album-art center">
              <a href="album/${ album.idAlbum }"><img class="z-depth-2" src="${ albumPhoto }" alt="album-cover"></a>
            </div>
            <div class="album-info center">
              <a href="album/${ album.idAlbum }"><p class="album-title flow-text">${ album.strAlbum }</p></a>
              <a href=""><p class="album-artist flow-text">${album.strArtist }</p></a>
              <div class="album-btns-small container">
                <a href="nominate/${ album.idAlbum }" class="hover-btn nominate-btn"><i class="material-icons purple-text">stars</i> nominate</a>
                <a class="hover-btn view-btn"><i class="material-icons blue-text">music_note</i> view</a>
              </div>
            </div>
          </div>`;
          searchResult.insertAdjacentHTML('beforeend', markup);       
        }
          
      };
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