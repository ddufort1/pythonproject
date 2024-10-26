const ctx = document.getElementById('myChart');

fetch('cap_wikichg.json')
.then(function(response){
    if (response.ok == true){
        return response.json();
        }
})
.then(function(data){
//    console.log(data);
    createChart(data, 'line');
});
            
                          
function createChart(data, type) {      
    new Chart(ctx, {
        type: type,
        data: {
            labels: data.map(row => row.Year),
            datasets: [{
                label: '# Mod Count',
                data: data.map(row => row.Mod_Ct),
                borderWidth: 1
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
  }    
