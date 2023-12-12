// Version: 1.0
// Date: 2021-05-31
// Description: Script voor het programma

// Chart.js
// https://www.chartjs.org/docs/latest/getting-started/installation.html
// https://www.chartjs.org/docs/latest/charts/bar.html
// https://www.chartjs.org/docs/latest/charts/line.html

  const ctx = document.getElementById('Weerstand_Chart_1');

  const Weerstand_Chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange', 'test', "test 2",'Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange', 'test', "test 2"],
      datasets: [{
        label: 'weerstand over tijd',
        data: [12, 19, 3, 5, 70, 3, 4, 30,12, 19, 3, 5, 2, 3, 4, 30],
        borderWidth: 1,
        borderColor: 'black',
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  // Grafiek 2
const ctx2 = document.getElementById('Weerstand_Chart_2');

const Weerstand_Chart_2 = new Chart(ctx2, {
  type: 'line',
  data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange', 'test', "test 2",'Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange', 'test', "test 2"],
    datasets: [{
      label: 'hoek over tijd',
      data: [12, 19, 3, 5, 2, 3, 4, 30,12, 19, 12, 50, 2, 30, 4, 30],
      borderWidth: 1,
      borderColor: 'black',
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

// Grafiek 3
const ctx3 = document.getElementById('Weerstand_Chart_3');

const Weerstand_Chart_3 = new Chart(ctx3, {
  type: 'line',
  data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange', 'test', "test 2",'Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange', 'test', "test 2"],
    datasets: [{
      label: 'nog iets over tijd',
      data: [12, 19, 3, 5, 2, 3, 4, 30,12, 19, 3, 5, 2, 3, 4, 30],
      borderWidth: 1,
      borderColor: 'black',
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});


// 
  