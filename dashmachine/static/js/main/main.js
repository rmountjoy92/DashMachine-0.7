let errorMessageModal = new bootstrap.Modal(
  document.getElementById("errorMessageModal")
);

let logsModal = new bootstrap.Modal(document.getElementById("logsModal"));
let iframeModal = new bootstrap.Modal(document.getElementById("iframeModal"));
let installerModal = new bootstrap.Modal(
  document.getElementById("installerModal")
);

let packageFileField = document.getElementById("packageFileField");
packageFileField.addEventListener("change", function (e) {
  submitLoadPackageFromZipForm();
});

let commandBarInput = document.querySelector("#commandBarInput");
commandBarInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    commandBarSubmit();
  }
});
commandBarInput.addEventListener("keyup", (e) => {
  commandBarSearch();
  setCommandBarDatalist();
});

let grid = document.querySelector("#grid");

let iso = new Isotope(grid, isotopeOptions);

loadGrid(iso);

appliedTags.forEach(function (tag) {
  applyTagFilter(tag);
});
