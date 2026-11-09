/* ghonchu.js: Ghonchu, a round tutor who bounces, hops, blinks and watches your finger.
   An original drawing. © 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.  SPDX-License-Identifier: GPL-3.0-or-later */
(function () {
  "use strict";
  var stage = document.getElementById("stage"), g = document.getElementById("ghonchu"), shadow = document.getElementById("shadow"),
      bubble = document.getElementById("bubble"), mouth = document.getElementById("mouth"), el = document.getElementById("el"), er = document.getElementById("er"),
      pupils = [[document.getElementById("pl"), 51, 71], [document.getElementById("pr"), 89, 71]];
  if (!stage || !g) return;
  var reduce = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  var SIZE = 130, GROUND = 34, W = 0, H = 0, x = 0, y = 0, vx = 140, vy = 0, squash = 0, last = 0, nextHop = 1.2, bubbleUntil = 0;
  var look = null, lines = ["Hi! I am Ghonchu.", "Show me your chassis!", "Ten minutes to build.", "Thirty to connect.", "Fifteen to tune.",
    "Check the ground wire first!", "Upar! Neeche! Bayein! Dayein!", "Is the battery charged?", "Tap me again!", "Let's build a robot!"], li = 0;
  for (var i = 0; i < 26; i++) { var s = document.createElement("span"); s.className = "spark"; s.style.left = (Math.random() * 100) + "%";
    s.style.top = (Math.random() * 62) + "%"; s.style.animationDelay = (Math.random() * 2.8) + "s"; stage.appendChild(s); }
  function size() { var r = stage.getBoundingClientRect(); W = r.width; H = r.height; }
  function floorY() { return H - GROUND + 6; }
  function say(t, sec) { bubble.textContent = t; bubble.className = "on"; bubbleUntil = performance.now() / 1000 + (sec || 2.4); }
  function hop(power, dir) { vy = -power; vx += dir; squash = -0.12; mouth.setAttribute("d", "M60 92 Q70 108 80 92 Q70 98 60 92"); }
  function blink() { [el, er].forEach(function (e) { e.setAttribute("ry", "2"); }); setTimeout(function () { [el, er].forEach(function (e) { e.setAttribute("ry", "14"); }); }, 130);
    setTimeout(blink, 2200 + Math.random() * 3200); }
  function eyes(cx, cy) {
    var r = g.getBoundingClientRect(), k = r.width / 140;
    pupils.forEach(function (p) {
      var ex = r.left + p[1] * k, ey = r.top + p[2] * k, dx = 0, dy = 0;
      if (cx !== null) { dx = cx - ex; dy = cy - ey; } else { dx = vx; dy = vy * 0.3; }
      var d = Math.sqrt(dx * dx + dy * dy) || 1, m = Math.min(5.5, d / 12);
      p[0].setAttribute("transform", "translate(" + (dx / d * m).toFixed(2) + " " + (dy / d * m).toFixed(2) + ")");
    });
  }
  function place() {
    var fy = floorY(), air = Math.max(0, fy - y), sy = 1 - squash, sx = 1 + squash * 0.6;
    g.style.transform = "translate(" + (x - SIZE / 2).toFixed(1) + "px," + (y - SIZE).toFixed(1) + "px) scale(" + sx.toFixed(3) + "," + sy.toFixed(3) + ")";
    var sh = Math.max(0.35, 1 - air / 260); shadow.style.transform = "translateX(" + x.toFixed(1) + "px) scale(" + sh.toFixed(2) + ")"; shadow.style.opacity = (0.2 + 0.6 * sh).toFixed(2);
    var bw = bubble.offsetWidth || 120; bubble.style.transform = "translate(" + Math.min(Math.max(8, x - bw / 2), W - bw - 8).toFixed(1) + "px," + Math.max(6, y - SIZE - 46).toFixed(1) + "px)";
  }
  function step(now) {
    var t = now / 1000, dt = Math.min(0.033, last ? t - last : 0.016); last = t;
    if (!reduce) {
      vy += 1500 * dt; x += vx * dt; y += vy * dt;
      var fy = floorY();
      if (y > fy) { y = fy; if (vy > 160) { squash = Math.min(0.32, vy / 2600); vy = -vy * 0.62; mouth.setAttribute("d", "M60 93 Q70 103 80 93"); } else { vy = 0; } }
      if (x < SIZE / 2) { x = SIZE / 2; vx = Math.abs(vx) * 0.9; } if (x > W - SIZE / 2) { x = W - SIZE / 2; vx = -Math.abs(vx) * 0.9; }
      if (y >= fy && vy === 0) { vx *= 0.985; nextHop -= dt; if (nextHop <= 0) { hop(420 + Math.random() * 260, (Math.random() - 0.5) * 380); nextHop = 1.4 + Math.random() * 2.4; } }
      squash *= 0.86; if (Math.abs(squash) < 0.004) squash = 0;
      if (vy < -60) squash = Math.max(squash, -Math.min(0.1, -vy / 7000));
    }
    if (bubbleUntil && t > bubbleUntil) { bubble.className = ""; bubbleUntil = 0; }
    place(); eyes(look ? look[0] : null, look ? look[1] : null); requestAnimationFrame(step);
  }
  function tap(cx) { var r = stage.getBoundingClientRect(), dir = cx === null ? 0 : (x - (cx - r.left)) > 0 ? 220 : -220;
    if (!reduce) hop(760, dir); say(lines[li++ % lines.length]); }
  stage.addEventListener("pointerdown", function (e) { if (e.target.id !== "jump") tap(e.clientX); });
  document.getElementById("jump").addEventListener("click", function (e) { e.stopPropagation(); tap(null); });
  window.addEventListener("pointermove", function (e) { look = [e.clientX, e.clientY]; });
  window.addEventListener("resize", function () { size(); x = Math.min(Math.max(SIZE / 2, x), W - SIZE / 2); });
  size(); x = W / 2; y = reduce ? floorY() : floorY() - 120; blink(); setTimeout(function () { say("Hi! I am Ghonchu.", 2.6); }, 700); requestAnimationFrame(step);
})();
