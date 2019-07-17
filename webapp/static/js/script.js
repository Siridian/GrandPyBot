var form = document.querySelector("form");

var historyElt = document.getElementById("history");



form.addEventListener("submit", askQuestion);

function askQuestion(e) {
    e.preventDefault();
    question = form.elements.question.value;
    console.log(question);
    historyElt.textContent += question;
    url = "http://127.0.0.1:5000/search?question=";
    getQuestion(url.concat('', question), "test");
    historyElt.textContent += "Désolé mon poussin, le parser n'est pas encore implémenté !";
}


function getQuestion(url, callback) {
    var req = new XMLHttpRequest();
    req.open("GET", url);
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status < 400) {
            console.log(req.responseText);
            //callback(req.responseText);
        } else {
            console.error(req.status + " " + req.statusText + " " + url);
        }
    });
    req.addEventListener("error", function () {
        console.error("Erreur réseau avec l'URL " + url);
    });
    req.send(null);
}

function displayAnswer(answer) {
    infos = JSON.parse(answer)
    if (infos.status === "unreadable"){
        historyElt.textContent += "Je n'ai pas compris mon poussin, peux-tu reformuler (en étant un peu plus clair) ?";
    }
    else if (infos.status === "not found"){
        historyElt.textContent += "Je suis désolé mon poussin, je ne connais pas cet endroit...";
    }
    else {
        historyElt.textContent += "Figure-toi que j'y suis déjà allé ! C'est au " + infos.address + ". Le voici sur la carte. " + infos.trivia;
    }

}
