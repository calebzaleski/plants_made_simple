document.getElementById("create-btn").addEventListener("click",
    async function createUser() {

    const data = {
        username: document.getElementById('username-create').value,
        nickname: document.getElementById('nickname').value || null,
        email: document.getElementById('email').value,
        password: document.getElementById('password-create').value,
        firstname: document.getElementById('firstname').value,
        lastname: document.getElementById('lastname').value,
    }

    const payload = await fetch(`/create_user`, {
        method: 'POST',
        headers: {"content-type": "application/json"},
        body: JSON.stringify(data)
    });
    
    // 1. Read the JSON FIRST
    const result = await payload.json();
    
    // 2. Check if the server rejected it (400, 401, 409, etc)
    if (!payload.ok) {
        // Log the exact error message from FastAPI
        console.error("Failed to create user:", result);
        throw new Error(result.detail);
    }

    // 3. If we made it here, it was a success!

    console.log("Successfully created user:", result);
    if (result.success === true) {localStorage.setItem("token", result.token);}
});

document.getElementById("login-btn").addEventListener("click", async function login() {
    const data = {
        username: document.getElementById('username-login').value,
        password: document.getElementById('password-login').value,
    }
    const payload = await fetch(`/login_user`, {
        method: 'POST',
        headers: {"content-type": "application/json"},
        body: JSON.stringify(data)

    })
    const result = await payload.json();

    if (!payload.ok) {console.error("Failed to login:", result.detail); return;}

    console.log("Success:", result.message);

    if (result.success === true) {localStorage.setItem("token", result.token);}


})

document.getElementById("create_plant-btn").addEventListener("click", async function creat_plant() {
    const data = {
        plant_name: document.getElementById('plant_name').value,
        scientific_name: document.getElementById('scientific_name').value,
        age: document.getElementById('age').value,
        image_url: document.getElementById('image_url').value | null,
        health: document.getElementById('health').value | null,
        notes: document.getElementById('notes').value | null,
        // Care Needs
        light_needs: document.getElementById('light_needs').value | null,
        fertilizer_needs: document.getElementById('fertilizer_needs').value | null,
        // Dates
        date_acquired: document.getElementById('date_acquired').value | null,
        date_last_water: document.getElementById('date_last_water').value | null,
        date_next_water: document.getElementById('date_next_water').value | null,
        date_last_pot: document.getElementById('date_last_pot').value | null,
        date_next_pot: document.getElementById('date_next_pot').value | null,
        }

        const payload = await fetch(`/create_plant`, {
            method: 'POST',
            headers: {"content-type": "application/json",
                      "Authorization": `Bearer ${localStorage.getItem("token")}` },
            body: JSON.stringify(data),})

        const result = await payload.json();

    if (!payload.ok) {
        console.error("Failed to create plant:", result.detail);
    }
    console.log("Successfully created plant:", result.message);

})

// --- KEYBOARD NAVIGATION MAGIC ---
// 1. Grab all the input boxes and the submit button
const inputs = document.querySelectorAll("input");
const submitBtn = document.getElementById("create-btn");

// 2. Loop through every single input box
inputs.forEach((input, index) => {
    // 3. Listen for any keys being pressed inside that box
    input.addEventListener("keydown", function(event) {
        
        // Did they press the Enter key?
        if (event.key === "Enter") {
            event.preventDefault(); // Stop any default browser behaviors
            
            // Is there another input box after this one?
            if (index < inputs.length - 1) {
                inputs[index + 1].focus(); // Jump the cursor to the next box!
            } else {
                // If it's the very last box, click the submit button for them!
                submitBtn.click();
            }
        }
    });
});