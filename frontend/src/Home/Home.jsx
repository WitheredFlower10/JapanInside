import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import Map from "./components/Map/Map.jsx";
import VilleInfoPanel from "./components/VilleInfoPanel.jsx";
import SpecialitesModal from "./components/SpecialitesModal.jsx";
import "./home.css";

const Home = () => {
  const [ville, setVille] = useState(null);
  const [villes, setVilles] = useState([]);
  const [showSpecialitesModal, setShowSpecialitesModal] = useState(false);
  const [specialitesJP, setSpecialitesJP] = useState([]);

 

  const onVilleClick = useCallback((nom) => {
    if (!nom) return setVille(null);

    fetch(`/api/villes/${nom}`)
      .then((res) => res.ok ? res.json() : Promise.reject("Ville non trouvée"))
      .then((data) => setVille({ ...data }))
      .catch((err) => setVille({ nom, error: err.toString() }));
  }, []);

useEffect(() => {
  const fetchVilles = async () => {
    try {
      const res = await fetch("/api/villes");
      const data = await res.json();
      setVilles(data);
    } catch (err) {
      console.error("Erreur récupération villes :", err);
    }
  };

  fetchVilles();
}, []);

  useEffect(() => {
    const fetchSpecialites = async () => {
      try {
        const res = await fetch("https://www.themealdb.com/api/json/v1/1/filter.php?a=japanese");
        const data = await res.json();
        setSpecialitesJP(data.meals || []);
      } catch (err) {
        console.error("Erreur chargement spécialités :", err);
      }
    };
    fetchSpecialites();
  }, []);

  return (
    <>
      <SpecialitesModal show={showSpecialitesModal} onClose={() => setShowSpecialitesModal(false)} specialites={specialitesJP} />
      <Map villes={villes} onVilleClick={onVilleClick} />
      <VilleInfoPanel ville={ville} onClose={() => setVille(null)} />

      <div className="ui-overlay">
        <button className="specialites-btn" onClick={() => setShowSpecialitesModal(true)}>Spécialités Japonaises</button>
    <Link
          to={'/admin'}
          className="admin-btn"
        >
          Administration
        </Link>
      </div>

      <div className="map-title">
        <h1>🇯🇵 Japan Inside - Itinéraire au Japon</h1>
        <p>{villes.map((v) => v.nom).join(" → ")}</p>
      </div>
    </>
  );
};

export default Home;
