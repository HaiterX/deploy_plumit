(function () {
  function ensurePreviewImg(coverInput) {
    var existing = document.getElementById('cover-preview-img');
    if (existing) return existing;

    var img = document.createElement('img');
    img.id = 'cover-preview-img';
    img.style.maxWidth = '100%';
    img.style.height = 'auto';
    img.style.borderRadius = '12px';
    img.style.display = 'block';
    img.style.marginTop = '10px';

    coverInput.insertAdjacentElement('afterend', img);
    return img;
  }

  function applyScale(img, scaleSelect) {
    if (!img || !scaleSelect) return;
    var v = parseInt(scaleSelect.value, 10);
    if (!v || isNaN(v)) v = 100;
    img.style.width = v + '%';
  }

  document.addEventListener('DOMContentLoaded', function () {
    var scaleSelect = document.getElementById('id_cover_scale');
    var coverInput = document.getElementById('id_cover_image');
    var img = document.getElementById('cover-preview-img');

    if (scaleSelect && img) {
      applyScale(img, scaleSelect);
      scaleSelect.addEventListener('change', function () {
        applyScale(img, scaleSelect);
      });
    }

    if (coverInput) {
      coverInput.addEventListener('change', function () {
        if (!coverInput.files || !coverInput.files.length) return;

        var file = coverInput.files[0];
        if (!file) return;

        var preview = ensurePreviewImg(coverInput);
        preview.src = URL.createObjectURL(file);
        applyScale(preview, scaleSelect);
      });
    }
  });
})();