// ===============================
// Monthly Bookings (Line Chart)
// ===============================

new Chart(document.getElementById("monthlyBookingChart"), {

    type: "line",

    data: {

        labels: monthly_labels,

        datasets: [{

            label: "Monthly Bookings",

            data: monthly_values,

            borderColor: "#3B82F6",

            backgroundColor: "rgba(59,130,246,0.15)",

            fill: true,

            tension: 0.45,

            borderWidth: 4,

            pointRadius: 6,

            pointHoverRadius: 9,

            pointBackgroundColor: "#ffffff",

            pointBorderColor: "#3B82F6",

            pointBorderWidth: 3

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false,

        interaction: {

            mode: "index",

            intersect: false

        },

        plugins: {

            legend: {

                display: false

            },

            tooltip: {

                backgroundColor: "#111827",

                titleColor: "#ffffff",

                bodyColor: "#ffffff",

                padding: 12,

                cornerRadius: 8

            }

        },

        scales: {

            x: {

                grid: {

                    display: false

                },

                ticks: {

                    callback: function(value) {

                        return monthly_labels[value].substring(0,3);

                    },

                    color: "#6B7280",

                    font: {

                        weight: "bold"

                    }

                }

            },

            y: {

                beginAtZero: true,

                grid: {

                    color: "rgba(0,0,0,.06)"

                },

                ticks: {

                    color: "#6B7280"

                }

            }

        }

    }

});

// ===============================
// Hotel Type Comparison
// ===============================

new Chart(document.getElementById("hotelTypeChart"), {

    type: "doughnut",

    data: {

        labels: hotel_labels,

        datasets: [{

            data: hotel_values,

            backgroundColor: [

                "#3B82F6",

                "#a25c87"

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


// ===============================
// Country Wise Bookings
// ===============================

new Chart(document.getElementById("countryBookingChart"), {

    type: "bar",

    data: {

        labels: country_labels,

        datasets: [{

            label: "Bookings",

            data: country_values,

            backgroundColor: "#3bb3a3"

        }]

    },

    options: {

        responsive: true,

        indexAxis: "y",

        plugins: {

            legend: {

                display: false

            }

        }

    }

});


// ===============================
// Market Segment
// ===============================

new Chart(document.getElementById("marketSegmentChart"), {

    type: "bar",

    data: {

        labels: market_labels,

        datasets: [{

            data: market_values,

            backgroundColor: "#ff8a57"

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


// ===============================
// Lead Time Distribution
// ===============================

new Chart(document.getElementById("leadTimeChart"), {

    type: "bar",

    data: {

        labels: lead_labels,

        datasets: [{

            data: lead_values,

            backgroundColor: "#9219b3"

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


// ===============================
// Reservation Status
// ===============================

new Chart(document.getElementById("reservationChart"), {

    type: "doughnut",

    data: {

        labels: reservation_labels,

        datasets: [{

            data: reservation_values,

            backgroundColor: [

                "#3c9f7e",
                "#EF4444",
                "#F59E0B"

            ],

            borderWidth: 2,

            borderColor: "#ffffff",

            hoverOffset: 15

        }]

    },

    options: {

        responsive: true,

        cutout: "65%",

        plugins: {

            legend: {

                position: "bottom"

            }

        }

    }

});




// stay duration delay

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

            borderWidth: 2,

            hoverOffset: 15

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false,

        plugins: {

            legend: {

                position: "bottom",

                labels: {

                    usePointStyle: true,

                    pointStyle: "circle",

                    padding: 20,

                    font: {

                        size: 12,

                        weight: "bold"

                    }

                }

            },

            tooltip: {

                backgroundColor: "#111827",

                titleColor: "#ffffff",

                bodyColor: "#ffffff",

                padding: 12,

                cornerRadius: 8,

                callbacks: {

                    label: function(context) {

                        return context.label + " : " + context.raw + " Guests";

                    }

                }

            }

        },

        scales: {

            r: {

                beginAtZero: true,

                ticks: {

                    display: false

                },

                grid: {

                    color: "rgba(0,0,0,0.08)"

                }

            }

        }

    }

});

console.log(stay_labels);
console.log(stay_values);