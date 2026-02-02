document.addEventListener("DOMContentLoaded", () => {
  const url = localStorage.getItem("lastAnalyzedUrl");
  

  if (!url) {
    alert("Please analyze a website first.");
    return;
  }

  document.getElementById("report-url").innerText = url;

  fetch(`/api/analyze/?url=${encodeURIComponent(url)}`)
    .then(res => res.json())
    .then(data => {
      document.getElementById("loader").style.display = "none";
      document.getElementById("report").classList.remove("hidden");

      renderScore(data);
      renderFeatures(data);
      renderIssues(data);
      renderChart(data);
    })
    .catch(err => {
      alert("Failed to load report.");
      console.error(err);
    });
});

/* ===== RENDER FUNCTIONS ===== */

function renderScore(data) {
  document.getElementById("seoScore").innerText = Math.round(data.seo_score);
}

function renderFeatures(data) {
  const list = document.getElementById("featuresList");
  const f = data.features || {};

  Object.entries(f).forEach(([k, v]) => {
    const li = document.createElement("li");
    li.innerHTML = `<strong>${k.replace(/_/g, " ")}:</strong> ${v}`;
    list.appendChild(li);
  });
}

function renderIssues(data) {
  const container = document.getElementById("issuesContainer");
  const issues = data.issues || [];

  if (!issues.length) {
    container.innerHTML = "<p>FIX YOUR WEBSITE</p>";
    return;
  }

  issues.forEach(i => {
    const div = document.createElement("div");
    div.className = "issue";
    div.innerHTML = `
      <h3>${i.title}</h3>
      <p>${i.description}</p>
      <p><strong>Theory:</strong> ${i.theory}</p>
      <p><strong>Fix:</strong> ${i.mitigation.summary}</p>
      <ul>${i.mitigation.steps.map(s => `<li>${s}</li>`).join("")}</ul>
    `;
    container.appendChild(div);
  });
}

function renderChart(data) {
  new Chart(document.getElementById("radarChart"), {
    type: "radar",
    data: {
      labels: ["Content", "Images", "Structure", "Links", "SEO"],
      datasets: [{
        label: "SEO Health",
        data: [
          data.semantic_effectiveness?.semantic_score || 50,
          100 - (data.features?.img_without_alt || 0),
          data.features?.h1_count ? 80 : 40,
          data.features?.internal_links || 40,
          data.seo_score
        ],
        backgroundColor: "rgba(99,102,241,0.25)",
        borderColor: "#6366f1"
      }]
    }
  });
}