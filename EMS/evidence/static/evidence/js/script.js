document.getElementById("submitBtn").addEventListener("click", function() {
    const form = document.getElementById("evidenceForm");
    const evidenceInput = document.getElementById("evidence");
    const errorMessage = document.getElementById("error-message");
  
    // Check if the form is filled out correctly and the evidence is selected
    if (!form.checkValidity() || evidenceInput.files.length === 0) {
      // If any required field is missing or no evidence file is selected, show error
      errorMessage.style.display = "block";
    } else {
      // If everything is correct, hide error message and proceed
      errorMessage.style.display = "none";
      
      const formData = new FormData(form);
  
      // Process files
      const files = formData.getAll("evidence"); // Get all evidence files
      console.log("Uploaded Files:", files);
  
      fetch("http://localhost:8080/api/evidence/submit", {
        method: "POST",
        body: formData,
      })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      })
      .then((data) => {
        alert(data); // Show success message
      })
      .catch((error) => {
        console.error("There was a problem with the fetch operation:", error);
      });
    }
  });
  