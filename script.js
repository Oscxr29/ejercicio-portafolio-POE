// Marca en la barra superior la sección que se está viendo.
(function () {
  "use strict";

  var links = document.querySelectorAll(".nav a");
  if (!links.length || !("IntersectionObserver" in window)) return;

  var byId = {};
  links.forEach(function (a) {
    byId[a.getAttribute("href").slice(1)] = a;
  });

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (a) { a.removeAttribute("aria-current"); });
        var active = byId[entry.target.id];
        if (active) active.setAttribute("aria-current", "true");
      });
    },
    { rootMargin: "-40% 0px -55% 0px" }
  );

  Object.keys(byId).forEach(function (id) {
    var section = document.getElementById(id);
    if (section) observer.observe(section);
  });
})();
