// reportWebVitals.js (with CommonJS require)
const reportWebVitals = (metric) => {
  console.log(metric);

  // Example: Sending data to Google Analytics (or another service)
  if (window.gtag) {
    window.gtag('event', 'web_vitals', {
      event_category: 'performance',
      event_label: metric.name,
      value: metric.value,
    });
  }
};

module.exports = reportWebVitals;
