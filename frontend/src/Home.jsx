import { useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./mapStyle.css";

const Home = () => {
  useEffect(() => {
    // Initialisation de la carte centrée sur le Japon
    const map = L.map('map').setView([36.2048, 138.2529], 6);

    // Ajout des tuiles OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap',
      maxZoom: 12,
      minZoom: 5
    }).addTo(map);

    // Limiter la vue au Japon
    map.setMaxBounds([[30, 128], [46, 146]]);

    // Données des villes
    const villes = {
      Tokyo: { lat: 35.6762, lon: 139.6503, color: "red", etape: 1, icon: "🏙️" },
      Hakone: { lat: 35.2324, lon: 139.1063, color: "blue", etape: 2, icon: "🏔️" },
      Kyoto: { lat: 35.0116, lon: 135.7681, color: "green", etape: 3, icon: "🏯" },
      Nara: { lat: 34.6851, lon: 135.8048, color: "orange", etape: 4, icon: "🦌" },
      Osaka: { lat: 34.6937, lon: 135.5023, color: "purple", etape: 5, icon: "🏰" },
      Hiroshima: { lat: 34.3853, lon: 132.4553, color: "darkred", etape: 6, icon: "☮️" }
    };

    const itineraire = ["Tokyo", "Hakone", "Kyoto", "Nara", "Osaka", "Hiroshima", "Tokyo"];

    // Fonction pour fermer le panneau d'information
    const closeInfoPanel = () => {
      const panel = document.getElementById("infoPanel");
      if (panel) panel.style.display = "none";
    };

    // Fonction pour afficher les détails d'une ville
    const onVilleClick = (nom) => {
      fetch(`/api/villes/${nom}`)
        .then(res => {
          if (!res.ok) throw new Error('Ville non trouvée');
          return res.json();
        })
        .then(data => {
          document.getElementById("villeTitle").textContent = `${data.nom} ${villes[nom].icon}`;
          let content = `
            <p><strong>Description:</strong> ${data.description}</p>
            <p><strong>Population:</strong> ${data.population}</p>
            <p><strong>Étape ${villes[nom].etape} sur 6</strong></p>
            <div class="info-grid">
              <div class="info-item">
                <strong>📍 Coordonnées</strong> ${data.latitude.toFixed(4)}°N, ${data.longitude.toFixed(4)}°E
              </div>
          `;
          if (data.informations_supp) {
            content += `
              <div class="info-item"><strong>🌤️ Climat</strong> ${data.informations_supp.climat}</div>
              <div class="info-item"><strong>🌸 Meilleure saison</strong> ${data.informations_supp.meilleure_saison}</div>
              <div class="info-item"><strong>🍜 Spécialités</strong> ${data.informations_supp.specialites}</div>
            `;
          }
          console.log(nom.toLowerCase());
         
          content += `</div>
            <p><strong>🏛️ Attractions principales:</strong></p>
            <ul class="attractions-list">${data.attractions.map(attr => `<li>${attr}</li>`).join('')}</ul>
            <a class="action-btn" href=/ville/${nom.toLowerCase()}>
              <i class="fas fa-external-link-alt"></i> Voir la page complète
            </a>
          `;
          document.getElementById("villeContent").innerHTML = content;
          document.getElementById("infoPanel").style.display = "block";
          map.setView([villes[nom].lat, villes[nom].lon], 10);
        })
        .catch(err => {
          document.getElementById("villeTitle").textContent = nom;
          document.getElementById("villeContent").innerHTML = `<p>Impossible de charger les détails de la ville.</p><p>Erreur: ${err.message}</p>`;
          document.getElementById("infoPanel").style.display = "block";
        });
    };

    // Création des marqueurs et itinéraire
    const points = [];
    Object.keys(villes).forEach(ville => {
      const v = villes[ville];
      points.push([v.lat, v.lon]);

      const icon = L.icon({
        iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${v.color}.png`,
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [30, 46],
        iconAnchor: [15, 46],
        popupAnchor: [0, -46]
      });

      const marker = L.marker([v.lat, v.lon], { icon, title: ville }).addTo(map);
      marker.bindPopup(`<div class="custom-popup"><div class="popup-title">${ville} ${v.icon}</div><div>Étape ${v.etape} du voyage</div><div class="popup-etape">Cliquez pour plus d'infos</div></div>`);
      marker.on('click', () => onVilleClick(ville));
    });

    L.polyline(points, { color: "#667eea", weight: 4, opacity: 0.8, dashArray: "10, 10", lineCap: 'round' }).addTo(map);

    // clic sur la carte ferme le panneau
    map.on('click', closeInfoPanel);

    // flèches et contour du Japon peuvent être ajoutés ici...
return () => {
    map.remove();
  };
  }, []);

  return (
    <>
      <div className="map-title">
        <h1>🇯🇵 Japan Inside - Itinéraire au Japon</h1>
        <p>Tokyo → Hakone → Kyoto → Nara → Osaka → Hiroshima → Tokyo</p>
      </div>
      <div id="map" style={{ width: "100vw", height: "100vh" }}></div>

      <div id="infoPanel" className="info-panel">
        <div className="info-header">
          <h3 id="villeTitle"></h3>
          <span className="close-btn" onClick={() => document.getElementById("infoPanel").style.display = "none"}>×</span>
        </div>
        <div id="villeContent" className="ville-details"></div>
      </div>
    </>
  );
};

export default Home;
