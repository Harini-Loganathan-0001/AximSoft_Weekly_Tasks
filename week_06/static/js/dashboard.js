const ctx = document.getElementById("revenueChart");

if (ctx) {

    new Chart(ctx, {

        type: "line",

        data: {

            labels: chartLabels,

            datasets: [{

                label: "Revenue",

                data: chartValues,

                borderColor: "#4F46E5",

                backgroundColor: "rgba(79,70,229,0.2)",

                fill: true,

                tension: 0.4

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

}


/* ==========================
   Payment Donut Chart
========================== */

const paymentCtx = document.getElementById("paymentChart");

if (paymentCtx) {

    new Chart(paymentCtx, {

        type: "doughnut",

        data: {

            labels: paymentLabels,

            datasets: [{

                data: paymentValues,

                backgroundColor: [

                    "#3B82F6",
                    "#d23988",
                    "#F59E0B",
                    "#EF4444",
                    "#8B5CF6"

                ]

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}

/* ==========================
   Top Categories Bar Chart
========================== */

const categoryCtx = document.getElementById("categoryChart");

if (categoryCtx) {

    new Chart(categoryCtx, {

        type: "bar",

        data: {

            labels: categoryLabels,

            datasets: [{

                data: categoryValues,

                borderRadius: 10,

                borderSkipped: false,

                backgroundColor: [

                    "#0ddbbc",
                    "#0ddbbc",
                    "#0ddbbc",
                    "#0ddbbc",
                    "#0ddbbc",
                    "#0ddbbc",
                    "#0ddbbc",
                    "#0ddbbc",
                    "#0ddbbc",
                    "#0ddbbc"

                ]

            }]

        },

        options: {

            indexAxis: "y",

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                x: {

                    grid: {
                        color: "#E5E7EB"
                    },

                    ticks: {

                        callback: function(value) {
                            return "₹ " + (value / 100000).toFixed(1) + "L";
                        },

                        maxRotation: 0,
                        minRotation: 0,

                        font: {
                            size: 12,
                            weight: "bold"
                        }

                    }

                },

                y: {

                    grid: {

                        display: false

                    },

                    ticks: {

                        color: "#111827",

                        font: {

                            size: 11,

                            weight: "bold"

                        }

                    }

                }

            }

        }

    });

}


/* ==========================
   Revenue by State Treemap
========================== */

const treemapCtx = document.getElementById("stateTreemap");

if (treemapCtx) {

    const treeData = stateLabels.map((label, index) => ({
        state: label,
        value: stateValues[index]
    }));

    new Chart(treemapCtx, {

        type: "treemap",

        data: {

            datasets: [{

                tree: treeData,

                key: "value",

                groups: ["state"],

                borderWidth: 2,

                borderColor: "#ffffff",

                spacing: 2,

                backgroundColor(ctx) {

                    const colors = [
                        "#4F46E5",
                        "#5988f7",
                        "#7addfe",
                        "#c049ef",
                        "#390985",
                        "#5922da",
                        "#daa9f8",
                        "#c8c1e6",
                        "#09114d",
                        "#3B82F6"
                    ];

                    return colors[ctx.dataIndex % colors.length];
                },

                labels: {

                    display: true,

                    color: "white",

                    font: {
                        size: 14,
                        weight: "bold"
                    },

                    formatter(ctx) {
                        return ctx.raw.g;
                    }

                }

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            }

        }

    });

}

console.log(stateLabels);
console.log(stateValues);

/* ==========================
   Top Sellers Chart
========================== */

const sellerCtx = document.getElementById("sellerChart");

if (sellerCtx) {

    new Chart(sellerCtx, {

        type: "bar",

        data: {

            labels: sellerLabels,

            datasets: [{

                data: sellerValues,

                backgroundColor: [

                    "#2563EB",
                    "#4F46E5",
                    "#10B981",
                    "#F59E0B",
                    "#EF4444",
                    "#8B5CF6",
                    "#EC4899",
                    "#14B8A6",
                    "#F97316",
                    "#06B6D4"

                ],

                borderRadius: 10

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    ticks: {

                        callback: function(value) {

                            return "₹ " + (value / 100000).toFixed(1) + "L";

                        }

                    }

                },

                x: {

                    ticks: {

                        maxRotation: 0,

                        minRotation: 0

                    }

                }

            }

        }

    });

}


/* ==========================
   Monthly Orders Area Chart
========================== */

const orderCtx = document.getElementById("orderChart");

if (orderCtx) {

    new Chart(orderCtx, {

        type: "line",

        data: {

            labels: orderLabels,

            datasets: [{

                label: "Orders",

                data: orderValues,

                borderColor: "#14B8A6",

                backgroundColor: "rgba(20,184,166,0.25)",

                fill: true,

                tension: 0.4,

                pointRadius: 5,

                pointBackgroundColor: "#14B8A6"

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    display: false

                }

            }

        }

    });

}



/* ==========================
   Order Status Distribution
========================== */

const statusCtx=document.getElementById("statusChart");

if(statusCtx){

new Chart(statusCtx,{

type:"pie",

data:{

labels:statusLabels,

datasets:[{

data:statusValues,

backgroundColor:[
"#5a75b5",
"#ea11a9",
"#0b2af5",
"#b20a0a",
"#4f0fe7",
"#1bcbea"
]

}]

},

});

}

console.log(statusLabels)
console.log(statusValues)
/* ==========================
   Review Score Distribution
========================== */

const reviewCtx=document.getElementById("reviewChart");

if(reviewCtx){

new Chart(reviewCtx,{

type:"bar",

data:{

labels:reviewLabels,

datasets:[{

data:reviewValues,

backgroundColor:[
"#EF4444",
"#F97316",
"#FACC15",
"#22C55E",
"#2563EB"
],

borderRadius:10

}]

},

options: {

    responsive: true,

    maintainAspectRatio: false,

    plugins: {

        legend: {

            display: false

        }

    },

    scales: {

        y: {

            beginAtZero: true

        }

    }

}

});

}