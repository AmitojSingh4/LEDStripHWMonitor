const si = require('systeminformation');
si.cpuTemperature().then(data => console.log(data));

//Returned Values
// {
//     main: null,
//     cores: [],
//     max: null,
//     socket: [],
//     chipset: null,
// }
//https://systeminformation.io/cpu.html
//Known issue