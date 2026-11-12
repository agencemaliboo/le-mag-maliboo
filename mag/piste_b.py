# -*- coding: utf-8 -*-
"""Piste B : le magazine moderne (charte Maliboo violet et vert, grandes couvertures, cartes, animations au défilement)."""
import glob, json, os, shutil
import build as B

ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ICI, "apercu-b")
T, e = B.T, B.e

POLICES = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=DM+Sans:ital,opsz,wght@0,9..40,400..700;1,9..40,400..700&display=swap">')

CSS = r'''
:root{--fond:#FFFFFF;--fond-2:#F6F0FB;--encre:#1E0F30;--mu:#5E4B73;--violet:#7A2BC2;--violet-f:#4E1590;--vert:#76E02F;--vert-f:#2F7D0C;--jaune:#FFD84D;--ligne:#E6DAF0;--carte:#FFFFFF;
 --titre:"Bricolage Grotesque","Trebuchet MS",system-ui,sans-serif;--texte:"DM Sans",system-ui,-apple-system,"Segoe UI",sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--fond:#150A22;--fond-2:#21103A;--encre:#F7F0FB;--mu:#C9B8D9;--violet:#A866EE;--violet-f:#4E1590;--vert-f:#8DEB4E;--ligne:#3B2552;--carte:#21103A;color-scheme:dark}}
:root[data-theme="dark"]{--fond:#150A22;--fond-2:#21103A;--encre:#F7F0FB;--mu:#C9B8D9;--violet:#A866EE;--violet-f:#4E1590;--vert-f:#8DEB4E;--ligne:#3B2552;--carte:#21103A;color-scheme:dark}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--fond);color:var(--encre);font:400 18px/1.6 var(--texte);-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit}
:focus-visible{outline:3px solid var(--vert);outline-offset:3px;border-radius:8px}
img,svg{max-width:100%;display:block}
h1,h2,h3,p,ul,ol,figure{margin:0}ul,ol{padding:0;list-style:none}
button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
.w{max-width:1240px;margin-inline:auto;padding-left:max(18px,env(safe-area-inset-left,0px));padding-right:max(18px,env(safe-area-inset-right,0px))}
.lecture{position:fixed;top:0;left:0;height:4px;width:100%;background:var(--vert);transform-origin:left;transform:scaleX(0);z-index:60}

/* barre du haut */
.barre{position:sticky;top:env(safe-area-inset-top,0px);z-index:40;background:color-mix(in srgb,var(--fond) 86%,transparent);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--ligne)}
.barre .w{display:flex;align-items:center;gap:10px 22px;padding-block:10px;flex-wrap:wrap}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;font:800 25px/1 var(--titre);letter-spacing:-.02em}
.logo svg{width:40px;height:40px}
.logo small{font:600 13px/1 var(--texte);color:var(--mu);display:block;margin-top:3px;letter-spacing:0}
.barre nav{display:flex;gap:4px;margin-left:auto;flex-wrap:wrap}
.barre nav a{text-decoration:none;font-weight:600;font-size:16px;padding:8px 14px;border-radius:999px}
.barre nav a:hover,.barre nav a[aria-current]{background:var(--fond-2)}
.barre .ed{width:40px;height:40px;border-radius:50%;border:1px solid var(--ligne);display:grid;place-items:center}
.lune{width:18px;height:18px;border-radius:50%;border:2px solid var(--encre);background:linear-gradient(90deg,var(--encre) 50%,transparent 50%);display:block}
.cta{font-weight:700;font-size:16px;text-decoration:none;padding:10px 18px;border-radius:999px;background:var(--vert);color:#150A22;transition:transform .2s}
.cta:hover{transform:translateY(-2px)}

/* couverture */
.couv{position:relative;overflow:hidden;border-radius:36px;margin-top:22px;padding:clamp(26px,4.5vw,60px);color:#fff;background:linear-gradient(135deg,#3F1078 0%,#7A2BC2 55%,#A04EE6 100%);display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,.9fr);gap:30px 44px;align-items:center}
.couv .bulle{position:absolute;border-radius:50%;pointer-events:none;animation:flotte 9s ease-in-out infinite}
.couv .b1{width:260px;height:260px;right:-70px;top:-90px;background:var(--vert);opacity:.9}
.couv .b2{width:150px;height:150px;left:42%;bottom:-70px;background:var(--jaune);animation-delay:-3s}
.couv .b3{width:90px;height:90px;left:-30px;top:38%;background:#fff;opacity:.16;animation-delay:-5s}
@keyframes flotte{0%,100%{transform:translate(0,0)}50%{transform:translate(14px,-22px)}}
.couv>div,.couv>figure{position:relative;z-index:1;min-width:0}
.puce{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:15px;padding:7px 14px;border-radius:999px;background:#fff;color:#4E1590;text-decoration:none}
.puce::before{content:"";width:9px;height:9px;border-radius:50%;background:var(--vert)}
.couv h1{font:800 clamp(36px,5vw,70px)/1.02 var(--titre);letter-spacing:-.03em;margin:18px 0 16px;text-wrap:balance}
.couv h1 a{text-decoration:none}
.couv .chapeau{font-size:clamp(18px,1.6vw,21px);line-height:1.5;opacity:.92;max-width:34em}
.couv .actions{display:flex;gap:12px 18px;flex-wrap:wrap;align-items:center;margin-top:24px}
.bouton{display:inline-flex;align-items:center;gap:10px;font-weight:700;font-size:17px;text-decoration:none;padding:14px 24px;border-radius:999px;background:var(--vert);color:#150A22;transition:transform .2s,box-shadow .2s}
.bouton:hover{transform:translateY(-3px);box-shadow:0 12px 26px rgba(20,5,40,.28)}
.bouton i{width:22px;height:22px;border-radius:50%;background:#150A22;position:relative;flex:none}
.bouton i::after{content:"";position:absolute;left:8px;top:6.5px;border-left:7px solid var(--vert);border-top:4.5px solid transparent;border-bottom:4.5px solid transparent}
.temps{font-size:15px;opacity:.85}
.vignette{background:#fff;border-radius:28px;padding:18px;transform:rotate(3deg);box-shadow:0 26px 60px rgba(20,5,40,.35);transition:transform .5s cubic-bezier(.2,.8,.2,1)}
.couv:hover .vignette{transform:rotate(0) scale(1.02)}
.vignette svg{width:100%;height:auto}
.enc{fill:#1E0F30}.ver{fill:#7A2BC2}.boo{fill:#76E02F}.pap{fill:#fff}.tr{fill:#1E0F30}
.s-enc{stroke:#1E0F30;fill:none}.s-ver{stroke:#7A2BC2;fill:none}
.oeil{transform-box:fill-box;transform-origin:center;animation:cligne 6s infinite}
@keyframes cligne{0%,94%,100%{transform:scaleY(1)}97%{transform:scaleY(.1)}}

/* bandeau de conseils */
.defile{margin:26px 0 6px;overflow:hidden;display:flex;-webkit-mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}
.defile .bande{display:flex;flex:none;animation:defile 55s linear infinite}
.defile:hover .bande,.defile.pause .bande{animation-play-state:paused}
.defile span{flex:none;margin-right:12px;padding:9px 18px;border-radius:999px;background:var(--fond-2);font-weight:600;font-size:15.5px;white-space:nowrap}
.defile span:nth-child(3n+1){background:var(--vert);color:#150A22}
.defile span:nth-child(3n+2){background:var(--jaune);color:#150A22}
@keyframes defile{to{transform:translateX(-50%)}}

/* cartes */
.entete{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin:38px 0 16px}
.entete h2{font:800 clamp(28px,3.2vw,40px)/1.05 var(--titre);letter-spacing:-.025em}
.entete a{font-weight:700;color:var(--violet)}
.bento{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:18px}
.carte{border-radius:28px;padding:26px;min-width:0;position:relative;overflow:hidden;border:1px solid var(--ligne);background:var(--carte);transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s,opacity .7s}
.carte:hover{transform:translateY(-6px);box-shadow:0 22px 44px rgba(60,20,110,.16)}
.js .carte.attend{opacity:0;transform:translateY(34px)}
.carte h3{font:800 clamp(24px,2.3vw,31px)/1.08 var(--titre);letter-spacing:-.02em;text-wrap:balance}
.carte h3 a{text-decoration:none}
.carte h3 a::after{content:"";position:absolute;inset:0}
.carte p{font-size:16.5px;line-height:1.5}
.etq{font-weight:700;font-size:14px;letter-spacing:.02em;color:var(--violet);margin-bottom:10px;display:block}
.c-art{grid-column:span 4;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.8fr);gap:22px;align-items:center;background:var(--fond-2);border-color:transparent}
.c-art .vignette{transform:rotate(-2.5deg);box-shadow:0 14px 30px rgba(60,20,110,.18);padding:12px;border-radius:22px}
.c-art:hover .vignette{transform:rotate(0)}
.c-art p{margin-top:10px;color:var(--mu)}
.c-art .lien{display:inline-block;margin-top:14px;font-weight:700;color:var(--violet)}
.c-conseil{grid-column:span 2;background:var(--jaune);color:#150A22;border-color:transparent}
.c-conseil .etq{color:#150A22}
.c-conseil ol{counter-reset:e;margin-top:12px;display:grid;gap:9px}
.c-conseil li{counter-increment:e;display:grid;grid-template-columns:28px 1fr;gap:8px;font-size:16px;line-height:1.4}
.c-conseil li::before{content:counter(e);width:26px;height:26px;border-radius:50%;background:#150A22;color:var(--jaune);font:800 14px/26px var(--titre);text-align:center}
.c-conseil button{margin-top:16px;font-weight:700;font-size:15.5px;padding:10px 16px;border-radius:999px;background:#150A22;color:#fff;position:relative;z-index:2}
.c-conseil .ok{display:block;font-size:14.5px;margin-top:8px;font-weight:600}
.c-conseil.decoupe{animation:tamponne .5s cubic-bezier(.2,.8,.2,1)}
@keyframes tamponne{40%{transform:scale(.97) rotate(-1deg)}100%{transform:none}}
.c-mot{grid-column:span 2}
.c-mot dfn{font:800 44px/1 var(--titre);font-style:normal;letter-spacing:-.03em;display:block;margin-bottom:8px;color:var(--violet)}
.c-mot p{color:var(--mu)}
.c-avis{grid-column:span 2;background:#1E0F30;color:#fff;border-color:transparent}
.c-avis .etq{color:var(--vert)}
.c-avis .gros{display:flex;align-items:flex-end;gap:10px;margin-bottom:8px}
.c-avis .gros b{font:800 76px/.85 var(--titre);letter-spacing:-.04em}
.c-avis .gros span{font-weight:600;opacity:.8;padding-bottom:4px}
.c-avis q{quotes:"«\00a0" "\00a0»";display:block;font-size:16.5px;line-height:1.5;margin-top:12px}
.c-avis cite{display:block;font-style:normal;font-weight:700;font-size:14.5px;margin-top:8px;opacity:.85}
.c-avis .lien{display:inline-block;margin-top:14px;font-weight:700;color:var(--vert);position:relative;z-index:2}
.etoiles{display:flex;gap:3px}.etoiles svg{width:22px;height:22px}
.etoiles .ver{fill:#FFD84D}.etoiles .s-enc{stroke:none}
.c-annonce{grid-column:span 2;background:linear-gradient(140deg,#7A2BC2,#4E1590);color:#fff;border-color:transparent}
.c-annonce .etq{color:var(--vert)}
.c-annonce p{margin-top:10px;opacity:.92}
.c-annonce .bouton{margin-top:18px;font-size:16px;padding:12px 20px;position:relative;z-index:2}
.c-annonce .tel{display:block;margin-top:12px;font-weight:700}

/* article */
.art-tete{max-width:900px;margin:34px auto 0;text-align:center}
.art-tete .puce{background:var(--fond-2);color:var(--violet)}
.art-tete h1{font:800 clamp(34px,5vw,64px)/1.04 var(--titre);letter-spacing:-.03em;margin:18px 0 16px;text-wrap:balance}
.art-tete .chapeau{font-size:clamp(19px,1.8vw,22px);line-height:1.5;color:var(--mu);max-width:36em;margin-inline:auto}
.art-tete .meta{margin-top:16px;font-size:15px;color:var(--mu);font-weight:600}
.art-couv{margin:30px auto 0;max-width:1000px;border-radius:36px;background:linear-gradient(135deg,#3F1078,#7A2BC2 60%,#A04EE6);padding:clamp(22px,4vw,44px);display:grid;place-items:center;position:relative;overflow:hidden}
.art-couv .vignette{max-width:460px;width:100%;transform:rotate(-2deg)}
.art-couv .bulle{position:absolute;border-radius:50%;animation:flotte 9s ease-in-out infinite}
.art-couv .b1{width:200px;height:200px;right:-60px;top:-70px;background:var(--vert)}
.art-couv .b2{width:120px;height:120px;left:-40px;bottom:-40px;background:var(--jaune);animation-delay:-4s}
.texte{max-width:700px;margin:38px auto 0;font-size:19.5px;line-height:1.7}
.texte>p{margin-top:1em}
.texte>p:first-child{font-size:1.12em;font-weight:500}
.texte h2{font:800 clamp(26px,2.8vw,34px)/1.12 var(--titre);letter-spacing:-.02em;margin-top:1.7em;text-wrap:balance}
.texte ul.pts{margin-top:1em;display:grid;gap:10px}
.texte ul.pts li{display:grid;grid-template-columns:26px 1fr;gap:10px;padding:14px 16px;border-radius:16px;background:var(--fond-2);font-size:18px;line-height:1.45}
.texte ul.pts li::before{content:"";width:22px;height:22px;border-radius:50%;background:var(--vert);margin-top:2px;box-shadow:inset 0 0 0 6px var(--fond-2),inset 0 0 0 22px #2F7D0C}
.bref{max-width:700px;margin:34px auto 0;border-radius:24px;border:2px solid var(--violet);padding:22px 24px}
.bref h3{font:800 24px/1 var(--titre);margin-bottom:10px;color:var(--violet)}
.bref li{padding:8px 0 8px 30px;position:relative;font-weight:500}
.bref li::before{content:"";position:absolute;left:0;top:.62em;width:16px;height:9px;border-left:3.5px solid var(--vert-f);border-bottom:3.5px solid var(--vert-f);transform:rotate(-45deg)}
.apres{max-width:1000px;margin:38px auto 0}
.apres .bento{grid-template-columns:repeat(4,minmax(0,1fr))}
.apres .c-conseil,.apres .c-mot,.apres .c-annonce,.apres .c-art{grid-column:span 2}
.apres .c-art{grid-template-columns:1fr}

/* avis */
.avis-couv{border-radius:36px;margin-top:22px;padding:clamp(26px,4.5vw,56px);color:#fff;background:linear-gradient(135deg,#1E0F30,#4E1590);display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:28px 44px;align-items:center;position:relative;overflow:hidden}
.avis-couv h1{font:800 clamp(34px,4.8vw,64px)/1.04 var(--titre);letter-spacing:-.03em;margin:16px 0 14px;text-wrap:balance}
.avis-couv p{font-size:19px;line-height:1.5;opacity:.92}
.score{background:#fff;color:#1E0F30;border-radius:28px;padding:24px;text-align:center;transform:rotate(2deg)}
.score b{font:800 clamp(86px,10vw,124px)/.85 var(--titre);letter-spacing:-.05em;display:block}
.score .etoiles{justify-content:center;margin:12px 0 8px}.score .etoiles svg{width:30px;height:30px}
.score p{font-size:15.5px;color:#5E4B73;opacity:1}
.mur{columns:3 300px;column-gap:18px;margin-top:22px}
.mur .carte{break-inside:avoid;margin-bottom:18px;display:inline-block;width:100%}
.mur .carte:nth-child(3n+2){background:var(--fond-2);border-color:transparent}
.mur q{quotes:"«\00a0" "\00a0»";display:block;font-size:16.5px;line-height:1.55;margin-top:10px}
.mur cite{display:flex;align-items:center;gap:10px;font-style:normal;font-weight:700;font-size:15px;margin-top:14px}
.mur cite i{width:36px;height:36px;border-radius:50%;background:var(--violet);color:#fff;font:800 16px/36px var(--titre);text-align:center;font-style:normal;flex:none}
.prose{max-width:760px;margin:10px auto 0;font-size:19px;line-height:1.65}
.prose h2{font:800 clamp(26px,2.8vw,34px)/1.12 var(--titre);letter-spacing:-.02em;margin-top:1.6em;text-wrap:balance}
.prose p{margin-top:.8em}
.qr{border-radius:18px;background:var(--fond-2);margin-top:10px;padding:0 20px}
.qr summary{font:700 19px/1.3 var(--titre);padding:16px 34px 16px 0;cursor:pointer;list-style:none;position:relative}
.qr summary::-webkit-details-marker{display:none}
.qr summary::after{content:"+";position:absolute;right:0;top:11px;width:30px;height:30px;border-radius:50%;background:var(--violet);color:#fff;font:700 22px/29px var(--texte);text-align:center;transition:transform .25s}
.qr[open] summary::after{transform:rotate(45deg)}
.qr p{margin:0;padding-bottom:18px;font-size:17.5px}

.plein{grid-column:1/-1!important;text-align:center}
.plein .bouton{margin-inline:auto}
/* pied */
.pied{margin-top:54px;background:#1E0F30;color:#F7F0FB;border-radius:36px 36px 0 0;padding-block:38px 30px}
.pied .g{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr) minmax(0,1fr);gap:24px 40px}
.pied .logo{color:#fff}.pied .logo small{color:#CDBCDA}
.pied p,.pied li{font-size:15.5px;line-height:1.55;color:#CDBCDA}
.pied h3{font:700 16px/1 var(--texte);color:var(--vert);margin-bottom:10px}
.pied li{padding:3px 0}

@media (max-width:980px){
 .couv,.avis-couv{grid-template-columns:1fr}
 .couv .vignette{max-width:420px}
 .bento{grid-template-columns:repeat(2,minmax(0,1fr))}
 .c-art{grid-column:1/-1}.c-conseil,.c-mot,.c-avis,.c-annonce{grid-column:span 1}
 .pied .g{grid-template-columns:1fr 1fr}.pied .g>*:first-child{grid-column:1/-1}
 .barre nav{order:3;width:100%;margin-left:0}
 .barre .ed{margin-left:auto}
}
@media (max-width:640px){
 body{font-size:17px}
 .couv,.avis-couv,.art-couv{border-radius:26px}
 .bento,.apres .bento{grid-template-columns:1fr}
 .c-art,.c-conseil,.c-mot,.c-avis,.c-annonce,.apres .c-conseil,.apres .c-mot,.apres .c-annonce,.apres .c-art{grid-column:1/-1}
 .c-art{grid-template-columns:1fr}.c-art .vignette{max-width:240px;order:-1}
 .texte{font-size:18.5px}
 .pied .g{grid-template-columns:1fr}
 .cta{display:none}
}
@media (prefers-reduced-motion:reduce){.couv .bulle,.art-couv .bulle,.defile .bande,.oeil{animation:none}.carte,.vignette,.bouton,.cta{transition:none}.js .carte.attend{opacity:1;transform:none}html{scroll-behavior:auto}}
'''

JS_PLUS = r'''
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
'''


def lien(ch, r):
    return r + ch + "index.html"


def barre(r, actif=None):
    nav = [("", "À la une", "une"), ("avis-maliboo/", "Avis Maliboo", "avis")]
    liens = "".join(f'<a href="{lien(c, r)}"{" aria-current=\"page\"" if actif == k else ""}>{t}</a>' for c, t, k in nav) + f'<a href="{B.AGENCE}">L\'agence</a>'
    return (f'<div class="lecture" aria-hidden="true"></div><header class="barre"><div class="w"><a class="logo" href="{lien("", r)}">{B.BOO_MINI}<span>Le Mag<small>par Maliboo</small></span></a>'
            f'<nav aria-label="Rubriques">{liens}</nav><button class="ed" type="button" data-edition aria-label="Passer du mode clair au mode sombre"><i class="lune" aria-hidden="true"></i></button>'
            f'<a class="cta" href="{B.AGENCE}agence-seo-resultats-garantis/">Audit gratuit</a></div></header>')


def pied(r):
    return (f'<footer class="pied"><div class="w"><div class="g"><div><a class="logo" href="{lien("", r)}">{B.BOO_MINI}<span>Le Mag<small>par Maliboo</small></span></a>'
            f'<p style="margin-top:14px">Le magazine de l\'agence Maliboo, qui rend les entreprises visibles sur Google et dans les réponses des IA depuis 2007. Deux articles par semaine, un conseil dans chacun.</p>'
            f'<p style="margin-top:8px">Maliboo France SARL, 455 promenade des Anglais, 06200 Nice. {B.TEL}.</p></div>'
            f'<div><h3>Dans le magazine</h3><ul><li><a href="{lien("", r)}">À la une</a></li><li><a href="{lien("avis-maliboo/", r)}">Avis Maliboo</a></li></ul></div>'
            f'<div><h3>Maliboo ailleurs</h3><ul><li><a href="{B.AGENCE}">maliboo-referencement.fr</a></li><li><a href="https://maliboo-ads.fr/">maliboo-ads.fr</a></li></ul></div></div></div></footer>')


def vignette(a):
    return f'<figure class="vignette">{B.dessin(a["rubrique"], "Illustration : " + a["titre"])}</figure>'


def c_conseil(a):
    c = a["conseil"]
    brut = c["titre"] + "\n" + "\n".join(f"{i}. {s}" for i, s in enumerate(c["etapes"], 1)) + "\n(Le Mag Maliboo)"
    return (f'<aside class="carte c-conseil coupon"><span class="etq">Le conseil de la semaine</span><h3>{T(c["titre"])}</h3>'
            f'<ol>{"".join(f"<li><span>{T(s)}</span></li>" for s in c["etapes"])}</ol><button type="button" data-copie="{e(B.typo(brut))}">Copier le conseil</button><span class="ok" role="status"></span></aside>')


def c_mot(a):
    return f'<div class="carte c-mot"><span class="etq">Le mot du jour</span><dfn>{T(a["mot"]["terme"])}</dfn><p>{T(a["mot"]["definition"])}</p></div>'


def c_avis(r):
    p, s, t = B.EXTRAIT
    return (f'<div class="carte c-avis"><span class="etq">Avis des clients</span><div class="gros"><b>{B.NOTE}</b><span>sur 5, {B.NB_AVIS} avis Google</span></div>{B.etoiles()}'
            f'<q>{T(t)}</q><cite>{p}, {s}</cite><a class="lien" href="{lien("avis-maliboo/", r)}">Lire les avis sur Maliboo</a></div>')


def c_annonce(n):
    return (f'<aside class="carte c-annonce"><span class="etq">Avec Maliboo</span><h3>{T(n["titre"])}</h3><p>{T(n["texte"])}</p>'
            f'<a class="bouton" href="{n["lien"]}">{T(n["bouton"])}<i aria-hidden="true"></i></a><span class="tel">ou au {B.TEL}</span></aside>')


def c_art(a, r):
    return (f'<article class="carte c-art"><div><span class="etq">{B.RUB[a["rubrique"]]}</span><h3><a href="{lien(a["slug"] + "/", r)}">{T(a["titre"])}</a></h3><p>{T(a["chapeau"])}</p>'
            f'<span class="lien">Lire l\'article</span></div>{vignette(a)}</article>')


def minutes(a):
    n = sum(len((b.get("p") or b.get("h2") or " ".join(b.get("liste", []))).split()) for b in a["corps"])
    return max(2, round(n / 200))


def page(chemin, titre, corps, principal=False):
    tete = f'<title>{e(titre)}</title><meta name="claude:viewport-fit-sides" content="cover">{POLICES}<style>{CSS}</style>'
    contenu = corps + f"<script>{B.JS}</script><script>{JS_PLUS}</script>"
    doc = tete + contenu if principal else (
        f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">{tete}</head><body>{contenu}</body></html>')
    dest = os.path.join(OUT, chemin, "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w", encoding="utf-8").write(doc)


def construire():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    arts = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(ICI, "articles", "*.json")))]
    arts.sort(key=lambda a: (a["date"], a.get("ordre", 0)), reverse=True)
    une, s = arts[0], arts[1]
    conseils = [a["conseil"]["titre"] for a in arts] + ["Une fiche Google complète", "Répondez à tous vos avis", "Écrivez vos prix sur votre site", "Une page par service, une page par ville",
                                                          "Demandez l'avis le jour même", "Les phrases précises se citent"]
    r = ""
    items = "".join(f"<span>{T(c)}</span>" for c in conseils)
    h = [barre(r, "une"), '<main><div class="w">',
         f'<section class="couv"><i class="bulle b1"></i><i class="bulle b2"></i><i class="bulle b3"></i><div><a class="puce" href="{lien(une["slug"] + "/", r)}">{B.RUB[une["rubrique"]]}</a>'
         f'<h1><a href="{lien(une["slug"] + "/", r)}">{T(une["titre"])}</a></h1><p class="chapeau">{T(une["chapeau"])}</p>'
         f'<div class="actions"><a class="bouton" href="{lien(une["slug"] + "/", r)}">Lire l\'article<i aria-hidden="true"></i></a><span class="temps">{minutes(une)} minutes de lecture, {B.date_fr(une["date"])}</span></div></div>{vignette(une)}</section>',
         f'<div class="defile" aria-hidden="true"><div class="bande"><div style="display:flex">{items}</div><div style="display:flex">{items}</div></div></div>',
         '<div class="entete"><h2>Aussi dans ce numéro</h2></div>',
         f'<div class="bento">{c_art(s, r)}{c_conseil(une)}{c_mot(une)}{c_avis(r)}{c_annonce(une["annonce"])}</div>', "</div></main>", pied(r)]
    page("", "Magazine Maliboo", "".join(h), principal=True)
    r = "../"
    for i, a in enumerate(arts):
        autre = arts[1 - i]
        corps = B.corps_html(a).replace(' class="inter"', "")
        c = [barre(r), '<main><div class="w"><article>',
             f'<header class="art-tete"><span class="puce">{B.RUB[a["rubrique"]]}</span><h1>{T(a["titre"])}</h1><p class="chapeau">{T(a["chapeau"])}</p>'
             f'<p class="meta">{B.date_fr(a["date"]).capitalize()}, par la rédaction Maliboo. {minutes(a)} minutes de lecture.</p></header>',
             f'<div class="art-couv"><i class="bulle b1"></i><i class="bulle b2"></i>{vignette(a)}</div>',
             f'<div class="texte">{corps}</div><div class="bref"><h3>En bref</h3><ul>{"".join(f"<li>{T(x)}</li>" for x in a["enbref"])}</ul></div>',
             f'</article><div class="apres"><div class="bento">{c_conseil(a)}{c_mot(a)}{c_art(autre, r)}{c_annonce(a["annonce"])}</div></div>', "</div></main>", pied(r)]
        page(a["slug"] + "/", a["titre"], "".join(c))
    mur = "".join(f'<div class="carte">{B.etoiles()}<q>{T(t)}</q><cite><i>{p[0]}</i>{p}, {s_}</cite></div>' for p, s_, t in B.AVIS)
    faq = "".join(f'<details class="qr"><summary>{T(q)}</summary><p>{T(rep)}</p></details>' for q, rep in B.FAQ_AVIS)
    n = {"titre": "Faites-vous votre propre avis", "texte": "Un audit gratuit de votre visibilité, sous 24 heures ouvrées : un diagnostic, un plan d'action et un prix. Sans engagement.", "lien": B.AGENCE + "agence-seo-resultats-garantis/", "bouton": "Demander mon audit"}
    c = [barre(r, "avis"), '<main><div class="w">',
         f'<section class="avis-couv"><div><span class="puce">Avis des clients</span><h1>Avis Maliboo : la parole est aux clients</h1>'
         f'<p>{T("Vous cherchez des avis sur Maliboo avant de confier votre référencement à l\'agence ? Voici la note que lui donnent ses clients sur Google, et leurs avis, publiés sans retouche.")}</p></div>'
         f'<div class="score"><b>{B.NOTE}</b>{B.etoiles()}<p>{T(f"sur 5, moyenne de {B.NB_AVIS} avis laissés par les clients de l\'agence sur sa fiche Google.")}</p></div></section>',
         f'<section class="mur">{mur}</section><div class="prose">',
         f'<h2>{T("Avis sur Maliboo référencement : ce qui revient le plus souvent")}</h2>',
         f'<p>{T("À la lecture de ces avis, quatre points reviennent d\'un client à l\'autre. La réactivité de l\'équipe d\'abord, citée dès les premières lignes. La pédagogie ensuite : chaque décision est expliquée, sans jargon. Les résultats, bien sûr, avec des mots-clés arrivés en première page de Google. Et la taille humaine de l\'agence, qui permet de parler directement à la personne qui s\'occupe du dossier.")}</p>',
         f'<h2>{T("Ce que l\'agence Maliboo écrit dans ses contrats")}</h2>',
         f'<p>{T("La plupart des agences expliquent qu\'on ne peut rien garantir en référencement. Maliboo s\'engage par écrit : au moins 30 % des mots-clés choisis avec le client en première page de Google dans l\'année. Si l\'objectif n\'est pas atteint, la prestation est reconduite gratuitement jusqu\'au résultat. En moyenne, 78 % des mots-clés de ses clients sont en première page, et 98,7 % des clients renouvellent leur contrat.")}</p>',
         f'<h2>{T("Vos questions sur les avis Maliboo")}</h2><div style="margin-top:16px">{faq}</div></div>',
         f'<div class="apres"><div class="bento" style="grid-template-columns:1fr">{c_annonce(n).replace("c-annonce", "c-annonce plein")}</div></div>', "</div></main>", pied(r)]
    page("avis-maliboo/", "Avis Maliboo", "".join(c))


if __name__ == "__main__":
    construire()
    print("ok", OUT)
