import folium
from folium import plugins
import webbrowser
import os

# Coordonnées des villes (latitude, longitude)
villes = {
    "Tokyo": (35.6762, 139.6503),
    "Nara": (34.6851, 135.8048),
    "Hiroshima": (34.3853, 132.4553),
    "Hakone": (35.2324, 139.1063),
    "Kyoto": (35.0116, 135.7681),
    "Osaka": (34.6937, 135.5023)
}

# Itinéraire
itineraire = ["Tokyo", "Hakone", "Kyoto", "Nara", "Osaka", "Hiroshima", "Tokyo"]

# Informations sur les villes
infos_villes = {
    "Tokyo": {
        "description": "Capitale du Japon, mégapole vibrante et centre économique",
        "population": "~14 millions",
        "attractions": ["Tour de Tokyo", "Senso-ji", "Shibuya Crossing"]
    },
    "Nara": {
        "description": "Ancienne capitale, connue pour ses temples et ses daims",
        "population": "~350 000",
        "attractions": ["Todai-ji", "Parc de Nara", "Grand Bouddha"]
    },
    "Hiroshima": {
        "description": "Ville historique, symbole de paix et de reconstruction",
        "population": "~1.2 million",
        "attractions": ["Mémorial de la Paix", "Dôme de Genbaku", "Miyajima"]
    },
    "Hakone": {
        "description": "Station thermale avec vue sur le Mont Fuji",
        "population": "~13 000",
        "attractions": ["Lac Ashi", "Owakudani", "Musée en plein air"]
    },
    "Kyoto": {
        "description": "Ancienne capitale impériale, cœur culturel du Japon",
        "population": "~1.5 million",
        "attractions": ["Fushimi Inari", "Kinkaku-ji", "Gion"]
    },
    "Osaka": {
        "description": "Ville dynamique connue pour sa cuisine",
        "population": "~2.7 millions",
        "attractions": ["Château d'Osaka", "Dotonbori", "Universal Studios"]
    }
}

# Carte
carte = folium.Map(
    location=[36.2048, 138.2529],
    zoom_start=6,
    tiles="CartoDB positron",
    max_bounds=True
)

groupe_villes = folium.FeatureGroup(name="Villes")
coords_itineraire = []

couleurs = ['red', 'blue', 'green', 'orange', 'purple', 'darkred']

# Marqueurs
for i, ville in enumerate(itineraire[:-1]):
    coords = villes[ville]
    coords_itineraire.append(coords)
    info = infos_villes[ville]

    popup_html = f"""
    <div style="width:250px">
        <h4>{ville}</h4>
        <b>Étape {i+1}</b><br><br>
        <b>Description :</b> {info['description']}<br>
        <b>Population :</b> {info['population']}<br><br>
        <b>Attractions :</b>
        <ul>
            {''.join(f"<li>{a}</li>" for a in info['attractions'])}
        </ul>
    </div>
    """

    folium.Marker(
        location=coords,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"Étape {i+1}: {ville}",
        icon=folium.Icon(color=couleurs[i % len(couleurs)], icon="info-sign")
    ).add_to(groupe_villes)

# Point final Tokyo
coords_itineraire.append(villes["Tokyo"])

folium.Marker(
    location=villes["Tokyo"],
    popup="Tokyo<br><b>Départ et arrivée</b>",
    tooltip="Tokyo (départ / arrivée)",
    icon=folium.Icon(color="black", icon="flag")
).add_to(groupe_villes)

groupe_villes.add_to(carte)

# Tracé de l'itinéraire
for i in range(len(coords_itineraire) - 1):
    depart = coords_itineraire[i]
    arrivee = coords_itineraire[i + 1]

    folium.PolyLine(
        locations=[depart, arrivee],
        color=couleurs[i % len(couleurs)],
        weight=3,
        opacity=0.8
    ).add_to(carte)

    mid_lat = (depart[0] + arrivee[0]) / 2
    mid_lon = (depart[1] + arrivee[1]) / 2

    folium.RegularPolygonMarker(
        location=[mid_lat, mid_lon],
        number_of_sides=3,
        radius=8,
        rotation=45,
        color=couleurs[i % len(couleurs)],
        fill_color=couleurs[i % len(couleurs)],
        fill_opacity=1
    ).add_to(carte)

# Titre
title_html = """
<h2 style="text-align:center;">
Itinéraire au Japon<br>
Tokyo → Hakone → Kyoto → Nara → Osaka → Hiroshima → Tokyo
</h2>
"""
carte.get_root().html.add_child(folium.Element(title_html))

# Sauvegarde
fichier_carte = "itineraire_japon.html"
carte.save(fichier_carte)

print("Carte générée avec succès.")
webbrowser.open("file://" + os.path.realpath(fichier_carte))
