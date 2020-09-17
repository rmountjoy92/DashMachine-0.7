let errorMessageModal = new bootstrap.Modal(
  document.getElementById("errorMessageModal"),
  { backdrop: "static" }
);

let logsModal = new bootstrap.Modal(document.getElementById("logsModal"));
let iframeModal = new bootstrap.Modal(document.getElementById("iframeModal"));

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

let iso = new Isotope(grid, {
  itemSelector: ".grid-item",
  layoutMode: "packery",
  packery: {
    gutter: 10,
  },
});

loadGrid(iso);

appliedTags.forEach(function (tag) {
  applyTagFilter(tag);
});
