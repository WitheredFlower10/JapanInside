import VilleItem from "./VilleItem";

export default function VilleList({ villes, ...actions }) {
  return (
    <div className="ville-list">
      {villes.map((ville, index) => (
        <VilleItem key={ville.id} ville={ville} index={index} {...actions} />
      ))}
    </div>
  );
}
