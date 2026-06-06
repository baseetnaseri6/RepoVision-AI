/* ==========================
   Helpers
========================== */

function readJsonScript(id, fallback) {
    const element = document.getElementById(id);

    if (!element) {
        return fallback;
    }

    try {
        return JSON.parse(element.textContent);
    } catch (error) {
        console.error(`Invalid JSON in ${id}:`, error);
        return fallback;
    }
}

const dashboardData = readJsonScript("dashboard-data", {
    overall: 0,
    code_quality: 0,
    security: 0,
    documentation: 0,
    health: 0
});

const fileData = readJsonScript("file-data", {
    labels: ["No Data"],
    values: [0]
});

const activityData = readJsonScript("activity-data", {
    labels: ["Commits", "Issues", "Pull Requests"],
    values: [0, 0, 0]
});


/* ==========================
   Theme
========================== */

const themeToggle = document.getElementById("themeToggle");
const settingsThemeBtn = document.getElementById("settingsThemeBtn");

function setTheme(theme) {
    const icon = themeToggle ? themeToggle.querySelector("i") : null;

    if (theme === "dark") {
        document.body.classList.add("dark");

        if (icon) {
            icon.className = "fa-regular fa-sun";
        }

        localStorage.setItem("theme", "dark");
    } else {
        document.body.classList.remove("dark");

        if (icon) {
            icon.className = "fa-regular fa-moon";
        }

        localStorage.setItem("theme", "light");
    }
}

function toggleTheme() {
    const isDark = document.body.classList.contains("dark");
    setTheme(isDark ? "light" : "dark");
}

if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme);
}

if (settingsThemeBtn) {
    settingsThemeBtn.addEventListener("click", toggleTheme);
}

setTheme(localStorage.getItem("theme") || "light");


/* ==========================
   Premium Page Loader
========================== */

window.addEventListener("load", () => {
    const loader = document.getElementById("pageLoader");
    const percent = document.getElementById("loaderPercent");
    const bar = document.getElementById("loaderBar");
    const text = document.getElementById("loaderText");

    if (!loader || !percent || !bar || !text) {
        return;
    }

    const messages = [
        "Initializing AI Engine...",
        "Connecting GitHub API...",
        "Loading Repository Analyzer...",
        "Preparing Dashboard...",
        "Ready..."
    ];

    let value = 0;

    const interval = setInterval(() => {
        value += 2;

        if (value > 100) {
            value = 100;
        }

        bar.style.width = `${value}%`;
        percent.innerText = `${value}%`;

        if (value >= 20 && value < 40) {
            text.innerText = messages[1];
        } else if (value >= 40 && value < 70) {
            text.innerText = messages[2];
        } else if (value >= 70 && value < 95) {
            text.innerText = messages[3];
        } else if (value >= 95) {
            text.innerText = messages[4];
        }

        if (value >= 100) {
            clearInterval(interval);

            setTimeout(() => {
                loader.classList.add("hide");
            }, 450);
        }
    }, 20);
});


/* ==========================
   Analyze Button Loading
========================== */

const form = document.querySelector(".repo-form");
const analyzeBtn = document.getElementById("analyzeBtn");

if (form && analyzeBtn) {
    form.addEventListener("submit", () => {
        analyzeBtn.innerHTML = `
            <i class="fa-solid fa-spinner fa-spin"></i>
            <span>Analyzing...</span>
        `;

        analyzeBtn.disabled = true;
    });
}


/* ==========================
   Sidebar Scroll + Zoom Focus
========================== */

const sideLinks = document.querySelectorAll(".side-link[data-scroll]");

sideLinks.forEach((button) => {
    button.addEventListener("click", () => {
        sideLinks.forEach((item) => item.classList.remove("active"));
        button.classList.add("active");

        const sectionId = button.getAttribute("data-scroll");
        const section = document.getElementById(sectionId);

        if (section) {
            section.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });

            document.querySelectorAll(".zoom-target").forEach((item) => {
                item.classList.remove("zoom-active");
            });

            setTimeout(() => {
                section.classList.add("zoom-active");
            }, 350);

            setTimeout(() => {
                section.classList.remove("zoom-active");
            }, 1400);
        }
    });
});


/* ==========================
   Modal System
========================== */

const modalBackdrop = document.getElementById("modalBackdrop");

function openModal(modalId) {
    const modal = document.getElementById(modalId);

    if (!modal || !modalBackdrop) {
        return;
    }

    modalBackdrop.classList.add("show");
    modal.classList.add("show");
}

function closeAllModals() {
    document.querySelectorAll(".popup-modal").forEach((modal) => {
        modal.classList.remove("show");
    });

    if (modalBackdrop) {
        modalBackdrop.classList.remove("show");
    }
}

document.querySelectorAll("[data-modal]").forEach((element) => {
    element.addEventListener("click", () => {
        const modalId = element.getAttribute("data-modal");
        openModal(modalId);
    });
});

document.querySelectorAll(".close-modal").forEach((button) => {
    button.addEventListener("click", closeAllModals);
});

if (modalBackdrop) {
    modalBackdrop.addEventListener("click", closeAllModals);
}

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closeAllModals();
    }
});


/* ==========================
   Animated Counters
========================== */

function animateCounters() {
    const counters = document.querySelectorAll(".count-number");

    counters.forEach((counter) => {
        const target = Number(counter.getAttribute("data-target")) || 0;
        let current = 0;

        const duration = 900;
        const stepTime = 16;
        const steps = duration / stepTime;
        const increment = target / steps;

        const timer = setInterval(() => {
            current += increment;

            if (current >= target) {
                counter.textContent = target;
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current);
            }
        }, stepTime);
    });
}

window.addEventListener("load", animateCounters);


/* ==========================
   Charts
========================== */

function createScoreChart() {
    const scoreChartElement = document.getElementById("scoreChart");

    if (!scoreChartElement || typeof Chart === "undefined") {
        return;
    }

    new Chart(scoreChartElement, {
        type: "radar",
        data: {
            labels: ["Overall", "Code", "Security", "Docs", "Health"],
            datasets: [
                {
                    label: "Repository Score",
                    data: [
                        dashboardData.overall,
                        dashboardData.code_quality,
                        dashboardData.security,
                        dashboardData.documentation,
                        dashboardData.health
                    ],
                    fill: true,
                    backgroundColor: "rgba(0, 188, 145, 0.22)",
                    borderColor: "#00bc91",
                    pointBackgroundColor: "#00bc91",
                    pointBorderColor: "#ffffff",
                    pointHoverBackgroundColor: "#ffffff",
                    pointHoverBorderColor: "#00bc91",
                    pointRadius: 5,
                    borderWidth: 3
                }
            ]
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
                r: {
                    min: 0,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        backdropColor: "transparent",
                        color: "#64748b"
                    },
                    grid: {
                        color: "rgba(100, 116, 139, 0.22)"
                    },
                    angleLines: {
                        color: "rgba(100, 116, 139, 0.22)"
                    },
                    pointLabels: {
                        color: "#64748b",
                        font: {
                            size: 12,
                            weight: "bold"
                        }
                    }
                }
            }
        }
    });
}

function createFileChart() {
    const fileChartElement = document.getElementById("fileChart");

    if (!fileChartElement || typeof Chart === "undefined") {
        return;
    }

    new Chart(fileChartElement, {
        type: "doughnut",
        data: {
            labels: fileData.labels,
            datasets: [
                {
                    data: fileData.values,
                    backgroundColor: [
                        "#00bc91",
                        "#0ea5e9",
                        "#22c55e",
                        "#f59e0b",
                        "#64748b",
                        "#ef4444"
                    ],
                    borderWidth: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "68%",
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        usePointStyle: true,
                        boxWidth: 8,
                        font: {
                            size: 12,
                            weight: "bold"
                        },
                        color: "#64748b"
                    }
                }
            }
        }
    });
}

function createActivityChart() {
    const activityChartElement = document.getElementById("activityChart");

    if (!activityChartElement || typeof Chart === "undefined") {
        return;
    }

    new Chart(activityChartElement, {
        type: "bar",
        data: {
            labels: activityData.labels,
            datasets: [
                {
                    label: "Repository Activity",
                    data: activityData.values,
                    backgroundColor: [
                        "rgba(0, 188, 145, 0.75)",
                        "rgba(14, 165, 233, 0.75)",
                        "rgba(245, 158, 11, 0.75)"
                    ],
                    borderRadius: 14,
                    borderSkipped: false
                }
            ]
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
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: "#64748b",
                        font: {
                            weight: "bold"
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: "rgba(100, 116, 139, 0.18)"
                    },
                    ticks: {
                        color: "#64748b"
                    }
                }
            }
        }
    });
}

window.addEventListener("load", () => {
    createScoreChart();
    createFileChart();
    createActivityChart();
});


/* ==========================
   Dashboard Screenshot Export
========================== */

function downloadDashboardScreenshot() {
    const target = document.getElementById("dashboardCapture");

    if (!target) {
        alert("Dashboard area not found.");
        return;
    }

    if (typeof html2canvas === "undefined") {
        alert("Screenshot library is not loaded.");
        return;
    }

    const buttons = document.querySelectorAll("#downloadScreenshotBtn, #downloadScreenshotBtn2");

    buttons.forEach((button) => {
        button.disabled = true;
        button.innerHTML = `
            <i class="fa-solid fa-spinner fa-spin"></i>
            Creating...
        `;
    });

    html2canvas(target, {
        scale: 2,
        useCORS: true,
        backgroundColor: null,
        logging: false
    }).then((canvas) => {
        const link = document.createElement("a");
        link.download = "repovision-ai-dashboard.png";
        link.href = canvas.toDataURL("image/png");
        link.click();
    }).catch((error) => {
        console.error("Screenshot error:", error);
        alert("Could not create screenshot.");
    }).finally(() => {
        buttons.forEach((button) => {
            button.disabled = false;

            if (button.id === "downloadScreenshotBtn") {
                button.innerHTML = `
                    <i class="fa-solid fa-camera"></i>
                    Export Image
                `;
            } else {
                button.innerHTML = `
                    <i class="fa-solid fa-download"></i>
                    Download Image
                `;
            }
        });
    });
}

const screenshotBtn = document.getElementById("downloadScreenshotBtn");
const screenshotBtn2 = document.getElementById("downloadScreenshotBtn2");

if (screenshotBtn) {
    screenshotBtn.addEventListener("click", downloadDashboardScreenshot);
}

if (screenshotBtn2) {
    screenshotBtn2.addEventListener("click", downloadDashboardScreenshot);
}