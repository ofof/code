// Meeting reminder hook for the Todo API website.
//
// main.py serves this file at /hooks/meeting-reminder.js and injects it into
// the Swagger UI page at /docs. Once a visitor has stayed on the page for
// DELAY_MS, a modal dialog pops up reminding them about the IT project
// management meeting.
(function () {
  "use strict";

  var DELAY_MS = 10 * 1000;
  var TITLE = "Meeting reminder";
  var MESSAGE =
    "IT Project Management meeting: next Wednesday at 10:00 AM in Room 888.";

  function showReminder() {
    if (document.getElementById("meeting-reminder")) {
      return; // already showing
    }

    var dialog = document.createElement("dialog");
    dialog.id = "meeting-reminder";
    dialog.setAttribute("aria-labelledby", "meeting-reminder-title");
    dialog.style.cssText =
      "border:0;border-radius:8px;padding:24px 28px;max-width:420px;" +
      "font-family:sans-serif;box-shadow:0 8px 32px rgba(0,0,0,.3);";

    var heading = document.createElement("h2");
    heading.id = "meeting-reminder-title";
    heading.textContent = TITLE;
    heading.style.cssText = "margin:0 0 12px;font-size:20px;";

    var body = document.createElement("p");
    body.textContent = MESSAGE;
    body.style.cssText = "margin:0 0 20px;font-size:16px;line-height:1.5;";

    var button = document.createElement("button");
    button.type = "button";
    button.textContent = "OK";
    button.style.cssText =
      "padding:8px 20px;font-size:15px;border:0;border-radius:4px;" +
      "background:#1a73e8;color:#fff;cursor:pointer;";
    button.addEventListener("click", function () {
      dialog.close();
    });

    dialog.appendChild(heading);
    dialog.appendChild(body);
    dialog.appendChild(button);
    dialog.addEventListener("close", function () {
      dialog.remove();
    });
    document.body.appendChild(dialog);

    if (typeof dialog.showModal === "function") {
      dialog.showModal();
      button.focus();
    } else {
      // Very old browsers without <dialog> support.
      window.alert(TITLE + "\n\n" + MESSAGE);
    }
  }

  window.setTimeout(showReminder, DELAY_MS);
})();
