document.getElementById('order-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const weight = parseFloat(document.getElementById('weight').value);
    const length = parseFloat(document.getElementById('length').value);
    const width = parseFloat(document.getElementById('width').value);
    const height = parseFloat(document.getElementById('height').value);
    const useAutoVolume = document.getElementById('use_auto_volume').checked;

    let volume = parseFloat(document.getElementById('volume').value);
    if (useAutoVolume || isNaN(volume)) {
        volume = length * width * height;
        document.getElementById('volume').value = volume.toFixed(2);
    }

    const destination = document.getElementById('destination').value;

    fetch('/calculate_shipping', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ weight: weight, length: length, width: width, height: height, volume: volume, destination: destination, use_auto_volume: useAutoVolume }),
    })
    .then(response => response.json())
    .then(data => {
        const cheapestOption = data.cheapest_option;
        const cheapestCost = data.cheapest_cost.toFixed(2);
        const costs = data.costs;
        let detailedCosts = '';
        for (const [key, value] of Object.entries(costs)) {
            detailedCosts += `${key}: ${value.toFixed(2)}<br>`;
        }
        document.getElementById('result').innerHTML = `
            <strong>Cheapest Option:</strong> ${cheapestOption}<br>
            <strong>Cheapest Cost:</strong> €${cheapestCost}<br>
            <strong>Detailed Costs:</strong><br>${detailedCosts}
        `;
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('use_auto_volume').addEventListener('change', function(e) {
    document.getElementById('volume').disabled = e.target.checked;
    if (e.target.checked) {
        const length = parseFloat(document.getElementById('length').value);
        const width = parseFloat(document.getElementById('width').value);
        const height = parseFloat(document.getElementById('height').value);
        const volume = length * width * height;
        document.getElementById('volume').value = volume.toFixed(2);
    }
});
