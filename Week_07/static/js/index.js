new Chart(document.getElementById("bookingTrendChart"),{

type:"line",

data:{
labels:monthly_labels,
datasets:[{
label:"Bookings",
data:monthly_values,
borderColor:"#2563EB",
backgroundColor:"rgba(37,99,235,.18)",
fill:true,
tension:.4
}]
},

options:{
responsive:true,
plugins:{legend:{display:false}}
}

});


new Chart(document.getElementById("revenueTrendChart"),{

type:"line",

data:{
labels:revenue_labels,
datasets:[{
label:"Revenue",
data:revenue_values,
borderColor:"#16A34A",
backgroundColor:"rgba(22,163,74,.18)",
fill:true,
tension:.4
}]
},

options:{
responsive:true,
plugins:{legend:{display:false}}
}

});

new Chart(document.getElementById("seasonChart"),{

type:"radar",

data:{
labels:season_labels,
datasets:[{
data:season_values,
backgroundColor:"rgba(245,158,11,.25)",
borderColor:"#F59E0B",
borderWidth:2
}]
},

options:{
responsive:true,
plugins:{legend:{display:false}}
}

});


new Chart(document.getElementById("sourceChart"),{

type:"bar",

data:{

labels:source_labels,

datasets:[{

label:"Bookings",

data:source_values,

backgroundColor:[
"#2563EB",
"#10B981",
"#F59E0B",
"#EF4444"
]

}]

},

options:{

responsive:true,

indexAxis:"y",

plugins:{

legend:{display:false}

}

}

});



new Chart(document.getElementById("depositChart"),{

type:"line",

data:{

labels:deposit_labels,

datasets:[{

data:deposit_values,

fill:true,

backgroundColor:"rgba(16,185,129,.2)",

borderColor:"#10B981",

tension:.4,

borderWidth:3

}]

},

options:{

responsive:true,

plugins:{

legend:{display:false}

}

}

});




// hotel type distribution

new Chart(document.getElementById("hotelTypeChart"),{

type:"bar",

data:{

labels:hotel_type_labels,

datasets:[{

data:hotel_type_values,

backgroundColor:[
"#3B82F6",
"#10B981"
]

}]

},

options:{

responsive:true,

plugins:{

legend:{
display:false
}

}

}

});

// booking value segment


new Chart(document.getElementById("bookingValueChart"),{

type:"polarArea",

data:{

labels:booking_segment_labels,

datasets:[{

data:booking_segment_values,

backgroundColor:[
"#3B82F6",
"#10B981",
"#F59E0B",
"#EF4444",
"#8B5CF6"
]

}]

},

options:{

responsive:true,

plugins:{

legend:{
position:"bottom"
}

}

}

});


// average adr by hotel

new Chart(document.getElementById("adrHotelChart"),{

type:"bar",

data:{

labels:adr_hotel_labels,

datasets:[{

label:"Average ADR",

data:adr_hotel_values,

backgroundColor:[
"#6366F1",
"#EC4899"
],

borderRadius:12

}]

},

options:{

indexAxis:"y",

responsive:true,

plugins:{
legend:{display:false}
},

scales:{
x:{beginAtZero:true}
}

}

});


new Chart(document.getElementById("scatterChart"),{

type:"scatter",

data:{

datasets:[{

label:"Bookings",

data:scatter_data,

backgroundColor:"rgba(59,130,246,.65)",

pointRadius:4,

pointHoverRadius:7

}]

},

options:{

responsive:true,

plugins:{

legend:{display:false}

},

scales:{

x:{

title:{

display:true,

text:"Lead Time (Days)"

}

},

y:{

title:{

display:true,

text:"Average Daily Rate ($)"

}

}

}

}

});

// Booking Status Distribution

new Chart(document.getElementById("statusChart"),{

type:"bar",

data:{
labels:status_labels,
datasets:[{
data:status_values,
backgroundColor:"#10B981",
borderRadius:10
}]
},

options:{
indexAxis:"y",
responsive:true,
plugins:{
legend:{display:false}
}
}

});

//monthly cancellation trend

new Chart(document.getElementById("cancelChart"),{

type:"line",

data:{

labels:cancel_labels,

datasets:[{

data:cancel_values,

borderColor:"#EF4444",

backgroundColor:"rgba(239,68,68,.2)",

fill:true,

tension:.4

}]

},

options:{

responsive:true,

plugins:{
legend:{display:false}
}

}

});

// Top Guest Countries

new Chart(document.getElementById("guestCountryChart"),{

type:"bar",

data:{

labels:guest_country_labels,

datasets:[{

label:"Bookings",

data:guest_country_values,

backgroundColor:"#3B82F6",

borderRadius:10

}]

},

options:{

responsive:true,

plugins:{
legend:{display:false}
},

scales:{
y:{beginAtZero:true}
}

}

});

// booking js by customer type

new Chart(document.getElementById("bookingChangeChart"),{

type:"line",

data:{

labels:booking_change_labels,

datasets:[{

label:"Average Changes",

data:booking_change_values,

borderColor:"#3B82F6",

backgroundColor:"rgba(59,130,246,.2)",

fill:true,

tension:.4

}]

},

options:{

responsive:true

}

});


// lead time category distribution

new Chart(document.getElementById("leadCategoryChart"),{

type:"bubble",

data:{

datasets:[

{
label:lead_category_labels[0],
data:[{x:1,y:lead_category_values[0],r:15}],
backgroundColor:"#3B82F6"
},

{
label:lead_category_labels[1],
data:[{x:2,y:lead_category_values[1],r:20}],
backgroundColor:"#10B981"
},

{
label:lead_category_labels[2],
data:[{x:3,y:lead_category_values[2],r:25}],
backgroundColor:"#F59E0B"
},

{
label:lead_category_labels[3],
data:[{x:4,y:lead_category_values[3],r:30}],
backgroundColor:"#EF4444"
}

]

},

options:{

responsive:true,

plugins:{
legend:{position:"bottom"}
}

}

});