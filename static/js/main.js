// Runs when page loads
document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('categoryChart');
    if (!canvas) return; // Only run on dashboard page

    // Get expense data from the table
    const rows = document.querySelectorAll('tbody tr');
    const categoryTotals = {};

    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length < 6) return;

        const category = cells[1].textContent.trim();
        const amount = parseFloat(cells[4].textContent.trim());

        if (!isNaN(amount)) {
            categoryTotals[category] = (categoryTotals[category] || 0) + amount;
        }
    });

    const labels = Object.keys(categoryTotals);
    const data = Object.values(categoryTotals);

    // Draw bar chart
    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Amount Spent (₹)',
                data: data,
                backgroundColor: [
                    '#4e79a7', '#f28e2b', '#e15759',
                    '#76b7b2', '#59a14f', '#edc948',
                    '#b07aa1', '#ff9da7'
                ],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => '₹' + value
                    }
                }
            }
        }
    });
});