# -*- coding: utf-8 -*-
"""Le Mag Maliboo, version retenue : magazine moderne (charte Maliboo violet et vert).
   python3 mag_b.py           -> apercu-b/ (aperçu : liens en index.html, CSS et JS dans chaque page)
   python3 mag_b.py prod      -> dist/     (site réel : www.referencement-maliboo.com)
   Un article = un fichier JSON dans articles/. Rien d'autre à modifier pour publier."""
import datetime, glob, json, os, shutil, sys
import build as B
import piste_b as P

ICI = os.path.dirname(os.path.abspath(__file__))
PROD = len(sys.argv) > 1 and sys.argv[1] == "prod"
# site réel : dossier docs/ à la racine du dépôt (publié par GitHub Pages) ; aperçu : mag/apercu-b/
OUT = os.path.join(os.path.dirname(ICI), "docs") if PROD else os.path.join(ICI, "apercu-b")
DOM, HOTE, AGENCE, TEL = B.DOM, B.HOTE, B.AGENCE, B.TEL
T, e, typo, RUB = B.T, B.e, B.typo, B.RUB
BD_EN_LIGNE = True
BD = "https://referencement-maliboo.fr/"

AVIS = B.AVIS + [("Ted", "Webcamo.com", "Nous avons confié le référencement de nos sites à la société Maliboo qui, grâce à leur discours professionnel, clair et précis, nous a permis d'avoir un prestataire à la hauteur de nos exigences. Webcamo est le leader de la rencontre par webcam en France, nous ne pouvions choisir une entreprise au hasard. Notre domaine d'activité est un des plus concurrentiels sur Internet et nous observons en permanence l'évolution du positionnement de nos sites même sur les mots clés les plus difficiles à placer. Si vous recherchez un prestataire de référencement vraiment efficace, c'est sans hésitation que je vous conseille Maliboo.")]

CSS_PLUS = r'''
[hidden]{display:none!important}
.evite{position:absolute;left:-999px;top:8px;background:#1E0F30;color:#fff;padding:8px 14px;z-index:99;border-radius:8px}
.evite:focus{left:8px}
.prose.legal{margin-top:34px}
.prose.legal h1{font:800 clamp(34px,4.6vw,56px)/1.05 var(--titre);letter-spacing:-.03em}
/* ---------- logo : Boo en vedette ---------- */
.logo{display:inline-flex;align-items:center;gap:.12em;white-space:nowrap;text-decoration:none;font:800 36px/1 var(--titre);letter-spacing:-.05em;color:var(--encre);padding:4px 0}
.logo svg{width:1.12em;height:1.12em;flex:none;overflow:visible;transform-origin:60% 60%;animation:penche 3.5s ease-in-out infinite alternate}
.logo .anneau{fill:#1E0F30}.logo .manche{stroke:#1E0F30}.logo .verre{fill:#fff}.logo .lentille{fill:#76E02F}
.logo u{text-decoration:none;color:#7A2BC2}
.logo mark{color:inherit;background:linear-gradient(transparent 60%,#76E02F 60% 90%,transparent 90%);padding:0 .06em}
.logo small{display:block;font:700 .3em/1 var(--texte);letter-spacing:0;color:#CDBCDA;margin-top:.5em}
.logo:hover svg{animation-duration:.6s}
:root[data-theme="dark"] .logo u{color:#C9A0F7}
:root[data-theme="dark"] .logo mark{background:linear-gradient(transparent 60%,#4E9A1C 60% 90%,transparent 90%)}
:root[data-theme="dark"] .logo .anneau{fill:#76E02F}:root[data-theme="dark"] .logo .manche{stroke:#55B81E}:root[data-theme="dark"] .logo .lentille{fill:#76E02F}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .logo u{color:#C9A0F7}
 :root:not([data-theme="light"]) .logo mark{background:linear-gradient(transparent 60%,#4E9A1C 60% 90%,transparent 90%)}
 :root:not([data-theme="light"]) .logo .anneau{fill:#76E02F}:root:not([data-theme="light"]) .logo .manche{stroke:#55B81E}}
.logo.grand{font-size:58px;color:#fff}
.logo.grand u{color:#C9A0F7}.logo.grand mark{background:linear-gradient(transparent 60%,#4E9A1C 60% 90%,transparent 90%)}
.logo.grand .anneau{fill:#76E02F}.logo.grand .manche{stroke:#55B81E}
@keyframes penche{0%{transform:rotate(-8deg)}100%{transform:rotate(8deg)}}

/* ---------- articles : cartes et page de tous les articles ---------- */
.grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:18px}
.c-mini{display:grid;gap:10px;align-content:start;padding:18px 18px 22px}
.c-mini .vignette{transform:none;box-shadow:none;background:var(--fond-2);padding:14px 30px;border-radius:18px;margin-bottom:6px;transition:transform .35s}
.c-mini:hover .vignette{transform:scale(1.03)}
.c-mini .etq{margin:0}
.c-mini h3{font-size:clamp(21px,2vw,25px)}
.c-mini p{color:var(--mu);font-size:15.5px}
.filtres{display:flex;gap:8px;flex-wrap:wrap;margin:22px 0 20px}
.filtres button{font-weight:700;font-size:15.5px;padding:9px 16px;border-radius:999px;background:var(--fond-2);transition:background .2s,color .2s}
.filtres button[aria-pressed="true"]{background:var(--violet);color:#fff}
.page-tete{margin:38px 0 6px}
.accueil{margin:22px 0 0;display:flex;align-items:center;gap:22px;padding:20px clamp(18px,3vw,30px);border-radius:28px;background:var(--fond-2);border:1px solid var(--ligne)}
.accueil .pastille{flex:0 0 auto;width:68px;height:68px;border-radius:50%;background:#fff;display:grid;place-items:center;box-shadow:0 0 0 4px var(--vert)}
.accueil .pastille svg{width:46px;height:46px}
.accueil .pastille .anneau{fill:#1E0F30}.accueil .pastille .manche{stroke:#1E0F30}.accueil .pastille .verre{fill:#fff}.accueil .pastille .lentille{fill:#76E02F}
.accueil h2{margin:0 0 4px;font:800 clamp(20px,2.2vw,25px)/1.2 var(--titre);letter-spacing:-.02em;color:var(--encre);text-wrap:balance}
.accueil h2 mark{background:linear-gradient(transparent 58%,var(--vert) 58%);color:inherit;padding:0 .08em}
.accueil p{margin:0;font:400 17px/1.55 var(--texte);color:var(--mu);max-width:62em;text-wrap:pretty}
@media (max-width:600px){.accueil{align-items:flex-start;gap:14px;padding:18px}.accueil .pastille{width:50px;height:50px;box-shadow:0 0 0 3px var(--vert)}.accueil .pastille svg{width:34px;height:34px}}
.page-tete h1{font:800 clamp(36px,5vw,64px)/1.04 var(--titre);letter-spacing:-.03em}
.page-tete p{color:var(--mu);font-size:19px;margin-top:10px;max-width:38em}
.vide{color:var(--mu);padding:20px 0}

/* ---------- pied : la rédaction au travail ---------- */
.pied{padding-block:0 30px;overflow:hidden}
.redac{display:block;width:100%;height:clamp(190px,21vw,270px)}
.pied .legende{font:700 15.5px/1.4 var(--texte);color:#CDBCDA;padding:14px 0 26px;border-bottom:1px solid #3B2552;margin-bottom:30px;display:flex;gap:8px 12px;align-items:center;flex-wrap:wrap}
.pied .legende i{width:10px;height:10px;border-radius:50%;background:#76E02F;animation:voyant 1.4s ease-in-out infinite;flex:none}
.pied .legende b{color:#fff}
@keyframes voyant{50%{opacity:.25}}
.redac .lampe{transform-box:view-box;animation:balance 5s ease-in-out infinite alternate}
.redac .l2{animation-delay:-1.6s}.redac .l3{animation-delay:-3.1s}
@keyframes balance{0%{transform:rotate(-2.2deg)}100%{transform:rotate(2.2deg)}}
.redac .lg{transform-box:fill-box;transform-origin:left center;animation:ecrit 3.6s steps(14,end) infinite}
.redac .lg2{animation-delay:.5s}.redac .lg3{animation-delay:1s}.redac .lg4{animation-delay:1.5s}
@keyframes ecrit{0%{transform:scaleX(0)}55%,100%{transform:scaleX(1)}}
.redac .curseur{animation:voyant .8s steps(1) infinite}
.redac .main{transform-box:fill-box;animation:tape .32s ease-in-out infinite alternate}
.redac .m2{animation-delay:-.16s}.redac .m3{animation-duration:.26s}.redac .m4{animation-duration:.26s;animation-delay:-.13s}.redac .m5{animation-duration:.4s}.redac .m6{animation-duration:.4s;animation-delay:-.2s}
@keyframes tape{0%{transform:translateY(0)}100%{transform:translateY(-5px)}}
.redac .tete{transform-box:fill-box;transform-origin:50% 100%;animation:hoche 3.2s ease-in-out infinite alternate}
.redac .t2{animation-delay:-1.1s}.redac .t3{animation-delay:-2.2s}
@keyframes hoche{0%{transform:rotate(-3deg)}100%{transform:rotate(3deg)}}
.redac .vap{animation:vapeur 2.6s ease-in infinite;opacity:0}
.redac .v2{animation-delay:.9s}.redac .v3{animation-delay:1.7s}
@keyframes vapeur{0%{transform:translateY(0);opacity:0}25%{opacity:.7}100%{transform:translateY(-22px);opacity:0}}
.redac .feuille{transform-box:fill-box;transform-origin:center;animation:envol 4.5s ease-out infinite;opacity:0}
.redac .f2{animation-delay:1.5s}.redac .f3{animation-delay:3s}
@keyframes envol{0%{transform:translate(0,0) rotate(0);opacity:0}8%{opacity:1}70%{opacity:1}100%{transform:translate(-190px,-96px) rotate(-38deg);opacity:0}}
.redac .aig{transform-box:view-box;transform-origin:1090px 62px;animation:tourne 40s linear infinite}
.redac .aig2{animation-duration:480s}
@keyframes tourne{to{transform:rotate(360deg)}}
.redac .coursier{animation:traverse 24s linear infinite}
  .redac .coursier>g{animation:saute .5s ease-in-out infinite alternate}
@keyframes traverse{0%{transform:translateX(-90px)}100%{transform:translateX(1290px)}}
@keyframes saute{0%{transform:translateY(0)}100%{transform:translateY(-7px)}}
.redac .del{animation:voyant 1s steps(1) infinite}
.redac .fil-led{animation:led 16s linear infinite}
@keyframes led{0%{transform:translateX(330px)}100%{transform:translateX(-560px)}}
.redac text{font-family:var(--titre);font-weight:800}
@media (prefers-reduced-motion:reduce){.redac *,.logo svg,.pied .legende i{animation:none!important}.redac .vap,.redac .feuille{opacity:.8}.redac .lg{transform:none}}
@media (max-width:640px){.logo{font-size:31px}.logo.grand{font-size:46px}}
'''

JS_PLUS2 = r'''
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
'''

CSS = P.CSS + CSS_PLUS
JS = B.JS + "\n" + P.JS_PLUS + "\n" + JS_PLUS2
POLICES = P.POLICES


# ------------------------------------------------------------------ dessins
def boo_logo():
    return ('<svg viewBox="-56 -48 108 108" aria-hidden="true"><path class="manche" d="M-22,24 L-46,50" stroke-width="17" stroke-linecap="round" fill="none"/><circle class="anneau" r="42"/><circle class="lentille" r="33"/><circle class="verre" r="23"/>'
            '<ellipse class="oeil" cx="-8" cy="-4" rx="3.6" ry="5.6" fill="#1E0F30"/><ellipse class="oeil" cx="8" cy="-4" rx="3.6" ry="5.6" fill="#1E0F30"/>'
            '<path d="M-8,7 q8,8 16,0" stroke="#1E0F30" stroke-width="3.4" fill="none" stroke-linecap="round"/></svg>')


def logo(r, grand=False):
    sous = "<small>le magazine de Maliboo</small>" if grand else ""
    return (f'<a class="logo{" grand" if grand else ""}" href="{lien("", r)}" aria-label="Le Mag, le magazine de Maliboo : retour à la une">{boo_logo()}'
            f'<span aria-hidden="true"><u>Le</u><mark>Mag</mark>{sous}</span></a>')


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="15" fill="#7A2BC2"/><g transform="translate(35,29) scale(.5)">'
           '<path d="M-22,24 L-46,50" stroke="#1E0F30" stroke-width="17" stroke-linecap="round"/><circle r="42" fill="#1E0F30"/><circle r="33" fill="#76E02F"/><circle r="23" fill="#fff"/>'
           '<ellipse cx="-8" cy="-4" rx="3.6" ry="5.6" fill="#1E0F30"/><ellipse cx="8" cy="-4" rx="3.6" ry="5.6" fill="#1E0F30"/><path d="M-8,7 q8,8 16,0" stroke="#1E0F30" stroke-width="3.4" fill="none" stroke-linecap="round"/></g></svg>')


def redaction():
    """Le pied de page : la rédaction du Mag en plein bouclage."""
    o = ['<svg class="redac" viewBox="0 0 1200 250" preserveAspectRatio="xMidYMax slice" role="img" aria-label="La rédaction du Mag au travail : trois journalistes tapent leurs articles, l\'imprimante sort des pages, Boo court porter une feuille.">',
         '<defs><clipPath id="ledc"><rect x="436" y="30" width="328" height="34" rx="8"/></clipPath></defs>',
         '<rect width="1200" height="250" fill="#1E0F30"/><rect width="1200" height="202" fill="#2A1447"/><rect y="202" width="1200" height="48" fill="#160A26"/>',
         # tableau des unes
         '<rect x="36" y="38" width="170" height="104" rx="10" fill="#3B2163"/>'
         '<g fill="#F7F0FB"><rect x="50" y="52" width="42" height="56" rx="3"/><rect x="100" y="60" width="42" height="56" rx="3" transform="rotate(4 121 88)"/><rect x="150" y="50" width="42" height="56" rx="3" transform="rotate(-3 171 78)"/></g>'
         '<g fill="#7A2BC2"><rect x="55" y="58" width="32" height="7"/><rect x="155" y="57" width="32" height="7" transform="rotate(-3 171 78)"/></g><rect x="105" y="67" width="32" height="7" fill="#76E02F" transform="rotate(4 121 88)"/>'
         '<g fill="#CDBCDA"><rect x="55" y="70" width="32" height="3"/><rect x="55" y="77" width="26" height="3"/><rect x="55" y="84" width="30" height="3"/><rect x="105" y="80" width="32" height="3" transform="rotate(4 121 88)"/><rect x="105" y="87" width="24" height="3" transform="rotate(4 121 88)"/><rect x="155" y="70" width="32" height="3" transform="rotate(-3 171 78)"/><rect x="155" y="77" width="28" height="3" transform="rotate(-3 171 78)"/></g>'
         '<circle cx="71" cy="50" r="4" fill="#FFD84D"/><circle cx="121" cy="58" r="4" fill="#76E02F"/><circle cx="171" cy="48" r="4" fill="#FFD84D"/>',
         # bandeau lumineux
         '<rect x="430" y="24" width="340" height="46" rx="12" fill="#160A26"/><g clip-path="url(#ledc)"><text class="fil-led" data-led x="436" y="54" font-size="19" fill="#76E02F" letter-spacing="1.5">BOUCLAGE EN COURS   •   PROCHAIN NUMÉRO LUNDI ET JEUDI   •   DEUX ARTICLES PAR SEMAINE</text></g>',
         # horloge
         '<circle cx="1090" cy="62" r="32" fill="#160A26"/><circle cx="1090" cy="62" r="27" fill="#F7F0FB"/><path class="aig aig2" d="M1090,62 V46" stroke="#1E0F30" stroke-width="4" stroke-linecap="round"/><path class="aig" d="M1090,62 V40" stroke="#7A2BC2" stroke-width="3" stroke-linecap="round"/><circle cx="1090" cy="62" r="3.5" fill="#1E0F30"/>']
    # lampes
    for i, x in enumerate((330, 620, 910)):
        o.append(f'<g class="lampe l{i+1}" style="transform-origin:{x}px 0px"><path d="M{x},0 V44" stroke="#160A26" stroke-width="3"/><path d="M{x-46},196 L{x-22},70 H{x+22} L{x+46},196 Z" fill="#FFD84D" opacity=".08"/>'
                 f'<path d="M{x-26},70 L{x-13},44 H{x+13} L{x+26},70 Z" fill="#FFD84D"/></g>')
    # bureau
    o.append('<rect x="150" y="178" width="830" height="12" rx="6" fill="#5F2EA3"/><g fill="#3B2163"><rect x="172" y="190" width="10" height="42"/><rect x="560" y="190" width="10" height="42"/><rect x="948" y="190" width="10" height="42"/></g>')
    persos = [("#F2C9A5", "#4A2412", "#76E02F", "court"), ("#C98B62", "#1E0F30", "#FFD84D", "chignon"), ("#F7D7B5", "#B5522D", "#A866EE", "carre")]
    for i, x0 in enumerate((196, 470, 744)):
        peau, cheveux, haut, coiffe = persos[i]
        px = x0 + 166
        ecran = "".join(f'<rect class="lg lg{k+1}" x="{x0+14}" y="{120+k*11}" width="{w}" height="5" rx="2.5" fill="{"#76E02F" if k == 0 else "#7A2BC2"}" style="animation-delay:{i*.7+k*.5:.1f}s"/>' for k, w in enumerate((62, 74, 50, 68)))
        o.append(f'<rect x="{x0}" y="106" width="104" height="66" rx="9" fill="#160A26"/><rect x="{x0+6}" y="112" width="92" height="54" rx="5" fill="#F7F0FB"/>{ecran}'
                 f'<rect class="curseur" x="{x0+86}" y="153" width="4" height="7" fill="#1E0F30"/><rect x="{x0+46}" y="172" width="12" height="8" fill="#160A26"/>')
        # siège, corps, tête
        o.append(f'<rect x="{px-28}" y="124" width="56" height="62" rx="16" fill="#3B2163"/><rect x="{px-23}" y="142" width="46" height="42" rx="17" fill="{haut}"/>')
        tete = f'<circle cx="{px}" cy="121" r="19" fill="{peau}"/>'
        if coiffe == "court":
            tete += f'<path d="M{px-19},119 a19,19 0 0 1 38,0 q-8,-9 -19,-8 q-11,-1 -19,8z" fill="{cheveux}"/>'
        elif coiffe == "chignon":
            tete = f'<circle cx="{px+2}" cy="97" r="9" fill="{cheveux}"/>' + tete + f'<path d="M{px-19},121 a19,19 0 0 1 38,0 q-6,-12 -19,-11 q-13,-1 -19,11z" fill="{cheveux}"/>'
        else:
            tete = f'<path d="M{px-22},136 v-18 a22,22 0 0 1 44,0 v18 q-7,3 -9,-3 h-26 q-2,6 -9,3z" fill="{cheveux}"/>' + tete + f'<path d="M{px-19},118 a19,19 0 0 1 38,0 q-19,-9 -38,0z" fill="{cheveux}"/>'
        tete += f'<circle cx="{px-9}" cy="122" r="2.2" fill="#1E0F30"/><circle cx="{px+3}" cy="122" r="2.2" fill="#1E0F30"/><path d="M{px-8},130 q5,4 10,0" stroke="#1E0F30" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
        o.append(f'<g class="tete t{i+1}">{tete}</g>')
        o.append(f'<rect x="{px-28}" y="172" width="56" height="7" rx="3.5" fill="#F7F0FB"/><circle class="main m{i*2+1}" cx="{px-13}" cy="171" r="6" fill="{peau}"/><circle class="main m{i*2+2}" cx="{px+13}" cy="171" r="6" fill="{peau}"/>')
        # tasse et vapeur
        tx = x0 + 122
        o.append(f'<rect x="{tx}" y="162" width="15" height="16" rx="3" fill="#F7F0FB"/><path d="M{tx+15},166 q7,1 0,8" stroke="#F7F0FB" stroke-width="3" fill="none"/>'
                 + "".join(f'<path class="vap v{k+1}" d="M{tx+4+k*4},158 q-3,-5 0,-9 q3,-4 0,-8" stroke="#CDBCDA" stroke-width="2" fill="none" stroke-linecap="round"/>' for k in range(3)))
    # imprimante et pages qui s'envolent
    o.append('<rect x="1004" y="156" width="150" height="76" rx="9" fill="#3B2163"/><rect x="1016" y="170" width="126" height="6" rx="3" fill="#2A1447"/><rect x="1016" y="196" width="126" height="6" rx="3" fill="#2A1447"/>'
             + "".join(f'<g class="feuille f{k+1}"><rect x="1048" y="96" width="56" height="40" rx="3" fill="#F7F0FB"/><rect x="1054" y="103" width="34" height="6" fill="#7A2BC2"/><rect x="1054" y="114" width="44" height="3" fill="#CDBCDA"/><rect x="1054" y="121" width="38" height="3" fill="#CDBCDA"/></g>' for k in range(3))
             + '<rect x="1014" y="122" width="130" height="38" rx="9" fill="#F7F0FB"/><rect x="1026" y="130" width="106" height="6" rx="3" fill="#160A26"/><circle class="del" cx="1130" cy="148" r="4" fill="#76E02F"/><rect x="1026" y="144" width="40" height="6" rx="3" fill="#CDBCDA"/>')
    # Boo le coursier
    o.append('<g class="coursier"><g><g transform="translate(0,214) scale(.42)"><path d="M-20,22 L-46,50" stroke="#55B81E" stroke-width="15" stroke-linecap="round"/><circle r="40" fill="#76E02F"/><circle r="27" fill="#F7F0FB"/>'
             '<ellipse cx="-2" cy="-4" rx="3.4" ry="5.2" fill="#1E0F30"/><ellipse cx="14" cy="-4" rx="3.4" ry="5.2" fill="#1E0F30"/><path d="M-1,8 q8,7 16,0" stroke="#1E0F30" stroke-width="3.4" fill="none" stroke-linecap="round"/></g>'
             '<g transform="translate(22,196) rotate(12)"><rect width="26" height="20" rx="2" fill="#F7F0FB"/><rect x="4" y="4" width="16" height="4" fill="#7A2BC2"/><rect x="4" y="11" width="18" height="2" fill="#CDBCDA"/></g></g></g>')
    o.append("</svg>")
    return "".join(o)


# ------------------------------------------------------------------ gabarit
def lien(ch, r):
    ancre = ""
    if "#" in ch:
        ch, ancre = ch.split("#", 1)
        ancre = "#" + ancre
    if PROD:
        return (r + ch + ancre) or "./"
    return r + ch + "index.html" + ancre


def barre(r, actif=None):
    nav = [("", "À la une", "une"), ("articles/", "Tous les articles", "articles"), ("avis-maliboo/", "Avis Maliboo", "avis")]
    liens = "".join(f'<a href="{lien(c, r)}"{" aria-current=\"page\"" if actif == k else ""}>{t}</a>' for c, t, k in nav)
    return (f'<a class="evite" href="#contenu">Aller au contenu</a><div class="lecture" aria-hidden="true"></div><header class="barre"><div class="w">{logo(r)}'
            f'<nav aria-label="Rubriques">{liens}</nav><button class="ed" type="button" data-edition aria-label="Passer du mode clair au mode sombre"><i class="lune" aria-hidden="true"></i></button>'
            f'<a class="cta" href="{AGENCE}agence-seo-resultats-garantis/">Audit gratuit</a></div></header>')


def pied(r):
    autres = f'<li><a href="{AGENCE}">maliboo-referencement.fr, le site de l\'agence</a></li><li><a href="https://maliboo-ads.fr/">maliboo-ads.fr, la publicité Google</a></li>'
    if BD_EN_LIGNE:
        autres += f'<li><a href="{BD}">Émilie et Boo, la bande dessinée</a></li>'
    return (f'<footer class="pied">{redaction()}<div class="w"><p class="legende"><i aria-hidden="true"></i><span>Pendant ce temps, à la rédaction : on boucle le prochain numéro. Il paraît <b data-prochain>lundi et jeudi</b>.</span></p>'
            f'<div class="g"><div>{logo(r, grand=True)}<p style="margin-top:20px">Le magazine de l\'agence Maliboo, qui rend les entreprises visibles sur Google et dans les réponses des IA depuis 2007. Deux articles par semaine, un conseil dans chacun.</p>'
            f'<p style="margin-top:8px">Une question ? {TEL}, du lundi au vendredi.</p></div>'
            f'<div><h3>Dans le magazine</h3><ul><li><a href="{lien("", r)}">À la une</a></li><li><a href="{lien("articles/", r)}">Tous les articles</a></li><li><a href="{lien("avis-maliboo/", r)}">Avis Maliboo</a></li>'
            f'<li><a href="{lien("mentions-legales/", r)}">Mentions légales</a></li><li><a href="{lien("confidentialite/", r)}">Confidentialité</a></li></ul></div>'
            f'<div><h3>Maliboo ailleurs</h3><ul>{autres}</ul></div></div></div></footer>')


def page(chemin, titre, desc, corps, r, ld=None, noindex=False, article=False, titre_apercu=None):
    canon = DOM + "/" + chemin
    dest = os.path.join(OUT, chemin) if chemin.endswith(".html") else os.path.join(OUT, chemin, "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if not PROD and chemin == "":
        titre = "Magazine Maliboo"
    tete = (f'<title>{e(titre)}</title><meta name="claude:viewport-fit-sides" content="cover"><meta name="description" content="{e(desc)}">'
            + ('<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{canon}">')
            + f'<meta property="og:type" content="{"article" if article else "website"}"><meta property="og:site_name" content="Le Mag Maliboo"><meta property="og:locale" content="fr_FR">'
            f'<meta property="og:title" content="{e(titre)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}">'
            f'<link rel="alternate" type="application/rss+xml" title="Le Mag Maliboo" href="{DOM}/flux.xml">' + POLICES
            + (f'<link rel="icon" href="{r}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{r}assets/mag.css">' if PROD else f'<style>{CSS}</style>')
            + (f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""))
    contenu = corps + (f'<script defer src="{r}assets/mag.js"></script>' if PROD else f"<script>{JS}</script>")
    if not PROD and chemin == "":
        doc = tete + contenu
    else:
        doc = (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
               f'<meta name="theme-color" content="#7A2BC2">{tete}</head><body>{contenu}</body></html>')
    open(dest, "w", encoding="utf-8").write(doc)
    return len(doc)


def vignette(a):
    return f'<figure class="vignette">{B.dessin(a["rubrique"], "Illustration : " + a["titre"])}</figure>'


def c_art(a, r):
    return (f'<article class="carte c-art"><div><span class="etq">{RUB[a["rubrique"]]}</span><h3><a href="{lien(a["url"], r)}">{T(a["titre"])}</a></h3><p>{T(a["chapeau"])}</p>'
            f'<span class="lien">Lire l\'article</span></div>{vignette(a)}</article>')


def c_mini(a, r):
    return (f'<article class="carte c-mini" data-rub="{a["rubrique"]}">{vignette(a)}<span class="etq">{RUB[a["rubrique"]]}, {B.date_fr(a["date"], False)}</span>'
            f'<h3><a href="{lien(a["url"], r)}">{T(a["titre"])}</a></h3><p>{T(a["description"])}</p></article>')


def c_avis(r):
    p, s, t = B.EXTRAIT
    return (f'<div class="carte c-avis"><span class="etq">Avis des clients</span><div class="gros"><b>{B.NOTE}</b><span>sur 5, {B.NB_AVIS} avis Google</span></div>{B.etoiles()}'
            f'<q>{T(t)}</q><cite>{p}, {s}</cite><a class="lien" href="{lien("avis-maliboo/", r)}">Lire les avis sur Maliboo</a></div>')


def construire():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    arts = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(ICI, "articles", "*.json")))]
    auj = datetime.date.today().isoformat()
    arts = [a for a in arts if a["date"] <= auj]
    arts.sort(key=lambda a: (a["date"], a.get("ordre", 0)), reverse=True)
    for a in arts:
        a["url"] = a["slug"] + "/"
    dates = sorted({a["date"] for a in arts})
    org = {"@type": "Organization", "@id": DOM + "/#maliboo", "name": "Maliboo", "url": AGENCE, "telephone": "+33972105555"}
    conseils = [a["conseil"]["titre"] for a in arts[:6]] + ["Une fiche Google complète", "Répondez à tous vos avis", "Écrivez vos prix sur votre site", "Une page par service, une page par ville",
                                                             "Demandez l'avis le jour même", "Les phrases précises se citent"]
    tailles = {}
    # ---------------- la une
    r = ""
    une, reste = arts[0], arts[1:]
    items = "".join(f"<span>{T(c)}</span>" for c in conseils)
    h = [barre(r, "une"), '<main id="contenu"><div class="w">',
         f'<section class="accueil" aria-label="Présentation du magazine"><span class="pastille">{boo_logo()}</span><div><h2>Bienvenue sur <mark>Le Mag</mark>, le magazine de l’agence Maliboo</h2><p>Chaque lundi et chaque jeudi, un article court et un conseil à appliquer tout de suite pour être mieux trouvé sur Google, sur Google Maps et dans les IA, et pour obtenir plus d’avis clients.</p></div></section>',
         f'<section class="couv"><i class="bulle b1"></i><i class="bulle b2"></i><i class="bulle b3"></i><div><a class="puce" href="{lien("articles/", r)}">{RUB[une["rubrique"]]}</a>'
         f'<h1><a href="{lien(une["url"], r)}">{T(une["titre"])}</a></h1><p class="chapeau">{T(une["chapeau"])}</p>'
         f'<div class="actions"><a class="bouton" href="{lien(une["url"], r)}">Lire l\'article<i aria-hidden="true"></i></a><span class="temps">{P.minutes(une)} minutes de lecture, {B.date_fr(une["date"])}</span></div></div>{vignette(une)}</section>',
         f'<div class="defile" aria-hidden="true"><div class="bande"><div style="display:flex">{items}</div><div style="display:flex">{items}</div></div></div>',
         f'<div class="entete"><h2>Aussi dans ce numéro</h2><a href="{lien("articles/", r)}">Tous les articles</a></div>',
         f'<div class="bento">{c_art(reste[0], r) if reste else ""}{P.c_conseil(une)}{P.c_mot(une)}{c_avis(r)}{P.c_annonce(une["annonce"])}</div>']
    if len(reste) > 1:
        h.append(f'<div class="entete"><h2>Les derniers articles</h2><a href="{lien("articles/", r)}">Tous les articles</a></div><div class="grille">{"".join(c_mini(a, r) for a in reste[1:7])}</div>')
    h += ["</div></main>", pied(r)]
    ld = {"@context": "https://schema.org", "@graph": [org, {"@type": "WebSite", "@id": DOM + "/#site", "url": DOM + "/", "name": "Le Mag Maliboo", "inLanguage": "fr", "publisher": {"@id": DOM + "/#maliboo"}}]}
    tailles["/"] = page("", "Le Mag Maliboo : le magazine de la visibilité sur Google et dans les IA",
                        "Le magazine de l'agence Maliboo. Deux articles par semaine, un conseil dans chacun, pour être visible sur Google, sur Google Maps et dans les réponses des IA.", "".join(h), r, ld)
    # ---------------- articles
    r = "../"
    for i, a in enumerate(arts):
        autre = arts[i + 1] if i + 1 < len(arts) else (arts[0] if i else None)
        corps = B.corps_html(a).replace(' class="inter"', "")
        c = [barre(r), '<main id="contenu"><div class="w"><article>',
             f'<header class="art-tete"><a class="puce" href="{lien("articles/", r)}">{RUB[a["rubrique"]]}</a><h1>{T(a["titre"])}</h1><p class="chapeau">{T(a["chapeau"])}</p>'
             f'<p class="meta"><time datetime="{a["date"]}">{B.date_fr(a["date"]).capitalize()}</time>, par la rédaction Maliboo. {P.minutes(a)} minutes de lecture.</p></header>',
             f'<div class="art-couv"><i class="bulle b1"></i><i class="bulle b2"></i>{vignette(a)}</div>',
             f'<div class="texte">{corps}</div><div class="bref"><h3>En bref</h3><ul>{"".join(f"<li>{T(x)}</li>" for x in a["enbref"])}</ul></div>',
             f'</article><div class="apres"><div class="bento">{P.c_conseil(a)}{P.c_mot(a)}{c_art(autre, r) if autre else ""}{P.c_annonce(a["annonce"])}</div></div>', "</div></main>", pied(r)]
        ld = {"@context": "https://schema.org", "@graph": [org, {"@type": "Article", "headline": a["titre"], "description": a["description"], "datePublished": a["date"], "dateModified": a.get("maj", a["date"]),
              "inLanguage": "fr", "articleSection": RUB[a["rubrique"]], "mainEntityOfPage": DOM + "/" + a["url"], "author": {"@id": DOM + "/#maliboo"}, "publisher": {"@id": DOM + "/#maliboo"}},
              {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Le Mag Maliboo", "item": DOM + "/"}, {"@type": "ListItem", "position": 2, "name": a["titre"], "item": DOM + "/" + a["url"]}]}]}
        tailles["/" + a["url"]] = page(a["url"], a.get("titre_seo", a["titre"]) + " | Le Mag Maliboo", a["description"], "".join(c), r, ld, article=True)
    # ---------------- tous les articles
    rubs = [k for k in RUB if any(a["rubrique"] == k for a in arts)]
    filtres = '<button type="button" data-filtre="tous" aria-pressed="true">Tous</button>' + "".join(f'<button type="button" data-filtre="{k}" aria-pressed="false">{RUB[k]}</button>' for k in rubs)
    c = [barre(r, "articles"), '<main id="contenu"><div class="w">', f'<header class="page-tete"><h1>Tous les articles</h1><p>{len(arts)} articles parus. Un nouveau numéro chaque lundi et chaque jeudi, avec un conseil à appliquer tout de suite.</p></header>',
         f'<div class="filtres" role="group" aria-label="Filtrer par rubrique">{filtres}</div><div class="grille">{"".join(c_mini(a, r) for a in arts)}</div><p class="vide" hidden>Aucun article dans cette rubrique pour le moment.</p>', "</div></main>", pied(r)]
    tailles["/articles/"] = page("articles/", "Tous les articles du Mag Maliboo, classés par rubrique", "Tous les articles du Mag Maliboo : Google, Google Maps et avis, intelligence artificielle, publicité. Deux nouveaux articles par semaine.", "".join(c), r)
    # ---------------- avis
    mur = "".join(f'<div class="carte">{B.etoiles()}<q>{T(t)}</q><cite><i>{p[0]}</i>{p}, {s_}</cite></div>' for p, s_, t in AVIS)
    faq = "".join(f'<details class="qr"><summary>{T(q)}</summary><p>{T(rep)}</p></details>' for q, rep in B.FAQ_AVIS)
    n = {"titre": "Faites-vous votre propre avis", "texte": "Un audit gratuit de votre visibilité, sous 24 heures ouvrées : un diagnostic, un plan d'action et un prix. Sans engagement.", "lien": AGENCE + "agence-seo-resultats-garantis/", "bouton": "Demander mon audit"}
    c = [barre(r, "avis"), '<main id="contenu"><div class="w">',
         f'<section class="avis-couv"><div><span class="puce">Avis des clients</span><h1>Avis Maliboo : la parole est aux clients</h1>'
         f'<p>{T("Vous cherchez des avis sur Maliboo avant de confier votre référencement à l\'agence ? Voici la note que lui donnent ses clients sur Google, et leurs avis, publiés sans retouche.")}</p></div>'
         f'<div class="score"><b>{B.NOTE}</b>{B.etoiles()}<p>{T(f"sur 5, moyenne de {B.NB_AVIS} avis laissés par les clients de l\'agence sur sa fiche Google.")}</p></div></section>',
         f'<section class="mur" aria-label="Avis de clients">{mur}</section><div class="prose">',
         f'<h2>{T("Avis sur Maliboo référencement : ce qui revient le plus souvent")}</h2>',
         f'<p>{T("À la lecture de ces avis, quatre points reviennent d\'un client à l\'autre. La réactivité de l\'équipe d\'abord, citée dès les premières lignes. La pédagogie ensuite : chaque décision est expliquée, sans jargon. Les résultats, bien sûr, avec des mots-clés arrivés en première page de Google. Et la taille humaine de l\'agence, qui permet de parler directement à la personne qui s\'occupe du dossier.")}</p>',
         f'<h2>{T("Ce que l\'agence Maliboo écrit dans ses contrats")}</h2>',
         f'<p>{T("La plupart des agences expliquent qu\'on ne peut rien garantir en référencement. Maliboo s\'engage par écrit : au moins 30 % des mots-clés choisis avec le client en première page de Google dans l\'année. Si l\'objectif n\'est pas atteint, la prestation est reconduite gratuitement jusqu\'au résultat. En moyenne, 78 % des mots-clés de ses clients sont en première page, et 98,7 % des clients renouvellent leur contrat.")}</p>',
         f'<p>{T("Cette garantie porte sur le référencement naturel dans Google. La visibilité dans les réponses des IA est suivie et mesurée chaque mois, sans garantie.")}</p>',
         f'<h2>{T("Vos questions sur les avis Maliboo")}</h2><div style="margin-top:16px">{faq}</div></div>',
         f'<div class="apres"><div class="bento" style="grid-template-columns:1fr">{P.c_annonce(n).replace("c-annonce", "c-annonce plein")}</div></div>', "</div></main>", pied(r)]
    ld = {"@context": "https://schema.org", "@graph": [org, {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": rep}} for q, rep in B.FAQ_AVIS]},
          {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Le Mag Maliboo", "item": DOM + "/"}, {"@type": "ListItem", "position": 2, "name": "Avis Maliboo", "item": DOM + "/avis-maliboo/"}]}]}
    tailles["/avis-maliboo/"] = page("avis-maliboo/", f"Avis Maliboo : {B.NOTE}/5 sur {B.NB_AVIS} avis Google, les clients de l'agence témoignent",
                                     f"Avis sur Maliboo, agence de référencement à Nice : {B.NOTE}/5 sur {B.NB_AVIS} avis Google. Les avis de ses clients publiés sans retouche, la garantie écrite au contrat et les réponses à vos questions.", "".join(c), r, ld)
    # ---------------- pages légales
    ml = (f'<h1>Mentions légales</h1><h2>Éditeur</h2><p>Le site {DOM} est édité par la société <strong>Maliboo France</strong>, SARL au capital social de 40 000 €, immatriculée au RCS de Cannes sous le numéro B 523 492 163 (SIRET 523 492 163 00028, code APE 6201 Z, TVA intracommunautaire FR 38523492163). Marque Maliboo déposée à l\'INPI.</p>'
          f'<p>Siège : Somaf Arénice, 6<sup>e</sup> étage, 455 promenade des Anglais, 06200 Nice. Téléphone : {TEL}.</p><p>Directrice de la publication : Tamara Devos.</p>'
          '<h2>Hébergement</h2><p>Le site est hébergé par GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>'
          '<h2>Contenu</h2><p>Les articles sont préparés par l\'équipe Maliboo. Ils donnent des conseils généraux et ne remplacent pas un audit de votre situation.</p>'
          '<h2>Propriété intellectuelle</h2><p>Les textes, les dessins et la mise en page du Mag Maliboo sont la propriété de Maliboo France. Toute reproduction sans autorisation est interdite. Les conseils peuvent être copiés et partagés en citant leur source.</p>'
          '<h2>Avis de clients</h2><p>Les avis reproduits sur ce site ont été rédigés par des clients de Maliboo et sont repris sans retouche.</p>'
          '<h2>Marques</h2><p>Google, Google Maps, Google Ads, Gemini, ChatGPT et Perplexity sont des marques de leurs propriétaires respectifs. Maliboo est une agence indépendante.</p>')
    conf = ('<h1>Confidentialité</h1><h2>Aucun cookie, aucun formulaire</h2><p>Le Mag Maliboo ne dépose aucun cookie de mesure d\'audience ou de publicité et ne contient aucun formulaire. Nous ne recueillons aucune donnée personnelle sur ce site.</p>'
            '<h2>Mode clair ou sombre</h2><p>Si vous changez de mode d\'affichage, ce choix est enregistré dans votre navigateur, sur votre appareil. Il ne nous est pas transmis.</p>'
            '<h2>Hébergeur</h2><p>Comme tout hébergeur, GitHub peut enregistrer l\'adresse IP des visiteurs dans ses journaux techniques, pour assurer la sécurité du service.</p>'
            '<h2>Polices de caractères</h2><p>Les polices du magazine sont chargées depuis Google Fonts. Votre navigateur communique pour cela votre adresse IP à Google.</p>'
            f'<h2>Liens vers nos autres sites</h2><p>Les liens vers maliboo-referencement.fr vous mènent au site de l\'agence, qui a sa propre politique de confidentialité.</p><h2>Nous contacter</h2><p>Par téléphone au {TEL}, du lundi au vendredi.</p>')
    for ch, ti, de, co in [("mentions-legales/", "Mentions légales du Mag Maliboo, le magazine de l'agence Maliboo", "Mentions légales du site " + HOTE + ", édité par Maliboo France.", ml),
                           ("confidentialite/", "Confidentialité : le Mag Maliboo ne dépose aucun cookie", "Politique de confidentialité du site " + HOTE + " : aucun cookie, aucun formulaire.", conf)]:
        tailles["/" + ch] = page(ch, ti, de, barre(r) + f'<main id="contenu"><div class="w"><div class="prose legal">{typo(co)}</div></div></main>' + pied(r), r)
    if not PROD:
        return tailles
    # ---------------- 404 et fichiers serveur
    c404 = (barre("/") + '<main id="contenu"><div class="w"><header class="page-tete"><h1>Cette page n\'est pas dans le magazine</h1><p>L\'adresse a changé, ou l\'article n\'existe plus. Le dernier numéro vous attend à la une.</p>'
            '<p style="margin-top:22px"><a class="bouton" href="/">Aller à la une<i aria-hidden="true"></i></a></p></header></div></main>' + pied("/"))
    page("404.html", "Page introuvable | Le Mag Maliboo", "Cette page n'existe pas ou a été déplacée.", c404, "/", noindex=True)
    # anciennes adresses du site de 2020 : renvoi vers la une (GitHub Pages ne fait pas de redirection 301)
    for vieux in ("referencement-naturel-site.html", "agence-societe-referencement.html"):
        open(os.path.join(OUT, vieux), "w", encoding="utf-8").write(
            f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Le Mag Maliboo</title><meta name="robots" content="noindex"><link rel="canonical" href="{DOM}/">'
            f'<meta http-equiv="refresh" content="0; url={DOM}/"></head><body><p><a href="{DOM}/">Le Mag Maliboo</a></p></body></html>')
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    open(os.path.join(OUT, "assets", "mag.css"), "w", encoding="utf-8").write(CSS)
    open(os.path.join(OUT, "assets", "mag.js"), "w", encoding="utf-8").write(JS)
    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(FAVICON)
    open(os.path.join(OUT, "CNAME"), "w").write(HOTE + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(
        "# Le Mag Maliboo : ouvert aux moteurs de recherche et aux robots des IA\nUser-agent: *\nAllow: /\n\n"
        + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended", "Bingbot"])
        + f"Sitemap: {DOM}/sitemap.xml\n")
    derniere = dates[-1]
    urls = [("", derniere), ("articles/", derniere), ("avis-maliboo/", derniere)] + [(a["url"], a.get("maj", a["date"])) for a in arts] + [("mentions-legales/", dates[0]), ("confidentialite/", dates[0])]
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{DOM}/{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n")
    rfc = lambda d: datetime.datetime.fromisoformat(d + "T07:00:00").strftime("%a, %d %b %Y %H:%M:%S +0100")
    open(os.path.join(OUT, "flux.xml"), "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Le Mag Maliboo</title><link>{DOM}/</link><description>Le magazine de la visibilité sur Google et dans les IA</description><language>fr</language>\n'
        + "".join(f'<item><title>{e(a["titre"])}</title><link>{DOM}/{a["url"]}</link><guid>{DOM}/{a["url"]}</guid><pubDate>{rfc(a["date"])}</pubDate><description>{e(a["description"])}</description></item>\n' for a in arts[:20])
        + "</channel></rss>\n")
    L = ["# Le Mag Maliboo", "", "> Le magazine de l'agence Maliboo : deux articles par semaine (lundi et jeudi) pour aider les entreprises à être visibles sur Google, sur Google Maps et dans les réponses des IA (ChatGPT, Gemini, Perplexity). Chaque article contient un conseil pratique.", "",
         f"Maliboo est une agence de visibilité fondée en 2007 (Nice, France) : référencement Google garanti par contrat (30 % des mots-clés en première page), visibilité dans les IA (GEO), Google Ads, fiche Google. Note de ses clients sur Google : {B.NOTE}/5 sur {B.NB_AVIS} avis. Site de l'agence : {AGENCE} . Téléphone : {TEL}.", "",
         "## Pages", "", f"- [Avis Maliboo]({DOM}/avis-maliboo/) : la note de l'agence sur Google et les avis de ses clients, publiés sans retouche.", f"- [Tous les articles]({DOM}/articles/)", "", "## Articles", ""]
    L += [f"- [{a['titre']}]({DOM}/{a['url']}) ({B.date_fr(a['date'], False)}) : {a['description']} Conseil : {a['conseil']['titre']}." for a in arts]
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    return tailles


if __name__ == "__main__":
    for k, v in construire().items():
        print(f"{v / 1024:6.0f} Ko  {k}")
