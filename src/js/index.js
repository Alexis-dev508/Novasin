import {addNewProduct} from '../firebase/main_firebase.js'

const new_prod_form = document.getElementById('new_prod_form');
window.addEventListener('DOMContentLoaded', async ()=>{

});

// ========== Guardando un nuevo producto ===========
new_prod_form.addEventListener('submit', (e)=>{  //Escucha el evento submit del formulario
  e.preventDefault(); // Evita que se refresque la pagina al enviar el formulario
  const nombre_prod=  new_prod_form['nombre_prod'];
  const desc_prod=  new_prod_form['desc_prod']; //Seleccionamos el elemento html
  addNewProduct(nombre_prod.value, desc_prod.value);
})
//==================================================


