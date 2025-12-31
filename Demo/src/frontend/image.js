document.addEventListener("DOMContentLoaded", () => {
  const uploadForm = document.getElementById("uploadForm");
  const imageInput = document.getElementById("imageInput");
  const emotionDisplay = document.getElementById("uploadEmotion");
  const probabilitiesDisplay = document.getElementById("uploadProbabilities");
  const canvas = document.getElementById("uploadCanvas");
  const ctx = canvas.getContext("2d");

  // Clear results when a new file is chosen
  imageInput.addEventListener("change", () => {
    emotionDisplay.textContent = "";
    probabilitiesDisplay.innerHTML = "";
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  });

  uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const file = imageInput.files[0];
    if (!file) {
      alert("Please select an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      swal({
        title: "Uploading image!",
        icon: "info",
        closeOnEsc: false,
        closeOnClickOutside: false,
      });

      const response = await fetch("/api/predict", {
        method: "POST",
        body: formData
      });

      if (!response.ok) throw new Error("Prediction request failed");

      let result = await response.json();
      if (result.code !== 200) {
        swal.close();
        swal({
          title: result.message,
          icon: "error",
          closeOnEsc: false,
          closeOnClickOutside: false,
        });
      } else {
        swal.close();
        swal({
          title: result.message,
          icon: "success",
          closeOnEsc: false,
          closeOnClickOutside: false,
          timer: 1000,
        }).then(function () {
          result = result.data;

          // Update emotion display
          emotionDisplay.textContent = `Predicted Emotion: ${result.predicted_emotion}`;

          // Update probabilities display
          probabilitiesDisplay.innerHTML = "";
          for (const [label, prob] of Object.entries(result.probabilities)) {
            const wrapper = document.createElement("div");
            wrapper.className = "emotion-bar";

            const labelSpan = document.createElement("span");
            labelSpan.className = "label";
            labelSpan.textContent = label;

            const bar = document.createElement("div");
            bar.className = "bar";

            const fill = document.createElement("div");
            fill.className = "fill " + label;
            fill.style.width = (prob * 100).toFixed(2) + "%";

            const percent = document.createElement("span");
            percent.className = "percent";
            percent.textContent = (prob * 100).toFixed(2) + "%";

            bar.appendChild(fill);
            wrapper.appendChild(labelSpan);
            wrapper.appendChild(bar);
            wrapper.appendChild(percent);

            probabilitiesDisplay.appendChild(wrapper);
          }

          // Draw image + bounding box on canvas
          const reader = new FileReader();
          reader.onload = function (event) {
            const img = new Image();
            img.onload = function () {
              canvas.width = img.width;
              canvas.height = img.height;

              ctx.drawImage(img, 0, 0);

              ctx.strokeStyle = "blue";
              ctx.lineWidth = 3;
              ctx.font = "20px Arial";
              ctx.fillStyle = "blue";

              result.bounding_boxes.forEach(box => {
                if (img.width <= 60 || img.height <= 60) {
                  box.x /= 4;
                  box.y /= 4;
                  box.w /= 4;
                  box.h /= 4;
                }
                ctx.strokeRect(box.x, box.y, box.w, box.h);
                ctx.fillText(result.predicted_emotion, box.x, box.y - 10);
              });
            };
            img.src = event.target.result;
          };
          reader.readAsDataURL(file);
        });
      }
    } catch (error) {
      console.error("Error:", error);
      swal.close();
      alert("Something went wrong with prediction.");
    }
  });
});
