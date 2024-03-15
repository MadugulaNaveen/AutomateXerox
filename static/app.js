const element = document.querySelectorAll('.abcd');
const content = document.querySelector('.content')
const form = document.querySelector('.form')
for (let i = 0; i< element.length; i++) {
  element[i].addEventListener('click',function(){
    content.classList.toggle('hide')
    form.classList.toggle('height_reducer')
  })
}
