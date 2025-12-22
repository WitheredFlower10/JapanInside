import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import * as villeService from "../services/villeService";

export const useVilles = () => {
  const [villes, setVilles] = useState([]);
  const fetchVilles = async () => {
    try {
      const data = await villeService.getVilles();
      setVilles(data);
    } catch {
      toast.error("Erreur lors du chargement des villes");
    }
  };

  const deleteVille = async (id) => {
    if (!window.confirm("Supprimer cette ville ?")) return;
    await villeService.deleteVilleById(id);
    setVilles((prev) => prev.filter((v) => v.id !== id));
    toast.success("Ville supprimée !");
  };

  const moveVille = async (index, direction) => {
    setVilles((prev) => {
      const newVilles = [...prev];
      const target = index + direction;
      if (target < 0 || target >= newVilles.length) return prev;

      [newVilles[index], newVilles[target]] = [newVilles[target], newVilles[index]];
      villeService.reorderVilles(
        newVilles.map((v, i) => ({ id: v.id, position: i + 1 }))
      ).then(() => toast.success("Ordre mis à jour !"));
      return newVilles;
    });
  };

  useEffect(() => {
    const fetchData = async () => {
      await fetchVilles();
    };
    fetchData();
  }, []);

  return { villes, fetchVilles, deleteVille, moveVille };
};
