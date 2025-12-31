document.addEventListener("DOMContentLoaded", () => {
  const video = document.getElementById("video");
  const overlay = document.getElementById("overlay");
  const overlayCtx = overlay.getContext("2d");
  const snapshotCanvas = document.getElementById("snapshot");
  const snapshotCtx = snapshotCanvas.getContext("2d");

  const startBtn = document.getElementById("startBtn");
  const captureBtn = document.getElementById("captureBtn");
  const cameraSelect = document.getElementById("cameraSelect");

  const emotionDisplay = document.getElementById("cameraEmotion");
  const probabilitiesDisplay = document.getElementById("cameraProbabilities");

  let currentStream = null;

  async function listCameras() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      alert("WebRTC not supported or blocked.");
      throw new Error("WebRTC not supported or blocked.");
    }
    await navigator.mediaDevices.getUserMedia({ video: true });
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = devices.filter(d => d.kind === "videoinput");
    cameraSelect.innerHTML = "";

    let integratedId = null;

    videoDevices.forEach((device, i) => {
      const option = document.createElement("option");
      option.value = device.deviceId;
      option.text = device.label || `Camera ${i + 1}`;
      cameraSelect.appendChild(option);

      // Look for "Integrated Camera" in the label
      if (device.label && device.label.toLowerCase().includes("integrated")) {
        integratedId = device.deviceId;
      }
    });

    // If we found an integrated camera, select it by default
    if (integratedId) {
      cameraSelect.value = integratedId;
    } else if (videoDevices.length > 0) {
      // fallback: first camera
      cameraSelect.value = videoDevices[0].deviceId;
    }
  }

  // Start camera
  async function startCamera(deviceId) {
    if (currentStream) {
      currentStream.getTracks().forEach(track => track.stop());
    }
    const constraints = {
      video: deviceId ? { deviceId: { exact: deviceId } } : true
    };
    currentStream = await navigator.mediaDevices.getUserMedia(constraints);
    video.srcObject = currentStream;

    video.onloadedmetadata = () => {
      video.play();
      overlay.width = video.videoWidth;
      overlay.height = video.videoHeight;
    };
    captureBtn.disabled = false;
    startBtn.textContent = "Stop Camera";
  }

  // Stop camera
  function stopCamera() {
    if (currentStream) {
      currentStream.getTracks().forEach(track => track.stop());
      currentStream = null;
    }
    overlayCtx.clearRect(0, 0, overlay.width, overlay.height);
    snapshotCtx.clearRect(0, 0, snapshotCanvas.width, snapshotCanvas.height);
    emotionDisplay.textContent = "";
    probabilitiesDisplay.innerHTML = "";
    startBtn.textContent = "Start Camera";
  }

  // Capture frame and send to backend
  async function captureFrame() {
    snapshotCtx.clearRect(0, 0, snapshotCanvas.width, snapshotCanvas.height);
    emotionDisplay.textContent = "";
    probabilitiesDisplay.innerHTML = "";
    
    snapshotCanvas.width = video.videoWidth;
    snapshotCanvas.height = video.videoHeight;
    snapshotCtx.drawImage(video, 0, 0);

    snapshotCanvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append("file", blob, "capture.png");

      try {
        const response = await fetch("/api/predict", {
          method: "POST",
          body: formData
        });
        if (!response.ok) throw new Error("Prediction failed");

        let result = await response.json();
        result = result.data;

        emotionDisplay.textContent = `Predicted Emotion: ${result.predicted_emotion}`;
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

        snapshotCtx.strokeStyle = "blue";
        snapshotCtx.lineWidth = 3;
        snapshotCtx.font = "20px Arial";
        snapshotCtx.fillStyle = "blue";

        result.bounding_boxes.forEach(box => {
          snapshotCtx.strokeRect(box.x, box.y, box.w, box.h);
          snapshotCtx.fillText(result.predicted_emotion, box.x, box.y - 10);
        });

      } catch (err) {
        console.error(err);
        alert("Error during prediction.");
      }
    }, "image/png");
  }

  // Toggle start/stop camera
  startBtn.addEventListener("click", async () => {
    if (!currentStream) {
      await listCameras();
      await startCamera(cameraSelect.value);
    } else {
      stopCamera();
    }
  });

  cameraSelect.addEventListener("change", async () => {
    if (currentStream) {
      await startCamera(cameraSelect.value);
    }
  });

  captureBtn.addEventListener("click", captureFrame);

  // Expose controls for the mode switch button
  window.CameraController = {
    start: async () => {
      await listCameras();
      await startCamera(cameraSelect.value);
    },
    stop: stopCamera
  };
});
