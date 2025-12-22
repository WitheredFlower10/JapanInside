export const fetchCoordinatesFromNominatim = async (query) => {
  const res = await fetch(
    `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=1`,
    {
      headers: {
        Accept: "application/json",
        "User-Agent": "JapanInsideAdmin/1.0",
      },
    }
  );

  const data = await res.json();
  if (!data || data.length === 0) return null;

  return {
    latitude: parseFloat(data[0].lat),
    longitude: parseFloat(data[0].lon),
  };
};
