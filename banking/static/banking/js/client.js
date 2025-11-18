document.addEventListener('DOMContentLoaded', function() {
        
    // ===== Gestion de la Navigation Principale (Accueil / Historique / Opérations) =====
    const navLinks = document.querySelectorAll('.main-nav .nav-link');
    const contentSections = document.querySelectorAll('.page-content .content-section');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // On empêche le rechargement si le lien ne pointe pas vers une vraie URL
            if (this.getAttribute('href') === '#') {
                e.preventDefault();
            }

            const targetId = this.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);

            // Gérer l'état actif du lien
            navLinks.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');

            // Gérer l'affichage de la section
            contentSections.forEach(section => section.classList.remove('active'));
            if (targetSection) {
                targetSection.classList.add('active');
            }
        });
    });

    // ===== Gestion des Onglets (Tabs) pour les Opérations (Dépôt / Retrait) =====
    const operationsCard = document.querySelector('#operations .card');
    if (operationsCard) {
        const tabLinks = operationsCard.querySelectorAll('.tab-nav .tab-link');
        const tabContents = operationsCard.querySelectorAll('.tab-content');

        tabLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('data-target');

                // Gérer l'état actif du lien d'onglet
                tabLinks.forEach(lnk => lnk.classList.remove('active'));
                this.classList.add('active');

                // Gérer l'affichage du contenu d'onglet
                tabContents.forEach(content => {
                    if (content.id === targetId) {
                        content.classList.add('active');
                    } else {
                        content.classList.remove('active');
                    }
                });
            });
        });
    }
});

    let map = document.querySelector('#map')
let paths = map.querySelectorAll('.map__image a')

let active = function (id){
map.querySelectorAll('.is-active').forEach(function(item){
    item.classList.remove('is-active')
}) 

if (id !==undefined){
    document.querySelector('#region-' + id).classList.add('is-active')
}
}

paths.forEach(function(path) {
path.addEventListener('mouseenter', function(){
    let id = this.id.replace('region-','') //enlever region en remplacant par rien

    active(id)
})

path.addEventListener('click', function(e){
    e.preventDefault();
    let title = this.getAttribute('xlink:title');
    let infoDiv = document.getElementById('region-info');
    infoDiv.innerHTML = '';

    if (typeof title === 'string' && title.startsWith('NovaBank')) {
const parts = title.split(';').map(p => p.trim());
const bankName = parts[0] || '';
let adresse = '';
let telephone = '';

for (const part of parts.slice(1)) {
if (/^\s*Adresse\s*:/i.test(part)) adresse = part.replace(/^\s*Adresse\s*:\s*/i, '');
else if (/^\s*Téléphone\s*:/i.test(part)) telephone = part.replace(/^\s*Téléphone\s*:\s*/i, '');
else {
  if (/^\+?[\d\s().-]{6,}$/.test(part)) telephone = telephone ? telephone + '; ' + part : part;
  else adresse = adresse ? adresse + '; ' + part : part;
}
}

// s'assurer que infoDiv existe
infoDiv.innerHTML = '';
const h4 = document.createElement('h4');
h4.textContent = bankName;

const pAdr = document.createElement('p');
const strongAdr = document.createElement('strong');
pAdr.appendChild(strongAdr);
pAdr.append(' ' + adresse);

const pTel = document.createElement('p');
const strongTel = document.createElement('strong');
strongTel.textContent = 'Téléphone:';
pTel.appendChild(strongTel);
pTel.append(' ' + telephone);

infoDiv.append(h4, pAdr, pTel);
}
else {
        infoDiv.innerHTML = '<p>Cette région n\'a pas de siège NovaBank.</p>';
    }
});
})

map.addEventListener('mouseleave', function(){
active()
})/*pour enlever le active lorsqu'on quitte l'interface

NB: mouseleave== miala amle interface iraymanontolo
    mouseover== miala ao amle element
*/

    function toggleText(id) {
        const element = document.getElementById(id);
        if (element) {
            element.style.display = element.style.display === 'none' || element.style.display === '' ? 'block' : 'none';
        }
    }

document.addEventListener('DOMContentLoaded', function() {
    const sectionAccueil = document.getElementById('accueil');
    const video = document.getElementById('introVideo');
    const btnUnmute = document.getElementById('unmuteBtn');
    let audioPlayed = false;

    function lancerVideo() {
        video.play().catch(err => console.log("Vidéo autoplay bloquée", err));
    }

    function jouerSonUneFois() {
        if (audioPlayed) return;
        audioPlayed = true;

        fetch("{% static 'media/pub.mp3' %}")
            .then(response => response.blob())
            .then(blob => {
                const audioUrl = URL.createObjectURL(blob);
                const audio = new Audio(audioUrl);
                audio.volume = 0.7;  // Volume pro et confortable
                audio.play().then(() => {
                    console.log("Musique jouée");
                    // Animation fluide pour cacher le bouton
                    btnUnmute.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    btnUnmute.style.opacity = '0';
                    btnUnmute.style.transform = 'translate(-50%, 10px)';
                    setTimeout(() => {
                        btnUnmute.style.display = 'none';
                    }, 500);
                }).catch(err => console.warn("Audio échoué", err));
            });
    }

    btnUnmute.addEventListener('click', function() {
        video.muted = false;
        jouerSonUneFois();
    });

    const observer = new MutationObserver(function() {
        if (sectionAccueil.classList.contains('active')) {
            lancerVideo();
        } else {
            video.pause();
        }
    });

    observer.observe(sectionAccueil, { attributes: true });

    if (sectionAccueil.classList.contains('active')) {
        lancerVideo();
    }
});