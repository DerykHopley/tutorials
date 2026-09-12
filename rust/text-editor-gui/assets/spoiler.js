/* A link into a folded answer has to unfold it, or it silently does nothing.
   Newer browsers auto-expand <details> for a fragment target; older ones do
   not, and this document is meant to work from a file:// URL on any of them.
   Also: printing, where a closed fold would just vanish from the page. */
(function () {
  function reveal(hash) {
    if (!hash || hash.length < 2) return;
    var target = document.getElementById(hash.slice(1));
    if (!target) return;
    for (var node = target; node; node = node.parentElement) {
      if (node.tagName === "DETAILS") node.open = true;
    }
    target.scrollIntoView();
  }

  window.addEventListener("hashchange", function () { reveal(location.hash); });
  document.addEventListener("DOMContentLoaded", function () { reveal(location.hash); });
  window.addEventListener("beforeprint", function () {
    var all = document.querySelectorAll("details");
    for (var i = 0; i < all.length; i++) all[i].open = true;
  });
})();
