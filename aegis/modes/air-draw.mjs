// Strokes use normalized camera coordinates, so resizing preserves the drawing.
export class AirDraw {
  constructor() {
    this.strokes = [];
    this.lift();
  }
  lift() {
    this.active = null;
    this.wrist = null;
  }
  clear() {
    this.strokes = [];
    this.lift();
  }
  undo() {
    this.strokes.pop();
    this.lift();
  }
  update(hands, color, size, aspect = 1) {
    if (!hands.length) {
      this.lift();
      return "Show one hand, then pinch to draw.";
    }
    const distance = (a, b) => Math.hypot((a.x - b.x) * aspect, a.y - b.y);
    const hand = this.wrist
      ? [...hands].sort(
          (a, b) => distance(a[0], this.wrist) - distance(b[0], this.wrist),
        )[0]
      : hands[0];
    if (this.wrist && distance(hand[0], this.wrist) > 0.3) this.lift();
    this.wrist = hand[0];
    const ratio =
      distance(hand[4], hand[8]) / Math.max(0.01, distance(hand[0], hand[9]));
    if (ratio > (this.active ? 0.5 : 0.35)) {
      this.active = null;
      return "Pen lifted · pinch thumb and index to draw.";
    }
    if (this.strokes.reduce((n, s) => n + s.points.length, 0) >= 12000) {
      this.lift();
      return "Drawing full · save, then clear to continue.";
    }
    if (!this.active) {
      this.active = { color, size, points: [] };
      this.strokes.push(this.active);
    }
    const previous = this.active.points.at(-1);
    const tip = hand[8];
    this.active.points.push(
      previous
        ? {
            x: previous.x * 0.55 + tip.x * 0.45,
            y: previous.y * 0.55 + tip.y * 0.45,
          }
        : { x: tip.x, y: tip.y },
    );
    return "Drawing · release your pinch to lift the pen.";
  }
  render(ctx, width, height) {
    ctx.lineCap = ctx.lineJoin = "round";
    for (const stroke of this.strokes) {
      ctx.strokeStyle = ctx.fillStyle = stroke.color;
      ctx.lineWidth = (stroke.size * width) / 640;
      ctx.beginPath();
      stroke.points.forEach((point, i) => {
        const x = point.x * width,
          y = point.y * height;
        if (i) ctx.lineTo(x, y);
        else ctx.moveTo(x, y);
      });
      ctx.stroke();
      if (stroke.points.length === 1) {
        const point = stroke.points[0];
        ctx.beginPath();
        ctx.arc(
          point.x * width,
          point.y * height,
          ctx.lineWidth / 2,
          0,
          Math.PI * 2,
        );
        ctx.fill();
      }
    }
  }
}
