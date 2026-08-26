(function () {
	"use strict";

	var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
	var hasIO = "IntersectionObserver" in window;

	/* ---- scroll reveals + diagram triggers ---- */
	var targets = document.querySelectorAll("[data-reveal], [data-anim]");
	if (reduced || !hasIO) {
		Array.prototype.forEach.call(targets, function (el) { el.classList.add("is-in"); });
	} else {
		var io = new IntersectionObserver(function (entries) {
			entries.forEach(function (e) {
				if (e.isIntersecting) {
					e.target.classList.add("is-in");
					io.unobserve(e.target);
				}
			});
		}, { threshold: 0.18, rootMargin: "0px 0px -6% 0px" });
		Array.prototype.forEach.call(targets, function (el) { io.observe(el); });
	}

	/* ---- the rail: one feature through /lfg (signature) ---- */
	var rail = document.getElementById("rail");
	if (rail) {
		if (reduced || !rail.querySelector("#rail-track").getTotalLength) {
			rail.classList.add("is-static");
		} else {
			runRail(rail);
		}
	}

	function runRail(svg) {
		var track = svg.querySelector("#rail-track");
		var loop = svg.querySelector(".rail__loop");
		var dot = svg.querySelector(".rail__dot");
		var phases = Array.prototype.slice.call(svg.querySelectorAll(".rail__phase"));
		var gates = {};
		Array.prototype.forEach.call(svg.querySelectorAll(".rail__gate"), function (g) { gates[g.getAttribute("data-gate")] = g; });

		var Lc = loop.getTotalLength();
		var firstPass = 538;               /* x 578 − 40 */
		var afterLoop = firstPass + Lc;    /* back at x 412 */
		var pos = {
			g1: 386 - 40,
			g2: firstPass,
			work: afterLoop,
			g2b: afterLoop + (578 - 412),
			g3: afterLoop + (930 - 412),
			end: afterLoop + (1140 - 412)
		};

		function stamp(gate, kind) {
			var g = gates[gate];
			Array.prototype.forEach.call(g.querySelectorAll(".rail__stamp"), function (s) { s.classList.remove("is-on"); });
			if (kind) g.querySelector(".rail__stamp--" + kind).classList.add("is-on");
			g.classList.toggle("is-hit", !!kind);
		}

		function reset() {
			phases.forEach(function (p) { p.classList.remove("is-lit"); });
			Object.keys(gates).forEach(function (k) { stamp(k, null); });
			svg.classList.remove("is-looping", "is-delivered");
		}

		var steps = [
			{ move: pos.g1, dur: 2100 },
			{ hold: 650, at: function () { stamp("g1", "ok"); } },
			{ move: pos.g2, dur: 1300 },
			{ hold: 900, at: function () { stamp("g2", "refuted"); } },
			{ move: pos.work, dur: 1500, at: function () { svg.classList.add("is-looping"); } },
			{ hold: 450 },
			{ move: pos.g2b, dur: 1300, at: function () { stamp("g2", null); } },
			{ hold: 800, at: function () { stamp("g2", "ok"); } },
			{ move: pos.g3, dur: 2100 },
			{ hold: 650, at: function () { stamp("g3", "ok"); } },
			{ move: pos.end, dur: 1100, at: function () { svg.classList.add("is-delivered"); } },
			{ hold: 2600 },
			{ hold: 500, at: function () { svg.classList.remove("is-live"); reset(); } },
			{ jump: 0, at: function () { svg.classList.add("is-live"); } }
		];

		var i = 0, t0 = null, from = 0, cur = 0;
		function ease(x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }

		function place(d) {
			var p = track.getPointAtLength(d);
			dot.setAttribute("transform", "translate(" + p.x.toFixed(1) + "," + p.y.toFixed(1) + ")");
			if (p.y < 226) {
				phases.forEach(function (ph) {
					if (p.x >= +ph.getAttribute("data-x") - 8) ph.classList.add("is-lit");
				});
			}
		}

		function frame(now) {
			var s = steps[i];
			if (t0 === null) {
				t0 = now; from = cur;
				if (s.at) s.at();
				if (s.jump !== undefined) { cur = s.jump; place(cur); t0 = null; i = (i + 1) % steps.length; return requestAnimationFrame(frame); }
			}
			var el = now - t0;
			if (s.move !== undefined) {
				var k = Math.min(1, el / s.dur);
				cur = from + (s.move - from) * ease(k);
				place(cur);
				if (k >= 1) { t0 = null; i = (i + 1) % steps.length; }
			} else if (el >= s.hold) {
				t0 = null; i = (i + 1) % steps.length;
			}
			requestAnimationFrame(frame);
		}

		var started = false;
		function start() {
			if (started) return;
			started = true;
			svg.classList.add("is-live");
			place(0);
			requestAnimationFrame(frame);
		}
		if (hasIO) {
			var once = new IntersectionObserver(function (entries) {
				if (entries.some(function (e) { return e.isIntersecting; })) { once.disconnect(); start(); }
			}, { threshold: 0.25 });
			once.observe(svg);
		} else {
			start();
		}
	}

	/* ---- transcript reveal ---- */
	var tx = document.getElementById("transcript");
	var replay = document.getElementById("replay");
	if (tx && !reduced && hasIO) {
		var lines = Array.prototype.slice.call(tx.querySelectorAll(".tx__line"));
		var timers = [];
		function clearTx() {
			timers.forEach(clearTimeout); timers = [];
			lines.forEach(function (l) { l.classList.remove("is-shown"); });
		}
		function playTx() {
			clearTx();
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
		var txOnce = new IntersectionObserver(function (entries) {
			if (entries.some(function (e) { return e.isIntersecting; })) { txOnce.disconnect(); playTx(); }
		}, { threshold: 0.2 });
		txOnce.observe(tx);
		replay.addEventListener("click", function () { replay.hidden = true; playTx(); });
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
				setTimeout(function () { btn.textContent = label; btn.classList.remove("is-done"); }, 1600);
			};
			if (navigator.clipboard && navigator.clipboard.writeText) {
				navigator.clipboard.writeText(text).then(done, function () { fallback(node); done(); });
			} else {
				fallback(node); done();
			}
		});
	});

	function fallback(node) {
		var range = document.createRange();
		range.selectNodeContents(node);
		var sel = window.getSelection();
		sel.removeAllRanges(); sel.addRange(range);
		try { document.execCommand("copy"); } catch (e) { /* selection stays for manual copy */ }
	}
})();
