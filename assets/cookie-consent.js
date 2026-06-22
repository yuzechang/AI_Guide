(function () {
  var STORAGE_KEY = 'ainav_cookie_consent';
  var consent = localStorage.getItem(STORAGE_KEY);
  if (consent) return; // 已做过选择，不再显示

  var banner = document.createElement('div');
  banner.id = 'cookie-banner';
  banner.innerHTML = [
    '<div style="max-width:900px;margin:0 auto;display:flex;align-items:center;gap:16px;flex-wrap:wrap">',
    '<p style="margin:0;flex:1;min-width:200px;font-size:13px;line-height:1.5;color:#e2e8f0">',
    'We use cookies to analyze site usage and serve personalized ads via Google AdSense. ',
    'See our <a href="/privacy-policy" style="color:#818cf8;text-decoration:underline">Privacy Policy</a>.',
    '</p>',
    '<div style="display:flex;gap:8px;flex-shrink:0">',
    '<button id="cookie-accept" style="background:#6366f1;color:#fff;border:none;padding:8px 18px;border-radius:6px;font-size:13px;font-weight:600;cursor:pointer">Accept</button>',
    '<button id="cookie-decline" style="background:transparent;color:#94a3b8;border:1px solid #334155;padding:8px 18px;border-radius:6px;font-size:13px;cursor:pointer">Essential Only</button>',
    '</div>',
    '</div>'
  ].join('');

  Object.assign(banner.style, {
    position: 'fixed',
    bottom: '0',
    left: '0',
    right: '0',
    background: '#1e293b',
    borderTop: '1px solid #334155',
    padding: '14px 20px',
    zIndex: '9999',
    boxShadow: '0 -4px 24px rgba(0,0,0,0.4)'
  });

  document.body.appendChild(banner);

  document.getElementById('cookie-accept').addEventListener('click', function () {
    localStorage.setItem(STORAGE_KEY, 'accepted');
    banner.remove();
  });

  document.getElementById('cookie-decline').addEventListener('click', function () {
    localStorage.setItem(STORAGE_KEY, 'declined');
    // 设置非个性化广告模式
    window['ga-disable-G-XXXXXXXXXX'] = true;
    banner.remove();
  });
})();
