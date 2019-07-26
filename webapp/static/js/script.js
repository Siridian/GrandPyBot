var form = document.querySelector("form");

var historyElt = document.getElementById("history");



form.addEventListener("submit", askQuestion);

function askQuestion(e) {
    e.preventDefault();
    question = form.elements.question.value;
    blockElt = document.createElement("div");
    blockElt.innerHTML += question + "<br /> <br />"
    historyElt.appendChild(blockElt);
    url = "http://127.0.0.1:5000/search?question=";
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
    infos = JSON.parse(answer)
    if (infos.status === "unreadable"){
        blockElt.innerHTML += "Je n'ai pas compris mon poussin, peux-tu reformuler (en étant un peu plus clair) ?";
    }
    else if (infos.status === "not found"){
        blockElt.innerHTML += "Je suis désolé mon poussin, je ne connais pas cet endroit...";
    }
    else {
        blockElt.innerHTML += "Figure-toi que j'y suis déjà allé ! C'est au " + infos.address + ". Le voici sur la carte. <br />"; 
        urlImg = "<img src=https://maps.googleapis.com/maps/api/staticmap?markers=" + infos.name + "&zoom=15&size=600x300&key=" + "AIzaSyCY8uAiaK0_0WecT1Xg405iPOv4aNLmHN0>" + "</img>";
        blockElt.innerHTML += urlImg;
        blockElt.innerHTML += "<br />" + infos.trivia;
        blockElt.innerHTML += "<a href=" + infos.link + "> [En savoir plus sur Wikipédia]</a> <br />" 
    }

}
