var form = document.querySelector("form");

var historyElt = document.getElementById("history");

var hg = document.createElement("img");
hg.src = "../static/images/hourglass.jpg";

var angle = 45

var rotator ;

function rotateHg(){
    hg.style.transform = "rotate(" + String(angle) + "deg)";
    angle += 45;
}

var unreadableAnswers = [
    "Je n'ai pas compris mon poussin, peux-tu reformuler ?",
    "Je ne comprends bien, que cherches-tu mon poussin ?",
    "J'ai du mal à te comprendre ! Tu sais, il faut rester simple et clair avec les gens de mon âge...",
    "Je ne comprends pas ce que tu me dis, as-tu bien vérifié ton orthographe mon poussin ?"
    ];

var notFoundAnswers = [
    "Désolé mon poussin, je ne connais pas cet endroit...",
    "Hmm, je n'en ai jamais entendu parler ! Désolé !",
    "Qu'est ce que c'est que ça ? Ça n'existait sûrement pas de mon temps...",
    "Oh, ma mémoire me joue des tours ! Je ne sais plus où c'est !"
    ];

var validAnswers = [
    "Bien sûr mon poussin, voici l'adresse : ",
    "Figure-toi que je suis déjà allé là-bas ! L'adresse est toujours la même : ",
    "Ouh, mais je connais cet endroit ! Rendez-vous ",
    "Mais voyons mon poussin, tout le monde sait que c'est "
    ];

function getRandomAnswer(array) {
  return array[Math.floor(Math.random() * Math.floor(4))];
}



form.addEventListener("submit", askQuestion);

function askQuestion(e) {
    e.preventDefault();
    question = form.elements.question.value;
    blockElt = document.createElement("div");
    blockElt.innerHTML += question + "<br /> <br />";
    historyElt.appendChild(blockElt);  
    historyElt.appendChild(hg);
    var compteurElt = document.getElementById("compteur");
    rotator = setInterval(rotateHg, 500);
    url = window.location.href + "search?question=";
    form.reset();
    getQuestion(url.concat('', question), displayAnswer, blockElt);
}


function getQuestion(url, callback, blockElt) {
    var req = new XMLHttpRequest();
    req.open("GET", url);
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status < 400) {
            callback(req.responseText, blockElt);
        } else {
            console.error(req.status + " " + req.statusText + " " + url);
        }
    });
    req.addEventListener("error", function () {
        console.error("Erreur réseau avec l'URL " + url);
    });
    req.send(null);
}

function displayAnswer(answer, blockElt) {
    historyElt.removeChild(hg);
    clearInterval(rotator);
    angle = 45;
    infos = JSON.parse(answer)
    if (infos.status === "unreadable"){
        blockElt.innerHTML += getRandomAnswer(unreadableAnswers);
    }
    else if (infos.status === "not found"){
        blockElt.innerHTML += getRandomAnswer(notFoundAnswers);
    }
    else {
        blockElt.innerHTML += getRandomAnswer(validAnswers) + infos.address + ". Voici l'adresse sur la carte. <br />"; 
        urlImg = "<img src=https://maps.googleapis.com/maps/api/staticmap?markers=" + infos.name + "&zoom=15&size=600x300&key=" + "AIzaSyCY8uAiaK0_0WecT1Xg405iPOv4aNLmHN0>" + "</img>";
        blockElt.innerHTML += urlImg;
        blockElt.innerHTML += "<br />" + infos.trivia;
        blockElt.innerHTML += "<a href=" + infos.link + "> [En savoir plus sur Wikipédia]</a> <br />" 
    }
    blockElt.scrollIntoView();
}
