const sleep = (milliseconds) => {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
};

function triggerEvent(el, type) {
  var e = document.createEvent("HTMLEvents");
  e.initEvent(type, false, true);
  el.dispatchEvent(e);
}

function evalJSFromHtml(html) {
  var newElement = document.createElement("div");
  newElement.innerHTML = html;

  var scripts = newElement.getElementsByTagName("script");
  for (var i = 0; i < scripts.length; ++i) {
    var script = scripts[i];
    eval(script.innerHTML);
  }
}

async function appendToGrid() {
  fetch(loadGridUrl + new URLSearchParams({ dashboard: dashboardName })).then(
    (response) => {
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.indexOf("application/json") !== -1) {
        return response.json().then((data) => {
          document.getElementById("errorMessageTitle").innerText =
            data.data["error_title"];
          document.getElementById("errorMessageBody").innerText =
            data.data["error"];
          errorMessageModal.show();
        });
      } else {
        return response.text().then((text) => {
          let elems = iso.getItemElements();
          iso.remove(elems);
          grid.innerHTML = text;
          evalJSFromHtml(text);
          iso.insert(grid);
          applyDashboardOptions();
          document
            .querySelectorAll(".data-source-container")
            .forEach(function (el) {
              loadDataSource(el.getAttribute("data-source"), el);
            });
        });
      }
    }
  );
  return "done";
}

function loadGrid() {
  appendToGrid().then(() => {
    sleep(100).then(() => {
      iso.layout();
      sleep(300).then(() => {
        iso.layout();
      });
    });
  });
}

function applyDashboardOptions() {
  let commandBarFloat = document.getElementById("commandBarFloat");
  let commandBarRow = document.getElementById("commandBarRow");

  if (commandBarFloat.innerText === "center") {
    commandBarRow.classList.add("justify-content-center");
  } else if (commandBarFloat.innerText === "right") {
    commandBarRow.classList.add("justify-content-end");
  } else {
    commandBarRow.classList.remove("justify-content-center");
    commandBarRow.classList.remove("justify-content-end");
  }
}

function loadDataSource(data_source_name, container) {
  let listGroup = container.closest(".list-group");
  let progress = listGroup.querySelector(".progress");
  let reloadBtnI = listGroup.querySelector(".reload-data-source-i");
  if( progress || reloadBtnI ) {
    progress.classList.remove("d-none");
    reloadBtnI.classList.add("d-none");
  }
  let reloadBtn = listGroup.querySelector(".reload-data-source");
  fetch(loadDataSourceUrl + new URLSearchParams({ ds: data_source_name }))
    .then((r) => r.text())
    .then(function (r) {
      container.innerHTML = r;
      evalJSFromHtml(r);
      container.classList.remove("d-none");
    if( reloadBtn && progress ) {
      reloadBtn.addEventListener("click", function (e) {
        loadDataSource(data_source_name, container);
      });
      progress.classList.add("d-none");
      reloadBtnI.classList.remove("d-none");
    }
    });
}

function changeDashboard(name) {
  clearAppliedTags();
  dashboardName = name;
  loadGrid(iso);
}

function applyTagFilter(tag) {
  if (!appliedTags.includes(tag)) {
    appliedTags.push(tag);
  }
  appliedTags.forEach(function (tagName) {
    iso.arrange({
      filter: function (el) {
        let tags = el.getAttribute("data-tags").split("%,%");
        return tags.includes(tagName);
      },
    });
  });
}

function clearAppliedTags() {
  appliedTags = [];
  iso.arrange({
    filter: "*",
  });
}

function showLogs() {
  fetch(getLogsUrl)
    .then((resp) => resp.text())
    .then(function (data) {
      document.querySelector("#logsContent").innerHTML = data;
      logsModal.show();
    });
}

function setCommandBarDatalist() {
  if (commandBarInput.value.startsWith("?")) {
    commandBarInput.setAttribute("list", "queryProvidersDatalist");
  } else if (commandBarInput.value.startsWith(":d")) {
    commandBarInput.setAttribute("list", "dashboardsDatalist");
  } else if (commandBarInput.value.startsWith(":t")) {
    commandBarInput.setAttribute("list", "tagsDatalist");
  } else {
    commandBarInput.setAttribute("list", "noDatalist");
    commandBarInput.blur();
    commandBarInput.focus();
  }
}

function commandBarSearch() {
  // SEARCHABLE
  if (commandBarInput.value.length === 0) {
    iso.arrange({
      filter: "*",
    });
  } else if (
    !commandBarInput.value.startsWith(":") &&
    !commandBarInput.value.startsWith("?")
  ) {
    iso.arrange({
      filter: function (el) {
        return (
          el
            .getAttribute("data-searchable")
            .trimRight()
            .toLowerCase()
            .indexOf(commandBarInput.value.toLowerCase()) > -1
        );
      },
    });
  }
}

function commandBarSubmit() {
  // SHOW LOGS
  if (commandBarInput.value.startsWith(":l")) {
    showLogs();
  }
  // OPEN EDITOR
  if (commandBarInput.value.startsWith(":e") && editorEnabled) {
    openIframe(editorUrl);
  }
  // CHANGE DASHBOARD
  else if (commandBarInput.value.startsWith(":d ")) {
    changeDashboard(commandBarInput.value.slice(3));
  }
  // CLEAR TAGS
  else if (commandBarInput.value === ":t clear") {
    clearAppliedTags();
  }
  // APPLY TAG
  else if (commandBarInput.value.startsWith(":t ")) {
    applyTagFilter(commandBarInput.value.slice(3));
  }
  // QUERY PROVIDERS
  else if (
    commandBarInput.value.startsWith("?") &&
    commandBarInput.value.length > 3
  ) {
    let prefix = commandBarInput.value.slice(
      1,
      commandBarInput.value.indexOf(" ")
    );
    let query_string = commandBarInput.value
      .slice(commandBarInput.value.indexOf(" ") + 1)
      .replace(" ", "+");
    let url = queryProviderUrls[prefix];
    window.location.href = url + query_string;
  }
  // CHANGE THEME
  else if (commandBarInput.value.startsWith(":x ")) {
    fetch(
      changeThemeUrl +
        new URLSearchParams({
          theme_name: commandBarInput.value.slice(3),
        })
    ).then((r) => {
      location.reload();
    });
  }
  // INSTALLER
  else if (commandBarInput.value.startsWith(":i")) {
    installerModal.show();
  }
  commandBarInput.value = "";
  commandBarInput.setAttribute("list", "noDatalist");
  commandBarInput.focus();
}

function setCommandBarText(v) {
  commandBarInput.value = v;
  triggerEvent(commandBarInput, "keyup");
  commandBarInput.focus();
}

function openIframeInNew() {
  let viewer = document.getElementById("iframe-viewer-iframe");
  window.open(viewer.getAttribute("src"));
  viewer.setAttribute("src", "");
}

function openIframe(url, no_reload = false) {
  iframeModal.show();
  document.querySelectorAll(".iframe-title").forEach(function (e) {
    e.innerHTML = url;
  });
  document.querySelectorAll(".iframe-open-in-new").forEach(function (e) {
    e.removeEventListener("click", openIframeInNew);
    e.addEventListener("click", openIframeInNew);
  });
  document.getElementById("minimizeIframe").addEventListener(
    "click",
    function (e) {
      document.getElementById("iframeMinimized").classList.remove("d-none");
    },
    { once: true }
  );
  document.getElementById("restoreIframe").addEventListener(
    "click",
    function (e) {
      document.getElementById("iframeMinimized").classList.add("d-none");
      openIframe(url, (no_reload = true));
    },
    { once: true }
  );
  document.querySelectorAll(".close-iframe").forEach(function (e) {
    e.addEventListener(
      "click",
      function (evt) {
        document.getElementById("iframeMinimized").classList.add("d-none");
      },
      { once: true }
    );
  });
  if (!no_reload) {
    document.getElementById("iframe-viewer-iframe").setAttribute("src", url);
  }
}

function submitLoadPackageFromZipForm() {
  let loadPackageFromZipForm = document.getElementById(
    "loadPackageFromZipForm"
  );
  let installerError = document.getElementById("installerError");
  let packageDetails = document.getElementById("packageDetails");
  let installSources = document.getElementById("installSources");

  installerError.classList.add("d-none");

  fetch(loadPackageFromZipUrl, {
    method: "post",
    body: new FormData(loadPackageFromZipForm),
  })
    .then((r) => r.json())
    .then(function (r) {
      if (r.data.error) {
        installerError.innerText = r.data.error;
        installerError.classList.remove("d-none");
      } else {
        packageDetails.innerHTML = r.data.html;
        installSources.classList.add("d-none");
        packageDetails.classList.remove("d-none");
        initInstallPackageForm();
      }
    });
}

function initInstallPackageForm() {
  let installPackageForm = document.getElementById("installPackageForm");
  let packageInstalled = document.getElementById("packageInstalled");
  let packageDetails = document.getElementById("packageDetails");
  let installerError2 = document.getElementById("installerError2");

  installPackageForm.addEventListener("submit", function (e) {
    e.preventDefault();

    fetch(installPackageUrl, {
      method: "post",
      body: new FormData(installPackageForm),
    })
      .then((r) => r.json())
      .then(function (r) {
        if (r.data.error) {
          installerError2.innerText = r.data.error;
          installerError2.classList.remove("d-none");
        } else {
          packageDetails.classList.add("d-none");
          packageInstalled.classList.remove("d-none");
        }
      });
  });
}

function resetInstaller() {
  let loadPackageFromZipForm = document.getElementById(
    "loadPackageFromZipForm"
  );
  let packageInstalled = document.getElementById("packageInstalled");
  let packageDetails = document.getElementById("packageDetails");
  let installSources = document.getElementById("installSources");
  let installerError = document.getElementById("installerError");
  let installerError2 = document.getElementById("installerError2");

  loadPackageFromZipForm.reset();
  packageDetails.innerHTML = "";
  packageDetails.classList.add("d-none");
  packageInstalled.classList.add("d-none");
  installSources.classList.remove("d-none");
  installerError.classList.add("d-none");
  installerError2.classList.add("d-none");
}
