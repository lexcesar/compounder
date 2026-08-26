(function () {
	"use strict";

	/* ---- transcript reveal (the signature) ---- */
	var tx = document.getElementById("transcript");
	var replay = document.getElementById("replay");
	var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

	if (tx && !reduced && "IntersectionObserver" in window) {
		var lines = Array.prototype.slice.call(tx.querySelectorAll(".tx__line"));
		var timers = [];

		function clear() {
			timers.forEach(clearTimeout);
			timers = [];
			lines.forEach(function (l) { l.classList.remove("is-shown"); });
		}

		function play() {
			clear();
			tx.classList.add("tx--armed");
			var t = 200;
			lines.forEach(function (line) {
				var isClaim = line.classList.contains("tx__claim");
				var isSummary = line.classList.contains("tx__summary");
				timers.push(setTimeout(function () { line.classList.add("is-shown"); }, t));
				t += isClaim ? 520 : isSummary ? 420 : 260;
			});
			timers.push(setTimeout(function () { replay.hidden = false; }, t + 200));
		}

		tx.classList.add("tx--armed");
		var once = new IntersectionObserver(function (entries) {
			if (entries.some(function (e) { return e.isIntersecting; })) {
				once.disconnect();
				play();
			}
		}, { threshold: 0.2 });
		once.observe(tx);

		replay.addEventListener("click", function () {
			replay.hidden = true;
			play();
		});
	}

	/* ---- copy buttons ---- */
	Array.prototype.forEach.call(document.querySelectorAll("[data-copy]"), function (btn) {
		btn.addEventListener("click", function () {
			var node = document.getElementById(btn.getAttribute("data-copy"));
			if (!node) return;
			var text = node.textContent.trim();
			var done = function () {
				var label = btn.textContent;
				btn.textContent = "Copied";
				btn.classList.add("is-done");
				setTimeout(function () {
					btn.textContent = label;
					btn.classList.remove("is-done");
				}, 1600);
			};
			if (navigator.clipboard && navigator.clipboard.writeText) {
				navigator.clipboard.writeText(text).then(done, function () { fallback(node); done(); });
			} else {
				fallback(node);
				done();
			}
		});
	});

	function fallback(node) {
		var range = document.createRange();
		range.selectNodeContents(node);
		var sel = window.getSelection();
		sel.removeAllRanges();
		sel.addRange(range);
		try { document.execCommand("copy"); } catch (e) { /* selection stays for manual copy */ }
	}
})();
