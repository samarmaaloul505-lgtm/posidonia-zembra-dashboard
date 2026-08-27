import pandas as pd
import plotly.express as px
import streamlit as st
import os
import zipfile
import io


def create_zip_download(files_dict):
    """files_dict: {filename: DataFrame or string content}"""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        for filename, content in files_dict.items():
            if isinstance(content, pd.DataFrame):
                zf.writestr(filename, content.to_csv(index=False))
            else:
                zf.writestr(filename, content)
    buffer.seek(0)
    return buffer

st.set_page_config(page_title="Posidonia oceanica - Zembra", layout="wide")
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import LoginError
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
# ============================================================
# Translator section and dictionnary
# ============================================================
if "language" not in st.session_state:
    st.session_state.language = "English"

st.session_state.language = st.sidebar.radio("🌐 Language / Langue", ["English", "Français"])
lang = st.session_state.language
T = {
    "title": {
        "English": "Posidonia oceanica monitoring - South Zembra",
        "Français": "Suivi de la Posidonia oceanica - Sud de Zembra"
    },
    "caption": {
        "English": "Association field data dashboard",
        "Français": "Tableau de bord des données de terrain de l'association"
    },
    "tab_overview": {
        "English": "Overview",
        "Français": "Aperçu"
    },
    "tab_stations": {
        "English": "Stations & Charts",
        "Français": "Stations et graphiques"
    },
    "tab_invasive": {
        "English": "Invasive Species",
        "Français": "Espèces invasives"
    },
    "tab_satellite": {
        "English": "Satellite Imagery",
        "Français": "Imagerie satellite"
    },
    "tab_submit": {
        "English": "Submit Mission Data",
        "Français": "Soumettre des données de mission"
    },
    "tab_methodology": {
        "English": "Methodology & Sources",
        "Français": "Méthodologie et sources"
    },
    "tab_gallery": {
        "English": "Photo Gallery",
        "Français": "Galerie photo"
    },
    "overview_intro": {
        "English": """
The Zembra archipelago sits at the eastern end of the Gulf of Tunis, facing the coast 
of Sidi Daoud, off the tip of Cap Bon. It's made up of five islets: the main island of 
Zembra, the smaller Zembretta, and three tiny outcrops — Lantorcho, La Cathédrale, and 
Zembrettina. Zembra itself rises to about 500m and covers roughly 400 hectares, with 
about 10km of coastline. It sits 13km from Ras El Hmar, 15km from Sidi Daoud, and 
55km from La Goulette (Tunis).
""",
        "Français": """
L'archipel de Zembra se situe à l'extrémité orientale du golfe de Tunis, face à la 
côte de Sidi Daoud, à la pointe du Cap Bon. Il se compose de cinq îlots : l'île 
principale de Zembra, la plus petite Zembretta, ainsi que trois affleurements — 
Lantorcho, La Cathédrale et Zembrettina. Zembra culmine à environ 500m et s'étend 
sur près de 400 hectares, avec environ 10km de littoral. Elle se trouve à 13km de 
Ras El Hmar, 15km de Sidi Daoud et 55km de La Goulette (Tunis).
"""
    },
    "overview_protection_header": {
        "English": "A protected area since 1973",
        "Français": "Une zone protégée depuis 1973"
    },
    "overview_protection": {
        "English": """
Zembra has one of the longest conservation histories in Tunisia:

- **1973** — declared a fully protected biological zone (1.5 nautical miles) by 
  ministerial decree
- **1977** — listed as a UNESCO Biosphere Reserve, and became Tunisia's first-ever 
  National Park (Zembra and Zembretta National Park)
- **2001** — designated a Specially Protected Area of Mediterranean Importance (ASPIM) 
  under the Barcelona Convention, and classified as an Important Bird Area
- **2020** — a co-management unit was established between APAL and ASPEN, funded by 
  The MedFund, to actively manage the marine and coastal protected area (AMCP)
""",
        "Français": """
Zembra possède l'un des plus longs historiques de conservation en Tunisie :

- **1973** — déclarée zone de protection biologique intégrale (1,5 mille marin) par 
  arrêté ministériel
- **1977** — inscrite comme Réserve de Biosphère par l'UNESCO, et devient le tout 
  premier Parc National de Tunisie (Parc National de Zembra et Zembretta)
- **2001** — désignée Aire Spécialement Protégée d'Importance Méditerranéenne (ASPIM) 
  au titre de la Convention de Barcelone, et classée Zone Importante pour la 
  Conservation des Oiseaux
- **2020** — une unité de cogestion est mise en place entre l'APAL et l'ASPEN, 
  financée par The MedFund, pour gérer activement l'aire marine et côtière 
  protégée (AMCP)
"""},
    "overview_why_header": {
        "English": "Why Zembra matters",
        "Français": "Pourquoi Zembra est importante"
    },
    "overview_why": {
        "English": """
Zembra's ecological value goes well beyond its seagrass meadows. The island hosts the 
**largest breeding colony of Scopoli's shearwater in the world** — a Mediterranean 
seabird considered vulnerable in Europe — with over 140,000 breeding pairs recorded. 
It's also a key stopover point for migratory birds crossing the Strait of Sicily 
between Europe and Africa, a route comparable in importance to Gibraltar or the 
Bosphorus for bird migration.

Underwater, the island's marine environment supports a diverse mix of Mediterranean 
species — groupers, dolphins, moray eels, sea turtles — alongside the *Posidonia 
oceanica* meadows this dashboard focuses on.
""",
        "Français": """
La valeur écologique de Zembra dépasse largement ses herbiers de posidonie. L'île 
abrite la **plus grande colonie de reproduction de Puffin de Scopoli au monde** — 
un oiseau marin méditerranéen considéré comme vulnérable en Europe — avec plus de 
140 000 couples nicheurs recensés. Elle constitue également une étape clé pour les 
oiseaux migrateurs traversant le détroit de Sicile entre l'Europe et l'Afrique, une 
voie de migration comparable en importance à Gibraltar ou au Bosphore.

Sous l'eau, le milieu marin de l'île abrite une biodiversité méditerranéenne variée 
— mérous, dauphins, murènes, tortues marines — aux côtés des herbiers de *Posidonia 
oceanica* qui font l'objet de ce tableau de bord.
"""
    },
    "overview_stations_header": {
        "English": "About the monitoring points",
        "Français": "À propos des points de suivi"
    },
    "overview_stations": {
        "English": """
Four stations were established along the meadow's upper limit (2–3m depth), 
except Station 4, located at a shallower reef (0.5–1m) inside the port. 
Each station combines quadrat counts (density, cover) with rhizome/leaf 
dissection (phenology) to assess meadow health.
""",
        "Français": """
Quatre stations ont été établies le long de la limite supérieure de l'herbier 
(profondeur de 2 à 3m), à l'exception de la Station 4, située sur un récif moins 
profond (0,5 à 1m) à l'intérieur du port. Chaque station combine des comptages 
au quadrat (densité, recouvrement) et une dissection des rhizomes/feuilles 
(phénologie) pour évaluer la santé de l'herbier.
"""
    },
    "glossary_header": {
        "English": "📖 Glossary of terms",
        "Français": "📖 Glossaire des termes"
    },
    "glossary_body": {
        "English": """
- **Déchaussement**: how much of the rhizome (the plant's horizontal root-like 
  stem) sits exposed above the sediment rather than buried. More exposure means 
  more vulnerability to storms, currents, and anchoring.
- **Coefficient A**: the percentage of leaves with a broken or grazed tip — used 
  to gauge how much stress a station is under from grazing (fish, urchins) versus 
  physical wave/current action.
- **Leaf Area Index (LAI)**: total leaf surface area per square meter of seafloor 
  — a single number combining shoot density, leaf count, and leaf size to reflect 
  overall meadow "leafiness."
- **Phenology**: the study of a plant's cyclical characteristics — here, leaf and 
  rhizome measurements used to assess the meadow's vitality.
- **Giraud (1977) classification**: ranks meadow density on an absolute scale, 
  regardless of depth.
- **Pergent (1995) classification**: ranks meadow density relative to what's 
  expected at that specific depth, since density naturally decreases with depth.
- **Balises**: the physical, numbered markers placed underwater to permanently 
  mark a station's location for future re-surveying.
""",
        "Français": """
- **Déchaussement** : la portion du rhizome (la tige horizontale de la plante, 
  semblable à une racine) qui reste exposée au-dessus du sédiment plutôt 
  qu'enfouie. Une exposition plus importante signifie une vulnérabilité accrue 
  face aux tempêtes, aux courants et à l'ancrage.
- **Coefficient A** : le pourcentage de feuilles dont l'extrémité est cassée ou 
  broutée — utilisé pour évaluer le stress subi par une station, qu'il soit dû 
  au broutage (poissons, oursins) ou à l'action physique des vagues/courants.
- **Indice foliaire (LAI)** : la surface foliaire totale par mètre carré de 
  fond marin — un chiffre unique combinant la densité des faisceaux, le nombre 
  de feuilles et leur taille pour refléter la "feuillure" globale de l'herbier.
- **Phénologie** : l'étude des caractéristiques cycliques d'une plante — ici, 
  les mesures des feuilles et rhizomes utilisées pour évaluer la vitalité de 
  l'herbier.
- **Classification de Giraud (1977)** : classe la densité de l'herbier sur une 
  échelle absolue, indépendamment de la profondeur.
- **Classification de Pergent (1995)** : classe la densité de l'herbier par 
  rapport à ce qui est attendu à cette profondeur précise, car la densité 
  diminue naturellement avec la profondeur.
- **Balises** : les marqueurs physiques numérotés placés sous l'eau pour 
  repérer durablement l'emplacement d'une station en vue de futurs suivis.
"""
    },
    "raw_data_header": {
        "English": "Raw data check",
        "Français": "Vérification des données brutes"
    },
    "classification_header": {
        "English": "Meadow classification",
        "Français": "Classification de l'herbier"
    },
    "classification_intro": {
        "English": """
Density can be read two ways: Giraud (1977) classifies density on an absolute 
scale, while Pergent (1995) adjusts expectations by depth — since natural density 
tends to be higher in shallow water. A meadow can be "dense" by one scale and 
"mediocre" by the other, which is exactly what shows up here.
""",
        "Français": """
La densité peut être interprétée de deux façons : Giraud (1977) la classe sur 
une échelle absolue, tandis que Pergent (1995) ajuste les attentes selon la 
profondeur — la densité naturelle étant généralement plus élevée en eau peu 
profonde. Un herbier peut donc être "dense" selon une échelle et "médiocre" 
selon l'autre, ce qui est exactement ce qu'on observe ici.
"""
    },
    "summary_header": {
        "English": "Summary",
        "Français": "Résumé"
    },
    "summary_body": {
        "English": """
**What the data shows.** The August 2022 survey found a continuous, structurally sound 
*Posidonia oceanica* meadow along the upper limit (2–3m) of south Zembra, with shoot 
densities of 434–516 shoots/m² across four stations. Under Giraud's (1977) absolute scale, 
this qualifies as "dense" — but under Pergent's (1995) depth-adjusted scale, the same 
densities read as "mediocre," since much higher densities are expected this close to the 
surface. Both readings are correct; they're just answering different questions; the meadow 
is objectively substantial, but arguably underperforming for its depth.

**Points of note.** Station 2 stands out — lower cover (50%, versus full cover at S1 and S3) 
and the presence of the invasive alga *Caulerpa taxifolia* — likely tied to its rockier 
substrate rather than the invasive species itself, but worth monitoring going forward. 
Station 1 shows the highest rhizome exposure (déchaussement), making it the most physically 
vulnerable to wave action and anchoring. Leaf damage at Station 3 is driven mainly by fish 
grazing rather than hydrodynamics, unlike the other three stations — a different kind of 
pressure worth tracking separately.

**Limitations.** This is a single time point from a single mission — it establishes a 
baseline, not a trend. None of the current stations extend past 3m, so the meadow's lower 
limit (previously estimated at 22–30m) remains uncharacterized in this dataset.

**Next steps.** The 2022 mission's own recommendations — echoed here — call for relocating 
the permanent transect markers, adding stations at 15m and at the lower limit (~30m), and 
establishing permanent quadrats specifically to track *Caulerpa taxifolia*'s spread. The 
planned 2026 deep mission is the opportunity to act on these, and would turn this dataset 
from a single snapshot into the start of an actual time series.
""",
        "Français": """
**Ce que montrent les données.** L'étude d'août 2022 a révélé un herbier de *Posidonia 
oceanica* continu et structurellement sain le long de la limite supérieure (2-3m) du sud 
de Zembra, avec des densités de 434 à 516 faisceaux/m² sur les quatre stations. Selon 
l'échelle absolue de Giraud (1977), cela correspond à un herbier "dense" — mais selon 
l'échelle ajustée par la profondeur de Pergent (1995), ces mêmes densités sont qualifiées 
de "médiocres", des densités bien plus élevées étant attendues si près de la surface. Les 
deux lectures sont correctes ; elles répondent simplement à des questions différentes : 
l'herbier est objectivement conséquent, mais probablement en dessous de son potentiel 
pour cette profondeur.

**Points à noter.** La Station 2 se distingue — recouvrement plus faible (50 %, contre un 
recouvrement total aux Stations 1 et 3) et présence de l'algue invasive *Caulerpa 
taxifolia* — probablement lié à son substrat plus rocheux plutôt qu'à l'espèce invasive 
elle-même, mais à surveiller. La Station 1 présente le déchaussement le plus élevé, la 
rendant la plus vulnérable physiquement à l'action des vagues et à l'ancrage. Les 
dommages foliaires à la Station 3 sont principalement dus au broutage par les poissons 
plutôt qu'à l'hydrodynamisme, contrairement aux trois autres stations — une pression 
différente qui mérite un suivi distinct.

**Limites.** Il s'agit d'un point temporel unique issu d'une seule mission — cela établit 
une référence, pas une tendance. Aucune des stations actuelles ne dépasse 3m de 
profondeur, la limite inférieure de l'herbier (estimée précédemment à 22-30m) reste donc 
non caractérisée dans ce jeu de données.

**Prochaines étapes.** Les recommandations de la mission de 2022 — reprises ici — 
appellent à relocaliser les balises permanentes, ajouter des stations à 15m et à la 
limite inférieure (~30m), et mettre en place des quadrats permanents pour suivre 
spécifiquement la propagation de *Caulerpa taxifolia*. La mission profonde prévue pour 
2026 est l'occasion d'agir sur ces recommandations, et transformerait ce jeu de données 
d'un simple instantané en un véritable suivi temporel.
"""
    },
    "chart_map_header": {
        "English": "Station locations",
        "Français": "Emplacement des stations"
    },
    "chart_map_title": {
        "English": "Monitoring stations - south Zembra",
        "Français": "Stations de suivi - sud de Zembra"
    },
        "chart_map_interp": {
        "English": """Stations 1, 2, and 3 sit along the meadow's upper limit at 2–3m, 
spread along the coastline south of the port, while Station 4 sits apart — inside the 
port itself, on the shallow ancient reef barrier (0.5–1m). This spatial split matters: 
S4 isn't really a fourth point on the same transect, it's a separate, shallower habitat 
that happens to be monitored alongside the others because of the reef's ecological and 
historical value.""",
        "Français": """Les stations 1, 2 et 3 se trouvent le long de la limite supérieure 
de l'herbier, à 2-3m de profondeur, réparties le long du littoral au sud du port, tandis 
que la Station 4 se trouve à part — à l'intérieur même du port, sur l'ancien récif barrière 
peu profond (0,5-1m). Cette répartition spatiale est importante : S4 n'est pas vraiment un 
quatrième point sur le même transect, mais un habitat distinct et moins profond, suivi aux 
côtés des autres en raison de la valeur écologique et patrimoniale du récif."""
    },
    "chart_cover_header": {
        "English": "Meadow cover",
        "Français": "Recouvrement de l'herbier"
    },
    "chart_cover_title": {
        "English": "Percentage of seafloor covered by living Posidonia",
        "Français": "Pourcentage du fond marin recouvert par la posidonie vivante"
    },
    "chart_cover_interp": {
        "English": """Cover is uniform and complete at S1 and S3 (100%), but drops sharply 
at S2 (50%). This isn't a sign of meadow dieback — the 2022 report attributes it to S2 
sitting on broken, rocky substrate rather than continuous sand, which naturally limits 
how much of the seafloor Posidonia can colonize. It's also the same station where 
*Caulerpa taxifolia* was recorded, which is worth continuing to monitor, though the 
report notes no clear sign yet that the invasive alga is displacing the meadow there.""",
        "Français": """Le recouvrement est uniforme et total à S1 et S3 (100 %), mais chute 
fortement à S2 (50 %). Cela ne traduit pas un dépérissement de l'herbier — le rapport de 
2022 attribue cela au substrat rocheux et fragmenté de S2, plutôt qu'à du sable continu, ce 
qui limite naturellement la surface colonisable par la posidonie. C'est également la station 
où *Caulerpa taxifolia* a été observée, ce qui mérite un suivi continu, bien que le rapport 
ne signale pour l'instant aucun signe clair de déplacement de l'herbier par l'algue 
invasive."""
    },
    "chart_coeffa_header": {
        "English": "Leaf damage — cause breakdown",
        "Français": "Dommages foliaires — répartition des causes"
    },
    "chart_coeffa_title": {
        "English": "Coefficient A: cause of leaf tip loss by station",
        "Français": "Coefficient A : cause de la perte d'apex foliaire par station"
    },
    "chart_coeffa_interp": {
        "English": """Damage is high everywhere (54–77% of leaves show tip loss), but the 
*cause* differs by station. At S1, S2, and S4, most damage comes from hydrodynamic stress 
— wave and current action tearing leaf tips, consistent with their exposed position along 
the coast. Station 3 breaks that pattern: less than 40% of its damage is hydrodynamic, 
while grazing accounts for the rest, and nearly half of all leaf damage there comes 
specifically from saupe fish. That points to biological grazing pressure as the dominant 
factor at S3, not physical exposure — a genuinely different stressor from the other three 
stations.""",
        "Français": """Les dommages sont élevés partout (54 à 77 % des feuilles présentent 
une perte d'apex), mais la *cause* diffère selon la station. À S1, S2 et S4, la majorité des 
dommages provient du stress hydrodynamique — l'action des vagues et des courants arrachant 
les extrémités des feuilles, cohérent avec leur position exposée le long du littoral. La 
Station 3 rompt ce schéma : moins de 40 % de ses dommages sont d'origine hydrodynamique, le 
reste étant dû au broutage, dont près de la moitié imputable spécifiquement à la saupe. Cela 
indique que la pression de broutage biologique domine à S3, plutôt que l'exposition 
physique — un stress d'une nature réellement différente des trois autres stations."""
    },
    "chart_lai_header": {
        "English": "Leaf area vs. depth",
        "Français": "Surface foliaire en fonction de la profondeur"
    },
    "chart_lai_title": {
        "English": "Leaf Area Index by depth",
        "Français": "Indice foliaire selon la profondeur"
    },
    "chart_lai_interp": {
        "English": """Leaf Area Index drops sharply at S4 (3.7 m²/m²) compared to S1, S2, 
and S3 (7.4–11.6 m²/m²) — but S4 is also the shallowest station by far (0.5–1m vs. 2–3m). 
This is consistent with what's expected physically: less water column means less light 
buffering and more wave exposure, both of which limit leaf growth. With only four points 
this isn't a statistically provable trend, but it's a pattern the 2026 deep-water stations 
(15m and ~30m) will be able to test properly — plotting the same relationship across a 
much wider depth range.""",
        "Français": """L'indice foliaire chute fortement à S4 (3,7 m²/m²) par rapport à S1, 
S2 et S3 (7,4 à 11,6 m²/m²) — mais S4 est également de loin la station la moins profonde 
(0,5-1m contre 2-3m). Cela correspond à ce qui est physiquement attendu : une colonne d'eau 
plus faible signifie moins d'atténuation lumineuse mais une exposition aux vagues accrue, 
deux facteurs qui limitent la croissance foliaire. Avec seulement quatre points, il ne 
s'agit pas d'une tendance statistiquement démontrable, mais c'est un schéma que les futures 
stations profondes de 2026 (15m et ~30m) permettront de tester correctement — en traçant la 
même relation sur une plage de profondeur bien plus large."""
    },

    "chart_radar_header": {
        "English": "Density profile (all stations)",
        "Français": "Profil de densité (toutes les stations)"
    },
    "chart_radar_title": {
        "English": "Shoot density - station comparison",
        "Français": "Densité des faisceaux - comparaison des stations"
    },
    "chart_radar_interp": {
        "English": """The four stations form a fairly balanced shape rather than one 
station dramatically outperforming the others — densities range narrowly between 
434 and 516 shoots/m². S1 is the clear high point of the four, but the overall picture 
is one of a consistent meadow across the surveyed area, not a site with one obviously 
strong or weak station.""",
        "Français": """Les quatre stations forment une figure relativement équilibrée, sans 
qu'une station ne se démarque nettement des autres — les densités varient dans une 
fourchette étroite, entre 434 et 516 faisceaux/m². S1 constitue clairement le point le plus 
élevé des quatre, mais l'image globale est celle d'un herbier cohérent sur l'ensemble de la 
zone étudiée, plutôt qu'un site avec une station manifestement forte ou faible."""
    },
    "chart_error_header": {
        "English": "Shoot density with uncertainty",
        "Français": "Densité des faisceaux avec incertitude"
    },
    "chart_error_title": {
        "English": "Shoot density ± standard error",
        "Français": "Densité des faisceaux ± erreur standard"
    },
    "chart_error_interp": {
        "English": """Once the error bars (±SE) are included, S2, S3, and S4 overlap 
almost entirely — their density estimates aren't meaningfully distinguishable from 
each other given the natural variability in the quadrat counts. S1 sits noticeably 
higher and its error range doesn't overlap with S4's, so that difference looks real. 
In short: S1 stands out, but treating S2/S3/S4 as three different density "tiers" 
would be overstating what the data actually supports.""",
        "Français": """En intégrant les barres d'erreur (± erreur standard), S2, S3 et S4 se 
chevauchent presque entièrement — leurs estimations de densité ne sont pas réellement 
distinguables les unes des autres compte tenu de la variabilité naturelle des comptages au 
quadrat. S1 se situe nettement plus haut, et sa plage d'erreur ne chevauche pas celle de 
S4, ce qui suggère une différence réelle. En résumé : S1 se démarque, mais considérer S2, 
S3 et S4 comme trois « niveaux » de densité distincts irait au-delà de ce que les données 
permettent réellement d'affirmer."""
    },
    "chart_leafage_header": {
        "English": "Leaf age structure",
        "Français": "Structure d'âge des feuilles"
    },
    "chart_leafage_title": {
        "English": "Adult, intermediate, and juvenile leaves per shoot",
        "Français": "Feuilles adultes, intermédiaires et juvéniles par faisceau"
    },
    "chart_leafage_interp": {
        "English": """The mix of adult, intermediate, and juvenile leaves per shoot is 
nearly identical across all four stations (roughly 3 adult, 1 intermediate, 1.6–1.7 
juvenile leaves per shoot). This consistency is actually a reassuring sign — it suggests 
all four stations are in an active, ongoing growth cycle rather than one station showing 
signs of reduced leaf turnover or stalled growth relative to the others.""",
        "Français": """La répartition des feuilles adultes, intermédiaires et juvéniles par 
faisceau est presque identique dans les quatre stations (environ 3 feuilles adultes, 1 
intermédiaire, 1,6 à 1,7 juvéniles par faisceau). Cette homogénéité est en réalité un signe 
rassurant — elle suggère que les quatre stations sont dans un cycle de croissance actif et 
continu, sans qu'aucune ne montre de signe de ralentissement du renouvellement foliaire par 
rapport aux autres."""
    },
    "chart_bubble_header": {
        "English": "Combined health profile",
        "Français": "Profil de santé combiné"
    },
    "chart_bubble_title": {
        "English": "Cover, density, and leaf area combined",
        "Français": "Recouvrement, densité et surface foliaire combinés"
    },
    "chart_bubble_interp": {
        "English": """S1 stands out as the strongest station overall — high cover, the 
highest density, and (implicitly, via bubble size) a large leaf area. S4 is the clear 
opposite: lower density and a visibly smaller bubble, reflecting its much lower LAI — 
consistent with it being the shallow reef station rather than part of the main meadow 
transect. S2 is the interesting middle case: its density is comparable to S3, but its 
lower cover pulls it further left on the chart, visually isolating it from the other 
2–3m stations — which lines up with its distinct rocky substrate rather than a broader 
health problem.""",
        "Français": """S1 se distingue comme la station globalement la plus performante — 
recouvrement élevé, densité la plus forte, et (via la taille de la bulle) une surface 
foliaire importante. S4 est à l'inverse le cas le plus faible : densité plus basse et bulle 
visiblement plus petite, reflétant son indice foliaire bien plus réduit — cohérent avec son 
statut de station de récif peu profond plutôt que de faire partie du transect principal de 
l'herbier. S2 constitue un cas intermédiaire intéressant : sa densité est comparable à celle 
de S3, mais son recouvrement plus faible la décale vers la gauche du graphique, l'isolant 
visuellement des autres stations à 2-3m — ce qui concorde avec son substrat rocheux distinct 
plutôt qu'un problème de santé plus général."""
    },
    "invasive_header": {
        "English": "Invasive species observed",
        "Français": "Espèces invasives observées"
    },
    "invasive_cover_header": {
        "English": "Cover % with invasive species flagged",
        "Français": "Recouvrement % avec espèces invasives signalées"
    },
    "invasive_cover_title": {
        "English": "Percentage of seafloor covered by living Posidonia",
        "Français": "Pourcentage du fond marin recouvert par la posidonie vivante"
    },
    "invasive_annotation": {
        "English": "Caulerpa taxifolia observed here",
        "Français": "Caulerpa taxifolia observée ici"
    },
    "invasive_species_names": {
        "English": {
            "Caulerpa taxifolia": "Caulerpa taxifolia",
            "Asparagopsis armata": "Asparagopsis armata",
            "Pinctada radiata": "Pinctada radiata",
            "Percnon gibbesi": "Percnon gibbesi"
        },
        "Français": {
            "Caulerpa taxifolia": "Caulerpa taxifolia",
            "Asparagopsis armata": "Asparagopsis armata",
            "Pinctada radiata": "Pinctada radiata",
            "Percnon gibbesi": "Percnon gibbesi"
        }
    },
    "invasive_category_names": {
        "English": {"Alga": "Alga", "Bivalve": "Bivalve", "Crab": "Crab"},
        "Français": {"Alga": "Algue", "Bivalve": "Bivalve", "Crab": "Crabe"}
    },
    "invasive_observed_at": {
        "English": "📍 Observed at",
        "Français": "📍 Observée à"
    },
    "satellite_header": {
        "English": "Study area imagery — change over time",
        "Français": "Imagerie de la zone d'étude — évolution dans le temps"
    },
    "satellite_intro": {
        "English": """
Four satellite images spanning 35 years give a rough visual sense of how the 
coastline and nearshore waters around the meadow have looked over time. These 
are not scientific meadow delineations — just visual context alongside the 
ground-truth station data in the other tabs.
""",
        "Français": """
Quatre images satellite couvrant 35 ans donnent un aperçu visuel approximatif 
de l'évolution du littoral et des eaux côtières autour de l'herbier. Il ne 
s'agit pas de délimitations scientifiques de l'herbier — seulement d'un 
contexte visuel complémentaire aux données de terrain présentées dans les 
autres onglets.
"""
    },
    "satellite_single_header": {
        "English": "View a single year",
        "Français": "Voir une seule année"
    },
    "satellite_selectbox_label": {
        "English": "Choose imagery",
        "Français": "Choisir une image"
    },
    "satellite_compare_header": {
        "English": "Compare all four side by side",
        "Français": "Comparer les quatre côte à côte"
    },
    "satellite_labels": {
        "English": {
            "landsat5": "Landsat 5 (1990)",
            "landsat7": "Landsat 7 (2000)",
            "landsat8": "Landsat 8 (2015)",
            "sentinel2": "Sentinel-2 (recent)"
        },
        "Français": {
            "landsat5": "Landsat 5 (1990)",
            "landsat7": "Landsat 7 (2000)",
            "landsat8": "Landsat 8 (2015)",
            "sentinel2": "Sentinel-2 (récent)"
        }
    },
    "submit_header": {
        "English": "Submit new mission data",
        "Français": "Soumettre de nouvelles données de mission"
    },
    "submit_intro": {
        "English": "For excursionists to log data from future field missions.",
        "Français": "Pour que les excursionnistes puissent enregistrer les données des futures missions de terrain."
    },
    "submit_context_header": {
        "English": "Mission context",
        "Français": "Contexte de la mission"
    },
    "submit_date": {
        "English": "Mission date",
        "Français": "Date de la mission"
    },
    "submit_team": {
        "English": "Team members present",
        "Français": "Membres de l'équipe présents"
    },
    "submit_team_placeholder": {
        "English": "e.g. Aymen, Bayrem, Yassine",
        "Français": "ex. Aymen, Bayrem, Yassine"
    },
    "submit_weather": {
        "English": "Weather / sea conditions",
        "Français": "Conditions météo / mer"
    },
    "submit_weather_placeholder": {
        "English": "e.g. calm, light current",
        "Français": "ex. calme, léger courant"
    },
    "submit_description": {
        "English": "Mission description (optional)",
        "Français": "Description de la mission (optionnel)"
    },
    "submit_description_placeholder": {
        "English": "objectives, notable events...",
        "Français": "objectifs, événements notables..."
    },
    "submit_location_header": {
        "English": "Station location",
        "Français": "Emplacement de la station"
    },
    "submit_station_name": {
        "English": "Station / point name",
        "Français": "Nom de la station / du point"
    },
    "submit_lat": {
        "English": "Latitude",
        "Français": "Latitude"
    },
    "submit_lon": {
        "English": "Longitude",
        "Français": "Longitude"
    },
    "submit_depth": {
        "English": "Depth (m)",
        "Français": "Profondeur (m)"
    },
    "submit_structure_header": {
        "English": "Structural measurements",
        "Français": "Mesures structurelles"
    },
    "submit_density": {
        "English": "Shoot density (shoots/m²)",
        "Français": "Densité des faisceaux (faisceaux/m²)"
    },
    "submit_cover": {
        "English": "Cover (%)",
        "Français": "Recouvrement (%)"
    },
    "submit_dechaussement": {
        "English": "Déchaussement (mm)",
        "Français": "Déchaussement (mm)"
    },
    "submit_phenology_expander": {
        "English": "Phenology details (optional)",
        "Français": "Détails phénologiques (optionnel)"
    },
    "submit_leaves_ad": {
        "English": "Adult leaves/shoot",
        "Français": "Feuilles adultes/faisceau"
    },
    "submit_leaves_int": {
        "English": "Intermediate leaves/shoot",
        "Français": "Feuilles intermédiaires/faisceau"
    },
    "submit_leaves_juv": {
        "English": "Juvenile leaves/shoot",
        "Français": "Feuilles juvéniles/faisceau"
    },
    "submit_invasive_header": {
        "English": "Invasive species",
        "Français": "Espèces invasives"
    },
    "submit_invasive_select": {
        "English": "Species observed at this station",
        "Français": "Espèces observées à cette station"
    },
    "submit_invasive_notes": {
        "English": "Notes on invasive species (optional)",
        "Français": "Notes sur les espèces invasives (optionnel)"
    },
    "submit_invasive_notes_placeholder": {
        "English": "location within station, apparent spread, etc.",
        "Français": "emplacement dans la station, propagation apparente, etc."
    },
    "submit_interpretation_header": {
        "English": "Interpretation",
        "Français": "Interprétation"
    },
    "submit_interpretation_label": {
        "English": "Observations / interpretation",
        "Français": "Observations / interprétation"
    },
    "submit_interpretation_placeholder": {
        "English": "What did you notice? Anything unusual?",
        "Français": "Qu'avez-vous remarqué ? Quelque chose d'inhabituel ?"
    },
    "submit_button": {
        "English": "Submit mission data",
        "Français": "Soumettre les données de mission"
    },
    "submit_success": {
        "English": "Mission data for {date} at {station} saved!",
        "Français": "Données de mission du {date} à {station} enregistrées !"
    },
    "submit_history_header": {
        "English": "Submitted missions so far",
        "Français": "Missions soumises jusqu'à présent"
    },
    "submit_no_data": {
        "English": "No mission data submitted yet.",
        "Français": "Aucune donnée de mission soumise pour le moment."
    },
    "method_header": {
        "English": "Methodology",
        "Français": "Méthodologie"
    },
    "method_body": {
        "English": """
Data collection followed standard Mediterranean *Posidonia oceanica* monitoring 
protocols:

- **Density**: 10 quadrat counts (40cm × 40cm) per station, extrapolated to 
  shoots/m², following Pergent-Martini et al. (2005).
- **Cover**: visual estimation by two independent observers per station.
- **Déchaussement**: measured *in situ* following the Boudouresque et al. (1980) 
  protocol for plagiotropic and orthotropic rhizomes.
- **Phenology**: 20 rhizomes with living leaf bundles, spaced 1m apart, collected 
  per station and dissected following Giraud (1979).
- **Permanent markers (balises)**: 11 stakes placed 5m apart along a 50m line at 
  the meadow's upper limit, following Pergent (2007) recommendations, to allow 
  future missions to relocate and re-survey the exact same transect.
""",
        "Français": """
La collecte de données a suivi les protocoles standards de suivi méditerranéen 
de *Posidonia oceanica* :

- **Densité** : 10 comptages au quadrat (40cm × 40cm) par station, extrapolés 
  en faisceaux/m², selon Pergent-Martini et al. (2005).
- **Recouvrement** : estimation visuelle par deux observateurs indépendants 
  par station.
- **Déchaussement** : mesuré *in situ* selon le protocole de Boudouresque et 
  al. (1980) pour les rhizomes plagiotropes et orthotropes.
- **Phénologie** : 20 rhizomes portant des faisceaux foliaires vivants, 
  espacés d'1m, prélevés par station et disséqués selon Giraud (1979).
- **Marqueurs permanents (balises)** : 11 piquets espacés de 5m le long d'une 
  ligne de 50m à la limite supérieure de l'herbier, selon les recommandations 
  de Pergent (2007), pour permettre aux futures missions de relocaliser et de 
  ré-échantillonner le même transect.
"""
    },
    "sources_header": {
        "English": "Sources",
        "Français": "Sources"
    },
    "sources_body": {
        "English": """
- ASPEN / APAL / The MedFund (2022). *Rapport de mission — Zembra, 15-18 août 2022.*
- ASPEN / APAL / The MedFund (2024). *Rapport d'activités 2023 — Projet de cogestion 
  de l'AMCP de Zembra.*
- Giraud, G. (1977, 1979). Classification of *Posidonia oceanica* meadows by 
  shoot density.
- Pergent, G. (1995). Depth-adjusted classification of *Posidonia oceanica* 
  meadow density.
- Pergent-Martini, C. et al. (2005). Descriptors of *Posidonia oceanica* meadows: 
  use and application. *Ecological Indicators*, 5, 213-230.
- Boudouresque, C.F. et al. (1980, 2006). Protocols for measuring rhizome 
  déchaussement and meadow preservation.
- Andromède Océanologie (2010). Étude et cartographie des biocénoses marines 
  de l'île de Zembra, Tunisie.
- Invasive species photographs adapted from images published on 
  doris.ffessm.fr, futura-sciences.com, alchetron.com, and 
  biodiversitycyprus.blogspot.com.
""",
        "Français": """
- ASPEN / APAL / The MedFund (2022). *Rapport de mission — Zembra, 15-18 août 2022.*
- ASPEN / APAL / The MedFund (2024). *Rapport d'activités 2023 — Projet de cogestion 
  de l'AMCP de Zembra.*
- Giraud, G. (1977, 1979). Classification des herbiers de *Posidonia oceanica* 
  selon la densité des faisceaux.
- Pergent, G. (1995). Classification de la densité des herbiers de *Posidonia 
  oceanica* ajustée selon la profondeur.
- Pergent-Martini, C. et al. (2005). Descripteurs des herbiers de *Posidonia 
  oceanica* : usage et application. *Ecological Indicators*, 5, 213-230.
- Boudouresque, C.F. et al. (1980, 2006). Protocoles de mesure du déchaussement 
  des rhizomes et de préservation des herbiers.
- Andromède Océanologie (2010). Étude et cartographie des biocénoses marines 
  de l'île de Zembra, Tunisie.
- Photographies des espèces invasives adaptées d'images publiées sur 
  doris.ffessm.fr, futura-sciences.com, alchetron.com, et 
  biodiversitycyprus.blogspot.com.
"""
    },
    "limitations_header": {
        "English": "Known limitations",
        "Français": "Limites connues"
    },
    "limitations_body": {
        "English": """
- Data reflects a **single mission (August 2022)** — no time series yet.
- No stations currently extend past **3m depth**; the meadow's lower limit 
  (previously estimated at 22-30m) remains uncharacterized in this dataset.
- Only one of four invasive species (*Caulerpa taxifolia*) is tied to a specific 
  station; the other three were observed during the mission but not localized.
- Satellite imagery in this dashboard shows the full island for geographic 
  context only — resolution is too coarse to delineate the meadow itself at 
  this scale.
""",
        "Français": """
- Les données reflètent une **seule mission (août 2022)** — pas encore de 
  série temporelle.
- Aucune station ne dépasse actuellement **3m de profondeur** ; la limite 
  inférieure de l'herbier (estimée précédemment à 22-30m) reste non 
  caractérisée dans ce jeu de données.
- Une seule des quatre espèces invasives (*Caulerpa taxifolia*) est associée 
  à une station précise ; les trois autres ont été observées durant la mission 
  sans être localisées.
- L'imagerie satellite de ce tableau de bord montre l'île entière à des fins 
  de contexte géographique uniquement — la résolution est trop grossière pour 
  délimiter l'herbier lui-même à cette échelle.
"""
    },
    "download_header": {
        "English": "Download the data",
        "Français": "Télécharger les données"
    },
    "download_intro": {
        "English": "All datasets used in this dashboard, available individually or as a bundle.",
        "Français": "Tous les jeux de données utilisés dans ce tableau de bord, disponibles individuellement ou en un seul lot."
    },
    "download_stations": {
        "English": "⬇ Station structure (CSV)",
        "Français": "⬇ Structure des stations (CSV)"
    },
    "download_phenology": {
        "English": "⬇ Phenology data (CSV)",
        "Français": "⬇ Données phénologiques (CSV)"
    },
    "download_invasive": {
        "English": "⬇ Invasive species (CSV)",
        "Français": "⬇ Espèces invasives (CSV)"
    },
    "download_future": {
        "English": "⬇ Submitted mission data (CSV)",
        "Français": "⬇ Données de mission soumises (CSV)"
    },
    "download_all_header": {
        "English": "Or download everything at once",
        "Français": "Ou tout télécharger en une fois"
    },
    "download_all_button": {
        "English": "📦 Download all data (ZIP)",
        "Français": "📦 Télécharger toutes les données (ZIP)"
    },
    "gallery_header": {
        "English": "Field mission photo gallery",
        "Français": "Galerie photo de la mission de terrain"
    },
    "gallery_intro": {
        "English": "Photos from the August 2022 field mission documenting the survey and monitoring setup.",
        "Français": "Photos de la mission de terrain d'août 2022 documentant le suivi et la mise en place du dispositif de surveillance."
    },
    "gallery_balise_section": {
        "English": "Balise installation (permanent markers)",
        "Français": "Installation des balises (marqueurs permanents)"
    },
    "gallery_balise_positioning": {
        "English": "Overview of balise line positioning",
        "Français": "Vue d'ensemble du positionnement de la ligne de balises"
    },
    "gallery_balise_1": {
        "English": "Balise 1",
        "Français": "Balise 1"
    },
    "gallery_balise_6": {
        "English": "Balise 6 (midpoint)",
        "Français": "Balise 6 (point médian)"
    },
    "gallery_balise_11": {
        "English": "Balise 11",
        "Français": "Balise 11"
    },
    "gallery_balise_n": {
        "English": "Balise {n}",
        "Français": "Balise {n}"
    },
    "gallery_quadrat_section": {
        "English": "Quadrat sampling",
        "Français": "Échantillonnage au quadrat"
    },
    "gallery_quadrat_deployment": {
        "English": "40cm quadrat used for density counts",
        "Français": "Quadrat de 40cm utilisé pour les comptages de densité"
    },
    "gallery_quadrat_diver": {
        "English": "Diver conducting a density count",
        "Français": "Plongeur effectuant un comptage de densité"
    },
    "gallery_see_all": {
        "English": "See all 11 balise photos",
        "Français": "Voir les 11 photos de balises"
    },
        "submit_edit_hint": {
        "English": "Click any cell to edit it. Hover over a row and click the trash icon to delete it. Click **Save changes** when done.",
        "Français": "Cliquez sur une cellule pour la modifier. Survolez une ligne et cliquez sur l'icône de corbeille pour la supprimer. Cliquez sur **Enregistrer les modifications** une fois terminé."
    },
    "submit_save_button": {
        "English": "💾 Save changes",
        "Français": "💾 Enregistrer les modifications"
    },
    "submit_save_success": {
        "English": "Changes saved successfully.",
        "Français": "Modifications enregistrées avec succès."
    },
        "submit_photos_label": {
        "English": "Upload photos from this mission (optional)",
        "Français": "Téléverser des photos de cette mission (optionnel)"
    },
    "gallery_new_missions_header": {
        "English": "Recent mission submissions",
        "Français": "Soumissions récentes de mission"
    },
    "gallery_no_new_photos": {
        "English": "No photos submitted yet.",
        "Français": "Aucune photo soumise pour le moment."
    },
        "account_settings_header": {
        "English": "⚙️ Account settings",
        "Français": "⚙️ Paramètres du compte"
    },
    "account_username_label": {
        "English": "Username",
        "Français": "Nom d'utilisateur"
    },
    "account_name_label": {
        "English": "Full name",
        "Français": "Nom complet"
    },
    "account_email_label": {
        "English": "Email",
        "Français": "E-mail"
    },
    "account_new_password_label": {
        "English": "New password (leave blank to keep current)",
        "Français": "Nouveau mot de passe (laisser vide pour conserver l'actuel)"
    },
    "account_save_button": {
        "English": "Save profile",
        "Français": "Enregistrer le profil"
    },
    "account_saved": {
        "English": "Profile updated.",
        "Français": "Profil mis à jour."
    },
    "account_change_username_header": {
        "English": "Change username",
        "Français": "Changer de nom d'utilisateur"
    },
    "account_new_username_label": {
        "English": "New username",
        "Français": "Nouveau nom d'utilisateur"
    },
    "account_change_username_button": {
        "English": "Change username",
        "Français": "Changer de nom d'utilisateur"
    },
    "account_username_taken": {
        "English": "That username is already taken.",
        "Français": "Ce nom d'utilisateur est déjà pris."
    },
    "account_username_changed": {
        "English": "Username changed. Please log in again with your new username.",
        "Français": "Nom d'utilisateur modifié. Veuillez vous reconnecter avec votre nouveau nom d'utilisateur."
    },
    "account_danger_zone": {
        "English": "Danger zone",
        "Français": "Zone à risque"
    },
    "account_confirm_delete_checkbox": {
        "English": "I understand this will permanently delete my account",
        "Français": "Je comprends que cela supprimera définitivement mon compte"
    },
    "account_delete_button": {
        "English": "Delete my account",
        "Français": "Supprimer mon compte"
    },
    "account_deleted": {
        "English": "Account deleted. You have been logged out.",
        "Français": "Compte supprimé. Vous avez été déconnecté."
    },
    "manage_accounts_header": {
        "English": "👥 Manage accounts",
        "Français": "👥 Gérer les comptes"
    },
    "add_account_header": {
        "English": "Add a new account",
        "Français": "Ajouter un nouveau compte"
    },
    "add_account_username": {
        "English": "Username",
        "Français": "Nom d'utilisateur"
    },
    "add_account_name": {
        "English": "Full name",
        "Français": "Nom complet"
    },
    "add_account_email": {
        "English": "Email",
        "Français": "E-mail"
    },
    "add_account_password": {
        "English": "Temporary password",
        "Français": "Mot de passe temporaire"
    },
    "add_account_role": {
        "English": "Role",
        "Français": "Rôle"
    },
    "add_account_button": {
        "English": "Create account",
        "Français": "Créer le compte"
    },
    "add_account_exists": {
        "English": "That username already exists.",
        "Français": "Ce nom d'utilisateur existe déjà."
    },
    "add_account_success": {
        "English": "Account created for {username}.",
        "Français": "Compte créé pour {username}."
    },
    "existing_accounts_header": {
        "English": "Existing accounts",
        "Français": "Comptes existants"
    },
    "existing_accounts_hint": {
        "English": "Select accounts to delete, then click below.",
        "Français": "Sélectionnez les comptes à supprimer, puis cliquez ci-dessous."
    },
    "delete_accounts_button": {
        "English": "🗑 Delete selected accounts",
        "Français": "🗑 Supprimer les comptes sélectionnés"
    },
    "delete_accounts_success": {
        "English": "Selected accounts deleted.",
        "Français": "Comptes sélectionnés supprimés."
    },
    "delete_self_warning": {
        "English": "You cannot delete your own account here — use Account Settings instead.",
        "Français": "Vous ne pouvez pas supprimer votre propre compte ici — utilisez plutôt les Paramètres du compte."
    },
    "no_accounts_selected": {
        "English": "Select at least one account to delete.",
        "Français": "Sélectionnez au moins un compte à supprimer."
    },
}


try:
    authenticator.login()
except LoginError:
    st.error("Your session has expired or is no longer valid. Please clear your "
              "browser cookies for this site, then reload the page and log in again.")
    st.stop()

if st.session_state.get('authentication_status') is False:
    st.error('Username or password is incorrect')
    st.stop()
elif st.session_state.get('authentication_status') is None:
    st.warning('Please log in to access the dashboard')
    st.stop()

# --- Logged in from here on ---
username = st.session_state['username']
user_role = config['credentials']['usernames'][username]['role']
is_admin = (user_role == 'admin')

authenticator.logout('Logout', 'sidebar')
st.sidebar.markdown(f"Logged in as **{st.session_state['name']}** ({user_role})")

# ---------------- Personal account settings ----------------
with st.sidebar.expander(T["account_settings_header"][lang]):
    st.markdown(f"**{T['account_username_label'][lang]}:** {username}")

    with st.form("edit_profile_form"):
        new_name = st.text_input(T["account_name_label"][lang], 
                                  value=config['credentials']['usernames'][username]['name'])
        new_email = st.text_input(T["account_email_label"][lang], 
                                   value=config['credentials']['usernames'][username]['email'])
        new_password = st.text_input(T["account_new_password_label"][lang], type="password")
        save_profile = st.form_submit_button(T["account_save_button"][lang])

        if save_profile:
            config['credentials']['usernames'][username]['name'] = new_name
            config['credentials']['usernames'][username]['email'] = new_email
            if new_password:
                hasher = stauth.Hasher()
                config['credentials']['usernames'][username]['password'] = hasher.hash(new_password)
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            st.success(T["account_saved"][lang])
            st.rerun()

    st.divider()
    st.markdown(f"**{T['account_change_username_header'][lang]}**")
    with st.form("change_username_form"):
        new_username_input = st.text_input(T["account_new_username_label"][lang])
        change_username_submit = st.form_submit_button(T["account_change_username_button"][lang])

        if change_username_submit and new_username_input:
            if new_username_input in config['credentials']['usernames']:
                st.error(T["account_username_taken"][lang])
            else:
                config['credentials']['usernames'][new_username_input] = config['credentials']['usernames'].pop(username)
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success(T["account_username_changed"][lang])
                for key in ["authentication_status", "name", "username"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

    st.divider()
    st.markdown(f"**{T['account_danger_zone'][lang]}**")
    confirm_delete = st.checkbox(T["account_confirm_delete_checkbox"][lang])
    if st.button(T["account_delete_button"][lang], disabled=not confirm_delete):
        del config['credentials']['usernames'][username]
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        for key in ["authentication_status", "name", "username"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success(T["account_deleted"][lang])
        st.rerun()

# ---------------- Admin: manage all accounts ----------------
if is_admin:
    with st.sidebar.expander(T["manage_accounts_header"][lang]):
        st.markdown(f"**{T['add_account_header'][lang]}**")
        with st.form("add_user_form"):
            new_acc_username = st.text_input(T["add_account_username"][lang])
            new_acc_name = st.text_input(T["add_account_name"][lang])
            new_acc_email = st.text_input(T["add_account_email"][lang])
            new_acc_password = st.text_input(T["add_account_password"][lang], type="password")
            new_acc_role = st.selectbox(T["add_account_role"][lang], ["member", "admin"])
            add_submitted = st.form_submit_button(T["add_account_button"][lang])

            if add_submitted:
                if new_acc_username in config['credentials']['usernames']:
                    st.error(T["add_account_exists"][lang])
                else:
                    hasher = stauth.Hasher()
                    config['credentials']['usernames'][new_acc_username] = {
                        'email': new_acc_email,
                        'name': new_acc_name,
                        'password': hasher.hash(new_acc_password),
                        'role': new_acc_role
                    }
                    with open('config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
                    st.success(T["add_account_success"][lang].format(username=new_acc_username))
                    st.rerun()

        st.divider()
        st.markdown(f"**{T['existing_accounts_header'][lang]}**")
        st.caption(T["existing_accounts_hint"][lang])

        accounts_list = [
            {"Select": False, "Username": u, "Name": d.get("name", ""), 
             "Email": d.get("email", ""), "Role": d.get("role", "")}
            for u, d in config['credentials']['usernames'].items()
        ]
        accounts_df = pd.DataFrame(accounts_list)
        edited_accounts = st.data_editor(
            accounts_df, use_container_width=True, hide_index=True,
            disabled=["Username", "Name", "Email", "Role"], key="accounts_editor"
        )

        if st.button(T["delete_accounts_button"][lang]):
            to_delete = edited_accounts[edited_accounts["Select"] == True]["Username"].tolist()
            if not to_delete:
                st.warning(T["no_accounts_selected"][lang])
            elif username in to_delete:
                st.error(T["delete_self_warning"][lang])
            else:
                for uname in to_delete:
                    del config['credentials']['usernames'][uname]
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success(T["delete_accounts_success"][lang])
                st.rerun()

# ============================================================
# DATA LOADING & PROCESSING — stays outside tabs, runs once
# ============================================================

stations = pd.read_csv("stations_structure.csv")
phenology = pd.read_csv("stations_phenology.csv")
invasive = pd.read_csv("invasive_species.csv")

# Safety net for stray whitespace in column names
stations.columns = stations.columns.str.strip()
phenology.columns = phenology.columns.str.strip()
invasive.columns = invasive.columns.str.strip()

def classify_giraud(density):
    if density > 700:
        return "Type I - Très dense"
    elif density >= 400:
        return "Type II - Dense"
    elif density >= 300:
        return "Type III - Clairsemé"
    elif density >= 150:
        return "Type IV - Très clairsemé"
    elif density >= 50:
        return "Type V - Semi-herbier"
    else:
        return "Faisceaux isolés"

pergent_table = {
    1: [1133, 930, 727, 524],
    2: [1067, 863, 659, 456],
    3: [1005, 808, 612, 415],
    4: [947, 757, 567, 377],
    5: [892, 709, 526, 343],
}

def classify_pergent(density, depth):
    depth_band = min(max(round(depth), 1), 5)
    thresholds = pergent_table[depth_band]
    if density > thresholds[0]:
        return "Très bonne"
    elif density > thresholds[1]:
        return "Bonne"
    elif density > thresholds[2]:
        return "Moyenne"
    elif density > thresholds[3]:
        return "Médiocre"
    else:
        return "Mauvaise"

stations["giraud_class"] = stations["density_m2"].apply(classify_giraud)
stations["pergent_class"] = stations.apply(
    lambda row: classify_pergent(row["density_m2"], row["depth_m"]), axis=1
)

merged = pd.merge(stations, phenology, on="station")

FUTURE_DATA_FILE = "future_missions.csv"
if not os.path.exists(FUTURE_DATA_FILE):
    pd.DataFrame(columns=[
        "mission_date", "team_members", "weather_conditions", "description",
        "station", "latitude", "longitude", "depth_m",
        "density_m2", "cover_pct", "uprooting_mm",
        "n_leaves_ad", "n_leaves_int", "n_leaves_juv",
        "invasive_species_observed", "invasive_notes",
        "interpretation"
    ]).to_csv(FUTURE_DATA_FILE, index=False)

import uuid

PHOTOS_DIR = "images/mission/submitted"
PHOTOS_MANIFEST = "mission_photos.csv"

if not os.path.exists(PHOTOS_DIR):
    os.makedirs(PHOTOS_DIR)

if not os.path.exists(PHOTOS_MANIFEST):
    pd.DataFrame(columns=["filename", "mission_date", "station", "caption"]).to_csv(PHOTOS_MANIFEST, index=False)


# ============================================================
# HEADER — shown above all tabs
# ============================================================

st.set_page_config(page_title="Posidonia oceanica - Zembra", layout="wide", page_icon="🌊")

# --- Top bar: partnership branding ---
st.markdown("""
<div style='text-align: right; font-size: 13px; color: #888; margin-bottom: -10px;'>
    In partnership with <b style='color: #444;'>ASPEN Cap Bon</b> · <b style='color: #444;'>Manouba School of Engineering</b>
</div>
""", unsafe_allow_html=True)

# --- Main title (only one, right here) ---
st.title(T["title"][lang])
st.caption(T["caption"][lang])


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    T["tab_overview"][lang], T["tab_stations"][lang], T["tab_invasive"][lang],
    T["tab_satellite"][lang], T["tab_submit"][lang], T["tab_methodology"][lang],
    T["tab_gallery"][lang]
])

# ------------------------------------------------------------
# TAB 1 — OVERVIEW
# ------------------------------------------------------------
with tab1:
    st.markdown(T["overview_intro"][lang])

    st.divider()
    st.subheader(T["overview_protection_header"][lang])
    st.markdown(T["overview_protection"][lang])

    st.divider()
    st.subheader(T["overview_why_header"][lang])
    st.markdown(T["overview_why"][lang])

    st.divider()
    st.subheader(T["overview_stations_header"][lang])
    st.markdown(T["overview_stations"][lang])

    st.divider()
    with st.expander(T["glossary_header"][lang]):
        st.markdown(T["glossary_body"][lang])

    st.divider()
    st.subheader(T["raw_data_header"][lang])
    st.dataframe(stations, use_container_width=True)
    st.dataframe(phenology, use_container_width=True)
    st.dataframe(invasive, use_container_width=True)

    st.divider()
    st.subheader(T["classification_header"][lang])
    st.markdown(T["classification_intro"][lang])
    st.dataframe(
        stations[["station", "depth_m", "density_m2", "giraud_class", "pergent_class"]],
        use_container_width=True, hide_index=True
    )

    st.divider()
    st.header(T["summary_header"][lang])
    st.markdown(T["summary_body"][lang])

# ------------------------------------------------------------
# TAB 2 — STATIONS & CHARTS
# ------------------------------------------------------------
with tab2:
    st.subheader(T["chart_map_header"][lang])
    fig = px.scatter_map(stations, lat="latitude", lon="longitude", 
                             text="station", color="density_m2", size="cover_pct",
                             zoom=13, map_style="open-street-map",
                             title=T["chart_map_title"][lang])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(T["chart_map_interp"][lang])

    st.divider()

    st.subheader(T["chart_cover_header"][lang])
    fig = px.bar(stations, x="station", y="cover_pct", 
                 labels={"cover_pct": "Cover %" if lang == "English" else "Recouvrement %", "station": ""},
                 title=T["chart_cover_title"][lang])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(T["chart_cover_interp"][lang])

    st.divider()

    st.subheader(T["chart_coeffa_header"][lang])
    fig = px.bar(phenology, x="station", 
                 y=["coeff_a_hydro_pct", "coeff_a_urchin_pct", "coeff_a_fish_pct"],
                 labels={"value": "% of leaves" if lang == "English" else "% de feuilles", 
                         "station": "", "variable": "Cause"},
                 barmode="stack",
                 title=T["chart_coeffa_title"][lang])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(T["chart_coeffa_interp"][lang])

    st.divider()

    st.subheader(T["chart_lai_header"][lang])
    fig = px.scatter(merged, x="depth_m", y="leaf_area_index_m2", 
                      text="station", size_max=15,
                      title=T["chart_lai_title"][lang])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(T["chart_lai_interp"][lang])

    st.divider()

    st.subheader(T["chart_radar_header"][lang])
    fig = px.line_polar(merged, r="density_m2", theta="station", line_close=True,
                         title=T["chart_radar_title"][lang])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(T["chart_radar_interp"][lang])

    st.divider()

    st.subheader(T["chart_error_header"][lang])
    fig = px.bar(stations, x="station", y="density_m2", error_y="density_se",
                 labels={"density_m2": "Density (shoots/m²)" if lang == "English" else "Densité (faisceaux/m²)"},
                 title=T["chart_error_title"][lang])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(T["chart_error_interp"][lang])

    st.divider()

    st.subheader(T["chart_leafage_header"][lang])
    fig = px.bar(phenology, x="station", 
                 y=["n_leaves_ad", "n_leaves_int", "n_leaves_juv"],
                 barmode="group",
                 labels={"value": "Leaves per shoot" if lang == "English" else "Feuilles par faisceau", 
                         "variable": "Leaf type" if lang == "English" else "Type de feuille"},
                 title=T["chart_leafage_title"][lang])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(T["chart_leafage_interp"][lang])

    st.divider()

    st.subheader(T["chart_bubble_header"][lang])
    fig = px.scatter(merged, x="cover_pct", y="density_m2", 
                      size="leaf_area_index_m2", color="station",
                      text="station",
                      title=T["chart_bubble_title"][lang])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(T["chart_bubble_interp"][lang])
# ------------------------------------------------------------
# TAB 3 — INVASIVE SPECIES
# ------------------------------------------------------------
with tab3:
    st.subheader(T["invasive_header"][lang])

    species_images = {
        "Caulerpa taxifolia": "images/invasive/caulerpa_taxifolia.jpg",
        "Asparagopsis armata": "images/invasive/asparagopsis_armata.jpg",
        "Pinctada radiata": "images/invasive/pinctada_radiata.jpg",
        "Percnon gibbesi": "images/invasive/percnon_gibbesi.jpg",
    }

    cols = st.columns(4)
    for col, (_, row) in zip(cols, invasive.iterrows()):
        with col:
            img_path = species_images.get(row["species"])
            if img_path:
                st.image(img_path, use_container_width=True)
            st.markdown(f"**_{row['species']}_**")
            category_translated = T["invasive_category_names"][lang].get(row["category"], row["category"])
            st.caption(f"{category_translated} · {row['origin']}")
            if pd.notna(row.get("station")) and str(row.get("station")).strip():
                st.caption(f"{T['invasive_observed_at'][lang]} {row['station']}")

    st.divider()
    st.dataframe(invasive, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader(T["invasive_cover_header"][lang])
    fig = px.bar(stations, x="station", y="cover_pct", 
                 labels={"cover_pct": "Cover %" if lang == "English" else "Recouvrement %", "station": ""},
                 title=T["invasive_cover_title"][lang])
    fig.add_annotation(
        x="S2", y=stations.loc[stations["station"] == "S2", "cover_pct"].values[0],
        text=T["invasive_annotation"][lang],
        showarrow=True, arrowhead=2, ay=-40
    )
    st.plotly_chart(fig, use_container_width=True)
# ------------------------------------------------------------
# TAB 4 — SATELLITE IMAGERY
# ------------------------------------------------------------
with tab4:
    st.header(T["satellite_header"][lang])
    st.markdown(T["satellite_intro"][lang])

    imagery_paths = {
    "landsat5": "landsat5_1990.png",
    "landsat7": "landsat7_2000.png",
    "landsat8": "landsat8_2015.png",
    "sentinel2": "sentinel2_recent.png",
}
    labels = T["satellite_labels"][lang]

    st.subheader(T["satellite_single_header"][lang])
    selected_key = st.selectbox(
        T["satellite_selectbox_label"][lang],
        list(imagery_paths.keys()),
        format_func=lambda k: labels[k]
    )
    st.image(imagery_paths[selected_key], caption=labels[selected_key], use_container_width=True)

    st.divider()

    st.subheader(T["satellite_compare_header"][lang])
    cols = st.columns(4)
    for col, key in zip(cols, imagery_paths.keys()):
        with col:
            st.image(imagery_paths[key], caption=labels[key], use_container_width=True)
# ------------------------------------------------------------
# TAB 5 — SUBMIT MISSION DATA
# ------------------------------------------------------------
with tab5:
    if not is_admin:
        st.warning("Only admin accounts can submit mission data.")
    else:
        st.header(T["submit_header"][lang])
        st.markdown(T["submit_intro"][lang])

        with st.form("new_mission_form"):
            st.subheader(T["submit_context_header"][lang])
            col1, col2 = st.columns(2)
            with col1:
                mission_date = st.date_input(T["submit_date"][lang])
                team_members = st.text_input(T["submit_team"][lang], 
                                              placeholder=T["submit_team_placeholder"][lang])
            with col2:
                weather_conditions = st.text_input(T["submit_weather"][lang], 
                                                    placeholder=T["submit_weather_placeholder"][lang])
                description = st.text_area(T["submit_description"][lang], 
                                            placeholder=T["submit_description_placeholder"][lang])

            st.divider()
            st.subheader(T["submit_location_header"][lang])
            col1, col2, col3 = st.columns(3)
            with col1:
                station = st.text_input(T["submit_station_name"][lang], placeholder="e.g. S5, Deep-1")
            with col2:
                latitude = st.number_input(T["submit_lat"][lang], min_value=-90.0, max_value=90.0, 
                                            format="%.6f", value=37.118000)
            with col3:
                longitude = st.number_input(T["submit_lon"][lang], min_value=-180.0, max_value=180.0, 
                                             format="%.6f", value=10.805000)
            depth_m = st.number_input(T["submit_depth"][lang], min_value=0.0, max_value=60.0, step=0.5)

            st.divider()
            st.subheader(T["submit_structure_header"][lang])
            col1, col2, col3 = st.columns(3)
            with col1:
                density_m2 = st.number_input(T["submit_density"][lang], min_value=0.0, step=1.0)
            with col2:
                cover_pct = st.number_input(T["submit_cover"][lang], min_value=0.0, max_value=100.0, step=1.0)
            with col3:
                dechaussement_mm = st.number_input(T["submit_dechaussement"][lang], min_value=0.0, step=1.0)

            with st.expander(T["submit_phenology_expander"][lang]):
                col1, col2, col3 = st.columns(3)
                with col1:
                    n_leaves_ad = st.number_input(T["submit_leaves_ad"][lang], min_value=0.0, step=0.1)
                with col2:
                    n_leaves_int = st.number_input(T["submit_leaves_int"][lang], min_value=0.0, step=0.1)
                with col3:
                    n_leaves_juv = st.number_input(T["submit_leaves_juv"][lang], min_value=0.0, step=0.1)

            st.divider()
            st.subheader(T["submit_invasive_header"][lang])
            invasive_species_observed = st.multiselect(
                T["submit_invasive_select"][lang],
                ["Caulerpa taxifolia", "Asparagopsis armata", "Pinctada radiata", "Percnon gibbesi", "Other"]
            )
            invasive_notes = st.text_area(T["submit_invasive_notes"][lang], 
                                           placeholder=T["submit_invasive_notes_placeholder"][lang])

            st.divider()
            st.subheader(T["submit_interpretation_header"][lang])
            interpretation = st.text_area(T["submit_interpretation_label"][lang],
                                           placeholder=T["submit_interpretation_placeholder"][lang])
            uploaded_photos = st.file_uploader(
                T["submit_photos_label"][lang],
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True
            )


            submitted = st.form_submit_button(T["submit_button"][lang])

            if submitted:
                new_row = pd.DataFrame([{
                    "mission_date": mission_date,
                    "team_members": team_members,
                    "weather_conditions": weather_conditions,
                    "description": description,
                    "station": station,
                    "latitude": latitude,
                    "longitude": longitude,
                    "depth_m": depth_m,
                    "density_m2": density_m2,
                    "cover_pct": cover_pct,
                    "dechaussement_mm": dechaussement_mm,
                    "n_leaves_ad": n_leaves_ad,
                    "n_leaves_int": n_leaves_int,
                    "n_leaves_juv": n_leaves_juv,
                    "invasive_species_observed": ", ".join(invasive_species_observed),
                    "invasive_notes": invasive_notes,
                    "interpretation": interpretation
                }])
                new_row.to_csv(FUTURE_DATA_FILE, mode="a", header=False, index=False)
                new_row.to_csv(FUTURE_DATA_FILE, mode="a", header=False, index=False)

                if uploaded_photos:
                    manifest = pd.read_csv(PHOTOS_MANIFEST)
                    new_photo_rows = []
                    for photo in uploaded_photos:
                        ext = photo.name.split(".")[-1]
                        unique_name = f"{mission_date}_{station}_{uuid.uuid4().hex[:8]}.{ext}"
                        filepath = os.path.join(PHOTOS_DIR, unique_name)
                        with open(filepath, "wb") as f:
                            f.write(photo.getbuffer())
                        new_photo_rows.append({
                            "filename": filepath,
                            "mission_date": str(mission_date),
                            "station": station,
                            "caption": f"{station} — {mission_date}"
                        })
                    manifest = pd.concat([manifest, pd.DataFrame(new_photo_rows)], ignore_index=True)
                    manifest.to_csv(PHOTOS_MANIFEST, index=False)

                st.success(T["submit_success"][lang].format(date=mission_date, station=station))
                st.success(T["submit_success"][lang].format(date=mission_date, station=station))

                st.subheader(T["submit_history_header"][lang])
        future_data = pd.read_csv(FUTURE_DATA_FILE)
        future_data = future_data.reset_index(drop=True)  # <-- add this line

        if len(future_data) > 0:
            st.markdown(T["submit_edit_hint"][lang])
            edited_data = st.data_editor(
                future_data,
                use_container_width=True,
                num_rows="dynamic",
                key="future_missions_editor"
            )
            if st.button(T["submit_save_button"][lang]):
                edited_data = edited_data.reset_index(drop=True)  # <-- and here, before saving
                edited_data.to_csv(FUTURE_DATA_FILE, index=False)
                st.success(T["submit_save_success"][lang])
                st.rerun()
        else:
            st.info(T["submit_no_data"][lang])

# ------------------------------------------------------------
# TAB 6 — METHODOLOGY & SOURCES
# ------------------------------------------------------------
with tab6:
    st.header(T["method_header"][lang])
    st.markdown(T["method_body"][lang])

    st.divider()
    st.header(T["sources_header"][lang])
    st.markdown(T["sources_body"][lang])

    st.divider()
    st.header(T["limitations_header"][lang])
    st.markdown(T["limitations_body"][lang])

    st.divider()
    st.header(T["download_header"][lang])
    st.markdown(T["download_intro"][lang])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(T["download_stations"][lang], 
                            stations.to_csv(index=False), "stations_structure.csv")
    with col2:
        st.download_button(T["download_phenology"][lang], 
                            phenology.to_csv(index=False), "stations_phenology.csv")
    with col3:
        st.download_button(T["download_invasive"][lang], 
                            invasive.to_csv(index=False), "invasive_species.csv")

    if os.path.exists(FUTURE_DATA_FILE):
        future_data_check = pd.read_csv(FUTURE_DATA_FILE)
        if len(future_data_check) > 0:
            st.download_button(T["download_future"][lang], 
                                future_data_check.to_csv(index=False), "future_missions.csv")

    st.divider()
    st.subheader(T["download_all_header"][lang])
    all_files = {
        "stations_structure.csv": stations,
        "stations_phenology.csv": phenology,
        "invasive_species.csv": invasive,
    }
    if os.path.exists(FUTURE_DATA_FILE):
        future_data_check = pd.read_csv(FUTURE_DATA_FILE)
        if len(future_data_check) > 0:
            all_files["future_missions.csv"] = future_data_check

    zip_buffer = create_zip_download(all_files)
    st.download_button(
        T["download_all_button"][lang], 
        zip_buffer, 
        "posidonia_zembra_data.zip",
        mime="application/zip"
    )

with tab7:
    st.header(T["gallery_header"][lang])
    st.markdown(T["gallery_intro"][lang])

    gallery_sections = {
    T["gallery_balise_section"][lang]: [
        ("images/mission/balise_positioning.png", T["gallery_balise_positioning"][lang]),
        ("images/mission/balise_1.png", T["gallery_balise_1"][lang]),
        ("images/mission/balise_6.png", T["gallery_balise_6"][lang]),
        ("images/mission/balise_11.png", T["gallery_balise_11"][lang]),
    ],
    T["gallery_quadrat_section"][lang]: [
        ("images/mission/quadrat_deployment.png", T["gallery_quadrat_deployment"][lang]),
        ("images/mission/quadrat_diver.png", T["gallery_quadrat_diver"][lang]),
    ],
}

    for section_title, photos in gallery_sections.items():
        with st.expander(section_title, expanded=True):
            cols = st.columns(3)
            for i, (path, caption) in enumerate(photos):
                with cols[i % 3]:
                    st.image(path, caption=caption, use_container_width=True)

            if section_title == T["gallery_balise_section"][lang]:
                with st.expander(T["gallery_see_all"][lang]):
                    all_balises = [
                        (f"images/mission/balise_{n}.png", T["gallery_balise_n"][lang].format(n=n)) 
                        for n in range(1, 12)
                        ]
                    cols2 = st.columns(4)
                    for i, (path, caption) in enumerate(all_balises):
                        with cols2[i % 4]:
                            st.image(path, caption=caption, use_container_width=True)
        st.divider()
    st.subheader(T["gallery_new_missions_header"][lang])
    manifest = pd.read_csv(PHOTOS_MANIFEST) if os.path.exists(PHOTOS_MANIFEST) else pd.DataFrame()
    if len(manifest) > 0:
        for date, group in manifest.groupby("mission_date"):
            with st.expander(str(date), expanded=False):
                cols = st.columns(3)
                for i, (_, row) in enumerate(group.iterrows()):
                    with cols[i % 3]:
                        if os.path.exists(row["filename"]):
                            st.image(row["filename"], caption=row["caption"], use_container_width=True)
    else:
        st.info(T["gallery_no_new_photos"][lang])