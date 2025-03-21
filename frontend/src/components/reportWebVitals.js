// src/reportWebVitals.js
const reportWebVitals = (metric) => {
  // Log the metric to the console
  console.log(metric);

  // Example: Sending data to Google Analytics (or another service)
  // If you want to track performance in an analytics platform
  if (window.gtag) {
    window.gtag('event', 'web_vitals', {
      event_category: 'performance',
      event_label: metric.name,
      value: metric.value,
    });
  }
};

export default reportWebVitals;
