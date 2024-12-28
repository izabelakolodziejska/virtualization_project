const API_URL = 'http://localhost:4000/api/flask/songs';

async function fetchSongs() {
  try {
    const response = await fetch(API_URL);
    const songs = await response.json();
    displaySongs(songs);
  } catch (error) {
    console.error('Error fetching songs:', error);
  }
}


function displaySongs(songs) {
    const songList = document.getElementById('song-list');
    
    songList.innerHTML = '';  
  
    if (songs.length === 0) {
      const placeholder = document.createElement('p');
      placeholder.classList.add('text-muted', 'text-center');
      placeholder.textContent = 'No songs added yet. Add your favorite songs on the left!';
      songList.appendChild(placeholder);
      return; 
    }
  
    songs.forEach(song => {
      const songElement = document.createElement('div');
      songElement.classList.add('song');
      
      songElement.innerHTML = `
        <p>${song.name} - ${song.artist} (${song.genre || 'No genre'})</p>
        <button class="btn btn-purple"  onclick="deleteSong(${song.id})">Delete</button>
      `;
      
      songList.appendChild(songElement);
    });
  }
  

async function deleteSong(id) {
  try {
    const response = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    if (response.ok) {
      fetchSongs();  
    }
  } catch (error) {
    console.error('Error deleting song:', error);
  }
}


document.getElementById('song-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  
  const name = document.getElementById('song-name').value;
  const artist = document.getElementById('song-artist').value;
  const genre = document.getElementById('song-genre').value;
  
  const songData = { name, artist, genre };
  
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(songData),
    });
    
    if (response.ok) {
      fetchSongs();  
    }
  } catch (error) {
    console.error('Error adding song:', error);
  }
});

fetchSongs();
