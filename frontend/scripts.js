document.addEventListener("DOMContentLoaded", () => {
    const populateForm = document.getElementById("populate-form");
    const queryForm = document.getElementById("query-form");
    const populateResponse = document.getElementById("populate-response");
    const queryResponse = document.getElementById("query-response");
  
    // Gestion du formulaire "populate"
    populateForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(populateForm);
      const response = await fetch("/populate", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
  
      /*
        On suppose que le résultat ressemble à :
        {
          "message": "Database populated successfully",
          "reset": false
        }
        On affiche seulement la partie "message".
      */
      if (result.message) {
        populateResponse.textContent = result.message;
      } else {
        populateResponse.textContent = JSON.stringify(result, null, 2);
      }
    });
  
    // Gestion du formulaire "query"
    queryForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(queryForm);
      const response = await fetch("/query", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
  
      /*
        On suppose que le résultat ressemble à :
        {
          "response": "Answer:\nGraphes are...\n\nSources:\n ['data/...','data/...']"
        }
  
        Objectif :
        - Ne plus afficher le JSON brut
        - Afficher uniquement le texte de la réponse
          (sans le préfixe "Answer:\n")
        - Afficher la liste des sources en dessous, à la ligne,
          sous la forme "Sources: data/Cours..., data/Cours..., ..."
      */
  
      let rawText = result.response || "";
  
      // Supprime "Answer:\n" au début s’il est présent
      rawText = rawText.replace(/^Answer:\n/i, "");
  
      // Sépare la réponse et les sources en cherchant le bloc "Sources:"
      let [answerText, sourcesText] = rawText.split(/\n+Sources:\n+/);
  
      // Si la séparation n'a pas fonctionné, on assigne des valeurs par défaut
      if (!answerText) answerText = rawText;
      if (!sourcesText) sourcesText = "";
  
      // Nettoie les crochets et les guillemets potentiels dans la liste des sources
      sourcesText = sourcesText.replace(/[\[\]']+/g, "");
      // On peut aussi remplacer les virgules pour un affichage plus lisible
      // (attention si les chemins contiennent des virgules, ajuster selon les besoins)
      sourcesText = sourcesText.replace(/,/g, ", ");
  
      // Construit l'affichage final
      let finalDisplay = answerText.trim();
      if (sourcesText.trim()) {
        finalDisplay += `\n\nSources: ${sourcesText.trim()}`;
      }
  
      // Affiche le texte formaté
      queryResponse.textContent = finalDisplay;
    });
  });
  