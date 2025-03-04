document.addEventListener('DOMContentLoaded', function() {
  // Initialize charts
  const completionChartCtx = document.getElementById('task-completion-chart').getContext('2d');
  const statusChartCtx = document.getElementById('task-status-chart').getContext('2d');
  
  // Create initial charts with default data
  const completionChart = new Chart(completionChartCtx, {
    type: 'line',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [
        {
          label: 'Completed',
          data: [2, 3, 1, 4, 2, 0, 1],
          borderColor: '#28a745',
          backgroundColor: 'rgba(40, 167, 69, 0.1)',
          tension: 0.4
        },
        {
          label: 'In Progress',
          data: [3, 2, 4, 1, 3, 1, 0],
          borderColor: '#ffc107',
          backgroundColor: 'rgba(255, 193, 7, 0.1)',
          tension: 0.4
        },
        {
          label: 'New',
          data: [1, 2, 1, 3, 2, 0, 1],
          borderColor: '#17a2b8',
          backgroundColor: 'rgba(23, 162, 184, 0.1)',
          tension: 0.4
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Task Completion Over Time'
        }
      }
    }
  });
  
  const statusChart = new Chart(statusChartCtx, {
    type: 'doughnut',
    data: {
      labels: ['Completed', 'In Progress', 'New'],
      datasets: [{
        data: [5, 3, 2],
        backgroundColor: [
          '#28a745',
          '#ffc107',
          '#17a2b8'
        ],
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Task Status Distribution'
        }
      }
    }
  });
  
  // Time period filter functionality
  const timePeriodSelect = document.getElementById('time-period');
  
  timePeriodSelect.addEventListener('change', function() {
    const timePeriod = this.value;
    
    // Fetch updated data based on time period
    fetch(`/api/dashboard/stats?time_period=${timePeriod}`)
      .then(response => response.json())
      .then(data => {
        // Update summary numbers
        document.querySelector('.summary-card:nth-child(1) .summary-number').textContent = data.summary.total;
        document.querySelector('.summary-card:nth-child(2) .summary-number').textContent = data.summary.completed;
        document.querySelector('.summary-card:nth-child(3) .summary-number').textContent = data.summary.in_progress;
        document.querySelector('.summary-card:nth-child(4) .summary-number').textContent = data.summary.new;
        
        // Update charts
        completionChart.data.labels = data.chart_data.labels;
        completionChart.data.datasets[0].data = data.chart_data.datasets[0].data;
        completionChart.data.datasets[1].data = data.chart_data.datasets[1].data;
        completionChart.data.datasets[2].data = data.chart_data.datasets[2].data;
        completionChart.update();
        
        // Update status chart
        statusChart.data.datasets[0].data = [
          data.summary.completed,
          data.summary.in_progress,
          data.summary.new
        ];
        statusChart.update();
      })
      .catch(error => {
        console.error('Error fetching dashboard data:', error);
      });
  });
}); 