const revenueCtx=document.getElementById("revenueTrendChart");

if(revenueCtx){

new Chart(revenueCtx,{

type:"line",

data:{

labels:revenueLabels,

datasets:[{

label:"Revenue",

data:revenueValues,

borderColor:"#2563EB",

backgroundColor:"rgba(37,99,235,0.15)",

fill:true,

tension:0.4,

pointRadius:5,

pointHoverRadius:7

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

plugins:{

legend:{

display:false

}

},

scales:{

y:{

beginAtZero:true,

title:{

display:true,

text:"Revenue"

}

},

x:{

title:{

display:true,

text:"Month"

}

}

}

}

});

}


const adrCtx=document.getElementById("adrChart");

if(adrCtx){

new Chart(adrCtx,{

type:"bar",

data:{

labels:adrLabels,

datasets:[{

data:adrValues,

backgroundColor:[

"#2563EB",

"#06B6D4"

],

borderRadius:8

}]

},

options:{

indexAxis:"y",

responsive:true,

maintainAspectRatio:false,

plugins:{

legend:{display:false}

}

}

});

}


const seasonCtx=document.getElementById("seasonRevenueChart");

if(seasonCtx){

new Chart(seasonCtx,{

type:"doughnut",

data:{

labels:seasonLabels,

datasets:[{

data:seasonValues,

backgroundColor:[

"#22C55E",

"#F59E0B",

"#3B82F6",

"#A855F7"

],

hoverOffset:15

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

cutout:"65%",

plugins:{

legend:{

position:"bottom"

}

}

}

});

}


const stayCtx = document.getElementById("stayChart");

if(stayCtx){

new Chart(stayCtx,{

type:"bar",

data:{

labels:stayLabels,

datasets:[{

data:stayValues,

backgroundColor:[

"#F97316",

"#3B82F6"

],

borderRadius:8

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

plugins:{

legend:{display:false}

}

}

});

}

const marketCtx = document.getElementById("marketChart");

if(marketCtx){

new Chart(marketCtx,{

type:"bar",

data:{

labels:marketLabels,

datasets:[{

data:marketValues,

backgroundColor:"#14B8A6",

borderRadius:8

}]

},

options:{

indexAxis:"y",

responsive:true,

maintainAspectRatio:false,

plugins:{

legend:{display:false}

}

}

});

}


const hotelCtx = document.getElementById("hotelRevenueChart");

if(hotelCtx){

new Chart(hotelCtx,{

type:"polarArea",

data:{

labels:hotelLabels,

datasets:[{

data:hotelValues,

backgroundColor:[

"#2563EB",

"#22C55E"

]

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

plugins:{

legend:{

position:"bottom"

}

}

}

});

}
