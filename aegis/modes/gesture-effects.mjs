// A bounded, two-dimensional canvas effect controlled by two visible hands.
export function drawGestureEffect(
  ctx,
  hands,
  width,
  height,
  time,
  reducedMotion,
) {
  if (hands.length < 2) return "Show both palms to create a color portal.";
  const palm = (points) =>
    [0, 5, 9, 13, 17].reduce(
      (p, i) => ({ x: p.x + points[i].x / 5, y: p.y + points[i].y / 5 }),
      { x: 0, y: 0 },
    );
  const a = palm(hands[0]),
    b = palm(hands[1]);
  const x = ((a.x + b.x) * width) / 2,
    y = ((a.y + b.y) * height) / 2;
  const distance = Math.hypot((a.x - b.x) * width, (a.y - b.y) * height);
  const radius = Math.max(15, Math.min(width * 0.42, distance / 2));
  // Vertical hand position changes hue; distance controls size.
  const hue = ((a.y + b.y) * 360) % 360;
  const phase = reducedMotion ? 0 : time / 1400;
  ctx.save();
  const glow = ctx.createRadialGradient(x, y, 0, x, y, radius * 1.4);
  glow.addColorStop(0, `hsla(${hue},95%,60%,.08)`);
  glow.addColorStop(0.7, `hsla(${hue + 60},95%,60%,.3)`);
  glow.addColorStop(1, "transparent");
  ctx.fillStyle = glow;
  ctx.fillRect(0, 0, width, height);
  for (let ring = 0; ring < 4; ring++) {
    ctx.strokeStyle = `hsla(${hue + ring * 45},95%,65%,.85)`;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.ellipse(
      x,
      y,
      radius * (1 - ring * 0.12),
      radius * (0.45 + ring * 0.12),
      phase + ring * 0.6,
      0,
      Math.PI * 2,
    );
    ctx.stroke();
  }
  for (let i = 0; i < 64; i++) {
    const angle = (i * Math.PI * 2) / 64 + phase;
    const r = radius * (1 + 0.12 * Math.sin(i * 2 + phase));
    ctx.fillStyle = `hsl(${hue + i * 5},95%,70%)`;
    ctx.beginPath();
    ctx.arc(
      x + Math.cos(angle) * r,
      y + Math.sin(angle) * r,
      2 + (i % 3),
      0,
      Math.PI * 2,
    );
    ctx.fill();
  }
  ctx.restore();
  return "Move hands apart to expand · move up/down to change colors.";
}
