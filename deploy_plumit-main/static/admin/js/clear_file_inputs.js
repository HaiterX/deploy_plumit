(function () {
  function findClearCheckbox(fileInput) {
    // Django admin: чекбокс очистки обычно имеет id вида id_<field>-clear
    var id = fileInput.id;
    if (!id) return null;

    var clear = document.getElementById(id + "-clear");
    if (clear) return clear;

    // fallback: поиск рядом (на всякий случай)
    var wrapper = fileInput.closest(".file-upload") || fileInput.parentElement;
    if (!wrapper) return null;

    var candidates = wrapper.querySelectorAll('input[type="checkbox"]');
    for (var i = 0; i < candidates.length; i++) {
      var cb = candidates[i];
      if ((cb.id || "").indexOf(id + "-clear") !== -1) return cb;
    }
    return null;
  }

  function ensureDeleteButton(fileInput) {
    // не добавлять повторно (особенно в inline formset)
    if (fileInput.dataset.hasDeleteBtn === "1") return;
    fileInput.dataset.hasDeleteBtn = "1";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "Удалить";
    btn.style.marginLeft = "10px";

    btn.addEventListener("click", function () {
      // убрать выбранный файл до сохранения
      fileInput.value = "";

      // если файл уже был сохранён ранее — отметить стандартный clear-чекбокс
      var clearCb = findClearCheckbox(fileInput);
      if (clearCb) clearCb.checked = true;

      // если рядом есть ссылка/текст "Currently:" — скрыть визуально (не обязательно, но помогает)
      var fileUpload = fileInput.closest(".file-upload");
      if (fileUpload) {
        // не ломаем верстку, просто прячем "Currently:" блок, если он есть
        var links = fileUpload.querySelectorAll("a");
        for (var i = 0; i < links.length; i++) links[i].style.display = "none";
      }
    });

    // если пользователь выбрал файл заново — снять clear
    fileInput.addEventListener("change", function () {
      var clearCb = findClearCheckbox(fileInput);
      if (clearCb && fileInput.value) clearCb.checked = false;
    });

    fileInput.insertAdjacentElement("afterend", btn);
  }

  function init(root) {
    var scope = root || document;
    var inputs = scope.querySelectorAll('input[type="file"]');
    for (var i = 0; i < inputs.length; i++) ensureDeleteButton(inputs[i]);
  }

  document.addEventListener("DOMContentLoaded", function () {
    init(document);

    // поддержка инлайнов: Django добавляет формы динамически
    document.body.addEventListener("click", function (e) {
      var t = e.target;
      if (!t) return;
      if (t.classList && (t.classList.contains("add-row") || t.classList.contains("add-another"))) {
        // дать DOM обновиться
        setTimeout(function () { init(document); }, 50);
      }
    });
  });
})();