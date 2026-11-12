(function () {
  var racine = document.documentElement;
  // --- édition du matin (claire) ou du soir (sombre)
  function sombre() {
    var t = racine.getAttribute('data-theme');
    if (t) return t === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  function libelle() {
    var b = document.querySelector('[data-edition] span');
    if (b) b.textContent = sombre() ? 'Édition du soir' : 'Édition du matin';
  }
  try { var choix = localStorage.getItem('mag-edition'); if (choix === 'dark' || choix === 'light') racine.setAttribute('data-theme', choix); } catch (e) {}
  function pret() {
    libelle();
    var ed = document.querySelector('[data-edition]');
    if (ed) ed.addEventListener('click', function () {
      var v = sombre() ? 'light' : 'dark';
      racine.setAttribute('data-theme', v);
      try { localStorage.setItem('mag-edition', v); } catch (e) {}
      libelle();
    });
    // --- le fil : pause
    var p = document.querySelector('[data-pause]');
    if (p) p.addEventListener('click', function () {
      var fil = p.closest('.fil'), on = fil.classList.toggle('pause');
      p.setAttribute('aria-pressed', on ? 'true' : 'false');
      p.textContent = on ? 'Reprendre' : 'Pause';
    });
    // --- le conseil à découper : on le détache et on le copie
    document.querySelectorAll('[data-copie]').forEach(function (b) {
      b.addEventListener('click', function () {
        var coupon = b.closest('.coupon'), ok = coupon.querySelector('.ok'), texte = b.getAttribute('data-copie');
        coupon.classList.add('decoupe');
        function dit(m) { ok.textContent = m; }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(texte).then(function () { dit('Conseil copié : collez-le où vous voulez.'); }, function () { secours(); });
        } else { secours(); }
        function secours() {
          var liste = coupon.querySelector('ol'), s = window.getSelection(), r = document.createRange();
          r.selectNodeContents(liste); s.removeAllRanges(); s.addRange(r);
          dit('Conseil sélectionné : copiez-le avec Ctrl + C.');
        }
      });
    });
    if (window.matchMedia) window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', libelle);
    new MutationObserver(libelle).observe(racine, { attributes: true, attributeFilter: ['data-theme'] });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', pret); else pret();
})();
