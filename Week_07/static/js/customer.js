new Chart(document.getElementById("customerTypeChart"),{

type:"bar",

data:{

labels:customer_type_labels,

datasets:[{

label:"Customers",

data:customer_type_values,

backgroundColor:[
"#3B82F6",
"#10B981",
"#F59E0B",
"#EF4444"
],

borderRadius:8

}]

},

options:{

responsive:true,

indexAxis:"y",

plugins:{

legend:{

display:false

}

},

scales:{

x:{

beginAtZero:true

}

}

}

});



// ============================
// Repeat Guest (Radar)
// ============================

const ctx = document.getElementById("repeatGuestChart");

new Chart(ctx, {

type: "bar",

data: {

labels: repeat_labels,

datasets: [

{

type: "line",

data: repeat_values,

borderColor: "#3B82F6",

borderWidth: 2,

pointRadius: 8,

pointHoverRadius: 10,

fill: false

},

{

type: "bar",

data: repeat_values,

backgroundColor: "#3B82F6",

barThickness: 4

}

]

},

options: {

plugins: {

legend: {

display: false

}

},

responsive: true,

scales: {

y: {

beginAtZero: true

}

}

}

});

// ============================
// Guest Demographics
// ============================

new Chart(document.getElementById("guestChart"),{

type:"bar",

data:{

labels:guest_labels,

datasets:[{

label:"Guests",

data:guest_values,

backgroundColor:[
"#3B82F6",
"#10B981",
"#F59E0B"
]

}]

},

options:{

responsive:true,

plugins:{

legend:{display:false}

}

}

});


// ============================
// Special Requests
// ============================

new Chart(document.getElementById("specialChart"),{

type:"line",

data:{

labels:special_labels,

datasets:[{

label:"Bookings",

data:special_values,

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




new Chart(document.getElementById("countryChart"), {

    data: {

        labels: country_labels,

        datasets: [

        {
            type: "bar",

            label: "Bookings",

            data: country_values,

            backgroundColor: "#60A5FA",

            borderRadius: 8,

            order: 2
        },

        {
            type: "line",

            label: "Trend",

            data: country_values,

            borderColor: "#EF4444",

            backgroundColor: "#EF4444",

            borderWidth: 3,

            tension: 0.4,

            pointRadius: 5,

            pointHoverRadius: 7,

            fill: false,

            order: 1
        }

        ]

    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                position: "top"

            }

        },

        scales: {

            y: {

                beginAtZero: true,

                title: {

                    display: true,

                    text: "Bookings"

                }

            },

            x: {

                title: {

                    display: true,

                    text: "Countries"

                }

            }

        }

    }

});



new Chart(document.getElementById("bookingValueChart"),{

type:"treemap",

data:{

datasets:[{

tree:value_labels.map((label,i)=>({

label:label,

value:value_values[i]

})),

key:"value",

groups:["label"],

borderWidth:1,

spacing:2

}]

},

options:{

responsive:true,

plugins:{

legend:{display:false}

}

}

});


// ==========================================
// Customer Loyalty Status
// ==========================================

new Chart(document.getElementById("loyaltyChart"),{

type:"bar",

data:{

labels:loyalty_labels,

datasets:[

{

label:"New Guests",

data:new_guest_values,

backgroundColor:"#3B82F6"

},

{

label:"Repeat Guests",

data:repeat_guest_values,

backgroundColor:"#10B981"

}

]

},

options:{

indexAxis:"y",

responsive:true,

plugins:{

legend:{

position:"bottom"

}

},

scales:{

x:{

stacked:true,

beginAtZero:true

},

y:{

stacked:true

}

}

}

});

// lead time distribution

new Chart(document.getElementById("stayDurationChart"), {

    type: "polarArea",

    data: {

        labels: stay_labels,

        datasets: [{

            data: stay_values,

            backgroundColor: [

                "#3B82F6",
                "#10B981",
                "#F59E0B"

            ],

            borderColor: "#ffffff",

            borderWidth: 2

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false,

        plugins: {

            legend: {

                position: "bottom"

            }

        }

    }

});