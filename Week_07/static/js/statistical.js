

const distributionCtx = document.getElementById("distributionChart");

if(distributionCtx){

new Chart(distributionCtx,{

type:"bar",

data:{

labels:distributionLabels,

datasets:[{

label:"Frequency",

data:distributionCounts,

backgroundColor:"#3B82F6",

borderRadius:4

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

x:{

title:{

display:true,

text:"ADR Range"

}

},

y:{

beginAtZero:true,

title:{

display:true,

text:"Number of Bookings"

}

}

}

}

});

}



const normalityCtx = document.getElementById("normalityChart");

if(normalityCtx){

new Chart(normalityCtx,{

type:"bar",

data:{

labels:normalityLabels,

datasets:[{

label:"P-Value",

data:normalityPvalues,

backgroundColor:"#EF4444"

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

text:"P-Value"

}

}

}

}

});

}


const hypothesisCtx=document.getElementById("hypothesisChart");

if(hypothesisCtx){

new Chart(hypothesisCtx,{

type:"bar",

data:{

labels:hypothesisLabels,

datasets:[{

label:"Statistic",

data:hypothesisValues,

backgroundColor:[

"#c92c7a",

"#c92c7a",
"#c92c7a",
"#c92c7a",
"#c92c7a"


],

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

indexAxis:"y",

plugins:{

legend:{display:false}

}

}

});

}


const correlationCtx=document.getElementById("correlationChart");

if(correlationCtx){

new Chart(correlationCtx,{

type:"bar",

data:{

labels:correlationLabels,

datasets:[{

label:"Correlation Coefficient",

data:correlationValues,
backgroundColor:[

"#6919ae",

"#921549"

],

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

plugins:{

legend:{display:false}

},

scales:{

y:{

beginAtZero:true,

max:1

}

}

}

});

}

const confidenceCtx=document.getElementById("confidenceChart");

if(confidenceCtx){

new Chart(confidenceCtx,{

type:"bar",

data:{

labels:confidenceLabels,

datasets:[{

label:"ADR",

data:confidenceValues,

backgroundColor:[

"#f0c361",

"#49b288",

"#2f6876"

]

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

plugins:{

legend:{

display:false

}

}

}

});

}


const decisionCtx=document.getElementById("decisionChart");

if(decisionCtx){

new Chart(decisionCtx,{

type:"doughnut",

data:{

labels:decisionLabels,

datasets:[{

data:decisionValues,

backgroundColor:[

"#30b48a",

"#b95b1c"

],

borderWidth:2

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

cutout:"70%",

plugins:{

legend:{

position:"bottom"

}

}

}

});

}
