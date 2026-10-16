
const featureGrid = document.getElementById("featureGrid");
const form = document.getElementById("predictionForm");
const resultBox = document.getElementById("result");
const formStatus = document.getElementById("formStatus");
const predictBtn = document.getElementById("predictBtn");

let sampleFeatures = {};

function showError(message) {
  resultBox.className = "result attack";
  resultBox.innerHTML = "";
  const heading = document.createElement("h3");
  heading.textContent = "Unable to complete prediction";
  const paragraph = document.createElement("p");
  paragraph.textContent = message;
  resultBox.append(heading, paragraph);
}

function renderFields(features) {
  featureGrid.replaceChildren();

  for (const [name, value] of Object.entries(features)) {
    const wrapper = document.createElement("div");
    wrapper.className = "field";

    const label = document.createElement("label");
    label.htmlFor = `feature-${name}`;
    label.textContent = name;

    const input = document.createElement("input");
    input.id = `feature-${name}`;
    input.name = name;
    input.value = value ?? "";
    input.required = true;
    input.autocomplete = "off";
    input.setAttribute("aria-label", name);

    wrapper.append(label, input);
    featureGrid.append(wrapper);
  }

  formStatus.textContent =
    `${Object.keys(features).length} model features loaded. ` +
    "Load a sample to start, then edit values if needed.";
}

async function loadSample() {
  formStatus.textContent = "Loading sample feature values…";

  try {
    const response = await fetch("/api/sample");
    const data = await response.json();

    if (!response.ok) throw new Error(data.error || "Could not load sample.");

    sampleFeatures = data.features;
    renderFields(sampleFeatures);
    resultBox.className = "result hidden";
    formStatus.textContent =
      "Sample values loaded from the local dataset. " +
      "You can edit them before predicting.";
  } catch (error) {
    formStatus.textContent = error.message;
  }
}

async function loadMetrics() {
  try {
    const response = await fetch("/api/metrics");
    const data = await response.json();

    if (!response.ok) throw new Error(data.error || "Metrics unavailable.");

    const values = data.metrics;
    for (const [key, elementId] of [
      ["accuracy", "accuracy"],
      ["precision", "precision"],
      ["recall", "recall"],
      ["f1_score", "f1"]
    ]) {
      const value = values[key];
      document.getElementById(elementId).textContent =
        typeof value === "number" ? `${(value * 100).toFixed(2)}%` : "N/A";
    }
  } catch {
    for (const id of ["accuracy", "precision", "recall", "f1"]) {
      document.getElementById(id).textContent = "Unavailable";
    }
  }
}

document.getElementById("sampleBtn").addEventListener("click", loadSample);

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  predictBtn.disabled = true;
  predictBtn.textContent = "Analyzing…";
  resultBox.className = "result hidden";

  try {
    const features = {};

    for (const input of featureGrid.querySelectorAll("input")) {
      features[input.name] = input.value;
    }

    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ features })
    });

    const data = await response.json();
    if (!response.ok) {
      const details = data.missing_features
        ? ` Missing fields: ${data.missing_features.join(", ")}`
        : "";
      throw new Error((data.error || "Prediction failed.") + details);
    }

    const isAttack = data.prediction === 1;
    resultBox.className = `result ${isAttack ? "attack" : "normal"}`;
    resultBox.replaceChildren();

    const heading = document.createElement("h3");
    heading.textContent = isAttack
      ? "⚠ Potential Attack"
      : "✓ Classified as Normal";

    const probability = document.createElement("p");
    probability.textContent =
      data.attack_probability == null
        ? "Attack probability is unavailable."
        : `Estimated attack probability: ${(data.attack_probability * 100).toFixed(2)}%`;

    const warning = document.createElement("p");
    warning.textContent = data.warning;

    resultBox.append(heading, probability, warning);
  } catch (error) {
    showError(error.message);
  } finally {
    predictBtn.disabled = false;
    predictBtn.textContent = "Analyze traffic record →";
  }
});

loadMetrics();
loadSample();
