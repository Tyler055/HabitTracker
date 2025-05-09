const quotes = [
  "Believe you can and you're halfway there.",
  "Don't watch the clock; do what it does. Keep going.",
  "Success is the sum of small efforts repeated daily.",
  "The secret to getting ahead is getting started."
];

let quoteIndex = 0;
function showNextQuote() {
  const quoteBox = document.getElementById("motivational-quote");
  quoteBox.style.opacity = 0;

  setTimeout(() => {
    quoteBox.textContent = quotes[quoteIndex];
    quoteBox.style.opacity = 1;
    quoteIndex = (quoteIndex + 1) % quotes.length;
  }, 500);
}

// Cycle every 10 seconds
showNextQuote();
setInterval(showNextQuote, 10000);
