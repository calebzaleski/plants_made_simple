/**
 * post.js  —  API helper functions + button event listeners
 * 
 * SECTION 1 (top): Reusable async functions that call each backend endpoint.
 *   Call these from dashboard.js or any other page script.
 * 
 * SECTION 2 (bottom): Direct button click listeners for the settings /
 *   auth pages (kept as-is so those pages still work).
 */

// ── SECTION 1: Reusable API Functions ────────────────────────────────────────

/** Returns the standard auth header using the stored JWT token. */
function getAuthHeader() {
    return { "Authorization": `Bearer ${localStorage.getItem("token")}` };
}

/**
 * GET /all_plants/
 * Fetches every plant that belongs to the logged-in user.
 * Returns the plants array, or throws on error.
 */
async function getAllPlants() {
    const resp = await fetch("/all_plants/", {
        method: "GET",
        headers: { "content-type": "application/json", ...getAuthHeader() }
    });
    const result = await resp.json();
    if (resp.status === 401) {
            await LogOut();
            throw new Error("Session expired. Please log in again.");
        }

        if (!resp.ok) { throw new Error(result.detail || "Failed to fetch plants")}
    return result.plants;
}

/**
 * GET /get_plant/{plantId}
 * Fetches a single plant by its ID.
 * Returns the plant object, or throws on error.
 */
async function getPlant(plantId) {
    const resp = await fetch(`/get_plant/${plantId}`, {
        method: "GET",
        headers: { "content-type": "application/json", ...getAuthHeader() }
    });
    const result = await resp.json();

    if (resp.status === 401) {
            await LogOut();
            throw new Error("Session expired. Please log in again.");
        }

        if (!resp.ok) { throw new Error(result.detail || "Failed to fetch plant")}
    return result.plant;
}

/**
 * PATCH /update_plant/{plantId}
 * Sends a partial update for a plant. Only the fields you include will change.
 * @param {number} plantId  - The plant's ID
 * @param {object} data     - An object with only the fields to update (PlantUpdate schema)
 */
async function updatePlant(plantId, data) {
    const payload = await fetch(`/update_plant/${plantId}`, {
        method: "PATCH",
        headers: { "content-type": "application/json", ...getAuthHeader() },
        body: JSON.stringify(data)
    });
    const result = await payload.json();
    if (payload.status === 401) {
            await LogOut();
            throw new Error("Session expired. Please log in again.");
        }

        // Catch any other general errors
        if (!payload.ok) { throw new Error(result.detail || "Failed to update plant")}
        return result;
}

// ─── Image Upload ────────────────────────────────────────────────────────────

/** Uploads an image file to the backend and returns the public URL. */
async function uploadImageFile(file) {
    const formData = new FormData();
    formData.append("image_file", file);
    
    const payload = await fetch("/upload_image", {
        method: "POST",
        headers: getAuthHeader(), // Note: Do NOT set Content-Type, fetch sets it automatically with boundary for FormData
        body: formData
    });
    
    const result = await payload.json();

        if (payload.status === 401) {
            await LogOut();
            throw new Error("Session expired. Please log in again.");
        }

        // Catch any other general errors
        if (!payload.ok) {
            throw new Error(result.detail || "Failed to upload image");
        }
        return result.image_url;
    }


/**
 * PATCH /water_plant/{plantId}
 * Marks a plant as watered today and sets the next watering date.
 */
async function waterPlant(plantId) {
    const resp = await fetch(`/water_plant/${plantId}`, {
        method: "PATCH",
        headers: { "content-type": "application/json", ...getAuthHeader() }
    });
    const result = await resp.json();
    if (resp.status === 401) {
            await LogOut();
            throw new Error("Session expired. Please log in again.");
        }

        if (!resp.ok) { throw new Error(result.detail || "Failed to water plant")}
    return result;
}

/**
 * PATCH /fertilize_plant/{plantId}
 * Marks a plant as fertilized today and sets the next fertilize date.
 */
async function fertilizePlant(plantId) {
    const resp = await fetch(`/fertilize_plant/${plantId}`, {
        method: "PATCH",
        headers: { "content-type": "application/json", ...getAuthHeader() }
    });
    const result = await resp.json();
    if (resp.status === 401) {
            await LogOut();
            throw new Error("Session expired. Please log in again.");
        }

        if (!resp.ok) { throw new Error(result.detail || "Failed to fertilize plant")}
    return result;
}

/**
 * PATCH /pot_plant/{plantId}
 * Marks a plant as repotted today and sets the next repotting date.
 */
async function repotPlant(plantId) {
    const resp = await fetch(`/pot_plant/${plantId}`, {
        method: "PATCH",
        headers: { "content-type": "application/json", ...getAuthHeader() }
    });
    const result = await resp.json();
    if (resp.status === 401) {
            await LogOut();
            throw new Error("Session expired. Please log in again.");
        }

        if (!resp.ok) { throw new Error(result.detail || "Failed to repot plant")}
    return result;
}

/**
 * POST /create_plant
 * Creates a new plant for the logged-in user.
 * @param {object} data - PlantCreate schema fields
 */
async function createPlant(data) {
    const resp = await fetch("/create_plant", {
        method: "POST",
        headers: { "content-type": "application/json", ...getAuthHeader() },
        body: JSON.stringify(data)
    });
    const result = await resp.json();
    if (resp.status === 401) {
            await LogOut();
            throw new Error("Session expired. Please log in again.");
        }

        if (!resp.ok) { throw new Error(result.detail || "Failed to create plant")}
    return result;
}
async function getUser() {
    const response = await fetch(`/get_user`, {
        method: "GET",
        headers: { "content-type": "application/json", ...getAuthHeader() },
    });
    const result = await response.json();
    if (response.status === 401) {
        await LogOut();
        throw new Error("Session expired. Please log in again.");
    }
    if (!response.ok) {
        throw new Error(result.detail || "Failed to get user");
    }
    return result.user;
}

async function updateUser(data) {
    const payload = await fetch(`/update_user/`, {
        method: "PATCH",
        headers: { "content-type": "application/json", ...getAuthHeader() },
        body: JSON.stringify(data)
    });
    const result = await payload.json();
    if (payload.status === 401) {
        await LogOut();
        throw new Error("Session expired. Please log in again.");
    }
    if (!payload.ok)
        { throw new Error(result.detail || "Failed to update user")}
    return result;
}



// ── SECTION 2: Button Event Listeners (settings / auth pages) ────────────────

document.getElementById("create-btn")?.addEventListener("click", async function createUser() {

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
    if (result.success === true) {
        localStorage.setItem("token", result.token); 
        localStorage.setItem("firstname", data.firstname); // Grabs from the input box!
        window.location.href = "index.html"
    }
});

document.getElementById("login-btn")?.addEventListener("click", async function login() {
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

    if (result.success === true) {
        localStorage.setItem("token", result.token); 
        
        // Only try to save the firstname if the backend actually sent it!
        if (result.firstname) {
            localStorage.setItem("firstname", result.firstname); 
        }
        
        // Auto-refresh the page to show the logged-in screen!
        window.location.href = "index.html"
    }
});



/**
 * dashboard.js
 *
 * Handles ALL dashboard behaviour:
 *   1. Rendering the plant grid (images + edit buttons)
 *   2. Building the Upcoming Tasks list from next-care dates
 *   3. Quick-action modals (Water / Fertilize / Re-pot)
 *   4. Edit-plant modal (pre-fills from backend, saves via PATCH)
 *
 * NOTE: All API calls go through the helper functions in post.js:
 *   getAllPlants(), getPlant(), updatePlant(),
 *   waterPlant(), fertilizePlant(), repotPlant()
 * post.js must be loaded BEFORE this file in index.html.
 */

// ─── Small Utilities (UI only, not API) ──────────────────────────────────────


function fmtDate(dateStr) {
    if (!dateStr) return null;
    const d = new Date(dateStr + "T00:00:00"); // pin to local midnight
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

/** Returns true if a date string is in the past (overdue). */
function isOverdue(dateStr) {
    if (!dateStr) return false;
    return new Date(dateStr + "T00:00:00") < new Date();
}

// ─── Today's Date ────────────────────────────────────────────────────────────

(function setTodayDate() {
    const el = document.getElementById("today-date");
    if (!el) return;
    el.textContent = new Date().toLocaleDateString("en-US", {
        weekday: "long", month: "long", day: "numeric", year: "numeric"
    });
})();

// ─── State ───────────────────────────────────────────────────────────────────

let cachedPlants = [];              // kept so modals don't re-fetch
let currentAction = null;          // "water" | "fertilize" | "repot"

// ─── 1. Plant Grid ───────────────────────────────────────────────────────────

/** Builds one plant card DOM element. */
function buildPlantCard(plant) {
    const template = document.getElementById('tpl-plant-card');
    const clone = template.content.cloneNode(true);
    const card = clone.querySelector('.plant-card');

    const imgWrap = clone.querySelector('.plant-img-wrap');
    if (plant.image_url) {
        const img = document.createElement('img');
        img.src = plant.image_url;
        img.alt = plant.plant_name;
        img.onerror = function() {
            imgWrap.innerHTML = '<span class="plant-fallback">🪴</span>';
        };
        imgWrap.appendChild(img);
    } else {
        imgWrap.innerHTML = '<span class="plant-fallback">🪴</span>';
    }

    clone.querySelector('.plant-card-name').textContent = plant.plant_name;
    clone.querySelector('.plant-card-sci').textContent = plant.scientific_name || "—";

    const struggling = /struggle|bad|poor|sick|dying/i.test(plant.health);
    if (plant.health) {
        const badge = document.createElement('span');
        badge.className = `health-badge ${struggling ? 'struggling' : ''}`;
        badge.textContent = plant.health;
        clone.querySelector('.plant-card-body').appendChild(badge);
    }

    card.addEventListener("click", (e) => {
        e.stopPropagation();
        openEditModal(plant.plant_id);
    });

    return clone;
}

/** Renders all plant cards into #plant-grid. */
function renderPlantGrid(plants) {
    const grid = document.getElementById("plant-grid");
    grid.innerHTML = "";

    // Add all existing plants first
    plants.forEach(p => grid.appendChild(buildPlantCard(p)));

    // Create the "Add New Plant" card to always sit at the end
    const template = document.getElementById('tpl-plant-card-new');
    const clone = template.content.cloneNode(true);
    const newCard = clone.querySelector('.plant-card-new');
    
    newCard.addEventListener("click", () => {
        openCreateModal();
    });

    grid.appendChild(clone);
}

// ─── 2. Upcoming Tasks List ──────────────────────────────────────────────────

/** Builds the task list from next-care dates on each plant. */
function renderTaskList(plants) {
    const list = document.getElementById("task-list");
    list.innerHTML = "";

    const tasks = [];

    plants.forEach(p => {
        if (p.date_next_water)      tasks.push({ plantName: p.plant_name, type: "💧 Water",     dateStr: p.date_next_water });
        if (p.date_next_fertilized) tasks.push({ plantName: p.plant_name, type: "🌿 Fertilize", dateStr: p.date_next_fertilized });
        if (p.date_next_pot)        tasks.push({ plantName: p.plant_name, type: "🪴 Re-pot",    dateStr: p.date_next_pot });
    });

    tasks.sort((a, b) => new Date(a.dateStr) - new Date(b.dateStr));

    if (!tasks.length) {
        const emptyTemplate = document.getElementById('tpl-task-empty');
        list.appendChild(emptyTemplate.content.cloneNode(true));
        return;
    }

    const taskTemplate = document.getElementById('tpl-task-item');
    tasks.forEach(t => {
        const overdue = isOverdue(t.dateStr);
        const clone = taskTemplate.content.cloneNode(true);
        const li = clone.querySelector('li');
        if (overdue) li.classList.add('overdue');
        
        clone.querySelector('.task-plant').textContent = `${t.type} — ${t.plantName}`;
        clone.querySelector('.task-date').textContent = `${overdue ? "⚠️ Overdue: " : "Due: "}${fmtDate(t.dateStr)}`;
        
        list.appendChild(clone);
    });
}

// ─── 3. Quick-Action Modal ───────────────────────────────────────────────────

const actionBackdrop  = document.getElementById("action-modal-backdrop");
const actionModalTitle = document.getElementById("action-modal-title");
const actionPlantList  = document.getElementById("action-plant-list");
const actionSubmitBtn  = document.getElementById("action-modal-submit");

function openActionModal(action) {
    currentAction = action;

    const titles = { water: "💧 Water a Plant", fertilize: "🌿 Fertilize a Plant", repot: "🪴 Re-pot a Plant" };
    actionModalTitle.textContent = titles[action];

    actionPlantList.innerHTML = "";
    if (!cachedPlants.length) {
        const emptyTemplate = document.getElementById('tpl-action-no-plants');
        actionPlantList.appendChild(emptyTemplate.content.cloneNode(true));
    } else {
        const itemTemplate = document.getElementById('tpl-action-plant-item');
        cachedPlants.forEach(p => {
            const clone = itemTemplate.content.cloneNode(true);
            clone.querySelector('input').value = p.plant_id;
            clone.querySelector('.action-plant-name').textContent = p.plant_name;
            if (p.scientific_name) {
                clone.querySelector('.action-plant-sci').textContent = `(${p.scientific_name})`;
            }
            actionPlantList.appendChild(clone);
        });
    }

    actionBackdrop.classList.add("open");
}

function closeActionModal() {
    actionBackdrop.classList.remove("open");
    currentAction = null;
}

/** On "Confirm" — call the right function from post.js */
actionSubmitBtn?.addEventListener("click", async () => {
    const selected = actionPlantList.querySelector("input[type='radio']:checked");
    if (!selected) { alert("Please select a plant first."); return; }

    const plantId = selected.value;

    // Map action string → the post.js helper function
    const actionFns = { water: waterPlant, fertilize: fertilizePlant, repot: repotPlant };
    const fn = actionFns[currentAction];
    if (!fn) return;

    actionSubmitBtn.textContent = "Saving…";
    actionSubmitBtn.disabled = true;

    try {
        await fn(plantId);   // calls waterPlant / fertilizePlant / repotPlant from post.js
        closeActionModal();
        await refreshDashboard();
    } catch (err) {
        alert("Error: " + err.message);
    } finally {
        actionSubmitBtn.textContent = "Confirm";
        actionSubmitBtn.disabled = false;
    }
});

document.getElementById("quick-water-btn")?.addEventListener("click",     () => openActionModal("water"));
document.getElementById("quick-fertilize-btn")?.addEventListener("click", () => openActionModal("fertilize"));
document.getElementById("quick-repot-btn")?.addEventListener("click",     () => openActionModal("repot"));
document.getElementById("action-modal-close")?.addEventListener("click",  closeActionModal);
actionBackdrop?.addEventListener("click", (e) => { if (e.target === actionBackdrop) closeActionModal(); });

// ─── 4. Edit Plant Modal ─────────────────────────────────────────────────────

const editBackdrop = document.getElementById("edit-modal-backdrop");
const editFeedback  = document.getElementById("edit-feedback");

/** Opens the edit modal and pre-fills fields using getPlant() from post.js */
async function openEditModal(plantId) {
    editFeedback.textContent = "Loading...";
    document.getElementById("edit-plant-id").value = plantId;
    editBackdrop.classList.add("open");

    try {
        const plant = await getPlant(plantId);   // from post.js
        
        document.getElementById("edit-plant_name").value = plant.plant_name || "";
        document.getElementById("edit-scientific_name").value = plant.scientific_name || "";
        document.getElementById("edit-age").value = plant.age || "";
        document.getElementById("edit-health").value = plant.health || "";
        document.getElementById("edit-light_needs").value = plant.light_needs || "";
        document.getElementById("edit-fertilizer_needs").value = plant.fertilizer_needs || "";
        document.getElementById("edit-water_frequency").value = plant.water_frequency || "";
        document.getElementById("edit-pot_frequency").value = plant.pot_frequency || "";
        document.getElementById("edit-fertilizer_frequency").value = plant.fertilizer_frequency || "";
        document.getElementById("edit-notes").value = plant.notes || "";
        
        editFeedback.textContent = ""; // Clear loading message
    } catch (err) {
        editFeedback.textContent = "⚠️ Could not load plant data.";
        editFeedback.style.color = "#e65100";
    }
}

function closeEditModal() {
    editBackdrop.classList.remove("open");
}

document.getElementById("edit-modal-close")?.addEventListener("click",  closeEditModal);
document.getElementById("edit-cancel-btn")?.addEventListener("click",   closeEditModal);
editBackdrop?.addEventListener("click", (e) => { if (e.target === editBackdrop) closeEditModal(); });

/** Save button — calls updatePlant() from post.js */
document.getElementById("edit-save-btn")?.addEventListener("click", async () => {
    const plantId = document.getElementById("edit-plant-id").value;
    if (!plantId) return;

    // Grab exactly what the user typed in
    const payload = {};
    if (document.getElementById("edit-plant_name").value) payload.plant_name = document.getElementById("edit-plant_name").value;
    if (document.getElementById("edit-scientific_name").value) payload.scientific_name = document.getElementById("edit-scientific_name").value;
    if (document.getElementById("edit-health").value) payload.health = document.getElementById("edit-health").value;
    if (document.getElementById("edit-light_needs").value) payload.light_needs = document.getElementById("edit-light_needs").value;
    if (document.getElementById("edit-fertilizer_needs").value) payload.fertilizer_needs = document.getElementById("edit-fertilizer_needs").value;
    if (document.getElementById("edit-notes").value) payload.notes = document.getElementById("edit-notes").value;
    
    // Numbers need to be parsed
    if (document.getElementById("edit-age").value) payload.age = parseInt(document.getElementById("edit-age").value, 10);
    if (document.getElementById("edit-water_frequency").value) payload.water_frequency = parseInt(document.getElementById("edit-water_frequency").value, 10);
    if (document.getElementById("edit-pot_frequency").value) payload.pot_frequency = parseInt(document.getElementById("edit-pot_frequency").value, 10);
    if (document.getElementById("edit-fertilizer_frequency").value) payload.fertilizer_frequency = parseInt(document.getElementById("edit-fertilizer_frequency").value, 10);

    const saveBtn = document.getElementById("edit-save-btn");
    saveBtn.textContent = "Saving…";
    saveBtn.disabled = true;
    editFeedback.textContent = "";
    editFeedback.style.color = "#388e3c";

    try {
        // Handle image upload if a file was selected
        const fileInput = document.getElementById("edit-image_file");
        if (fileInput && fileInput.files.length > 0) {
            editFeedback.textContent = "Uploading image…";
            payload.image_url = await uploadImageFile(fileInput.files[0]);
        }

        await updatePlant(plantId, payload);   // from post.js
        editFeedback.textContent = "✅ Plant updated!";
        setTimeout(async () => {
            closeEditModal();
            await refreshDashboard();
        }, 800);
    } catch (err) {
        editFeedback.textContent = "❌ " + err.message;
        editFeedback.style.color = "#e65100";
    } finally {
        saveBtn.textContent = "Save Changes";
        saveBtn.disabled = false;
    }
});

// ─── 5. Create Plant Modal ───────────────────────────────────────────────────

const createBackdrop = document.getElementById("create-modal-backdrop");
const createFeedback  = document.getElementById("create-feedback");

function openCreateModal() {
    createFeedback.textContent = "";
    
    // Clear all fields
    document.getElementById("create-plant_name").value = "";
    document.getElementById("create-scientific_name").value = "";
    document.getElementById("create-age").value = "";
    document.getElementById("create-health").value = "";
    document.getElementById("create-light_needs").value = "";
    document.getElementById("create-fertilizer_needs").value = "";
    document.getElementById("create-water_frequency").value = "";
    document.getElementById("create-pot_frequency").value = "";
    document.getElementById("create-fertilizer_frequency").value = "";
    document.getElementById("create-notes").value = "";
    
    // Clear the file input too
    if (document.getElementById("create-image_file")) {
        document.getElementById("create-image_file").value = ""; 
    }

    createBackdrop.classList.add("open");
}

function closeCreateModal() {
    createBackdrop.classList.remove("open");
}

document.getElementById("create-modal-close")?.addEventListener("click",  closeCreateModal);
document.getElementById("create-cancel-btn")?.addEventListener("click",   closeCreateModal);
createBackdrop?.addEventListener("click", (e) => { if (e.target === createBackdrop) closeCreateModal(); });

/** Save button — calls createPlant() from post.js */
document.getElementById("create-save-btn")?.addEventListener("click", async () => {
    
    const plantName = document.getElementById("create-plant_name").value;
    if (!plantName) {
        createFeedback.textContent = "❌ Plant Name is required!";
        createFeedback.style.color = "#e65100";
        return;
    }

    // Grab exactly what the user typed in
    const payload = { plant_name: plantName };
    if (document.getElementById("create-scientific_name").value) payload.scientific_name = document.getElementById("create-scientific_name").value;
    if (document.getElementById("create-health").value) payload.health = document.getElementById("create-health").value;
    if (document.getElementById("create-light_needs").value) payload.light_needs = document.getElementById("create-light_needs").value;
    if (document.getElementById("create-fertilizer_needs").value) payload.fertilizer_needs = document.getElementById("create-fertilizer_needs").value;
    if (document.getElementById("create-notes").value) payload.notes = document.getElementById("create-notes").value;
    
    // Numbers need to be parsed
    if (document.getElementById("create-age").value) payload.age = parseInt(document.getElementById("create-age").value, 10);
    if (document.getElementById("create-water_frequency").value) payload.water_frequency = parseInt(document.getElementById("create-water_frequency").value, 10);
    if (document.getElementById("create-pot_frequency").value) payload.pot_frequency = parseInt(document.getElementById("create-pot_frequency").value, 10);
    if (document.getElementById("create-fertilizer_frequency").value) payload.fertilizer_frequency = parseInt(document.getElementById("create-fertilizer_frequency").value, 10);

    const saveBtn = document.getElementById("create-save-btn");
    saveBtn.textContent = "Saving…";
    saveBtn.disabled = true;
    createFeedback.textContent = "";
    createFeedback.style.color = "#388e3c";

    try {
        // Handle image upload if a file was selected
        const fileInput = document.getElementById("create-image_file");
        if (fileInput && fileInput.files.length > 0) {
            createFeedback.textContent = "Uploading image…";
            payload.image_url = await uploadImageFile(fileInput.files[0]);
        }

        await createPlant(payload);   // from post.js
        createFeedback.textContent = "✅ Plant created!";
        setTimeout(async () => {
            closeCreateModal();
            await refreshDashboard();
        }, 800);
    } catch (err) {
        createFeedback.textContent = "❌ " + err.message;
        createFeedback.style.color = "#e65100";
    } finally {
        saveBtn.textContent = "Create Plant";
        saveBtn.disabled = false;
    }
});

// ─── Refresh helper ──────────────────────────────────────────────────────────

/** Re-fetches all plants and redraws the grid + task list. */
async function refreshDashboard() {
    const plants = await getAllPlants();   // from post.js
    cachedPlants = plants;
    renderPlantGrid(plants);
    renderTaskList(plants);
}

// ─── Init ────────────────────────────────────────────────────────────────────

(async function init() {
    // Only run this initialization if we are on the dashboard page
    if (!document.getElementById("plant-grid")) return;

    const token = localStorage.getItem("token");
    if (!token || token === "null" || token === "undefined") {
        const gridTemplate = document.getElementById('tpl-logged-out-grid');
        const tasksTemplate = document.getElementById('tpl-logged-out-tasks');
        
        const plantGrid = document.getElementById("plant-grid");
        plantGrid.innerHTML = "";
        if (gridTemplate) plantGrid.appendChild(gridTemplate.content.cloneNode(true));
        
        const taskList = document.getElementById("task-list");
        taskList.innerHTML = "";
        if (tasksTemplate) taskList.appendChild(tasksTemplate.content.cloneNode(true));
        
        return;
    }

    await refreshDashboard();
})();

// ────────────────────────────log out──────────────────────────────
async function LogOut() {
    localStorage.removeItem("token");
    localStorage.removeItem("firstname");

    const plantGrid = document.getElementById("plant-grid");
    const gridTemplate = document.getElementById('tpl-logged-out-grid');
    if (plantGrid && gridTemplate) {
        plantGrid.innerHTML = "";
        plantGrid.appendChild(gridTemplate.content.cloneNode(true));
    }

    const taskList = document.getElementById("task-list");
    const tasksTemplate = document.getElementById('tpl-logged-out-tasks');
    if (taskList && tasksTemplate) {
        taskList.innerHTML = "";
        taskList.appendChild(tasksTemplate.content.cloneNode(true));
    }
}













// -------------------SETTINGS-----------------------------------
(async function initSettings() {
    // Only run if we are on the settings page and logged in
    if (!document.getElementById("edit-username")) return;
    
    const token = localStorage.getItem("token");
    if (!token || token === "null" || token === "undefined") return;

    try {
        const user = await getUser();
        if (user) {
            document.getElementById("edit-username").value = user.username || "";
            document.getElementById("edit-email").value = user.email || "";
            document.getElementById("edit-nickname").value = user.nickname || "";
            document.getElementById("edit-firstname").value = user.firstname || "";
            document.getElementById("edit-lastname").value = user.lastname || "";
        }
    } catch (err) {
        console.error("Failed to load user settings:", err);
    }
})();

document.getElementById("save-settings-btn")?.addEventListener("click", async () => {
    const feedback = document.getElementById("settings-feedback");
    const saveBtn = document.getElementById("save-settings-btn");
    
    const password = document.getElementById("edit-current-password").value;
    if (!password) {
        feedback.textContent = "❌ Current password is required to save changes.";
        feedback.style.color = "#e65100";
        return;
    }

    const data = {
        password: password
    };
    
    const username = document.getElementById("edit-username").value;
    if (username) data.username = username;
    
    const email = document.getElementById("edit-email").value;
    if (email) data.email = email;
    
    const nickname = document.getElementById("edit-nickname").value;
    if (nickname) data.nickname = nickname;
    
    const firstname = document.getElementById("edit-firstname").value;
    if (firstname) data.firstname = firstname;
    
    const lastname = document.getElementById("edit-lastname").value;
    if (lastname) data.lastname = lastname;

    saveBtn.textContent = "Saving...";
    saveBtn.disabled = true;
    feedback.textContent = "";

    try {
        const result = await updateUser(data);
        
        // If the backend sent a new token (because the username changed), save it!
        if (result.token) {
            localStorage.setItem("token", result.token);
        }
        
        feedback.textContent = "✅ Settings saved successfully!";
        feedback.style.color = "#388e3c";
        
        // If firstname was updated, update localStorage and navbar
        if (data.firstname) {
            localStorage.setItem("firstname", data.firstname);
            const nameElement = document.getElementById('nav-firstname');
            if (nameElement) nameElement.textContent = data.firstname;
        }
        
        // Clear password field for safety
        document.getElementById("edit-current-password").value = "";
    } catch (err) {
        feedback.textContent = "❌ " + (err.message || "Failed to update settings");
        feedback.style.color = "#e65100";
    } finally {
        saveBtn.textContent = "Save Changes";
        saveBtn.disabled = false;
    }
});
