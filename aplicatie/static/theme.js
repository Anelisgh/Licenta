document.querySelectorAll('#colorSelector .dropdown-content a').forEach(function(link) {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        setTheme(this.dataset.value);
        localStorage.setItem('theme', this.dataset.value);
    });
});

document.addEventListener('DOMContentLoaded', (event) => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme);
    } else {
        setTheme('default'); 
    }
});

function setTheme(theme) {
    let root = document.documentElement.style;
    switch(theme) {
        case 'twilight':
            root.setProperty('--flash-text', 'white');
            root.setProperty('--flash-background', '#5e5e85');
            root.setProperty('--flash-border', '#4b4b66');
            root.setProperty('--table-shadow', '#454562');
            root.setProperty('--table-border', '#4e4e6e');
            root.setProperty('--table-color-title', '#666690');
            root.setProperty('--table-color-elements', '#70709a');
            root.setProperty('--text-table-title', 'black');
            root.setProperty('--hover-table', '#565679');
            root.setProperty('--firma', '#35354b');
            break;
        case 'earth':
            root.setProperty('--flash-text', 'black');
            root.setProperty('--flash-background', '#5e8562');
            root.setProperty('--flash-border', '#4e6e51');
            root.setProperty('--table-shadow', '#456248');
            root.setProperty('--table-border', '#4e6e51');
            root.setProperty('--table-color-title', '#66906a');
            root.setProperty('--table-color-elements', '#709a74');
            root.setProperty('--text-table-title', 'black');
            root.setProperty('--hover-table', '#567959');
            root.setProperty('--firma', '#1a291e');
            break;
        case 'blush':
            root.setProperty('--flash-text', 'black');
            root.setProperty('--flash-background', '#b27c84');
            root.setProperty('--flash-border', '#9f5d67');
            root.setProperty('--table-shadow', '#7e4a52');
            root.setProperty('--table-border', '#a96c75');
            root.setProperty('--table-color-title', '#b27c84');
            root.setProperty('--table-color-elements', '#bc8c93');
            root.setProperty('--text-table-title', 'black');
            root.setProperty('--hover-table', '#9f5d67');
            root.setProperty('--firma', '#6f4148');
            break;
/*
        case '':
            root.setProperty('--flash-text', '#');
            root.setProperty('--flash-background', '#');
            root.setProperty('--flash-border', '#');
            root.setProperty('--table-shadow', '#');
            root.setProperty('--table-border', '#');
            root.setProperty('--table-color-title', '#');
            root.setProperty('--table-color-elements', '#');
            root.setProperty('--text-table-title', 'white');
            root.setProperty('--hover-table', '#');
            root.setProperty('--firma', '#');
            break;
*/
        default:
            root.setProperty('--flash-text', 'black');
            root.setProperty('--flash-background', '#f3f3f3');
            root.setProperty('--flash-border', '#ebebeb');
            root.setProperty('--table-shadow', '#cccccc');
            root.setProperty('--table-border', '#ebebeb');
            root.setProperty('--table-color-title', '#ebebeb');
            root.setProperty('--table-color-elements', '#f5f5f5');
            root.setProperty('--text-table-title', 'black');
            root.setProperty('--hover-table', '#e0e0e0');
            root.setProperty('--firma', 'black');
    }
}
function createColorPreview(theme) {
    let colorPreview = document.createElement('div');
    colorPreview.style.position = 'absolute';
    colorPreview.style.right = '-60px'; // Position the preview box to the right of the dropdown
    colorPreview.style.border = '1px solid #ccc';
    colorPreview.style.borderRadius = '4px';
    colorPreview.style.padding = '2px';
    colorPreview.style.backgroundColor = '#f3f3f3';
    colorPreview.style.width = '60px'; // Adjusted width to match the total width of color boxes
    colorPreview.style.height = '60px';
    colorPreview.style.display = 'flex'; // Use CSS flex layout
    colorPreview.style.flexDirection = 'row'; // Set the direction of items in the flex container
    colorPreview.style.flexWrap = 'wrap'; // Allow the items to wrap as needed

    let colors;
    switch(theme) {
        case 'twilight':
            colors = ['#35354b', '#565679', '#666690', '#70709a'];
            break;
        case 'earth':
            colors = ['#4e6e51', '#567959', '#66906a', '#709a74'];
            break;
        case 'blush':
            colors = ['#6f4148', '#9f5d67', '#b27c84', '#bc8c93'];
            break;
        default:
            colors = ['black', '#e0e0e0', '#ebebeb', 'white'];
    }

    colors.forEach(function(color) {
        let colorBox = document.createElement('div');
        colorBox.style.width = '20px'; 
        colorBox.style.height = '20px'; 
        colorBox.style.backgroundColor = color;
        colorBox.style.margin = '5px';
        colorPreview.appendChild(colorBox);
    });
    return colorPreview;
}

document.querySelectorAll('#colorSelector .dropdown-content a').forEach(function(link) {
    link.addEventListener('mouseover', function() {
        let colorPreview = createColorPreview(this.dataset.value);
        this.appendChild(colorPreview);

    });

    link.addEventListener('mouseout', function() {
        this.removeChild(this.lastChild);
    });

    link.addEventListener('click', function(e) {
        e.preventDefault();
        setTheme(this.dataset.value);
        localStorage.setItem('theme', this.dataset.value);
    });

    var url = window.location.href;  // obțineți URL-ul curent
    var parts = url.split("/");  // împărțiți URL-ul în părți
    var breadcrumbs = "<a href='/'>Acasă</a> ➙ ";
    parts = parts.map(part => part.split("_").join(" ")); // eliminăm "_" și adăugăm spațiu
    for (var i = 3; i < parts.length; i++) {
        var part = parts[i];
        part = decodeURIComponent(part);  // decodează numele angajatului
        part = part.charAt(0).toUpperCase() + part.slice(1);  // transformați prima literă în majusculă
        var link = "/" + parts.slice(3, i+1).join("/");  // construiți URL-ul pentru fiecare pagină
        breadcrumbs += "<a href='" + link + "'>" + part + "</a> ➙ ";  // adăugați fiecare parte ca link la firul de pâine
    }
    breadcrumbs = breadcrumbs.slice(0, -3);  // eliminați ultimul " > "
    $("#breadcrumbs").html(breadcrumbs);  // afișați firul de pâine


});