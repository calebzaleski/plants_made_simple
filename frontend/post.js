document.getElementById("create-btn").addEventListener("click", async function createUser() {

    const data = {
        username: document.getElementById('username').value,
        nickname: document.getElementById('nickname').value || null,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        firstname: document.getElementById('firstname').value,
        lastname: document.getElementById('lastname').value,
    }

    const response = await fetch(`/create_user`, {
        method: 'POST',
        headers: {"content-type": "application/json"},
        body: JSON.stringify(data)
    });
    
    // 1. Read the JSON FIRST
    const result = await response.json();
    
    // 2. Check if the server rejected it (400, 401, 409, etc)
    if (!response.ok) {!
        // Log the exact error message from FastAPI
        console.error("Failed to create user:", result);
        throw new Error(result.detail);
    }

    // 3. If we made it here, it was a success!
    console.log("Success:", result.message);
});

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