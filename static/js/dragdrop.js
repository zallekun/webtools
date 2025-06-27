document.addEventListener('DOMContentLoaded', () => {
  const dropArea = document.querySelector('.drop-area');
  const input = document.querySelector('input[type="file"]');

  // Pastikan ada elemen yang ditarget
  if (!dropArea || !input) return;

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
    const file = e.dataTransfer.files[0];
    input.files = e.dataTransfer.files;
    showFilename(file);
  });

  input.addEventListener('change', () => {
    const file = input.files[0];
    showFilename(file);
  });

  // Fungsi khusus untuk PDF
  function showFilename(file) {
    if (!file || !file.type.startsWith('image/')) return;
    const preview = document.querySelector('.preview-img');
    if (preview) {
      const reader = new FileReader();
      reader.onload = e => {
        preview.src = e.target.result;
        preview.classList.remove('d-none');
      };
      reader.readAsDataURL(file);
    }
    // Optional: tampilkan nama file di label jika ingin
    const label = dropArea.querySelector('p');
    if (label) label.textContent = `🖼️ ${file.name}`;
  }
});
