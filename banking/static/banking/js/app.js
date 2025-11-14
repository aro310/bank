let map = document.querySelector('#map')
let paths = map.querySelectorAll('.map__image a')
let links = map.querySelectorAll('.map__list a')

let active = function (id){
    map.querySelectorAll('.is-active').forEach(function(item){
        item.classList.remove('is-active')
    }) 

    if (id !==undefined){
        document.querySelector('#list-' + id).classList.add('is-active')//selectionner l'id list en ajoutant - le id du region et ajouter class isactive pour styliser niveau css
        document.querySelector('#region-' + id).classList.add('is-active')//selectionner l'id list en ajoutant - le id du region et ajouter class isactive pour styliser niveau css
    }
}

paths.forEach(function(path) {
    path.addEventListener('mouseenter', function(){
        let id = this.id.replace('region-','') //enlever region en remplacant par rien

        active(id)
    })
})

links.forEach(function(link){
    link.addEventListener('mouseenter', function(){
        let id = this.id.replace('list-','')
        
        active(id)
    })
})

map.addEventListener('mouseover', function(){
    active()
})/*pour enlever le active lorsqu'on quitte l'interface

    NB: mouseleave== miala amle interface iraymanontolo
        mouseover== miala ao amle element
*/