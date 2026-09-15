// Drawing helpers shared by hand and body modes.
export function skeleton(ctx, canvas, points, lines, color, isPose = false) {
  const valid = (p) =>
    p &&
    Number.isFinite(p.x) &&
    Number.isFinite(p.y) &&
    (!isPose || (p.visibility ?? 0) > 0.5);
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = 2;
  for (const [a, b] of lines) {
    if (!valid(points[a]) || !valid(points[b])) continue;
    ctx.beginPath();
    ctx.moveTo(points[a].x * canvas.width, points[a].y * canvas.height);
    ctx.lineTo(points[b].x * canvas.width, points[b].y * canvas.height);
    ctx.stroke();
  }
  for (let i = 0; i < points.length; i++) {
    if (!valid(points[i])) continue;
    ctx.beginPath();
    ctx.arc(
      points[i].x * canvas.width,
      points[i].y * canvas.height,
      isPose ? 3 : 4,
      0,
      Math.PI * 2,
    );
    ctx.fill();
  }
}
