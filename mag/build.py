# -*- coding: utf-8 -*-
"""Le Mag Maliboo : générateur du site statique (www.referencement-maliboo.com).
Usage : python3 build.py            -> dist/ (site réel, liens en dossiers)
        python3 build.py apercu     -> apercu/ (liens en index.html, CSS et JS dans chaque page)
Un article = un fichier JSON dans articles/. Rien d'autre à modifier pour publier."""
import datetime, glob, html, json, os, re, shutil, sys

ICI = os.path.dirname(os.path.abspath(__file__))
APERCU = len(sys.argv) > 1 and sys.argv[1] == "apercu"
OUT = os.path.join(ICI, "apercu" if APERCU else "dist")
HOTE = "www.referencement-maliboo.com"
DOM = "https://" + HOTE
AGENCE = "https://www.maliboo-referencement.fr/"
BD_EN_LIGNE = False            # passer à True quand referencement-maliboo.fr affiche la BD
BD = "https://referencement-maliboo.fr/"
TEL = "09 72 10 55 55"

RUB = {"ia": "Intelligence artificielle", "avis": "Carte et avis", "google": "Sur Google", "pub": "Publicité", "coulisses": "Coulisses"}
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

CSS = open(os.path.join(ICI, "style.css"), encoding="utf-8").read()
JS = open(os.path.join(ICI, "mag.js"), encoding="utf-8").read()
POLICES = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..800;1,6..72,400..700&family=Sofia+Sans+Extra+Condensed:wght@600;800;900&display=swap">')


def e(t):
    return html.escape(t, quote=True)


def typo(t):
    """Espaces insécables de la typographie française."""
    t = re.sub(r" ([:;?!»])", "\u00a0\\1", t)
    t = t.replace("« ", "«\u00a0")
    t = re.sub(r"(\d) (%|€|h\b|heures|avis|km)", "\\1\u00a0\\2", t)
    return t


def T(t):
    return e(typo(t))


def date_fr(d, jour=True):
    j = datetime.date.fromisoformat(d)
    s = f"{j.day if j.day > 1 else '1er'} {MOIS[j.month - 1]} {j.year}"
    return f"{JOURS[j.weekday()]} {s}" if jour else s


def lien(chemin, r):
    """Lien interne relatif. chemin : '' (accueil), 'avis-maliboo/', 'archives/#ia'..."""
    ancre = ""
    if "#" in chemin:
        chemin, ancre = chemin.split("#", 1)
        ancre = "#" + ancre
    if APERCU:
        return (r + chemin + "index.html" + ancre) if (chemin.endswith("/") or chemin == "") else r + chemin + ancre
    return (r + chemin + ancre) or "./"


# ------------------------------------------------------------------ dessins (deux encres)
TRAME = ('<defs><pattern id="trame" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><circle cx="3.5" cy="3.5" r="1.7" class="tr"/></pattern>'
         '<pattern id="trame2" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><circle cx="2.5" cy="2.5" r=".9" class="tr"/></pattern></defs>')


def boo(x, y, k=1.0):
    """Boo, la loupe de Maliboo."""
    return (f'<g transform="translate({x},{y}) scale({k})"><path d="M-20,22 L-46,50" class="s-enc" stroke-width="15" stroke-linecap="round"/>'
            f'<circle r="40" class="enc"/><circle r="31" class="ver boo"/><circle r="22" class="pap"/>'
            f'<ellipse cx="-8" cy="-4" rx="3.2" ry="5" class="enc oeil"/><ellipse cx="8" cy="-4" rx="3.2" ry="5" class="enc oeil"/>'
            f'<path d="M-8,7 q8,8 16,0" class="s-enc" stroke-width="3" stroke-linecap="round"/></g>')


def etoile(cx, cy, R, cls):
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = R if i % 2 == 0 else R * .42
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" {cls}/>'


def dessin(motif, titre):
    c = {
        "ia": ('<g class="v"><path d="M52,62 h266 a22,22 0 0 1 22,22 v112 a22,22 0 0 1 -22,22 h-150 l-44,42 v-42 h-72 a22,22 0 0 1 -22,-22 v-112 a22,22 0 0 1 22,-22z" class="ver" transform="translate(-14,12)"/></g>'
               '<path d="M52,62 h266 a22,22 0 0 1 22,22 v112 a22,22 0 0 1 -22,22 h-150 l-44,42 v-42 h-72 a22,22 0 0 1 -22,-22 v-112 a22,22 0 0 1 22,-22z" class="pap"/>'
               '<path d="M52,62 h266 a22,22 0 0 1 22,22 v112 a22,22 0 0 1 -22,22 h-150 l-44,42 v-42 h-72 a22,22 0 0 1 -22,-22 v-112 a22,22 0 0 1 22,-22z" class="s-enc" stroke-width="7" stroke-linejoin="round"/>'
               '<rect x="62" y="92" width="190" height="16" fill="url(#trame)"/>'
               '<g class="v"><rect x="62" y="124" width="236" height="26" class="ver"/></g><rect x="74" y="133" width="150" height="8" class="enc"/>'
               '<rect x="62" y="166" width="150" height="16" fill="url(#trame)"/>' + boo(318, 226, 1.05)),
        "avis": ('<g class="v">' + etoile(206, 132, 96, 'class="ver" transform="translate(-14,12)"') + '</g>'
                 + etoile(206, 132, 96, 'fill="url(#trame)"') + etoile(206, 132, 96, 'class="s-enc" stroke-width="7" stroke-linejoin="round"')
                 + "".join(etoile(62 + i * 70, 262, 26, 'class="enc"') for i in range(4))
                 + '<g class="v">' + etoile(342, 262, 26, 'class="ver"') + '</g>' + etoile(342, 262, 26, 'class="s-enc" stroke-width="4" stroke-linejoin="round"')),
        "google": ('<g class="v"><rect x="36" y="46" width="310" height="52" rx="26" class="ver" transform="translate(-12,10)"/></g>'
                   '<rect x="36" y="46" width="310" height="52" rx="26" class="pap"/><rect x="36" y="46" width="310" height="52" rx="26" class="s-enc" stroke-width="7"/>'
                   '<rect x="62" y="66" width="150" height="12" class="enc"/>'
                   '<g class="v"><rect x="36" y="124" width="290" height="40" class="ver"/></g><rect x="50" y="138" width="170" height="12" class="enc"/>'
                   '<rect x="36" y="182" width="250" height="26" fill="url(#trame)"/><rect x="36" y="224" width="270" height="26" fill="url(#trame2)"/><rect x="36" y="266" width="200" height="26" fill="url(#trame2)"/>'
                   + boo(322, 232, 1.05)),
        "pub": ('<g class="v"><path d="M70,120 L250,50 V250 L70,180z" class="ver" transform="translate(-14,12)"/></g>'
                '<path d="M70,120 L250,50 V250 L70,180z" fill="url(#trame)"/><path d="M70,120 L250,50 V250 L70,180z" class="s-enc" stroke-width="7" stroke-linejoin="round"/>'
                '<rect x="34" y="118" width="40" height="64" class="enc"/><path d="M96,186 l18,74 h34 l-16,-64" class="enc"/>'
                '<g class="v"><path d="M282,96 l44,-22 M290,150 h54 M282,204 l44,22" class="s-ver" stroke-width="12" stroke-linecap="round"/></g>'),
        "coulisses": ('<g class="v"><rect x="60" y="50" width="280" height="200" class="ver" transform="translate(-14,12)"/></g>'
                      '<rect x="60" y="50" width="280" height="200" class="pap"/><rect x="60" y="50" width="280" height="200" class="s-enc" stroke-width="7"/>'
                      '<rect x="82" y="74" width="236" height="26" class="enc"/><rect x="82" y="116" width="108" height="112" fill="url(#trame)"/>'
                      '<rect x="206" y="116" width="112" height="10" class="enc"/><rect x="206" y="138" width="112" height="10" fill="url(#trame)"/><rect x="206" y="160" width="112" height="10" fill="url(#trame)"/><rect x="206" y="182" width="80" height="10" fill="url(#trame)"/>'
                      + boo(318, 236, .9)),
    }[motif if motif in ("ia", "avis", "google", "pub", "coulisses") else "google"]
    return f'<svg viewBox="0 0 400 300" role="img" aria-label="{e(titre)}">{TRAME}{c}</svg>'


def etoiles(n=5):
    return '<span class="etoiles" role="img" aria-label="%d étoiles sur 5">%s</span>' % (n, "".join(
        '<svg viewBox="0 0 24 24" aria-hidden="true">' + etoile(12, 12.6, 11, 'class="ver"') + etoile(12, 12.6, 11, 'class="s-enc" stroke-width="1.6" stroke-linejoin="round"') + '</svg>' for _ in range(n)))


BOO_MINI = '<svg viewBox="-52 -46 104 104" aria-hidden="true">' + boo(0, 0, 1) + '</svg>'
FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#14204A"/><rect x="6" y="6" width="52" height="52" fill="#ECEEE4"/>'
           '<text x="32" y="47" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="44" fill="#63D11F" transform="translate(-2,2)">M</text>'
           '<text x="32" y="47" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="44" fill="#14204A">M</text></svg>')

# ------------------------------------------------------------------ avis (publiés sur maliboo-referencement.fr, sans retouche)
AVIS = [
    ("Dorian", "MC Cryolipolyse", "Nous sommes vraiment très satisfaits du travail effectué par l'agence Maliboo autant au niveau du référencement naturel que de la publicité Adwords. On a tout de suite senti un haut niveau d'expertise dans la prise en charge de notre dossier. Ils nous ont positionné en Top 3 sur presque tous nos mots clés importants. Le téléphone n'arrête pas de sonner grâce à vous, Merci !"),
    ("Guillaume", "Deluxe Auto", "Très surprenant ! cela fait plusieurs années que l'on travaille avec cette entreprise de référencement et nous en sommes très satisfaits. Ils sont très réactifs, et surtout ils connaissent parfaitement leur domaine ! Ils sont bien plus compétent que la concurrence avec un prix correct. On recommande !"),
    ("Frédéric", "Réussir son BPJEPS", "J'ai fait appel à Maliboo il y a 2 mois pour améliorer le référencement d'un site internet qui était très mal référencé. Le courant étant très bien passé, l'équipe de Maliboo s'est occupée rapidement d'optimiser le site. En 2 mois, le site est passé de quasi introuvable à numéro 1 sur Google sur le principal mot clé et en première page sur 6 autres mots clés. Incroyable !"),
    ("Pierre-Alain", "Lactalis", "Nous avons trouvé avec Maliboo un référenceur à la fois professionnel et pédagogique dans son approche. Chaque décision est discutée et expliquée clairement, ce qui permet de mieux cerner l’évolution et les résultats de notre site Internet. La taille \"humaine\" de Maliboo nous a permis d’engager des rapports directs, des discussions franches et des prises de décisions rapides, ce qui est indispensable aujourd’hui dans le monde du Web. Notre site Internet apparaît aujourd’hui en 1ère page des mots-clés identifiés initialement et notre trafic est en constante progression."),
    ("Philippe", "Decathlon", "Toute l'équipe Décathlon vous remercie pour vos expertise et votre professionnalisme. Notre stratégie digitale et notre positionnement naturel ont pu ainsi être renforcés grâce à vos conseils et vos actions. Merci encore à Maliboo."),
    ("Philippe", "Hôtel Galion, Flers", "Très bon contact avec l'équipe de Maliboo, résultat rapides et au-delà de mes espérance. Merci pour tout."),
    ("Antonin", "Manapani", "Notre studio dans sa partie web recherchait un partenaire sur lequel s’appuyer pour le référencement de ses sites et particulièrement pour les sites dédiés aux opticiens. L’agence Maliboo par ses conseils, sa disponibilité et compétences, nous a permis de gagner du temps sur le référencement de ces sites. Les résultats de positionnement en référencement naturel ne sont plus a démontrer. Sur quasiment tous les mots clés demandés, les sites se sont retrouvés en première page Google."),
    ("Guillaume", "Amorosart", "Nous avons confié notre référencement à la société Maliboo pour les mots clés les plus concurrentiels, dès que notre site est apparu en première page, notre trafic, déjà important, a bondi de 50%... Un tel gain de trafic s'en ressent immédiatement sur le nombre de contacts que nous obtenons et le nombre de membres qui s'inscrivent sur notre plateforme."),
]
NOTE, NB_AVIS = "4,8", "194"
EXTRAIT = ("Dorian", "MC Cryolipolyse", "Ils nous ont positionné en Top 3 sur presque tous nos mots clés importants. Le téléphone n'arrête pas de sonner grâce à vous, Merci !")

FAQ_AVIS = [
    ("Où lire les avis Google sur Maliboo ?", "Sur la fiche Google de l'agence. Tapez « Maliboo Nice » dans Google ou dans Google Maps : la note et tous les avis s'affichent, avec les réponses de l'agence."),
    ("Les avis publiés sur cette page sont-ils authentiques ?", "Oui. Ce sont des avis rédigés par des clients de Maliboo, repris sans retouche, fautes de frappe comprises, avec le prénom de leur auteur et le nom de son entreprise."),
    ("Maliboo est-elle une agence sérieuse ?", "Maliboo est une agence de référencement installée à Nice, qui accompagne des entreprises depuis 2007 : plus de 1 500 projets confiés, des artisans aux grandes marques. Son engagement de résultat est écrit dans le contrat, ce qui reste rare dans ce métier."),
    ("Que se passe-t-il si les résultats promis ne sont pas atteints ?", "Le contrat de référencement garanti prévoit qu'au moins 30 % des mots-clés choisis ensemble arrivent en première page de Google dans l'année. Si ce n'est pas le cas, la prestation est reconduite gratuitement jusqu'au résultat."),
    ("Comment donner mon avis sur Maliboo ?", "Si vous êtes client, vous pouvez publier votre avis depuis la fiche Google de l'agence. Vous pouvez aussi appeler votre chef de projet au " + TEL + " : un reproche dit de vive voix se règle souvent dans la journée."),
]


# ------------------------------------------------------------------ gabarit
def manchette(r, numero, date, petite=False, actif=None):
    nav = [("", "À la une", "une"), ("archives/", "Tous les articles", "archives"), ("avis-maliboo/", "Avis Maliboo", "avis")]
    liens = "".join(f'<a href="{lien(c, r)}"{" aria-current=\"page\"" if actif == k else ""}>{t}</a>' for c, t, k in nav)
    if BD_EN_LIGNE:
        liens += f'<a href="{BD}">La BD</a>'
    liens += f'<a href="{AGENCE}">L\'agence</a>'
    nom = f'<a class="nom" href="{lien("", r)}" data-t="Le Mag Maliboo">Le Mag Maliboo</a>'
    if petite:
        haut = f'<div class="haut" style="grid-template-columns:1fr">{nom}</div>'
    else:
        haut = (f'<div class="haut"><p class="oreille">{BOO_MINI}<span>Boo cherche, vous trouvez.</span></p>{nom}'
                f'<p class="oreille d"><strong>Prix : gratuit</strong>comme tous les bons conseils</p></div>'
                f'<p class="devise">Le journal de la visibilité sur Google et dans les IA</p>')
    return (f'<header class="manchette{" petite" if petite else ""}"><div class="w">{haut}'
            f'<div class="bandeau"><span>Nice, {date_fr(date)}</span><span>Numéro {numero}</span><span>Paraît le lundi et le jeudi</span>'
            f'<button class="ed" type="button" data-edition aria-label="Changer d\'édition : matin (clair) ou soir (sombre)"><i aria-hidden="true"></i><span>Édition du matin</span></button></div>'
            f'<nav class="rubriques" aria-label="Rubriques">{liens}</nav></div></header>')


def fil(conseils):
    items = "".join(f"<span>{T(c)}</span>" for c in conseils)
    return (f'<div class="fil" role="region" aria-label="Le fil des conseils"><b>Le fil</b><div class="rail"><div class="bande"><div style="display:flex">{items}</div>'
            f'<div style="display:flex" aria-hidden="true">{items}</div></div></div><button type="button" data-pause aria-pressed="false">Pause</button></div>')


def ours(r):
    autres = f'<li><a href="{AGENCE}">maliboo-referencement.fr, le site de l\'agence</a></li><li><a href="https://maliboo-ads.fr/">maliboo-ads.fr, la publicité Google</a></li>'
    if BD_EN_LIGNE:
        autres += f'<li><a href="{BD}">Émilie et Boo, la bande dessinée</a></li>'
    return (f'<footer class="ours"><div class="w"><div class="g"><div><h2>L\'ours</h2>'
            f'<p>Le Mag Maliboo est le journal de l\'agence Maliboo, qui rend les entreprises visibles sur Google et dans les réponses des IA depuis 2007. Deux articles par semaine, un conseil à découper dans chacun.</p>'
            f'<p style="margin-top:10px">Éditeur : Maliboo France SARL, 455 promenade des Anglais, 06200 Nice. Directrice de la publication : Tamara Devos. Rédaction : l\'équipe Maliboo. Téléphone : {TEL}.</p></div>'
            f'<div><h3>Dans le journal</h3><ul><li><a href="{lien("", r)}">À la une</a></li><li><a href="{lien("archives/", r)}">Tous les articles</a></li><li><a href="{lien("avis-maliboo/", r)}">Avis Maliboo</a></li>'
            f'<li><a href="{lien("mentions-legales/", r)}">Mentions légales</a></li><li><a href="{lien("confidentialite/", r)}">Confidentialité</a></li></ul></div>'
            f'<div><h3>Maliboo ailleurs</h3><ul>{autres}</ul></div></div>'
            f'<div class="bas"><span>Le Mag Maliboo, {datetime.date.today().year}</span><span>Imprimé avec deux encres : bleu nuit et vert Boo</span></div></div></footer>')


def page(chemin, titre, desc, corps, r, ld=None, noindex=False, og=None, article=False):
    canon = DOM + "/" + chemin
    dest = os.path.join(OUT, chemin, "index.html") if not chemin.endswith(".html") else os.path.join(OUT, chemin)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if APERCU and chemin == "":
        titre = "Le Mag Maliboo"
    tete = (f'<title>{e(titre)}</title><meta name="claude:viewport-fit-sides" content="cover"><meta name="description" content="{e(desc)}">'
            + ('<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{canon}">')
            + f'<meta property="og:type" content="{"article" if article else "website"}"><meta property="og:site_name" content="Le Mag Maliboo"><meta property="og:locale" content="fr_FR">'
            f'<meta property="og:title" content="{e(titre)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}">'
            + (f'<meta property="og:image" content="{DOM}/{og}"><meta name="twitter:card" content="summary_large_image">' if og else "")
            + f'<link rel="alternate" type="application/rss+xml" title="Le Mag Maliboo" href="{DOM}/flux.xml">'
            + POLICES + ("" if APERCU else f'<link rel="icon" href="{r}favicon.svg" type="image/svg+xml">')
            + (f'<style>{CSS}</style>' if APERCU else f'<link rel="stylesheet" href="{r}assets/mag.css">')
            + (f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""))
    script = f'<script>{JS}</script>' if APERCU else f'<script defer src="{r}assets/mag.js"></script>'
    contenu = f'<a class="evite" href="#contenu">Aller au contenu</a>{corps}{script}'
    if APERCU and chemin == "":
        doc = tete + contenu                      # page principale de l'aperçu : fragment, l'hôte fournit le squelette
    else:
        doc = (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
               f'<meta name="theme-color" content="#14204A">{tete}</head><body>{contenu}</body></html>')
    open(dest, "w", encoding="utf-8").write(doc)
    return len(doc)


def coupon(a, r=""):
    c = a["conseil"]
    brut = c["titre"] + "\n" + "\n".join(f"{i}. {s}" for i, s in enumerate(c["etapes"], 1)) + f"\n(Le Mag Maliboo, {HOTE})"
    return (f'<aside class="coupon" aria-label="Le conseil à découper"><p class="etq">Le conseil à découper</p><h3>{T(c["titre"])}</h3><p>{T(c["texte"])}</p>'
            f'<ol>{"".join(f"<li><span>{T(s)}</span></li>" for s in c["etapes"])}</ol>'
            f'<div class="bas"><button type="button" data-copie="{e(typo(brut))}">Découper et copier</button><span class="ok" role="status"></span></div></aside>')


def annonce(a):
    n = a["annonce"]
    return (f'<aside class="annonce" aria-label="Petite annonce"><p class="etq">Petite annonce</p><h3>{T(n["titre"])}</h3><p>{T(n["texte"])}</p>'
            f'<a class="b" href="{n["lien"]}">{T(n["bouton"])}</a><span class="tel">ou au {TEL}</span></aside>')


def mot(a):
    m = a["mot"]
    return f'<div class="bloc mot"><h3>Le mot du jour</h3><dfn>{T(m["terme"])}</dfn><p>{T(m["definition"])}</p></div>'


def courrier(r):
    p, s, t = EXTRAIT
    return (f'<div class="courrier"><h3>Courrier des lecteurs</h3><div class="lettre">{etoiles()}<q>{T(t)}</q><cite>{p}, {s}</cite></div>'
            f'<div class="note"><b>{NOTE}</b><span>sur 5, moyenne de {NB_AVIS}\u00a0avis laissés par les clients de Maliboo sur Google.</span></div>'
            f'<a class="lire" href="{lien("avis-maliboo/", r)}">Lire les avis sur Maliboo</a></div>')


def corps_html(a):
    o = []
    for b in a["corps"]:
        if "p" in b:
            o.append(f"<p>{T(b['p'])}</p>")
        elif "h2" in b:
            o.append(f'<h2 class="inter">{T(b["h2"])}</h2>')
        elif "liste" in b:
            o.append('<ul class="pts">' + "".join(f"<li><span>{T(x)}</span></li>" for x in b["liste"]) + "</ul>")
        elif "photo" in b:
            o.append(photo_html(a, b))
    return "".join(o)


def photo_html(a, b):
    """Bloc photo : le fichier est dans photos/<slug>/ ; il est copié à côté de la page de l'article."""
    taille = ""
    try:
        from PIL import Image
        with Image.open(os.path.join(ICI, "photos", a["slug"], b["photo"])) as im:
            taille = f' width="{im.width}" height="{im.height}"'
    except Exception:
        pass
    credit = e(b["credit"])
    if b.get("source"):
        credit = f'<a href="{e(b["source"])}" rel="nofollow noopener">{credit}</a>'
    lic = b.get("licence", "")
    if lic and b.get("licence_url"):
        lic = f'<a href="{e(b["licence_url"])}" rel="license nofollow noopener">{e(lic)}</a>'
    else:
        lic = e(lic)
    leg = f"{T(b['legende'])} " if b.get("legende") else ""
    return (f'<figure class="photo"><img src="{e(b["photo"])}" alt="{e(b["alt"])}"{taille} loading="lazy" decoding="async">'
            f'<figcaption>{leg}<span class="credit">Photo\u00a0: {credit}{", " + lic if lic else ""}</span></figcaption></figure>')


def construire():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    arts = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(ICI, "articles", "*.json")))]
    aujourdhui = datetime.date.today().isoformat()
    arts = [a for a in arts if a["date"] <= aujourdhui]                    # un article daté du futur attend son jour
    arts.sort(key=lambda a: (a["date"], a.get("ordre", 0)), reverse=True)
    dates = sorted({a["date"] for a in arts})
    numero = len(dates)
    derniere = dates[-1]
    for a in arts:
        a["num"] = dates.index(a["date"]) + 1
        a["url"] = a["slug"] + "/"
    conseils = [f"{a['conseil']['titre']} : {a['conseil']['etapes'][0]}" for a in arts[:8]] + [
        "Une fiche Google complète, c'est déjà une longueur d'avance.", "Répondez à tous vos avis, même aux plus courts.",
        "Une page par service, une page par ville.", "Écrivez vos prix : vos clients les cherchent, les IA aussi."]
    org = {"@type": "Organization", "@id": DOM + "/#maliboo", "name": "Maliboo", "url": AGENCE, "telephone": "+33972105555",
           "address": {"@type": "PostalAddress", "streetAddress": "455 promenade des Anglais", "postalCode": "06200", "addressLocality": "Nice", "addressCountry": "FR"}}
    tailles = {}

    # ---------------- accueil
    r = ""
    une, reste = arts[0], arts[1:]
    debut = "".join(f"<p>{T(b['p'])}</p>" for b in une["corps"] if "p" in b)[:1] and "".join(f"<p>{T(b['p'])}</p>" for b in [x for x in une["corps"] if "p" in x][:2])
    h = [fil(conseils), manchette(r, numero, derniere, actif="une"), '<main id="contenu"><div class="w">', '<section class="une" aria-label="À la une"><article class="grand">',
         f'<a class="rub" href="{lien("archives/#" + une["rubrique"], r)}">{RUB[une["rubrique"]]}</a>',
         f'<h1 class="titre"><a class="calage" data-t="{T(une["titre"])}" href="{lien(une["url"], r)}">{T(une["titre"])}</a></h1>',
         f'<p class="chapeau">{T(une["chapeau"])}</p>',
         f'<div class="duo"><div class="debut">{debut}<a class="suite" href="{lien(une["url"], r)}">Lire la suite</a></div><figure class="illu">{dessin(une["rubrique"], "Illustration : " + une["titre"])}</figure></div>',
         '</article>', f'<div class="colonne">{coupon(une)}{courrier(r)}</div></section>']
    if reste:
        s = reste[0]
        h.append(f'<section class="rang" aria-label="Aussi dans ce numéro"><article class="second"><div><a class="rub" href="{lien("archives/#" + s["rubrique"], r)}">{RUB[s["rubrique"]]}</a>'
                 f'<h2><a href="{lien(s["url"], r)}">{T(s["titre"])}</a></h2><p>{T(s["chapeau"])}</p><a class="lire" href="{lien(s["url"], r)}">Lire l\'article</a></div>'
                 f'<figure class="illu">{dessin(s["rubrique"], "Illustration : " + s["titre"])}</figure></article>{mot(une)}<div>{annonce(une)}</div></section>')
    else:
        h.append(f'<section class="rang" aria-label="Aussi dans ce numéro">{mot(une)}<div>{annonce(une)}</div></section>')
    if len(reste) > 1:
        h.append('<section class="archives" aria-label="Numéros précédents"><h2>Dans les numéros précédents</h2><ol>' + "".join(
            f'<li><time datetime="{a["date"]}">{date_fr(a["date"], False)}, {RUB[a["rubrique"]].lower()}</time><a href="{lien(a["url"], r)}">{T(a["titre"])}</a></li>' for a in reste[1:7])
            + f'</ol><a class="lire" href="{lien("archives/", r)}">Tous les articles</a></section>')
    h += ["</div></main>", ours(r)]
    ld = {"@context": "https://schema.org", "@graph": [org, {"@type": "WebSite", "@id": DOM + "/#site", "url": DOM + "/", "name": "Le Mag Maliboo", "inLanguage": "fr", "publisher": {"@id": DOM + "/#maliboo"},
          "description": "Le journal de l'agence Maliboo : deux articles par semaine pour être visible sur Google et dans les réponses des IA."}]}
    tailles["/"] = page("", "Le Mag Maliboo : le journal de la visibilité sur Google et dans les IA",
                        "Le journal de l'agence Maliboo. Deux articles par semaine, un conseil à découper dans chacun, pour être visible sur Google, sur Google Maps et dans les réponses des IA.", "".join(h), r, ld)

    # ---------------- articles
    r = "../"
    for i, a in enumerate(arts):
        autre = arts[i + 1] if i + 1 < len(arts) else (arts[0] if i else None)
        fin = f'<div class="fin">{coupon(a)}' + (f'<div class="aussi"><h3>À lire aussi</h3><a href="{lien(autre["url"], r)}">{T(autre["titre"])}</a></div>' if autre else "") + "</div>"
        c = [manchette(r, a["num"], a["date"], petite=True), '<main id="contenu"><div class="w"><article class="article"><header class="tete">',
             f'<p class="meta"><a class="rub" href="{lien("archives/#" + a["rubrique"], r)}">{RUB[a["rubrique"]]}</a><span class="signature"><time datetime="{a["date"]}">{date_fr(a["date"]).capitalize()}</time>, par la rédaction Maliboo</span></p>',
             f'<h1 class="titre calage" data-t="{T(a["titre"])}">{T(a["titre"])}</h1><p class="chapeau">{T(a["chapeau"])}</p></header>',
             f'<div class="texte"><figure class="illu">{dessin(a["rubrique"], "Illustration : " + a["titre"])}</figure>{corps_html(a)}{fin}</div>',
             f'<div class="marge"><div class="bref"><h3>En bref</h3><ul>{"".join(f"<li>{T(x)}</li>" for x in a["enbref"])}</ul></div>{mot(a)}{annonce(a)}{courrier(r)}</div>',
             "</article></div></main>", ours(r)]
        ld = {"@context": "https://schema.org", "@graph": [org, {"@type": "Article", "headline": a["titre"], "description": a["description"], "datePublished": a["date"], "dateModified": a.get("maj", a["date"]),
              "inLanguage": "fr", "articleSection": RUB[a["rubrique"]], "mainEntityOfPage": DOM + "/" + a["url"], "author": {"@id": DOM + "/#maliboo"}, "publisher": {"@id": DOM + "/#maliboo"}},
              {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Le Mag Maliboo", "item": DOM + "/"}, {"@type": "ListItem", "position": 2, "name": a["titre"], "item": DOM + "/" + a["url"]}]}]}
        tailles["/" + a["url"]] = page(a["url"], a.get("titre_seo", a["titre"]) + " | Le Mag Maliboo", a["description"], "".join(c), r, ld, article=True)

    # ---------------- archives
    blocs = []
    for k, nom in RUB.items():
        l = [a for a in arts if a["rubrique"] == k]
        if l:
            blocs.append(f'<section class="archives" id="{k}"><h2>{nom}</h2><ol>' + "".join(
                f'<li><time datetime="{a["date"]}">{date_fr(a["date"], False)}</time><a href="{lien(a["url"], r)}">{T(a["titre"])}</a></li>' for a in l) + "</ol></section>")
    c = [manchette(r, numero, derniere, petite=True, actif="archives"), '<main id="contenu"><div class="w"><div class="prose" style="padding-bottom:10px"><h1>Tous les articles</h1>',
         f'<p>{len(arts)} articles parus, classés par rubrique. Un nouveau numéro paraît chaque lundi et chaque jeudi.</p></div>', "".join(blocs), "</div></main>", ours(r)]
    tailles["/archives/"] = page("archives/", "Tous les articles du Mag Maliboo, classés par rubrique", "Tous les articles du Mag Maliboo : Google, Google Maps et avis, intelligence artificielle, publicité. Deux nouveaux articles par semaine.", "".join(c), r)

    # ---------------- avis Maliboo
    lettres = "".join(f'<div class="lettre">{etoiles()}<q>{T(t)}</q><cite>{p}, {s}</cite></div>' for p, s, t in AVIS)
    faq = "".join(f'<details class="qr"><summary>{T(q)}</summary><p>{T(rep)}</p></details>' for q, rep in FAQ_AVIS)
    n = {"titre": "Faites-vous votre propre avis", "texte": "Un audit gratuit de votre visibilité, sous 24 heures ouvrées : un diagnostic, un plan d'action et un prix. Sans engagement.", "lien": AGENCE + "agence-seo-resultats-garantis/", "bouton": "Demander mon audit"}
    c = [manchette(r, numero, derniere, petite=True, actif="avis"), '<main id="contenu"><div class="w">',
         f'<section class="avis-tete"><div style="display:grid;gap:16px"><span class="rub">Courrier des lecteurs</span><h1 class="titre calage" data-t="Avis Maliboo : la parole est aux clients">Avis Maliboo : la parole est aux clients</h1>'
         f'<p class="chapeau">{T("Vous cherchez des avis sur Maliboo avant de confier votre référencement à l\'agence ? Voici la note que lui donnent ses clients sur Google, et leurs avis, publiés sans retouche.")}</p></div>'
         f'<div class="resultat"><div class="gros"><b>{NOTE}</b><span>sur 5</span></div>{etoiles()}<p>{T(f"Moyenne de {NB_AVIS} avis laissés par les clients de l\'agence sur sa fiche Google. Pour les lire tous, tapez « Maliboo Nice » dans Google.")}</p></div></section>',
         f'<section class="lettres" aria-label="Avis de clients">{lettres}</section>',
         '<div class="avis-tete" style="align-items:start;border-top:5px solid var(--encre)"><div class="prose" style="padding:0">',
         f'<h2 style="margin-top:0">{T("Avis sur Maliboo référencement : ce qui revient le plus souvent")}</h2>',
         f'<p>{T("À la lecture de ces avis, quatre points reviennent d\'un client à l\'autre. La réactivité de l\'équipe d\'abord, citée dès les premières lignes. La pédagogie ensuite : chaque décision est expliquée, sans jargon. Les résultats, bien sûr, avec des mots-clés arrivés en première page de Google. Et la taille humaine de l\'agence, qui permet de parler directement à la personne qui s\'occupe du dossier.")}</p>',
         f'<h2>{T("Ce que l\'agence Maliboo écrit dans ses contrats")}</h2>',
         f'<p>{T("La plupart des agences expliquent qu\'on ne peut rien garantir en référencement. Maliboo s\'engage par écrit : au moins 30 % des mots-clés choisis avec le client en première page de Google dans l\'année. Si l\'objectif n\'est pas atteint, la prestation est reconduite gratuitement jusqu\'au résultat. En moyenne, 78 % des mots-clés de ses clients sont en première page, et 98,7 % des clients renouvellent leur contrat.")}</p>',
         f'<p>{T("Cette garantie porte sur le référencement naturel dans Google. La visibilité dans les réponses des IA est suivie et mesurée chaque mois, sans garantie.")}</p>',
         f'<h2>{T("Vos questions sur les avis Maliboo")}</h2><div style="margin-top:14px;border-bottom:1.5px solid var(--encre)">{faq}</div></div>',
         f'<div style="display:grid;gap:26px">{annonce({"annonce": n})}</div></div>', "</div></main>", ours(r)]
    ld = {"@context": "https://schema.org", "@graph": [org, {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": rep}} for q, rep in FAQ_AVIS]},
          {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Le Mag Maliboo", "item": DOM + "/"}, {"@type": "ListItem", "position": 2, "name": "Avis Maliboo", "item": DOM + "/avis-maliboo/"}]}]}
    tailles["/avis-maliboo/"] = page("avis-maliboo/", f"Avis Maliboo : {NOTE}/5 sur {NB_AVIS} avis Google, les clients de l'agence témoignent",
                                     f"Avis sur Maliboo, agence de référencement à Nice : {NOTE}/5 sur {NB_AVIS} avis Google. Les avis de ses clients publiés sans retouche, la garantie écrite au contrat et les réponses à vos questions.", "".join(c), r, ld)

    # ---------------- pages légales
    ml = (f'<h1>Mentions légales</h1><h2>Éditeur</h2><p>Le site {DOM} est édité par la société <strong>Maliboo France</strong>, SARL au capital social de 40 000 €, immatriculée au RCS de Cannes sous le numéro B 523 492 163 (SIRET 523 492 163 00028, code APE 6201 Z, TVA intracommunautaire FR 38523492163). Marque Maliboo déposée à l\'INPI.</p>'
          f'<p>Siège : Somaf Arénice, 6<sup>e</sup> étage, 455 promenade des Anglais, 06200 Nice. Téléphone : {TEL}.</p><p>Directrice de la publication : Tamara Devos.</p>'
          '<h2>Hébergement</h2><p>__HEBERGEUR__</p>'
          '<h2>Rédaction</h2><p>Les articles sont préparés par l\'équipe Maliboo. Ils donnent des conseils généraux et ne remplacent pas un audit de votre situation.</p>'
          '<h2>Propriété intellectuelle</h2><p>Les textes, les dessins et la mise en page du Mag Maliboo sont la propriété de Maliboo France. Toute reproduction sans autorisation est interdite. Les conseils à découper peuvent être copiés et partagés en citant leur source.</p>'
          '<h2>Avis de clients</h2><p>Les avis reproduits sur ce site ont été rédigés par des clients de Maliboo et sont repris sans retouche.</p>'
          '<h2>Marques</h2><p>Google, Google Maps, Google Ads, Gemini, ChatGPT et Perplexity sont des marques de leurs propriétaires respectifs. Maliboo est une agence indépendante.</p>')
    ml = ml.replace("__HEBERGEUR__", "Le site est hébergé par GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.")
    conf = ('<h1>Confidentialité</h1><h2>Aucun cookie, aucun formulaire</h2><p>Le Mag Maliboo ne dépose aucun cookie de mesure d\'audience ou de publicité et ne contient aucun formulaire. Nous ne recueillons aucune donnée personnelle sur ce site.</p>'
            '<h2>Votre édition</h2><p>Si vous choisissez l\'édition du matin ou l\'édition du soir, ce choix est enregistré dans votre navigateur, sur votre appareil. Il ne nous est pas transmis.</p>'
            '<h2>Hébergeur</h2><p>Comme tout hébergeur, GitHub peut enregistrer l\'adresse IP des visiteurs dans ses journaux techniques, pour assurer la sécurité du service.</p>'
            '<h2>Polices de caractères</h2><p>Les polices du journal sont chargées depuis Google Fonts. Votre navigateur communique pour cela votre adresse IP à Google.</p>'
            f'<h2>Liens vers nos autres sites</h2><p>Les liens vers maliboo-referencement.fr vous mènent au site de l\'agence, qui a sa propre politique de confidentialité.</p><h2>Nous contacter</h2><p>Maliboo France SARL, 455 promenade des Anglais, 06200 Nice. Téléphone : {TEL}.</p>')
    for ch, ti, de, co in [("mentions-legales/", "Mentions légales du Mag Maliboo, le journal de l'agence Maliboo", "Mentions légales du site " + HOTE + ", édité par Maliboo France.", ml),
                           ("confidentialite/", "Confidentialité : le Mag Maliboo ne dépose aucun cookie", "Politique de confidentialité du site " + HOTE + " : aucun cookie, aucun formulaire.", conf)]:
        tailles["/" + ch] = page(ch, ti, de, manchette(r, numero, derniere, petite=True) + f'<main id="contenu"><div class="w"><div class="prose">{typo(co)}</div></div></main>' + ours(r), r)

    if APERCU:
        return tailles
    # ---------------- 404 (liens absolus : la page est servie à n'importe quelle adresse)
    c404 = (manchette("/", numero, derniere, petite=True) + '<main id="contenu"><div class="w"><div class="prose"><h1>Cette page n\'est pas dans le journal</h1>'
            '<p>L\'adresse a changé, ou l\'article n\'existe plus. Le dernier numéro vous attend à la une.</p><p><a class="suite" href="/">Aller à la une</a></p></div></div></main>' + ours("/"))
    page("404.html", "Page introuvable | Le Mag Maliboo", "Cette page n'existe pas ou a été déplacée.", c404, "/", noindex=True)
    # ---------------- fichiers serveur
    open(os.path.join(OUT, "assets", "mag.css"), "w", encoding="utf-8").write(CSS)
    open(os.path.join(OUT, "assets", "mag.js"), "w", encoding="utf-8").write(JS)
    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(FAVICON)
    open(os.path.join(OUT, "CNAME"), "w").write(HOTE + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(
        "# Le Mag Maliboo : ouvert aux moteurs de recherche et aux robots des IA\nUser-agent: *\nAllow: /\n\n"
        + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended", "Bingbot"])
        + f"Sitemap: {DOM}/sitemap.xml\n")
    urls = [("", derniere), ("avis-maliboo/", derniere), ("archives/", derniere)] + [(a["url"], a.get("maj", a["date"])) for a in arts] + [("mentions-legales/", dates[0]), ("confidentialite/", dates[0])]
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{DOM}/{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n")
    def rfc(d):
        return datetime.datetime.fromisoformat(d + "T07:00:00").strftime("%a, %d %b %Y %H:%M:%S +0100")
    open(os.path.join(OUT, "flux.xml"), "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Le Mag Maliboo</title><link>{DOM}/</link><description>Le journal de la visibilité sur Google et dans les IA</description><language>fr</language>\n'
        + "".join(f'<item><title>{e(a["titre"])}</title><link>{DOM}/{a["url"]}</link><guid>{DOM}/{a["url"]}</guid><pubDate>{rfc(a["date"])}</pubDate><description>{e(a["description"])}</description></item>\n' for a in arts[:20])
        + "</channel></rss>\n")
    L = ["# Le Mag Maliboo", "", "> Le journal de l'agence Maliboo : deux articles par semaine (lundi et jeudi) pour aider les entreprises à être visibles sur Google, sur Google Maps et dans les réponses des IA (ChatGPT, Gemini, Perplexity). Chaque article contient un conseil pratique.", "",
         f"Maliboo est une agence de visibilité fondée en 2007 (Nice, France) : référencement Google garanti par contrat (30 % des mots-clés en première page), visibilité dans les IA (GEO), Google Ads, fiche Google. Note de ses clients sur Google : {NOTE}/5 sur {NB_AVIS} avis. Site de l'agence : {AGENCE} . Téléphone : {TEL}.", "",
         "## Pages", "", f"- [Avis Maliboo]({DOM}/avis-maliboo/) : la note de l'agence sur Google et les avis de ses clients, publiés sans retouche.", f"- [Tous les articles]({DOM}/archives/)", "", "## Articles", ""]
    for a in arts:
        L.append(f"- [{a['titre']}]({DOM}/{a['url']}) ({date_fr(a['date'], False)}) : {a['description']} Conseil : {a['conseil']['titre']}.")
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    return tailles


if __name__ == "__main__":
    for k, v in construire().items():
        print(f"{v / 1024:6.0f} Ko  {k}")
