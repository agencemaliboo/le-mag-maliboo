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


(function(){
  document.documentElement.classList.add('js');
  function pret(){
    var cartes=[].slice.call(document.querySelectorAll('.carte'));
    cartes.forEach(function(c,i){if(c.getBoundingClientRect().top>window.innerHeight*0.94){c.classList.add('attend');c.style.transitionDelay=(i%3)*90+'ms';}});
    function verifie(){cartes=cartes.filter(function(c){if(!c.classList.contains('attend'))return false;if(c.getBoundingClientRect().top<window.innerHeight*0.94){c.classList.remove('attend');return false;}return true;});if(!cartes.length&&minuterie){clearInterval(minuterie);minuterie=0;}}
    var minuterie=setInterval(verifie,500);
    window.addEventListener('scroll',verifie,{passive:true});window.addEventListener('resize',verifie);
    var barre=document.querySelector('.lecture');
    if(barre){var maj=function(){var h=document.documentElement.scrollHeight-window.innerHeight;barre.style.transform='scaleX('+(h>0?Math.min(1,window.scrollY/h):0)+')';};window.addEventListener('scroll',maj,{passive:true});maj();}
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',pret);else pret();
})();


(function(){
  function pret(){
    // filtres de la page « Tous les articles »
    var boutons=[].slice.call(document.querySelectorAll('[data-filtre]'));
    boutons.forEach(function(b){b.addEventListener('click',function(){
      var f=b.getAttribute('data-filtre'),n=0;
      boutons.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
      [].slice.call(document.querySelectorAll('[data-rub]')).forEach(function(c){var ok=f==='tous'||c.getAttribute('data-rub')===f;c.hidden=!ok;if(ok){n++;c.classList.remove('attend');}});
      var v=document.querySelector('.vide');if(v)v.hidden=n>0;
    });});
    // prochain numéro : lundi ou jeudi
    var cible=document.querySelector('[data-prochain]');
    if(cible){var j=new Date().getDay(),h=new Date().getHours();
      var jeudi=(j===1&&h>=7)||j===2||j===3||(j===4&&h<7);
      cible.textContent=jeudi?'jeudi':'lundi';
      var led=document.querySelector('[data-led]');if(led)led.textContent='BOUCLAGE EN COURS   •   PROCHAIN NUMÉRO '+(jeudi?'JEUDI':'LUNDI')+'   •   DEUX ARTICLES PAR SEMAINE';}
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',pret);else pret();
})();
