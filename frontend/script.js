const fileInput = document.getElementById('fileInput');
const previewImage = document.getElementById('previewImage');
const message = document.getElementById('message');

const fileNameLabel = document.getElementById('fileName');

fileInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  if (!file) {
    previewImage.classList.add("hidden");
    fileNameLabel.innerText = "Nie wybrano pliku";
    return;
  }

  fileNameLabel.innerText = file.name;

  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.src = e.target.result;
    previewImage.classList.remove("hidden");
    message.innerText = "";
  };
  reader.readAsDataURL(file);
});

async function uploadImage() {
  const file = fileInput.files[0];
  if (!file) {
    alert("Please select an image.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  message.innerText = "Uploading and processing...";

  try {
    const response = await fetch("/upload", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (response.ok) {
      message.innerText = data.message;
      previewImage.src = data.detected_image_url + `?t=${Date.now()}`;
      previewImage.classList.remove("hidden");
    } else {
      message.innerText = "Error: " + data.detail;
    }

  } catch (err) {
    message.innerText = "Request failed.";
    console.error(err);
  }
}
