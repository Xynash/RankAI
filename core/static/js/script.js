function analyzeWebsite() {
  const urlInput = document.getElementById("websiteUrl");
  if (!urlInput || !urlInput.value.trim()) {
    alert("Please enter a website URL");
    return;
  }

  const url = urlInput.value.trim();

  fetch(`/api/analyze/?url=${encodeURIComponent(url)}`)
    .then(res => res.json())
    .then(data => {
      console.log("AI DATA:", data);
      localStorage.setItem("lastAnalyzedUrl", url);
      window.location.href = "/reports/";

      
      window.location.href = `/reports/?url=${encodeURIComponent(url)}`;


      /* ================= SEO SCORE ================= */
      const seoScoreEl = document.getElementById("seoScore");
      const seoScoreTextEl = document.getElementById("seoScoreText");

      if (seoScoreEl)
        seoScoreEl.innerText = Number(data.seo_score || 0).toFixed(2);

      if (seoScoreTextEl)
        seoScoreTextEl.innerText = "Analysis Complete";

      /* ================= SEMANTIC EFFECTIVENESS ================= */
      const semanticEl = document.getElementById("semanticScore");
      if (semanticEl && data.semantic_effectiveness) {
        semanticEl.innerText =
          `Score: ${data.semantic_effectiveness.semantic_score} | ` +
          `Unique Terms: ${data.semantic_effectiveness.unique_terms}`;
      }

      /* ================= AI PROMPT VISIBILITY ================= */
      const pvList = document.getElementById("promptVisibility");
      const pv = data.ai_visibility?.prompt_visibility;

      if (pvList && pv) {
        pvList.innerHTML = `
          <li>Search intent match — ${pv.search_intent}</li>
          <li>Content clarity — ${pv.content_clarity}</li>
          <li>Keyword coverage — ${pv.keyword_coverage}</li>
        `;
      }

      /* ================= SITE AUDIT ================= */
      const auditList = document.getElementById("siteAuditList");
      if (auditList) {
        auditList.innerHTML = "";

        const audit = data.site_audit?.audit;
        if (!audit) {
          auditList.innerHTML = "<li>No audit data available</li>";
        } else {
          const items = [
            ["Meta Descriptions", audit.meta_description?.status],
            ["Mobile Responsive", audit.mobile_responsive?.status],
            ["Page Speed", audit.page_speed?.status],
            ["Broken Links", audit.broken_links?.status]
          ];

          items.forEach(([label, status]) => {
            const li = document.createElement("li");

            let icon = "⚠";
            if (status === "Good" || status === "Clean") icon = "✔";
            if (status === "Missing" || status === "Poor") icon = "❌";

            li.textContent = `${label} — ${icon} ${status || "Unknown"}`;
            auditList.appendChild(li);
          });
        }
      }

      /* ================= AI RECOMMENDED KEYWORDS ================= */
      const keywordList = document.getElementById("keywordList");
      if (keywordList) {
        keywordList.innerHTML = "";

        const keywords = data.recommended_keywords || [];
        if (!keywords.length) {
          keywordList.innerHTML = "<li>No keyword data available</li>";
        } else {
          keywords.forEach(k => {
            const li = document.createElement("li");
            li.innerHTML = `
              <strong>${k.keyword}</strong>
              <small>
                (Freq: ${k.frequency}, Importance: ${k.importance}%, Intent: ${k.intent})
              </small>
            `;
            keywordList.appendChild(li);
          });
        }
      }

      /* ================= SEO RANKING OVERVIEW ================= */
      const visibility = document.getElementById("visibility");
      const top_keywords = document.getElementById("top_keywords");
      const estimated_traffic = document.getElementById("estimated_traffic");

      if (visibility)
        visibility.innerText = data.tracking_overview?.llm_visibility ?? "--";

      if (top_keywords)
        top_keywords.innerText = (data.recommended_keywords || []).length;
      if (estimated_traffic)
        estimated_traffic.innerText = data.seo_ranking_overview?.estimated_traffic ?? "--";
        
      /* ================= AI TRACKING OVERVIEW (PERCENT BARS) ================= */
      setBar("llmBar", data.tracking_overview?.llm_visibility);
      setBar("chatgptBar", data.tracking_overview?.chatgpt);
      setBar("perplexityBar", data.tracking_overview?.perplexity);
      setBar("claudeBar", data.tracking_overview?.claude);
      /* ===== Helper for animated bars ===== */
      function setBar(id, value) {
      const bar = document.getElementById(id);
      if (!bar || value == null) return;

      bar.style.width = value + "%";
      bar.innerText = value + "%";
}
     
    })
    
    .catch(err => {
      console.error("Analysis Error:", err);
      alert("Analysis failed. Check console.");
    });
} 
