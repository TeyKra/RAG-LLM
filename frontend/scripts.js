document.addEventListener("DOMContentLoaded", () => {
    const populateForm = document.getElementById("populate-form");
    const queryForm = document.getElementById("query-form");
  
    populateForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(populateForm);
      const response = await fetch("/populate", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
      document.getElementById("populate-response").innerText = JSON.stringify(result, null, 2);
    });
  
    queryForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(queryForm);
      const response = await fetch("/query", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
      document.getElementById("query-response").innerText = JSON.stringify(result, null, 2);
    });
  });
  