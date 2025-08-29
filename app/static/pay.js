// pay.js - XSS detection payload
// This script is loaded to detect successful XSS exploitation
console.log('x');

// Additional detection markers
if (typeof notifyXSS === 'function') {
    notifyXSS();
}

// Alternative detection method
if (window.reportTriggered) {
    window.reportTriggered();
}