const API_BASE_URL = "http://localhost:8004";
const BACKEND_URL = "http://localhost:8000";
const LOGIN_URL = `${BACKEND_URL}/auth/login`;
const REGISTER_URL = `${BACKEND_URL}/users/`;

let currentUser = null;
let currentSlots = [];
let currentVehicles = [];
let selectedSlot = null;

function $(id) {
  return document.getElementById(id);
}

function authHeaders(includeJson = false) {
  const headers = {};
  const token = localStorage.getItem("access_token");

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  if (includeJson) {
    headers["Content-Type"] = "application/json";
  }

  return headers;
}

async function apiRequest(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: {
      ...authHeaders(Boolean(options.body)),
      ...(options.headers || {})
    }
  });

  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json")
    ? await response.json()
    : null;

  if (response.status === 401) {
    logout();
    throw new Error("Your session has expired. Please login again.");
  }

  if (!response.ok) {
    const detail = data && data.detail;
    throw new Error(
      typeof detail === "string"
        ? detail
        : `Request failed (HTTP ${response.status}).`
    );
  }

  return data;
}

async function apiGet(path, baseUrl = API_BASE_URL) {
  try {
    return {
      ok: true,
      data: await apiRequest(`${baseUrl}${path}`)
    };
  } catch (error) {
    console.error(`API error: ${path}`, error);
    return { ok: false, error: error };
  }
}

function showStatus(key, result, okText) {
  document.querySelectorAll(`[data-status="${key}"]`).forEach((element) => {
    element.classList.toggle("ok", result.ok);
    element.classList.toggle("fail", !result.ok);
    element.textContent = result.ok ? okText : "Service unavailable";
  });
}

function setAllLoading() {
  document.querySelectorAll("[data-status]").forEach((element) => {
    element.className = "status";
    element.textContent = "Checking...";
  });
}

function serviceText(result) {
  if (result.ok && result.data && result.data.status) {
    return result.data.status.charAt(0).toUpperCase()
      + result.data.status.slice(1);
  }

  return "Unavailable";
}

async function loadDashboard() {
  setAllLoading();

  const [health, users, parking, bookings] = await Promise.all([
    apiGet("/health"),
    apiGet("/users"),
    apiGet("/parking"),
    apiGet("/bookings")
  ]);

  showStatus("health", health, "Healthy");
  showStatus("users", users, serviceText(users));
  showStatus("parking", parking, serviceText(parking));
  showStatus("bookings", bookings, serviceText(bookings));
}

async function loadCurrentUser() {
  currentUser = await apiRequest(`${BACKEND_URL}/auth/me`);
  $("welcome").textContent = `Welcome, ${currentUser.name}.`;
}

function formatDateTime(value) {
  return new Date(value).toLocaleString();
}

function showParkingMessage(message, isError = false) {
  const element = $("parking-message");
  element.textContent = message;
  element.className = isError ? "error" : "muted";
  element.hidden = !message;
}

function renderSlots() {
  const container = $("slots");
  container.innerHTML = "";

  if (!currentSlots.length) {
    showParkingMessage("No parking slots are currently configured.");
    return;
  }

  showParkingMessage("");

  currentSlots.forEach((slot) => {
    const available = slot.status === "AVAILABLE";
    const button = document.createElement("button");

    button.type = "button";
    button.className = `slot ${available ? "available" : "occupied"}`;
    button.textContent = `${slot.slot_number} (${slot.status})`;
    button.disabled = !available;
    button.title = available
      ? "Click to book this slot"
      : "This slot is occupied";

    if (available) {
      button.addEventListener("click", () => openBookingForm(slot));
    }

    container.appendChild(button);
  });
}

async function loadParking() {
  showParkingMessage("Loading parking slots...");

  try {
    currentSlots = await apiRequest(`${BACKEND_URL}/parking-slots/`);
    renderSlots();
    showStatus("parking", { ok: true }, "Running");
  } catch (error) {
    console.error("Parking error:", error);
    currentSlots = [];
    $("slots").innerHTML = "";
    showParkingMessage(error.message, true);
    showStatus("parking", { ok: false }, "Unavailable");
  }
}

async function loadVehicles() {
  const vehicles = await apiRequest(`${BACKEND_URL}/vehicles/`);
  currentVehicles = vehicles.filter(
    (vehicle) => currentUser && vehicle.user_id === currentUser.id
  );
  return currentVehicles;
}

function setDateDefaults() {
  const start = new Date();
  const end = new Date(start.getTime() + 60 * 60 * 1000);
  const toInputValue = (date) => {
    const offset = date.getTimezoneOffset() * 60000;
    return new Date(date.getTime() - offset).toISOString().slice(0, 16);
  };

  $("booking-start").value = toInputValue(start);
  $("booking-end").value = toInputValue(end);
}

function renderVehicleOptions() {
  const select = $("booking-vehicle");
  select.innerHTML = "";

  currentVehicles.forEach((vehicle) => {
    const option = document.createElement("option");
    option.value = vehicle.id;
    option.textContent =
      `${vehicle.vehicle_number} (${vehicle.vehicle_type})`;
    select.appendChild(option);
  });

  const newOption = document.createElement("option");
  newOption.value = "new";
  newOption.textContent = "Add a new vehicle";
  select.appendChild(newOption);

  $("new-vehicle-fields").hidden = currentVehicles.length > 0;
}

function updateVehicleFields() {
  $("new-vehicle-fields").hidden =
    $("booking-vehicle").value !== "new";
}

async function openBookingForm(slot) {
  selectedSlot = slot;
  $("selected-slot-label").textContent =
    `${slot.slot_number} (Floor ${slot.floor})`;
  $("booking-card").hidden = false;
  $("booking-message").hidden = true;
  setDateDefaults();

  try {
    await loadVehicles();
    renderVehicleOptions();
  } catch (error) {
    $("booking-message").textContent = error.message;
    $("booking-message").hidden = false;
  }
}

function closeBookingForm() {
  selectedSlot = null;
  $("booking-card").hidden = true;
}

async function createVehicleIfNeeded() {
  const vehicleId = $("booking-vehicle").value;

  if (vehicleId !== "new") {
    return Number(vehicleId);
  }

  const vehicleNumber = $("vehicle-number").value.trim();
  const vehicleType = $("vehicle-type").value.trim();

  if (!vehicleNumber || !vehicleType) {
    throw new Error("Vehicle number and type are required.");
  }

  const vehicle = await apiRequest(`${BACKEND_URL}/vehicles/`, {
    method: "POST",
    body: JSON.stringify({
      user_id: currentUser.id,
      vehicle_number: vehicleNumber,
      vehicle_type: vehicleType
    })
  });

  return vehicle.id;
}

async function submitBooking(event) {
  event.preventDefault();

  const message = $("booking-message");
  const button = $("booking-submit-btn");
  message.hidden = true;
  button.disabled = true;

  try {
    if (!selectedSlot || selectedSlot.status !== "AVAILABLE") {
      throw new Error("This parking slot is no longer available.");
    }

    const vehicleId = await createVehicleIfNeeded();
    await apiRequest(`${BACKEND_URL}/bookings/`, {
      method: "POST",
      body: JSON.stringify({
        user_id: currentUser.id,
        vehicle_id: vehicleId,
        slot_id: selectedSlot.id,
        start_time: new Date($("booking-start").value).toISOString(),
        end_time: new Date($("booking-end").value).toISOString()
      })
    });

    closeBookingForm();
    await loadParking();
    await loadBookings();
  } catch (error) {
    console.error("Booking error:", error);
    message.textContent = error.message;
    message.hidden = false;
  } finally {
    button.disabled = false;
  }
}

async function loadBookings() {
  const list = $("bookings-list");
  const message = $("bookings-message");
  list.innerHTML = "";
  message.hidden = true;

  try {
    const [bookings, slots, vehicles] = await Promise.all([
      apiRequest(`${BACKEND_URL}/bookings/me`),
      apiRequest(`${BACKEND_URL}/parking-slots/`),
      loadVehicles()
    ]);
    const slotById = new Map(slots.map((slot) => [slot.id, slot]));
    const vehicleById = new Map(
      vehicles.map((vehicle) => [vehicle.id, vehicle])
    );

    if (!bookings.length) {
      list.innerHTML =
        '<div class="card empty"><p>No bookings found.</p></div>';
      return;
    }

    bookings.forEach((booking) => {
      const slot = slotById.get(booking.slot_id);
      const vehicle = vehicleById.get(booking.vehicle_id);
      const card = document.createElement("div");
      card.className = "card booking-item";
      card.innerHTML = `
        <h4>Booking #${booking.id}</h4>
        <p>Slot: ${slot ? slot.slot_number : `#${booking.slot_id}`}</p>
        <p>Vehicle: ${vehicle ? vehicle.vehicle_number : `#${booking.vehicle_id}`}</p>
        <p>Status: ${booking.status}</p>
        <p>${formatDateTime(booking.start_time)} - ${formatDateTime(booking.end_time)}</p>
      `;

      const cancelButton = document.createElement("button");
      cancelButton.className = "btn";
      cancelButton.type = "button";
      cancelButton.textContent = "Cancel Booking";
      cancelButton.addEventListener(
        "click",
        () => cancelBooking(booking.id)
      );
      card.appendChild(cancelButton);
      list.appendChild(card);
    });
  } catch (error) {
    console.error("Bookings error:", error);
    message.textContent = error.message;
    message.hidden = false;
  }
}

async function cancelBooking(bookingId) {
  if (!window.confirm("Cancel this booking?")) {
    return;
  }

  try {
    await apiRequest(`${BACKEND_URL}/bookings/${bookingId}`, {
      method: "DELETE"
    });
    await loadParking();
    await loadBookings();
  } catch (error) {
    $("bookings-message").textContent = error.message;
    $("bookings-message").hidden = false;
  }
}

async function login(event) {
  event.preventDefault();
  const errorBox = $("login-error");
  const button = $("login-btn");
  errorBox.hidden = true;
  button.disabled = true;
  button.textContent = "Logging in...";

  try {
    const data = await apiRequest(LOGIN_URL, {
      method: "POST",
      body: JSON.stringify({
        email: $("email").value.trim(),
        password: $("password").value
      })
    });

    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("user_email", $("email").value.trim());
    $("password").value = "";
    await showApp();
  } catch (error) {
    console.error("Login error:", error);
    errorBox.textContent = error instanceof TypeError
      ? "Cannot reach the login service. Is the backend running?"
      : error.message;
    errorBox.hidden = false;
  } finally {
    button.disabled = false;
    button.textContent = "Login";
  }
}

async function register(event) {
  event.preventDefault();
  const messageBox = $("register-message");
  const button = $("register-btn");
  messageBox.hidden = true;

  const password = $("register-password").value;
  if (password !== $("register-confirm-password").value) {
    messageBox.textContent = "Passwords do not match.";
    messageBox.hidden = false;
    return;
  }

  if (password.length < 6) {
    messageBox.textContent = "Password must be at least 6 characters.";
    messageBox.hidden = false;
    return;
  }

  button.disabled = true;
  button.textContent = "Creating Account...";

  try {
    await apiRequest(REGISTER_URL, {
      method: "POST",
      body: JSON.stringify({
        name: $("register-name").value.trim(),
        email: $("register-email").value.trim(),
        password: password
      })
    });

    messageBox.className = "success";
    messageBox.textContent = "Account created successfully! Please login.";
    messageBox.hidden = false;
    $("register-form").reset();
    window.setTimeout(showLogin, 1500);
  } catch (error) {
    console.error("Registration error:", error);
    messageBox.className = "error";
    messageBox.textContent = error instanceof TypeError
      ? "Cannot reach the registration service. Is the backend running?"
      : error.message;
    messageBox.hidden = false;
  } finally {
    button.disabled = false;
    button.textContent = "Create Account";
  }
}

function showLogin() {
  $("register-screen").hidden = true;
  $("login-screen").hidden = false;
  $("login-error").hidden = true;
}

function showRegister() {
  $("login-screen").hidden = true;
  $("register-screen").hidden = false;
  $("register-message").hidden = true;
}

function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user_email");
  currentUser = null;
  $("app").hidden = true;
  $("login-screen").hidden = false;
  $("register-screen").hidden = true;
}

async function showSection(name) {
  document.querySelectorAll(".section").forEach((section) => {
    section.hidden = section.id !== name;
  });

  document.querySelectorAll(".nav-btn[data-section]").forEach((button) => {
    button.classList.toggle("active", button.dataset.section === name);
  });

  if (name === "parking") {
    await loadParking();
  }

  if (name === "bookings") {
    await loadBookings();
  }
}

async function showApp() {
  $("login-screen").hidden = true;
  $("register-screen").hidden = true;
  $("app").hidden = false;

  try {
    await loadCurrentUser();
    await showSection("dashboard");
    await loadDashboard();
  } catch (error) {
    console.error("Session error:", error);
    $("login-error").textContent = error.message;
    logout();
    $("login-error").hidden = false;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  $("login-form").addEventListener("submit", login);
  $("register-form").addEventListener("submit", register);
  $("show-register-btn").addEventListener("click", showRegister);
  $("show-login-btn").addEventListener("click", showLogin);
  $("logout-btn").addEventListener("click", logout);
  $("refresh-btn").addEventListener("click", loadDashboard);
  $("refresh-parking-btn").addEventListener("click", loadParking);
  $("booking-form").addEventListener("submit", submitBooking);
  $("booking-cancel-btn").addEventListener("click", closeBookingForm);
  $("booking-vehicle").addEventListener("change", updateVehicleFields);

  document.querySelectorAll(".nav-btn[data-section]").forEach((button) => {
    button.addEventListener("click", () => showSection(button.dataset.section));
  });

  if (localStorage.getItem("access_token")) {
    showApp();
  }
});
