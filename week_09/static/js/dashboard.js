// Class Distribution

new Chart(document.getElementById("classChart"),{

    type:"bar",

    data:{

        labels:[
            "Melanoma",
            "Nevus",
            "BCC",
            "AKIEC",
            "BKL",
            "DF",
            "VASC"
        ],

        datasets:[{

            data:[
                1113,
                6705,
                514,
                327,
                1099,
                115,
                142
            ]

        }]

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

// Accuracy

new Chart(document.getElementById("accuracyChart"),{

    type:"line",

    data:{

        labels:[1,2,3,4,5,6,7,8,9,10],

        datasets:[{

            data:[60,72,79,85,89,92,94,96,97,97.8],

            fill:true

        }]

    }

});

// Loss

new Chart(document.getElementById("lossChart"),{

    type:"line",

    data:{

        labels:[1,2,3,4,5,6,7,8,9,10],

        datasets:[{

            data:[1.4,1.0,.8,.6,.5,.4,.3,.2,.15,.09],

            fill:true

        }]

    }

});