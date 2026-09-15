// Pin JS and WASM to the same release. Camera frames are never sent to these hosts.
const VERSION = "0.10.21";
const BASE = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@" + VERSION;
const HAND =
  "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task";
const POSE =
  "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task";

export async function loadDetectors(includePose) {
  let hand = null,
    pose = null;
  try {
    const { FilesetResolver, HandLandmarker, PoseLandmarker } = await import(
      BASE + "/vision_bundle.mjs"
    );
    const files = await FilesetResolver.forVisionTasks(BASE + "/wasm");
    hand = await HandLandmarker.createFromOptions(files, {
      baseOptions: { modelAssetPath: HAND, delegate: "CPU" },
      runningMode: "VIDEO",
      numHands: 2,
      minHandDetectionConfidence: 0.65,
      minHandPresenceConfidence: 0.65,
      minTrackingConfidence: 0.65,
    });
    if (includePose)
      pose = await PoseLandmarker.createFromOptions(files, {
        baseOptions: { modelAssetPath: POSE, delegate: "CPU" },
        runningMode: "VIDEO",
        numPoses: 1,
        minPoseDetectionConfidence: 0.5,
        minPosePresenceConfidence: 0.5,
        minTrackingConfidence: 0.5,
      });
    return {
      detect(video, timestamp) {
        const hands = hand.detectForVideo(video, timestamp);
        const body = pose ? pose.detectForVideo(video, timestamp) : null;
        return { hands, body };
      },
      close() {
        try {
          hand?.close();
        } finally {
          pose?.close();
        }
      },
    };
  } catch (error) {
    try {
      hand?.close();
    } finally {
      pose?.close();
    }
    throw error;
  }
}
