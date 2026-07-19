#!/usr/bin/env node
/** 장기 토큰(60일) 갱신 — 만료 전 주기적으로 실행(예: 주 1회). config.json의 토큰을 갱신해 다시 저장. */
const fs=require("fs"),path=require("path");
const P=path.join(__dirname,"config.json"); const CFG=JSON.parse(fs.readFileSync(P));
async function refIG(t){const u=`https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=${t}`;return (await (await fetch(u)).json());}
async function refTH(t){const u=`https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token=${t}`;return (await (await fetch(u)).json());}
(async()=>{
  try{const a=await refIG(CFG.ig.accessToken); if(a.access_token){CFG.ig.accessToken=a.access_token; console.log("IG 토큰 갱신, 유효 약",Math.round((a.expires_in||0)/86400),"일");}else console.log("IG 갱신 응답:",JSON.stringify(a));}catch(e){console.log("IG 갱신 실패:",e.message);}
  try{const b=await refTH(CFG.threads.accessToken); if(b.access_token){CFG.threads.accessToken=b.access_token; console.log("Threads 토큰 갱신, 유효 약",Math.round((b.expires_in||0)/86400),"일");}else console.log("TH 갱신 응답:",JSON.stringify(b));}catch(e){console.log("TH 갱신 실패:",e.message);}
  fs.writeFileSync(P,JSON.stringify(CFG,null,2)); console.log("config.json 저장 완료");
})();
