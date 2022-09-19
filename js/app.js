let source;
let destination;
let db;
let data;
let matches;

function addCustomLabel() {

    // Add new custom record to db
    var id = 99999;
    var libid = String(document.getElementById('custom-libid').value);
    var name = document.getElementById('custom-name').value;
    var address = document.getElementById('custom-address').value;
    var address2 = document.getElementById('custom-address2').value;
    var city = document.getElementById('custom-city').value;
    var state = document.getElementById('custom-state').value;
    var zip = document.getElementById('custom-zip').value;

    if (id > 0) {
        db.insert({
            "id": parseInt(id),
            "libid": libid,
            "name": name,
            "address": address,
            "address2": address2,
            "city": city,
            "state": state,
            "zip": parseInt(zip),
            "hub": null,
            "route": null
        });

        let x = document.createElement("option");
        x.text = name + " (" + libid + ") ";
        x.value = id;
        document.getElementById("source").add(x);
        document.getElementById("source").value = id;

        getLabelData();
    }

    this_modal.hide();

    return false;
}

function getLabelData() {
    if (!matches) {
        // Generate NodeList of all label data elements
        matches = window.frames["output"].contentDocument.querySelectorAll('[data-label]');
    }

    source = db({id: parseInt(document.labels.source.value)}).first();
    destination = db({id: parseInt(document.labels.destination.value)}).first();

    for (const e of matches) {
        switch (e.dataset.label) {
            case "from-id":
                e.textContent = ["FROM:", source.libid].join(" ");
                break;
            case "from-name":
                e.textContent = source.name;
                break;
            case "from-address-1":
                e.textContent = source.address;
                break;
            case "from-address-2":
                e.textContent = source.address2;
                break;
            case "from-city-state-zip":
                e.textContent = [source.city, source.state, source.zip].join(" ");
                break;
            case "to-id":
                e.textContent = ["TO:", destination.libid].join(" ");
                break;
            case "to-name":
                e.textContent = destination.name;
                break;
            case "to-address-1":
                e.textContent = destination.address;
                break;
            case "to-address-2":
                e.textContent = destination.address2;
                break;
            case "to-city-state-zip":
                e.textContent = [destination.city, destination.state, destination.zip].join(" ");
                break;
            case "hub":
                e.textContent = destination.hub;
                break;
            case "route-id":
                e.textContent = destination.route;
                break;
            default:
                e.textContent = 'ERROR'
        }
    }
}

function printLabels() {
    window.frames["output"].focus();
    window.frames["output"].contentWindow.print();
}

// Populate the form dropdowns
function loadOptions() {
    db().each(function (record) {
        let x, y;
        x = document.createElement("option");
        y = document.createElement("option");
        x.text = y.text = record["name"] + " (" + record["libid"] + ") ";
        x.value = y.value = record["id"];
        document.getElementById("source").add(x);
        document.getElementById("destination").add(y);
    });
}

// Initialise TaffyDB from JSON file
function initDB() {
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            data = JSON.parse(this.responseText);
            db = TAFFY(data);
            db.sort("name"); // Alphabetize
            loadOptions();
        }
    };
    xmlhttp.open("GET", "output.json", true);
    xmlhttp.send();
}

// Small helper for modal form focus
let myModal = document.getElementById('custom-label');
let myInput = document.getElementById('custom-libid');
myModal.addEventListener('shown.bs.modal', function () {
    myInput.focus();
});

// Needed for toggling modal visibility
let this_modal = new bootstrap.Modal(document.getElementById('custom-label'), {
    keyboard: false
})
