loadHistory();

const placeholders = {

    romantic: "محبت",
    sad: "تنہائی",
    motivational: "کامیابی",
    islamic: "اللہ",
    story: "ایک دن"
};

document
.getElementById("category")
.addEventListener("change", function(){

    document.getElementById("seed")
    .placeholder =
    placeholders[this.value];
});


async function generatePoetry(){

    const category =
    document.getElementById("category").value;

    const seed =
    document.getElementById("seed").value;

    const output =
    document.getElementById("output");

    output.innerHTML = "Generating...";

    const response = await fetch(
        "/generate",
        {
            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                category:category,
                seed:seed
            })
        }
    );

    const data = await response.json();

    output.innerHTML = data.output;

    saveHistory(data.output);
}


function saveHistory(text){

    let history =
    JSON.parse(
        localStorage.getItem("history")
    ) || [];

    history.unshift(text);

    localStorage.setItem(
        "history",
        JSON.stringify(history.slice(0,10))
    );

    loadHistory();
}


function loadHistory(){

    let history =
    JSON.parse(
        localStorage.getItem("history")
    ) || [];

    const list =
    document.getElementById("historyList");

    if(!list) return;

    list.innerHTML = "";

    history.forEach(item=>{

        const li =
        document.createElement("li");

        li.innerText = item;

        list.appendChild(li);
    });
}


function toggleDarkMode(){

    document.body.classList.toggle(
        "dark-mode"
    );
}