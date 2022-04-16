function confirmarEliminar(ruta){
    let confirmacion = confirm("¿Desea eliminar el registro?")
    if(confirmacion){
      location.href = ruta
    }
  }