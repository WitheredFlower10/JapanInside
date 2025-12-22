export const getVilles = () =>
  fetch("/api/villes").then(res => res.json());

export const createVille = (ville) =>
  fetch("/api/villes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ville),
  });

export const updateVille = (id, ville) =>{
       console.log(ville)
        fetch(`/api/villes/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ville),
  });
}
 
 

export const deleteVilleById = (id) =>
  fetch(`/api/villes/${id}`, { method: "DELETE" });

export const reorderVilles = (payload) =>
  fetch("/api/villes/reorder", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

export const flushAndInsertTemplate = async () => {
  await fetch("/api/flushDB", { method: "POST" });
  await fetch("/api/insertDATA", { method: "POST" });
};
