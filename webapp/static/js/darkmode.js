window.onload = function() {
    const toggle = document.getElementById("darkmode_toggle");
    const theme = document.getElementById("stylesheet_toggle");
    const selected = localStorage.getItem("css");

    if (selected !== null){
        theme.href = selected;
    }

    toggle.addEventListener("click", function() {
        if (theme.getAttribute("href") == "../static/css/light-theme.css") {
            theme.href = "../static/css/dark-theme.css";
        } else {
            theme.href = "../static/css/light-theme.css";
        }
        localStorage.setItem("css", theme.href);
    });
}