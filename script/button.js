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

if (infoType === 'box1') { 
    document.getElementById('name__case').textContent = 'Бесплатный за промокод';
    document.getElementById('case__image').src = `../../assets/case/${infoType}.png`;

} else if (infoType === 'box2') {
    document.getElementById('name__case').textContent = 'Бесплатный за пополнение от 1000';
    document.getElementById('case__image').src = `../../assets/case/${infoType}.png`;

} else if (infoType === 'box3') {
    document.getElementById('name__case').textContent = 'Бесплатный за пополнение от 2000';
    document.getElementById('case__image').src = `../../assets/case/${infoType}.png`;

} else if (infoType === 'box4') {
    document.getElementById('name__case').textContent = 'Бесплатный за пополнение от 5000';
    document.getElementById('case__image').src = `../../assets/case/${infoType}.png`;

} else if (infoType === 'box5') {
    document.getElementById('name__case').textContent = 'Бесплатный за пополнение от 10000';
    document.getElementById('case__image').src = `../../assets/case/${infoType}.png`;


} else if (infoType === 'box11') {
    document.getElementById('name__case').textContent = 'Бомж';
    document.getElementById('case__image').src = `../../assets/case/${infoType}.png`;

} else if (infoType === 'box12') {
    document.getElementById('name__case').textContent = 'Работяга';
    document.getElementById('case__image').src = `../../assets/case/${infoType}.png`;

} else if (infoType === 'box13') {
    document.getElementById('name__case').textContent = 'Офисный клерк';
    document.getElementById('case__image').src = `../../assets/case/${infoType}.png`;

} else if (infoType === 'box14') {
    document.getElementById('name__case').textContent = 'Директор';
    document.getElementById('case__image').src = `../../assets/case/${infoType}.png`;

} else if (infoType === 'box15') {
    document.getElementById('name__case').textContent = 'Олигарх';
    document.getElementById('case__image').src = `../../assets/case/${infoType}.png`;

}