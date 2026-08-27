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

	/* ---- cursor + magnetic buttons (fine pointer, motion allowed) ---- */
	var fine = window.matchMedia("(pointer: fine)").matches;
	if (fine && !reduced) initCursor();

	function initCursor() {
		var dot = document.querySelector(".cur-dot");
		var ring = document.querySelector(".cur-ring");
		if (!dot || !ring) return;
		document.documentElement.classList.add("has-cursor");
		var mx = -200, my = -200, rx = -200, ry = -200, seen = false;
		var mags = Array.prototype.slice.call(document.querySelectorAll("[data-mag]"));
		var magState = mags.map(function () { return { x: 0, y: 0 }; });
		var HOVER = "a, button, [data-mag], .rail__phase, .roster__agent, .loop__station, .grid__cell";
		var GOLD = ".rail__phase, .roster__agent, .loop__station, .grid__cell";

		document.addEventListener("mousemove", function (e) {
			mx = e.clientX; my = e.clientY;
			if (!seen) { seen = true; rx = mx; ry = my; }
			dot.classList.remove("is-out"); ring.classList.remove("is-out");
			var t = e.target.closest ? e.target.closest(HOVER) : null;
			dot.classList.toggle("is-hov", !!t);
			ring.classList.toggle("is-hov", !!t);
			ring.classList.toggle("is-gold", !!(t && t.matches(GOLD)));
		}, { passive: true });
		document.addEventListener("mouseleave", function () { dot.classList.add("is-out"); ring.classList.add("is-out"); });
		document.addEventListener("mousedown", function () { ring.classList.add("is-hov"); });
		document.addEventListener("mouseup", function () { if (!ring.classList.contains("is-gold")) ring.classList.remove("is-hov"); });

		function tick() {
			rx += (mx - rx) * 0.18; ry += (my - ry) * 0.18;
			dot.style.transform = "translate3d(" + mx + "px," + my + "px,0)";
			ring.style.transform = "translate3d(" + rx.toFixed(2) + "px," + ry.toFixed(2) + "px,0)";
			mags.forEach(function (el, i) {
				var r = el.getBoundingClientRect();
				var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
				var dx = mx - cx, dy = my - cy;
				var reach = Math.max(r.width, r.height) / 2 + 28;
				var s = magState[i];
				var tx = 0, ty = 0;
				if (Math.abs(dx) < reach && Math.abs(dy) < reach) { tx = dx * 0.28; ty = dy * 0.28; }
				s.x += (tx - s.x) * 0.2; s.y += (ty - s.y) * 0.2;
				if (Math.abs(s.x) > 0.05 || Math.abs(s.y) > 0.05) el.style.transform = "translate3d(" + s.x.toFixed(2) + "px," + s.y.toFixed(2) + "px,0)";
				else if (el.style.transform) el.style.transform = "";
			});
			requestAnimationFrame(tick);
		}
		requestAnimationFrame(tick);
	}

	/* ---- smooth scrolling (wheel lerp + animated anchors; native on touch/keyboard) ---- */
	if (fine && !reduced) initSmoothScroll();

	function initSmoothScroll() {
		var doc = document.documentElement;
		doc.style.scrollBehavior = "auto";
		var target = window.scrollY, current = target, raf = 0;
		var nav = document.querySelector(".nav");
		function maxY() { return doc.scrollHeight - window.innerHeight; }
		function go() { if (!raf) raf = requestAnimationFrame(step); }
		function step() {
			current += (target - current) * 0.11;
			if (Math.abs(target - current) < 0.4) current = target;
			window.scrollTo(0, current);
			raf = current === target ? 0 : requestAnimationFrame(step);
		}
		window.addEventListener("wheel", function (e) {
			if (e.ctrlKey || Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
			var d = e.deltaY;
			if (e.deltaMode === 1) d *= 16; else if (e.deltaMode === 2) d *= window.innerHeight;
			e.preventDefault();
			target = Math.max(0, Math.min(maxY(), target + d));
			go();
		}, { passive: false });
		window.addEventListener("scroll", function () {
			if (Math.abs(window.scrollY - current) > 1.5) { current = target = window.scrollY; }
		}, { passive: true });
		document.addEventListener("click", function (e) {
			var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
			if (!a) return;
			var id = a.getAttribute("href").slice(1);
			var el = id ? document.getElementById(id) : null;
			if (!el) return;
			e.preventDefault();
			var top = el.getBoundingClientRect().top + window.scrollY - (nav ? nav.offsetHeight : 0);
			target = Math.max(0, Math.min(maxY(), top));
			go();
			if (history.pushState) history.pushState(null, "", "#" + id);
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
