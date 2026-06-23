/* ===== AI Nav – 收藏夹系统 ===== */
const FAVORITES_KEY = 'ainav_favorites';

function getFavorites() {
  return JSON.parse(localStorage.getItem(FAVORITES_KEY) || '[]');
}

function isFavorited(toolId) {
  return getFavorites().includes(toolId);
}

function toggleFavorite(toolId) {
  let favs = getFavorites();
  if (favs.includes(toolId)) {
    favs = favs.filter(function(id) { return id !== toolId; });
  } else {
    favs.push(toolId);
  }
  localStorage.setItem(FAVORITES_KEY, JSON.stringify(favs));
  return favs.includes(toolId);
}

function initFavoriteBtn(toolId) {
  var btn = document.getElementById('favoriteBtn');
  if (!btn) return;
  updateFavBtn(btn, isFavorited(toolId));
  btn.addEventListener('click', function() {
    var isNowFaved = toggleFavorite(toolId);
    updateFavBtn(btn, isNowFaved);
    showToast(isNowFaved ? 'Added to favorites ♥' : 'Removed from favorites');
  });
}

function updateFavBtn(btn, isFaved) {
  btn.innerHTML = isFaved ? '♥ Saved' : '♡ Save';
  btn.classList.toggle('fav-active', isFaved);
}

function showToast(msg) {
  var toast = document.getElementById('ainav-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'ainav-toast';
    Object.assign(toast.style, {
      position: 'fixed',
      bottom: '72px',
      left: '50%',
      transform: 'translateX(-50%)',
      background: '#1e293b',
      color: '#e2e8f0',
      padding: '10px 20px',
      borderRadius: '8px',
      fontSize: '13px',
      fontWeight: '500',
      zIndex: '10000',
      boxShadow: '0 4px 16px rgba(0,0,0,0.3)',
      transition: 'opacity 0.3s'
    });
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.opacity = '1';
  clearTimeout(toast._timer);
  toast._timer = setTimeout(function() { toast.style.opacity = '0'; }, 2000);
}
