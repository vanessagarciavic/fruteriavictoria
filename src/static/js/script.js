function toggleMenu() {
            const navLinks = document.getElementById('nav-links');
            navLinks.classList.toggle('show');
}


const getOptionChart1 = () => {
    return {
        tooltip: {
            show: true,
            trigger: "axis",
            triggerOn: "mousemove|click"
        },
        dataZoom: {
            show: true,
            start: 50
        },
        xAxis: [
            {
                type: "category",
                data: ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            }
        ],
        yAxis: [
            {
                type: "value",
                name: 'Calidad-Precio',
                axisLabel: {
                    formatter: '{value}'
                }
            }
        ],
        series: [
            {
                name: 'Calidad-Precio',
                data: [90, 92, 91, 93, 90, 89, 94],
                type: "line",
                smooth: true,
                lineStyle: {
                    color: '#72b365',
                    width: 3
                },
                itemStyle: {
                    color: '#72b365'
                }
            }
        ]
    };
};

const getOptionChart2 = () => {
    return {
        color: ["#6C70AE", "#538738", "#BF4C37", "#EAD58D"],
        tooltip: {
            show: true,
            trigger: "axis"
        },
        legend: {
            data: ["Naucalpan", "Atizapan", "Nicolas Romero", "Otras Areas"]
        },
        grid: {
            left: "3%",
            right: "4%",
            bottom: "3%",
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: [
            {
                type: "category",
                boundaryGap: false,
                data: ["2024", "2022", "2020", "2015"],
                axisLine: { show: false },
                axisTick: { show: false },
                axisPointer: { type: "shadow" }
            }
        ],
        yAxis: [
            {
                type: "value"
            }
        ],
        series: [
            {
                name: "Naucalpan",
                type: "line",
                stack: "Total",
                data: [5, 5, 4, 2]
            },
            {
                name: "Atizapan",
                type: "line",
                stack: "Total",
                data: [8, 5, 3, 2]
            },
            {
                name: "Nicolas Romero",
                type: "line",
                stack: "Total",
                data: [4, 2, 0, 0]
            },
            {
                name: "Otras Areas",
                type: "line",
                stack: "Total",
                data: [5, 5, 3, 1]
            }
        ]
    };
};

const getOptionChart3 = () => {
    return {
        tooltip: {
            show: true
        },
        xAxis: {
            type: "category",
            data: ["2023", "2022", "2021", "2019", "2018", "2020", "2017", "2016", "2015"]
        },
        yAxis: {
            type: "value"
        },
        series: [
            {
                data: [11100, 10400, 9400, 8700, 7700, 7000, 6300, 5200, 3800],
                type: "bar"
            }
        ]
    };
};

const getOptionChart4 = () => {
    return {
        tooltip: {
            trigger: "item"
        },
        legend: {
            top: "5%",
            left: "center"
        },
        series: [
            {
                name: "Access From",
                type: "pie",
                radius: ["40%", "70%"],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: "#fff",
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: "center"
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: "40",
                        fontWeight: "bold"
                    }
                },
                labelLine: {
                    show: false
                },
                data: [
                    { value: 20900, name: "Naucalpan" },
                    { value: 19200, name: "Nicolas Romero" },
                    { value: 19900, name: "Atizapan" },
                    { value: 9600, name: "Otras Areas" }
                ]
            }
        ]
    };
};

const initCharts = () => {
    const chart1 = echarts.init(document.getElementById("chart1"));
    const chart2 = echarts.init(document.getElementById("chart2"));
    const chart3 = echarts.init(document.getElementById("chart3"));
    const chart4 = echarts.init(document.getElementById("chart4"));

    chart1.setOption(getOptionChart1());
    chart2.setOption(getOptionChart2());
    chart3.setOption(getOptionChart3());
    chart4.setOption(getOptionChart4());

    chart1.resize();
    chart2.resize();
    chart3.resize();
    chart4.resize();
};

window.addEventListener("load", () => {
    initCharts();
});

function showToast() {
    var urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('success')) {
        var toastEl = document.getElementById('successToast');
        var toast = new bootstrap.Toast(toastEl);
        toast.show();
    }
}
window.onload = showToast;

function toggleUserMenu() {
    const menu = document.getElementById('dropdown-menu');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}

window.onclick = function(event) {
    if (!event.target.matches('.user-icon')) {
        const dropdowns = document.getElementsByClassName('dropdown-menu');
        for (let i = 0; i < dropdowns.length; i++) {
            const openDropdown = dropdowns[i];
            if (openDropdown.style.display === 'block') {
                openDropdown.style.display = 'none';
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var successToast = document.getElementById('funcionandoToast');
    var toast = new bootstrap.Toast(successToast, {
      animation: true, // Habilita animación
      autohide: true,  // Oculta automáticamente después de un tiempo
      delay: 5000       // Duración en milisegundos (5000 ms = 5 segundos)
    });
    toast.show();
  });
