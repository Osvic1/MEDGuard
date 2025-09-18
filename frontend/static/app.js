// =========================
// Rotating tagline
// =========================
const taglines = [
  "Because your health deserves the truth.",
  "No more guessing — just scanning.",
  "Keeping counterfeit meds off the streets.",
  "Your pocket pharmacist."
];
let taglineIndex = 0;
function rotateTagline() {
  const taglineEl = document.getElementById('tagline');
  if (taglineEl) {
    taglineEl.textContent = taglines[taglineIndex];
    taglineIndex = (taglineIndex + 1) % taglines.length;
  }
}
setInterval(rotateTagline, 3000);
rotateTagline(); // initial load

// =========================
// QR Scanner
// =========================
let html5QrCode;
const qrRegionId = "qr-reader";

function startScanner() {
  if (!html5QrCode) {
    html5QrCode = new Html5Qrcode(qrRegionId);
  }
  html5QrCode.start(
    { facingMode: "environment" },
    { fps: 10, qrbox: 250 },
    (decodedText) => {
      stopScanner();
      // NEW: open verification page in new tab
      openVerificationPage(decodedText);
    },
    () => {} // ignore scan errors
  ).catch(err => {
    console.error("Unable to start scanning:", err);
    showMessage("Camera access failed. Please check permissions.", "error");
  });
}

function stopScanner() {
  if (html5QrCode) {
    html5QrCode.stop().catch(err => console.error("Stop failed:", err));
  }
}

// =========================
// NEW: Open verification page in new tab
// =========================
function openVerificationPage(batchNumber) {
  if (!batchNumber) {
    showMessage("Please enter a batch number.", "error");
    return;
  }
  window.open(`/verify/${encodeURIComponent(batchNumber)}`, "_blank");
}

// =========================
// Verify batch (manual or QR) — OLD JSON flow
// =========================
// Keeping this in case you still want AJAX verification inside the page.
// But manual verify button will now use openVerificationPage instead.
function verifyBatch(batchNumber) {
  if (!batchNumber) {
    showMessage("Please enter a batch number.", "error");
    return;
  }
  fetch(`/api/verify/${encodeURIComponent(batchNumber)}`)
    .then(res => res.json())
    .then(data => {
      showResult(data);
    })
    .catch(err => {
      console.error(err);
      showMessage("Error verifying batch", "error");
    });
}

function showResult(data) {
  const resultContainer = document.getElementById("result");
  if (!resultContainer) return;

  let statusClass = "";
  let statusText = "";

  if (data.status === "valid") {
    statusClass = "result-valid";
    statusText = "✅ Valid";
  } else if (data.status === "expired") {
    statusClass = "result-expired";
    statusText = "⚠️ Expired";
  } else if (data.status === "counterfeit") {
    statusClass = "result-counterfeit";
    statusText = "❌ Counterfeit";
  } else {
    statusText = "ℹ️ Unknown status";
  }

  resultContainer.innerHTML = `
    <div class="result-box ${statusClass}">
      <strong>${statusText}</strong>
      <div class="msg">${data.message || ""}</div>
    </div>
  `;
}

// =========================
// Report counterfeit
// =========================
function reportCounterfeit() {
  const drug = document.getElementById("report-drug").value.trim();
  const batch = document.getElementById("report-batch").value.trim();
  const location = document.getElementById("report-location").value.trim();
  const note = document.getElementById("report-note").value.trim();

  if (!batch) {
    showMessage("Batch number is required to report.", "error");
    return;
  }

  fetch("/api/report", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      drug_name: drug,
      batch_number: batch,
      location,
      note
    })
  })
    .then(res => res.json())
    .then(data => {
      showMessage(data.message || "Report submitted successfully", "success");
    })
    .catch(err => {
      console.error(err);
      showMessage("Error submitting report", "error");
    });
}


// =========================
// Utility: show message
// =========================
function showMessage(msg, type) {
  const resultContainer = document.getElementById("result");
  if (!resultContainer) return;
  let colorClass = "";
  if (type === "success") colorClass = "result-valid";
  if (type === "error") colorClass = "result-counterfeit";

  resultContainer.innerHTML = `
    <div class="result-box ${colorClass}">
      <div class="msg">${msg}</div>
    </div>
  `;
}

// =========================
// Event listeners
// =========================
document.addEventListener("DOMContentLoaded", () => {
  // Start/Stop scanner
  const startBtn = document.getElementById("start-scan");
  const stopBtn = document.getElementById("stop-scan");
  if (startBtn) startBtn.addEventListener("click", startScanner);
  if (stopBtn) stopBtn.addEventListener("click", stopScanner);

  // Manual verify — UPDATED to open new tab
  const verifyBtn = document.getElementById("verify-btn");
  if (verifyBtn) {
    verifyBtn.addEventListener("click", () => {
      const batchInput = document.getElementById("verify-batch");
      openVerificationPage(batchInput.value.trim());
    });
  }

  // Report counterfeit
  const reportBtn = document.getElementById("report-btn");
  if (reportBtn) {
    reportBtn.addEventListener("click", reportCounterfeit);
  }
});
