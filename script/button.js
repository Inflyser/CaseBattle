function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return typeof sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
}

var infoType = getUrlParameter('info');

if (infoType === 'box1') { // Интерстеллар
    document.getElementById('name__case').textContent = 'Бесплатный за промокод';
    document.getElementById('name__film').textContent = 'Интерстеллар';


} else if (infoType === 'box2') {
    document.getElementById('content').textContent = 'Бесплатный за пополнение от 1000';
    document.getElementById('name__film').textContent = 'Унесённые призраками';
    document.getElementById('short__text').textContent = '...';
    document.getElementById('year').textContent = '...';
    document.getElementById('country').textContent = '...';
    document.getElementById('genre').textContent = '...';

} else if (infoType === 'film3') {
    document.getElementById('content').textContent = 'Это вторая часть информации.';
    document.getElementById('name__film').textContent = 'Унесённые призраками';
    document.getElementById('short__text').textContent = '...';
    document.getElementById('year').textContent = '...';
    document.getElementById('country').textContent = '...';
    document.getElementById('genre').textContent = '...';

}