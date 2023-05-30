let service = new PeopleCounterService();

const selectElement = document.getElementById("sensorName");
const submitButton = document.getElementById("getOccupancy");
service.addSelectOptions(selectElement).then(() => {
    submitButton.addEventListener("click", ev => {
        ev.preventDefault();
        service.submit(selectElement.value);
    })
})

document.getElementById("addRecord").addEventListener("submit", ev => {
    ev.preventDefault();
    let data = {
        "name": document.querySelector("input#name").value,
        "ts": document.querySelector("input#ts").value,
        "in": document.querySelector("input#in").value,
        "out": document.querySelector("input#out").value
    }
    service.createRecord(data).then(async r => {
        let result = document.createElement("div")
        if (r.ok){
            result.innerHTML = "<div class='alert alert-success'>Record added</div>";
            ev.target.reset()
        } else {
            let errors = await r.json();
            result.innerHTML = "<div class='alert alert-danger'>" + JSON.stringify(errors) + "</div>"
        }
        ev.target.after(result)
    })
})
