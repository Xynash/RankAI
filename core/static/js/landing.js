document.getElementById("analyzeBtn").addEventListener("click", () => {
  const url = document.getElementById("urlInput").value;

  if (!url) {
    alert("Please enter a website URL");
    return;
  }

  alert("SEO analysis will be available in the dashboard.");
});