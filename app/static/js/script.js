const cityField = document.getElementById('city_output');
const status = document.getElementById('status_message');
const submitBtn = document.getElementById('submit_btn');

async function fetchCity() {
    const country = document.getElementById('country_input').value.trim().toLowerCase();
    const zip = document.getElementById('zip_input').value.trim();

    if (!country || !zip) return;

    cityField.value = "Loading...";

    try {
        const response = await fetch(`https://api.zippopotam.us/${country}/${zip}`);

        if (!response.ok) {
            cityField.value = "Not found";
            return;
        }

        const data = await response.json();

        if (data.places && data.places.length > 0) {
            cityField.value = data.places[0]['place name'];
        } else {
            cityField.value = "Unknown";
        }

    } catch (error) {
        console.error("Zippo Error:", error);
        cityField.value = "Error";
    }
}

async function saveToDB() {
    if (document.getElementById('bug_ui_ghost').checked) {
        status.style.display = "block";
        status.style.color = "";
        status.innerText = "Error";
        return; 
    }

    submitBtn.disabled = true;

    const payload = {
        zip: document.getElementById('zip_input').value,
        country: document.getElementById('country_input').value,
        city: cityField.value,
        bugs: {
            slow_db: document.getElementById('bug_slow_db').checked,
            integrity: document.getElementById('bug_integrity').checked,
            data_loss: document.getElementById('bug_data_loss').checked,
            ui_ghost: document.getElementById('bug_ui_ghost').checked
        }
    };

    status.style.display = "block";
    status.style.color = "";
    status.innerText = "Saving...";

  try {
        const response = await fetch('/api/save_location', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!response.ok) {
            status.innerText = "Error";
        } else {
            status.innerText = result.message || "Saved!";
        }

    } catch (e) {
        status.innerText = "Error"; 
    } finally {
        submitBtn.disabled = false;
    }
}

document.getElementById('zip_input').addEventListener('blur', fetchCity);
submitBtn.addEventListener('click', saveToDB);