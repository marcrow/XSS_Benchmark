// Example function to report test result for a scenario/payload
function reportXssResult(scenarioId, payloadId, wasTriggered) {
    let url, method, data;
    if (wasTriggered) {
        url = '/results/report';
        method = 'POST';
        data = new URLSearchParams({
            scenario_id: scenarioId,
            payload_id: payloadId
        });
    } else {
        url = '/results/report_not_triggered';
        method = 'POST';
        data = new URLSearchParams({
            scenario_id: scenarioId,
            payload_id: payloadId
        });
    }

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: data
    })
    .then(response => response.text())
    .then(text => {
        console.log('Report response:', text);
    })
    .catch(error => {
        console.error('Error reporting XSS result:', error);
    });
}

// Example usage after running a test:
function onTestComplete(scenarioId, payloadId, xssDetected) {
    reportXssResult(scenarioId, payloadId, xssDetected);
    // ...your existing logic for updating UI or polling scoreboard
}