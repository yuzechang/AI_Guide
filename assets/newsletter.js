/**
 * Newsletter 订阅表单逻辑
 * - 前端邮箱格式验证
 * - 优先调用 Formspree API 提交
 * - Formspree 失败时退回 localStorage 模式
 * - 已订阅状态检测，避免重复显示表单
 */
(function () {
  'use strict';

  var FORMSPREE_URL = 'https://formspree.io/f/xdkkoajz';
  var LS_DONE_KEY = 'ainav_newsletter_done';
  var LS_EMAILS_KEY = 'ainav_newsletter';

  /**
   * 验证邮箱格式
   * @param {string} email
   * @returns {boolean}
   */
  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
  }

  /**
   * 显示订阅成功状态，隐藏表单
   */
  function showSuccess(formWrap, successEl) {
    localStorage.setItem(LS_DONE_KEY, '1');
    window.location.href = '/newsletter-thank-you';
  }

  /**
   * 在按钮上显示短暂的错误提示文案
   * @param {HTMLButtonElement} btn
   * @param {string} msg
   */
  function showBtnError(btn, msg) {
    var original = btn.textContent;
    btn.textContent = msg;
    btn.disabled = true;
    setTimeout(function () {
      btn.textContent = original;
      btn.disabled = false;
    }, 3000);
  }

  /**
   * 保存邮箱到 localStorage（Formspree 失败时的降级方案）
   * @param {string} email
   */
  function saveToLocalStorage(email) {
    var existing = [];
    try {
      existing = JSON.parse(localStorage.getItem(LS_EMAILS_KEY) || '[]');
      if (!Array.isArray(existing)) existing = [];
    } catch (e) {
      existing = [];
    }
    if (existing.indexOf(email) === -1) {
      existing.push(email);
    }
    localStorage.setItem(LS_EMAILS_KEY, JSON.stringify(existing));
  }

  /**
   * 初始化订阅表单
   */
  function initNewsletter() {
    var form = document.getElementById('newsletterForm');
    var emailInput = document.getElementById('newsletterEmail');
    var successEl = document.getElementById('newsletterSuccess');
    var formWrap = form ? form.parentElement : null;

    if (!form || !emailInput || !successEl) return;

    // 已订阅状态：直接显示成功，不显示表单
    if (localStorage.getItem(LS_DONE_KEY)) {
      showSuccess(form, successEl);
      return;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var email = emailInput.value.trim();
      var btn = form.querySelector('.newsletter-btn');

      // 前端邮箱格式验证
      if (!isValidEmail(email)) {
        showBtnError(btn, '请输入有效的邮箱地址');
        emailInput.focus();
        return;
      }

      // 提交中状态
      btn.textContent = 'Subscribing…';
      btn.disabled = true;

      // 尝试调用 Formspree
      fetch(FORMSPREE_URL, {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email })
      })
        .then(function (res) {
          if (res.ok) {
            // Formspree 提交成功
            showSuccess(form, successEl);
          } else {
            // Formspree 返回错误，降级到 localStorage
            throw new Error('Formspree 返回非 2xx：' + res.status);
          }
        })
        .catch(function (err) {
          // 网络错误或 Formspree 不可用，退回 localStorage 模式
          console.warn('[newsletter] Formspree 提交失败，已降级到本地存储：', err.message);
          saveToLocalStorage(email);

          // 更新成功文案为降级提示
          successEl.innerHTML =
            '感谢订阅！我们将于近期开始发送更新邮件。';
          showSuccess(form, successEl);
        });
    });
  }

  // DOM 就绪后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNewsletter);
  } else {
    initNewsletter();
  }
})();
