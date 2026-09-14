import {loadDetectors} from './detectors.mjs';
import {countFingers,StableCount,HAND_LINES,POSE_LINES} from './tracking.mjs';
const $=id=>document.getElementById(id);
const video=$('video'),canvas=$('overlay'),ctx=canvas.getContext('2d');
let session=null;
function timeout(promise,ms,message){
 let timer;
 return Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(new Error(message)),ms);})]).finally(()=>clearTimeout(timer));
}
function clearMetrics(){
 $('fingers').textContent='0';$('hands').textContent='0';$('fps').textContent='—';
 $('hand-detail').textContent='No hands detected.';ctx.clearRect(0,0,canvas.width,canvas.height);
}
function dispose(s){
 if(!s||s.disposed)return;s.disposed=true;
 cancelAnimationFrame(s.frame);
 clearTimeout(s.watchdog);
 s.stream?.getTracks().forEach(t=>t.stop());
 try{s.detectors?.close();}catch{/* release remaining session even if a library close fails */}
}
function stop(message='Camera is off.'){
 const old=session;session=null;dispose(old);
 video.pause();video.srcObject=null;
 $('start').disabled=false;$('stop').disabled=true;$('settings').disabled=false;
 $('start').innerHTML='Start Camera <span>↗</span>';
 $('status').textContent=message;$('mode-label').textContent='CAMERA OFF';
 $('indicator').classList.remove('active');$('empty').hidden=false;clearMetrics();
}
function errorMessage(error){
 const messages={
  NotAllowedError:'Camera permission was denied. Allow camera access in your browser settings, then try again.',
  NotFoundError:'No camera was found. Connect a webcam and try again.',
  NotReadableError:'Camera is busy or unavailable. Close other camera apps and try again.',
  OverconstrainedError:'This camera cannot use the requested settings. Try the other camera option.'
 };
 return messages[error.name]||error.message||'Tracking could not start. Check your connection and browser, then retry.';
}
function skeleton(points,lines,color,isPose=false){
 const valid=p=>p&&Number.isFinite(p.x)&&Number.isFinite(p.y)&&(!isPose||(p.visibility??0)>.5);
 ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=2;
 for(const[a,b]of lines){
  if(!valid(points[a])||!valid(points[b]))continue;
  ctx.beginPath();ctx.moveTo(points[a].x*canvas.width,points[a].y*canvas.height);
  ctx.lineTo(points[b].x*canvas.width,points[b].y*canvas.height);ctx.stroke();
 }
 for(let i=isPose?11:0;i<points.length;i++){
  if(!valid(points[i]))continue;ctx.beginPath();
  ctx.arc(points[i].x*canvas.width,points[i].y*canvas.height,isPose?3:4,0,Math.PI*2);ctx.fill();
 }
}
function draw(results,s){
 const width=video.videoWidth,height=video.videoHeight;
 if(canvas.width!==width||canvas.height!==height){canvas.width=width;canvas.height=height;}
 ctx.clearRect(0,0,width,height);
 const hands=results.hands.landmarks||[];
 for(const body of results.body?.landmarks||[])skeleton(body,POSE_LINES,'#739ab7',true);
 let total=0;const details=[];
 hands.forEach((points,i)=>{
  skeleton(points,HAND_LINES,'#70e4ef');
  const count=countFingers(points,width,height);total+=count;
  const category=(results.hands.handednesses||results.hands.handedness)?.[i]?.[0];
  details.push((category?.categoryName||'Hand')+': '+count);
 });
 $('hands').textContent=String(hands.length);
 $('fingers').textContent=String(s.smoother.update(total,hands.length));
 $('hand-detail').textContent=details.length?details.join(' · '):'No hands detected.';
}
function loop(s,now){
 if(session!==s)return;
 try{
  if(video.readyState>=2&&video.videoWidth&&video.currentTime!==s.videoTime&&now-s.lastInference>=66){
   const timestamp=Math.max(s.timestamp+1,Math.floor(now));
   const result=s.detectors.detect(video,timestamp);
   s.timestamp=timestamp;s.videoTime=video.currentTime;
   const instant=s.lastInference?1000/(now-s.lastInference):0;
   s.fps=s.fps ? .8*s.fps+.2*instant : instant;
   s.lastInference=now;s.lastFrame=performance.now();
   draw(result,s);$('fps').textContent=s.fps?Math.round(s.fps).toString():'—';
   $('viewport').dataset.frames=String(++s.processed);
  }
  s.frame=requestAnimationFrame(t=>loop(s,t));
 }catch(error){
  stop('Tracking stopped.');$('error').textContent='Tracking failed: '+errorMessage(error);
 }
}
function watch(s){
 if(session!==s)return;
 if(performance.now()-s.lastFrame>12000){
  stop('Camera stopped.');$('error').textContent='No fresh camera frames arrived. Check your camera and start again.';return;
 }
 s.watchdog=setTimeout(()=>watch(s),2000);
}
async function start(){
 if(session)return;
 $('error').textContent='';
 if(!window.isSecureContext||!navigator.mediaDevices?.getUserMedia){$('error').textContent='Camera access requires HTTPS and a supported browser. Open this page directly in a recent Chrome, Edge, Firefox or Safari browser.';return;}
 const s={stream:null,detectors:null,frame:0,watchdog:0,disposed:false,smoother:new StableCount(),timestamp:-1,lastInference:0,videoTime:-1,processed:0,lastFrame:performance.now(),fps:0};
 session=s;$('start').disabled=true;$('stop').disabled=false;$('settings').disabled=true;
 $('start').textContent='Starting…';$('status').textContent='Loading tracking models…';$('mode-label').textContent='INITIALIZING';
 const pose=$('pose').checked,facing=$('facing').value;
 try{
  // Late model results are always closed after cancellation or a timeout.
  const pending=loadDetectors(pose).then(detectors=>{
   if(session!==s){detectors.close();return null;}
   s.detectors=detectors;return detectors;
  });
  await timeout(pending,90000,'Models took too long to load. Check your internet connection and retry.');
  if(session!==s)return;
  $('status').textContent='Waiting for camera permission…';
  // Permission prompts cannot be cancelled; stop any late stream immediately.
  const stream=await navigator.mediaDevices.getUserMedia({audio:false,video:{facingMode:{ideal:facing},width:{ideal:640},height:{ideal:480},frameRate:{ideal:24,max:30}}});
  if(session!==s){stream.getTracks().forEach(t=>t.stop());return;}
  s.stream=stream;
  stream.getVideoTracks().forEach(track=>track.addEventListener('ended',()=>{
   if(session===s){stop('Camera disconnected.');$('error').textContent='Camera access ended. Reconnect or allow it, then start again.';}
  }));
  video.srcObject=stream;
  await timeout(video.play(),10000,'Camera could not begin playback. Try starting again.');
  if(session!==s)return;
  if(!video.videoWidth)throw new Error('Camera returned no video dimensions. Try another camera.');
  $('viewport').style.aspectRatio=video.videoWidth+'/'+video.videoHeight;
  $('viewport').classList.toggle('mirrored',$('mirror').checked);
  $('empty').hidden=true;$('indicator').classList.add('active');
  $('status').textContent=pose?'Tracking hands and body locally.':'Tracking hands locally.';
  $('mode-label').textContent='CAMERA ON';$('start').textContent='Camera Running';
  s.lastFrame=performance.now();watch(s);
  s.frame=requestAnimationFrame(t=>loop(s,t));
 }catch(error){if(session===s){stop('Camera is off.');$('error').textContent=errorMessage(error);}}
}
$('start').addEventListener('click',start);
$('stop').addEventListener('click',()=>stop());
$('mirror').addEventListener('change',()=>{$('viewport').classList.toggle('mirrored',$('mirror').checked);});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&session)stop('Camera stopped because the tab is hidden.');});
window.addEventListener('pagehide',()=>stop());
