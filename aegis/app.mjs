import { loadDetectors } from "./detectors.mjs";
import {
  countFingers,
  StableCount,
  HAND_LINES,
  POSE_LINES,
} from "./tracking.mjs";
import { skeleton } from "./render.mjs";
import { AirDraw } from "./modes/air-draw.mjs";
import { drawGestureEffect } from "./modes/gesture-effects.mjs";
const drawing = new AirDraw();
let mode = "hands";
const $ = (id) => document.getElementById(id);
const video = $("video"),
  canvas = $("overlay"),
  ctx = canvas.getContext("2d");
let session = null;
function timeout(promise, ms, message) {
  let timer;
  return Promise.race([
    promise,
    new Promise((_, reject) => {
      timer = setTimeout(() => reject(new Error(message)), ms);
    }),
  ]).finally(() => clearTimeout(timer));
}
function clearMetrics() {
  $("fingers").textContent = "0";
  $("hands").textContent = "0";
  $("fps").textContent = "—";
  $("hand-detail").textContent = "No hands detected.";
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}
function dispose(s) {
  if (!s || s.disposed) return;
  s.disposed = true;
  cancelAnimationFrame(s.frame);
  clearTimeout(s.watchdog);
  s.stream?.getTracks().forEach((t) => t.stop());
  try {
    s.detectors?.close();
  } catch {
    /* release remaining session even if a library close fails */
  }
}
function stop(message = "Camera is off.") {
  drawing.lift();
  const old = session;
  session = null;
  dispose(old);
  video.pause();
  video.srcObject = null;
  $("start").disabled = false;
  $("stop").disabled = true;
  $("settings").disabled = false;
  $("start").innerHTML = "Start Camera <span>↗</span>";
  $("status").textContent = message;
  $("mode-label").textContent = "CAMERA OFF";
  $("indicator").classList.remove("active");
  $("empty").hidden = false;
  clearMetrics();
}
function errorMessage(error) {
  const messages = {
    NotAllowedError:
      "Camera permission was denied. Allow camera access in your browser settings, then try again.",
    NotFoundError: "No camera was found. Connect a webcam and try again.",
    NotReadableError:
      "Camera is busy or unavailable. Close other camera apps and try again.",
    OverconstrainedError:
      "This camera cannot use the requested settings. Try the other camera option.",
  };
  return (
    messages[error.name] ||
    error.message ||
    "Tracking could not start. Check your connection and browser, then retry."
  );
}
function draw(results, s) {
  const width = video.videoWidth,
    height = video.videoHeight;
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }
  ctx.clearRect(0, 0, width, height);
  const hands = results.hands.landmarks || [];
  if (mode === "body") {
    for (const body of results.body?.landmarks || [])
      skeleton(ctx, canvas, body, POSE_LINES, "#a4e881", true);
    $("mode-help").textContent = results.body?.landmarks?.length
      ? "Body detected · keep your head and feet in view."
      : "Step back until your full body fits in the camera.";
  }
  let total = 0;
  const details = [];
  hands.forEach((points, i) => {
    skeleton(
      ctx,
      canvas,
      points,
      HAND_LINES,
      mode === "draw" ? "#ffffff66" : "#70e4ef",
    );
    const count = countFingers(points, width, height);
    total += count;
    const category = (results.hands.handednesses || results.hands.handedness)?.[
      i
    ]?.[0];
    details.push((category?.categoryName || "Hand") + ": " + count);
  });
  if (mode === "draw") {
    $("mode-help").textContent = drawing.update(
      hands,
      $("ink").value,
      Number($("brush").value),
      width / height,
    );
    drawing.render(ctx, width, height);
  }
  if (mode === "effects")
    $("mode-help").textContent = drawGestureEffect(
      ctx,
      hands,
      width,
      height,
      performance.now(),
      matchMedia("(prefers-reduced-motion: reduce)").matches,
    );
  $("hands").textContent = String(hands.length);
  $("fingers").textContent = String(s.smoother.update(total, hands.length));
  $("hand-detail").textContent = details.length
    ? details.join(" · ")
    : "No hands detected.";
}
function loop(s, now) {
  if (session !== s) return;
  try {
    if (
      video.readyState >= 2 &&
      video.videoWidth &&
      video.currentTime !== s.videoTime &&
      now - s.lastInference >= 66
    ) {
      const timestamp = Math.max(s.timestamp + 1, Math.floor(now));
      const result = s.detectors.detect(video, timestamp);
      s.timestamp = timestamp;
      s.videoTime = video.currentTime;
      const instant = s.lastInference ? 1000 / (now - s.lastInference) : 0;
      s.fps = s.fps ? 0.8 * s.fps + 0.2 * instant : instant;
      s.lastInference = now;
      s.lastFrame = performance.now();
      draw(result, s);
      $("fps").textContent = s.fps ? Math.round(s.fps).toString() : "—";
      $("viewport").dataset.frames = String(++s.processed);
    }
    s.frame = requestAnimationFrame((t) => loop(s, t));
  } catch (error) {
    stop("Tracking stopped.");
    $("error").textContent = "Tracking failed: " + errorMessage(error);
  }
}
function watch(s) {
  if (session !== s) return;
  if (performance.now() - s.lastFrame > 12000) {
    stop("Camera stopped.");
    $("error").textContent =
      "No fresh camera frames arrived. Check your camera and start again.";
    return;
  }
  s.watchdog = setTimeout(() => watch(s), 2000);
}
async function start() {
  if (session) return;
  $("error").textContent = "";
  if (!window.isSecureContext || !navigator.mediaDevices?.getUserMedia) {
    $("error").textContent =
      "Camera access requires HTTPS and a supported browser. Open this page directly in a recent Chrome, Edge, Firefox or Safari browser.";
    return;
  }
  const s = {
    stream: null,
    detectors: null,
    frame: 0,
    watchdog: 0,
    disposed: false,
    smoother: new StableCount(),
    timestamp: -1,
    lastInference: 0,
    videoTime: -1,
    processed: 0,
    lastFrame: performance.now(),
    fps: 0,
  };
  session = s;
  $("start").disabled = true;
  $("stop").disabled = false;
  $("settings").disabled = true;
  $("start").textContent = "Starting…";
  $("status").textContent = "Loading tracking models…";
  $("mode-label").textContent = "INITIALIZING";
  const pose = mode === "body",
    facing = $("facing").value;
  try {
    // Late model results are always closed after cancellation or a timeout.
    const pending = loadDetectors(pose).then((detectors) => {
      if (session !== s) {
        detectors.close();
        return null;
      }
      s.detectors = detectors;
      return detectors;
    });
    await timeout(
      pending,
      90000,
      "Models took too long to load. Check your internet connection and retry.",
    );
    if (session !== s) return;
    $("status").textContent = "Waiting for camera permission…";
    // Permission prompts cannot be cancelled; stop any late stream immediately.
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: false,
      video: {
        facingMode: { ideal: facing },
        width: { ideal: 640 },
        height: { ideal: 480 },
        frameRate: { ideal: 24, max: 30 },
      },
    });
    if (session !== s) {
      stream.getTracks().forEach((t) => t.stop());
      return;
    }
    s.stream = stream;
    stream.getVideoTracks().forEach((track) =>
      track.addEventListener("ended", () => {
        if (session === s) {
          stop("Camera disconnected.");
          $("error").textContent =
            "Camera access ended. Reconnect or allow it, then start again.";
        }
      }),
    );
    video.srcObject = stream;
    await timeout(
      video.play(),
      10000,
      "Camera could not begin playback. Try starting again.",
    );
    if (session !== s) return;
    if (!video.videoWidth)
      throw new Error(
        "Camera returned no video dimensions. Try another camera.",
      );
    $("viewport").style.aspectRatio =
      video.videoWidth + "/" + video.videoHeight;
    $("viewport").classList.toggle("mirrored", $("mirror").checked);
    $("empty").hidden = true;
    $("indicator").classList.add("active");
    $("status").textContent = pose
      ? "Tracking hands and body locally."
      : "Tracking hands locally.";
    $("mode-label").textContent = "CAMERA ON";
    $("start").textContent = "Camera Running";
    s.lastFrame = performance.now();
    watch(s);
    s.frame = requestAnimationFrame((t) => loop(s, t));
  } catch (error) {
    if (session === s) {
      stop("Camera is off.");
      $("error").textContent = errorMessage(error);
    }
  }
}
$("start").addEventListener("click", start);
$("stop").addEventListener("click", () => stop());
$("mirror").addEventListener("change", () => {
  $("viewport").classList.toggle("mirrored", $("mirror").checked);
});
document.addEventListener("visibilitychange", () => {
  if (document.hidden && session)
    stop("Camera stopped because the tab is hidden.");
});
window.addEventListener("pagehide", () => stop());

const descriptions = {
  hands: "Hold your palms toward the camera to count fingers.",
  body: "Step back until your full body fits in the camera.",
  draw: "Pinch thumb and index to draw. Release to lift the pen.",
  effects: "Show both hands. Spread them apart, then move them up/down.",
};
for (const button of document.querySelectorAll("[data-mode]")) {
  button.addEventListener("click", () => {
    if (mode === button.dataset.mode) return;
    const running = Boolean(session);
    stop("Mode changed.");
    mode = button.dataset.mode;
    for (const item of document.querySelectorAll("[data-mode]"))
      item.setAttribute("aria-pressed", String(item === button));
    $("draw-tools").hidden = mode !== "draw";
    $("mode-help").textContent = descriptions[mode];
    if (running) start();
  });
}
function redrawArt() {
  if (mode !== "draw") return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawing.render(ctx, canvas.width, canvas.height);
}
$("clear-art").addEventListener("click", () => {
  drawing.clear();
  redrawArt();
});
$("undo-art").addEventListener("click", () => {
  drawing.undo();
  redrawArt();
});
$("save-art").addEventListener("click", () => {
  const output = document.createElement("canvas");
  output.width = canvas.width || 640;
  output.height = canvas.height || 480;
  const context = output.getContext("2d");
  if ($("mirror").checked) {
    context.translate(output.width, 0);
    context.scale(-1, 1);
  }
  drawing.render(context, output.width, output.height);
  const link = document.createElement("a");
  link.download = "aegis-air-drawing.png";
  link.href = output.toDataURL("image/png");
  link.click();
});
