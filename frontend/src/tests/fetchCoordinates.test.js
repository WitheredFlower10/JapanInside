// src/tests
import { fetchCoordinatesFromNominatim } from "../Admin/services/geocodingService.js";

describe("fetchCoordinatesFromNominatim", () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it("should return coordinates when API returns data", async () => {
    const mockResponse = [
      { lat: "35.6895", lon: "139.6917" } 
    ];
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    const coords = await fetchCoordinatesFromNominatim("Tokyo");

    expect(coords).toEqual({
      latitude: 35.6895,
      longitude: 139.6917,
    });

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("Tokyo"),
      expect.any(Object)
    );
  });

  it("should return null if API returns empty array", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    const coords = await fetchCoordinatesFromNominatim("UnknownPlace");
    expect(coords).toBeNull();
  });
});
