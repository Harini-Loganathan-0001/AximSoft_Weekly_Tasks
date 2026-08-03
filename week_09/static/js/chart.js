document.addEventListener("DOMContentLoaded", function(){


const models = window.optimizationModels;

const accuracy = window.optimizationAccuracy;



new Chart(
document.getElementById("optimizationAccuracyChart"),

{

type:"bar",


data:{


labels:models,


datasets:[{


label:"Test Accuracy (%)",


data:accuracy,


backgroundColor:[

"#2563EB",
"#16A34A",
"#F59E0B",
"#DC2626",
"#9333EA",
"#0891B2",
"#DB2777",
"#65A30D"

],


borderRadius:10,


borderWidth:1


}]


},


options:{


responsive:true,


plugins:{


legend:{


display:false


},


title:{


display:true,

text:"Optimization Accuracy Comparison"


}


},



scales:{


x:{


title:{


display:true,

text:"Models"


},


ticks:{


display:false

}


},



y:{


title:{


display:true,

text:"Accuracy (%)"


},


beginAtZero:true,


max:100


}


}



}


}


);



});