fetch('header-template.html')
  .then(response => response.text())
  .then(data => {
    const templateDiv = document.createElement('div');
    templateDiv.innerHTML = data;
    const template = templateDiv.querySelector('#header-template');
    const clone = template.content.cloneNode(true);
    document.body.prepend(clone); // или вставить в нужный контейнер
  });