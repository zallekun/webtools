document.addEventListener('DOMContentLoaded', () => {
  const dropArea = document.querySelector('.drop-area');
  const input = dropArea.querySelector('input[type="file"]');
  const previewGallery = document.getElementById('preview-gallery');

  dropArea.addEventListener('click', () => input.click());

  dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.classList.add('dragover');
  });

  dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('dragover');
  });

  dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.classList.remove('dragover');
    input.files = e.dataTransfer.files;
    showPreview(input.files);
  });

  input.addEventListener('change', () => showPreview(input.files));

  function showPreview(files) {
    previewGallery.innerHTML = "";
    Array.from(files).forEach(file => {
      if (!file.type.startsWith('image/')) return;

      const reader = new FileReader();
      reader.onload = e => {
        const col = document.createElement('div');
        col.className = "col-6 col-md-3";
        col.innerHTML = `<img src="${e.target.result}" class="img-fluid rounded border" />`;
        previewGallery.appendChild(col);
      };
      reader.readAsDataURL(file);
    });
  }
});
