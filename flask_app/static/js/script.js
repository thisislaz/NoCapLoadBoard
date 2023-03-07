const passwordInput = document.querySelector('#password')
const eye = document.querySelector('#eye')
const confirmPasswordInput = document.querySelector('#password2')
const eyeTwo = document.querySelector('#eye2')

eye.addEventListener('click', function (){
  this.classList.toggle('fa-eye-slash')
  const type = passwordInput.getAttribute('type') === 'password' ?
  "text" : "password"
  passwordInput.setAttribute("type", type)
})

eyeTwo.addEventListener('click', function(){
  this.classList.toggle('fa-eye-slash')
  const type = confirmPasswordInput.getAttribute('type') === 'password' ?
  "text" : "password"
  confirmPasswordInput.setAttribute("type", type)
})

function removeDiv(button) {
  var div = button.parentNode;
  div.parentNode.removeChild(div);
}