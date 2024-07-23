let links = document.getElementsByTagName('a');
for(let i=0; i<links.length; i++) {
  if(links[i].classList.contains('disabled')) {
    links[i].addEventListener('click', function(e) {
      e.preventDefault();
    });
  }
}