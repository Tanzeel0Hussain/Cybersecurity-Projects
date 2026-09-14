export function countFingers(landmarks,width=1,height=1){
 if(landmarks.length!==21||width<=0||height<=0)return 0;
 const points=landmarks.map(p=>[p.x*width,p.y*height]);
 if(points.some(p=>p.some(v=>!Number.isFinite(v))))return 0;
 const distance=(a,b)=>Math.hypot(points[a][0]-points[b][0],points[a][1]-points[b][1]);
 const palm=distance(0,9);if(palm<1e-8)return 0;
 const margin=palm*.08;
 return Number(distance(4,17)>distance(3,17)+margin)+[8,12,16,20].filter(t=>distance(t,0)>distance(t-2,0)+margin).length;
}
export class StableCount{
 constructor(window=7){this.window=window;this.values=[];this.hands=null;}
 update(count,hands){
  if(hands!==this.hands||hands===0)this.values=[];
  this.hands=hands;if(!hands)return 0;
  this.values.push(count);if(this.values.length>this.window)this.values.shift();
  const frequencies=new Map();for(const value of this.values)frequencies.set(value,(frequencies.get(value)||0)+1);
  const max=Math.max(...frequencies.values());
  return [...this.values].reverse().find(v=>frequencies.get(v)===max);
 }
}
export const HAND_LINES=[[0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[5,9],[9,10],[10,11],[11,12],[9,13],[13,14],[14,15],[15,16],[13,17],[17,18],[18,19],[19,20],[0,17]];
export const POSE_LINES=[[11,12],[11,13],[13,15],[15,17],[15,19],[15,21],[17,19],[12,14],[14,16],[16,18],[16,20],[16,22],[18,20],[11,23],[12,24],[23,24],[23,25],[24,26],[25,27],[26,28],[27,29],[28,30],[29,31],[30,32],[27,31],[28,32]];
