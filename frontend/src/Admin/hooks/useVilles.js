import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import * as villeService from "../services/villeService";

export const useVilles = () => {
  const [villes, setVilles] = useState([]);

  const fetchVilles = async () => {
    try {
      setVilles(await villeService.getVilles());
    } catch {
      toast.error("Erreur lors du chargement des villes");
    }
  };

  const deleteVille = async (id) => {
    if (!window.confirm("Supprimer cette ville ?")) return;
    await villeService.deleteVilleById(id);
    setVilles(villes.filter(v => v.id !== id));
    toast.success("Ville supprimée !");
  };

  const moveVille = async (index, direction) => {
    const newVilles = [...villes];
    const target = index + direction;
    if (target < 0 || target >= newVilles.length) return;

    [newVilles[index], newVilles[target]] = [newVilles[target], newVilles[index]];
    await villeService.reorderVilles(
      newVilles.map((v, i) => ({ id: v.id, position: i + 1 }))
    );
    setVilles(newVilles);
    toast.success("Ordre mis à jour !");
  };

  useEffect(() => {
    fetchVilles();
  }, []);

  return { villes, fetchVilles, deleteVille, moveVille };
};
