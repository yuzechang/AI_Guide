/**
 * AI Nav — 全局语言管理
 * 优先级：URL param ?lang=xx > localStorage > 默认 'en'
 * 切换时同步写入 URL param 和 localStorage
 */
(function () {
  function getLangFromURL() {
    try {
      return new URLSearchParams(location.search).get('lang');
    } catch (e) { return null; }
  }

  function applyLang(lang) {
    if (lang !== 'zh' && lang !== 'en') lang = 'en';
    document.documentElement.setAttribute('data-lang', lang);
    document.documentElement.setAttribute('lang', lang === 'zh' ? 'zh-CN' : 'en');

    // 更新所有语言按钮
    document.querySelectorAll('[data-langbtn]').forEach(function (btn) {
      btn.classList.toggle('active', btn.getAttribute('data-langbtn') === lang);
    });

    // 写入 URL param（不跳转，不加历史记录）
    try {
      var url = new URL(location.href);
      url.searchParams.set('lang', lang);
      history.replaceState(null, '', url.toString());
    } catch (e) {}

    // 写入 localStorage
    try { localStorage.setItem('ai-nav-lang', lang); } catch (e) {}
  }

  // 暴露全局 setLang（各页面按钮 onclick 调用）
  window.setLang = applyLang;

  // 页面初始化
  var lang = getLangFromURL()
    || (function () { try { return localStorage.getItem('ai-nav-lang'); } catch (e) { return null; } })()
    || 'en';

  // 立即设置 data-lang 防止 FOUC（CSS 依赖此属性隐藏 .en/.zh）
  document.documentElement.setAttribute('data-lang', lang);

  // DOM ready 后更新按钮 active 状态
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { applyLang(lang); });
  } else {
    applyLang(lang);
  }
})();
