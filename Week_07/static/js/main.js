// ---- Heatmap grid (Booking Forecast) ----
// Replace `values` with your real day-of-week intensity data (0-1 scale).
document.addEventListener("DOMContentLoaded", () => {
  const heatmap = document.getElementById("heatmapForecast");
  if (!heatmap) return;
 
  const rows = 7;   // e.g. weeks
  const cols = 7;   // Sun..Sat
  const values = Array.from({ length: rows * cols }, () => Math.random());
 
  values.forEach((v) => {
    const cell = document.createElement("div");
    cell.className = "cell";
    cell.style.opacity = (0.25 + v * 0.75).toFixed(2);
    heatmap.appendChild(cell);
  });
});
 
// ---- Your existing chart code goes here ----
// Target these canvas ids with Chart.js (or whatever lib you already use):
//   chartBookingTrends, chartHotelType, chartTopCountries,
//   chartRevenuePerformance, chartGuestDemographics, chartBookingForecast

// statistical charts

