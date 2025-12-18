from typing import Dict, List
from pathlib import Path
CSS_PATH = Path(__file__).parent / "style.css"
# Données des villes
villes_data = {
    "Tokyo": {
        "nom": "Tokyo",
        "latitude": 35.6762,
        "longitude": 139.6503,
        "description": "Capitale du Japon, mégapole vibrante et centre économique",
        "population": "~14 millions",
        "attractions": ["Tour de Tokyo", "Senso-ji", "Shibuya Crossing", "Palais Impérial"],
        "informations_supp": {
            "climat": "Subtropical humide",
            "meilleure_saison": "Printemps (mars-mai)",
            "specialites": "Sushi, Ramen, Tempura"
        }
    },
    "Hakone": {
        "nom": "Hakone",
        "latitude": 35.2324,
        "longitude": 139.1063,
        "description": "Station thermale dans les montagnes, vue sur le Mont Fuji",
        "population": "~13,000",
        "attractions": ["Lac Ashi", "Owakudani", "Musée en plein air", "Sources chaudes"],
        "informations_supp": {
            "climat": "Montagnard",
            "meilleure_saison": "Automne pour les couleurs",
            "specialites": "Œufs noirs (Kuro-tamago), Onsen"
        }
    },
    "Kyoto": {
        "nom": "Kyoto",
        "latitude": 35.0116,
        "longitude": 135.7681,
        "description": "Ancienne capitale impériale, cœur culturel du Japon",
        "population": "~1.5 million",
        "attractions": ["Fushimi Inari", "Kinkaku-ji", "Gion", "Kiyomizu-dera"],
        "informations_supp": {
            "climat": "Tempéré",
            "meilleure_saison": "Printemps (cerisiers) et Automne (érables)",
            "specialites": "Kaiseki, Matcha, Yatsuhashi"
        }
    },
    "Nara": {
        "nom": "Nara",
        "latitude": 34.6851,
        "longitude": 135.8048,
        "description": "Ancienne capitale, connue pour ses temples et ses daims",
        "population": "~350,000",
        "attractions": ["Todai-ji", "Parc de Nara", "Daibutsu", "Kasuga-taisha"],
        "informations_supp": {
            "climat": "Tempéré",
            "meilleure_saison": "Printemps",
            "specialites": "Kaki-no-hazushi (sushi au persimmon)"
        }
    },
    "Osaka": {
        "nom": "Osaka",
        "latitude": 34.6937,
        "longitude": 135.5023,
        "description": "Ville dynamique connue pour sa cuisine et son château",
        "population": "~2.7 millions",
        "attractions": ["Château d'Osaka", "Dotonbori", "Universal Studios", "Umeda Sky Building"],
        "informations_supp": {
            "climat": "Subtropical humide",
            "meilleure_saison": "Printemps et Automne",
            "specialites": "Takoyaki, Okonomiyaki, Kushikatsu"
        }
    },
    "Hiroshima": {
        "nom": "Hiroshima",
        "latitude": 34.3853,
        "longitude": 132.4553,
        "description": "Ville historique, symbole de paix et de reconstruction",
        "population": "~1.2 million",
        "attractions": ["Mémorial de la Paix", "Dôme de Genbaku", "Miyajima", "Château d'Hiroshima"],
        "informations_supp": {
            "climat": "Subtropical humide",
            "meilleure_saison": "Printemps",
            "specialites": "Okonomiyaki d'Hiroshima, Huîtres"
        }
    }
}

# Itinéraire
itineraire = ["Tokyo", "Hakone", "Kyoto", "Nara", "Osaka", "Hiroshima", "Tokyo"]

def generate_map_html() -> str:
    """Génère le HTML complet de la carte interactive"""
  
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Carte Interactive du Japon - Japan Inside</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
   <link rel="stylesheet" href="static/style.css" />
</head>
<body>

<!-- Titre de la carte -->
<div class="map-title">
    <h1>🇯🇵 Japan Inside - Itinéraire au Japon</h1>
    <p>Tokyo → Hakone → Kyoto → Nara → Osaka → Hiroshima → Tokyo</p>
</div>

<!-- Carte -->
<div id="map"></div>

<!-- Panneau d'information -->
<div id="infoPanel" class="info-panel">
    <div class="info-header">
        <h3 id="villeTitle"></h3>
        <span class="close-btn" onclick="closeInfoPanel()">×</span>
    </div>
    <div id="villeContent" class="ville-details"></div>
</div>

<!-- Légende -->
<div class="legende">
    <h4>📋 LÉGENDE DES VILLES</h4>
    <div class="legende-item">
        <div class="color-dot" style="background-color: #ff4444;"></div>
        <span>Tokyo (Départ/Arrivée)</span>
    </div>
    <div class="legende-item">
        <div class="color-dot" style="background-color: #4444ff;"></div>
        <span>Hakone (Étape 2)</span>
    </div>
    <div class="legende-item">
        <div class="color-dot" style="background-color: #44cc44;"></div>
        <span>Kyoto (Étape 3)</span>
    </div>
    <div class="legende-item">
        <div class="color-dot" style="background-color: #ffa500;"></div>
        <span>Nara (Étape 4)</span>
    </div>
    <div class="legende-item">
        <div class="color-dot" style="background-color: #aa44ff;"></div>
        <span>Osaka (Étape 5)</span>
    </div>
    <div class="legende-item">
        <div class="color-dot" style="background-color: #cc0000;"></div>
        <span>Hiroshima (Étape 6)</span>
    </div>
</div>
<script src="/static/script.js"></script>

</body>
</html>
"""

def generate_japan_map(output_path: str = None) -> str:
    """
    Génère la carte du Japon et la sauvegarde si un chemin est fourni
    Retourne le HTML généré
    """
    html_content = generate_map_html()

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Carte sauvegardée à : {output_path}")

    return html_content

if __name__ == "__main__":
    # Test : générer et sauvegarder la carte
    generate_japan_map("carte_japon_test.html")
    print("Carte générée avec succès !")