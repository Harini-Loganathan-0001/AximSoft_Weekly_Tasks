// Class Distribution

new Chart(document.getElementById("classChart"), {

    type: "bar",

    data: {

        labels: [
            "Melanoma",
            "Nevus",
            "BCC",
            "AKIEC",
            "BKL",
            "DF",
            "VASC"
        ],

        datasets: [{

            data: [
                1113,
                6705,
                514,
                327,
                1099,
                115,
                142
            ],

            backgroundColor: [
                "#3B82F6", // Blue
                "#10B981", // Green
                "#F59E0B", // Orange
                "#EF4444", // Red
                "#8B5CF6", // Purple
                "#06B6D4", // Cyan
                "#EC4899"  // Pink
            ],

            borderRadius: 8

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

// Model Comparison

new Chart(document.getElementById("modelChart"),{

    type:"bar",

    data:{

        labels:[
            "CNN",
            "MobileNet",
            "ResNet",
            "DenseNet",
            "EffNet"
        ],

        datasets:[{

            data:[
                88,
                93,
                95,
                96,
                97.8
            ]

        }]

    }

});

// Dataset Split

new Chart(document.getElementById("splitChart"),{

    type:"pie",

    data:{

        labels:["Train","Validation","Test"],

        datasets:[{

            data:[70,15,15]

        }]

    }

});
