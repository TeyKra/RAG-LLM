document.addEventListener("DOMContentLoaded", () => {
  const populateForm = document.getElementById("populate-form");
  const queryForm = document.getElementById("query-form");
  const populateResponse = document.getElementById("populate-response");
  const queryResponse = document.getElementById("query-response");

  // Handle the "populate" form submission
  populateForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior
    const formData = new FormData(populateForm);
    const response = await fetch("/populate", {
      method: "POST",
      body: formData,
    });
    const result = await response.json();

    /*
      We assume the result has the following structure:
      {
        "message": "Database populated successfully",
        "reset": false
      }
      We only display the "message" part.
    */
    if (result.message) {
      populateResponse.textContent = result.message;
    } else {
      populateResponse.textContent = JSON.stringify(result, null, 2);
    }
  });

  // Handle the "query" form submission
  queryForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior
    const formData = new FormData(queryForm);
    const response = await fetch("/query", {
      method: "POST",
      body: formData,
    });
    const result = await response.json();

    /*
      We assume the result has the following structure:
      {
        "response": "Answer:\nGraphes are...\n\nSources:\n ['data/...','data/...']"
      }

      Objective:
      - Do not display the raw JSON.
      - Display only the text of the response (without the "Answer:\n" prefix).
      - Display the list of sources below, on a new line, formatted as:
        "Sources: data/Cours..., data/Cours..., ..."
    */

    let rawText = result.response || "";

    // Remove "Answer:\n" at the beginning if present
    rawText = rawText.replace(/^Answer:\n/i, "");

    // Split the answer and the sources by searching for the "Sources:" block
    let [answerText, sourcesText] = rawText.split(/\n+Sources:\n+/);

    // If the split did not work, assign default values
    if (!answerText) answerText = rawText;
    if (!sourcesText) sourcesText = "";

    // Clean up any brackets and quotes that may be present in the sources list
    sourcesText = sourcesText.replace(/[\[\]']+/g, "");
    // Optionally, replace commas with a comma and space for better readability
    // (if the paths contain commas, adjust as needed)
    sourcesText = sourcesText.replace(/,/g, ", ");

    // Build the final display text
    let finalDisplay = answerText.trim();
    if (sourcesText.trim()) {
      finalDisplay += `\n\nSources: ${sourcesText.trim()}`;
    }

    // Display the formatted text in the query response area
    queryResponse.textContent = finalDisplay;
  });
});
