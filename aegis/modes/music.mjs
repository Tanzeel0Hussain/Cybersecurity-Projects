// Gesture mapping is pure JavaScript and can be tested without a camera or audio.
const SCALE = [48, 50, 52, 55, 57, 60, 62, 64, 67, 69, 72];
const clamp = (value, low, high) => Math.min(high, Math.max(low, value));
const frequency = (midi) => 440 * 2 ** ((midi - 69) / 12);
const noteName = (midi) =>
  ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"][midi % 12] +
  (Math.floor(midi / 12) - 1);

export function musicGesture(hands, mirrored = true, quantized = true) {
  if (hands.length !== 2 || hands.some((hand) => !hand?.[0] || !hand?.[8]))
    return null;
  const wrists = hands.map((hand) => hand[0]);
  if (
    hands.some((hand) =>
      [hand[0], hand[8]].some(
        (point) => !Number.isFinite(point.x) || !Number.isFinite(point.y),
      ),
    )
  )
    return null;
  // Screen-right hand controls pitch, independent of detector result ordering.
  const rightIndex = wrists[0].x > wrists[1].x !== mirrored ? 0 : 1;
  if (Math.abs(wrists[0].x - wrists[1].x) < 0.08) return null; // Crossing hands lifts the note.
  const tip = hands[rightIndex][8];
  const height = clamp((0.85 - tip.y) / 0.7, 0, 1);
  const midi = quantized
    ? SCALE[Math.round(height * (SCALE.length - 1))]
    : 48 + height * 24;
  const volume = clamp(
    (Math.abs(wrists[0].x - wrists[1].x) - 0.12) / 0.6,
    0,
    1,
  );
  return {
    frequency: frequency(midi),
    volume,
    note: quantized ? noteName(midi) : `${Math.round(frequency(midi))} Hz`,
    tip,
    wrists,
  };
}

// One oscillator, no audio files, no microphone, and no sound before a user click.
export class TouchlessInstrument {
  constructor(
    createContext = () =>
      new (window.AudioContext || window.webkitAudioContext)(),
  ) {
    this.createContext = createContext;
    this.context = null;
    this.generation = 0;
    this.enabled = false;
  }
  async enable() {
    this.close();
    const generation = this.generation;
    const context = this.createContext();
    this.context = context;
    try {
      this.oscillator = context.createOscillator();
      this.gain = context.createGain();
      this.gain.gain.value = 0;
      this.oscillator.connect(this.gain);
      this.gain.connect(context.destination);
      this.oscillator.start();
      await context.resume();
      if (generation !== this.generation) return false;
      if (context.state !== "running")
        throw new Error("Sound could not start. Try Enable Sound again.");
      this.enabled = true;
      return true;
    } catch (error) {
      if (generation !== this.generation) return false;
      this.close();
      throw error;
    }
  }
  update(gesture, level = 0.3, tone = "sine") {
    if (!this.enabled || !this.context) return;
    const now = this.context.currentTime;
    const gain = this.gain.gain;
    gain.cancelScheduledValues(now);
    gain.setValueAtTime(gain.value, now);
    if (!gesture) {
      gain.linearRampToValueAtTime(0, now + 0.04);
      return;
    }
    this.oscillator.type = tone === "triangle" ? "triangle" : "sine";
    this.oscillator.frequency.setTargetAtTime(gesture.frequency, now, 0.035);
    const volume = clamp(level, 0, 1) * gesture.volume * 0.12;
    gain.linearRampToValueAtTime(volume, now + 0.025);
    // Audio-clock dead man's switch: silence even if inference/main thread stalls.
    gain.setValueAtTime(volume, now + 0.15);
    gain.linearRampToValueAtTime(0, now + 0.25);
  }
  close() {
    this.generation++;
    this.enabled = false;
    if (this.context) {
      try {
        this.gain?.gain.cancelScheduledValues(this.context.currentTime);
        this.gain?.gain.setValueAtTime(0, this.context.currentTime);
        this.oscillator?.stop();
      } catch {
        /* context may already be closed */
      }
      this.context.close().catch(() => {});
    }
    this.context = this.oscillator = this.gain = null;
  }
}

export function renderMusic(ctx, gesture, width, height) {
  if (!gesture) return;
  ctx.save();
  ctx.strokeStyle = "#b7a0ff";
  ctx.lineWidth = 2;
  const [a, b] = gesture.wrists;
  ctx.beginPath();
  ctx.moveTo(a.x * width, a.y * height);
  ctx.lineTo(b.x * width, b.y * height);
  ctx.stroke();
  ctx.strokeStyle = "#70e4ef";
  ctx.beginPath();
  ctx.arc(
    gesture.tip.x * width,
    gesture.tip.y * height,
    12 + gesture.volume * 16,
    0,
    Math.PI * 2,
  );
  ctx.stroke();
  ctx.restore();
}
