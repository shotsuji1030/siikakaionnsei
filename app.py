"""詩歌会 展示音声ガイド — Streamlit Community Cloud compatible."""
from pathlib import Path
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="展示音声ガイド", page_icon="📖", layout="centered")
st.markdown("""<style>
.stApp {background: #faf8f4; color: #282521;}
.block-container {max-width: 760px; padding-top: 3rem;}
h1 {letter-spacing:.04em;}
</style>""", unsafe_allow_html=True)
#st.caption("詩歌会")
st.title("展示音声ガイド")

audio_path = Path(__file__).resolve().parent / "guide.m4a"
if not audio_path.exists():
    st.error("guide.mp3 が見つかりません。app.py と同じフォルダに配置してください。")
    st.stop()

@st.cache_data
def audio_data(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")

b64 = audio_data(str(audio_path))
html = """<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,'Noto Sans JP',sans-serif;color:#302a25;background:transparent}.panel{background:white;border:1px solid #e3dcd3;border-radius:19px;padding:24px;box-shadow:0 8px 25px #4c3b2510}.status{font-size:13px;color:#746c64;margin-bottom:10px}.bar{width:100%;accent-color:#416b70;cursor:pointer}.times{display:flex;justify-content:space-between;color:#746c64;font-variant-numeric:tabular-nums;font-size:13px}.actions{display:flex;gap:10px;margin:22px 0;flex-wrap:wrap}button{cursor:pointer;border:1px solid #d6d0c7;border-radius:12px;padding:13px 18px;background:#f7f5f1;font-weight:600;font-size:16px;color:#302a25}button.primary{background:#315c62;color:white;border-color:#315c62;flex:1;min-width:160px}.settings{display:flex;gap:18px;flex-wrap:wrap;align-items:center;font-size:14px}.setting{display:flex;align-items:center;gap:7px}select{padding:8px;border:1px solid #ddd5cb;border-radius:8px;background:white}input[type=range]{accent-color:#416b70;max-width:125px}.note{font-size:12px;color:#857d74;margin-top:16px}@media(max-width:430px){.panel{padding:17px}.settings{gap:12px}}</style></head>
<body><section class="panel"><div class="status" id="status">停止中</div><audio id="audio" preload="auto" src="data:audio/mpeg;base64,AUDIOBASE64"></audio>
<input id="seek" class="bar" type="range" value="0" min="0" max="1000" aria-label="再生位置"/>
<div class="times"><span id="current">0:00</span><span id="duration">--:--</span></div>
<div class="actions"><button class="primary" id="play">▶ 再生する</button><button id="restart">↺ 最初から</button></div>
<div class="settings"><label class="setting"><input type="checkbox" id="loop" checked/>自動で繰り返す</label><label class="setting">次の再生まで <select id="delay"><option value="0">0秒</option><option value="3" selected>3秒</option><option value="5">5秒</option><option value="10">10秒</option><option value="20">20秒</option></select></label><label class="setting">音量 <input type="range" id="volume" min="0" max="1" step="0.05" value="1"/></label></div>
<div class="note"> </div></section>
<script>
const a=document.getElementById('audio'), play=document.getElementById('play'), restart=document.getElementById('restart'), seek=document.getElementById('seek'), loop=document.getElementById('loop'), delay=document.getElementById('delay'), volume=document.getElementById('volume'), status=document.getElementById('status');let timer=null;
const fmt=t=>{if(!Number.isFinite(t))return '--:--';return Math.floor(t/60)+':'+String(Math.floor(t%60)).padStart(2,'0')};
function cancel(){if(timer!==null){clearTimeout(timer);timer=null}}
function update(){document.getElementById('current').textContent=fmt(a.currentTime);document.getElementById('duration').textContent=fmt(a.duration);seek.value=Number.isFinite(a.duration)&&a.duration>0?String(Math.floor(1000*a.currentTime/a.duration)):'0';}
function refresh(){play.textContent=a.paused?'▶ 再生する':'Ⅱ 一時停止';if(!a.paused)status.textContent='音声を再生中';else if(timer===null)status.textContent='一時停止中';}
async function start(){cancel();try{await a.play();refresh()}catch(e){status.textContent='再生できませんでした。もう一度押してください。'}}
play.addEventListener('click',()=>{if(timer!==null){cancel();start()}else if(a.paused)start();else{a.pause();refresh()}});
restart.addEventListener('click',()=>{cancel();a.currentTime=0;start()});
a.addEventListener('timeupdate',update);a.addEventListener('loadedmetadata',update);a.addEventListener('play',refresh);a.addEventListener('pause',refresh);
seek.addEventListener('input',()=>{if(Number.isFinite(a.duration))a.currentTime=a.duration*Number(seek.value)/1000});volume.addEventListener('input',()=>{a.volume=Number(volume.value)});
a.addEventListener('ended',()=>{update();refresh();if(!loop.checked){status.textContent='再生終了';return}const seconds=Number(delay.value);status.textContent=seconds?`再生終了・${seconds}秒後に繰り返します`:'繰り返し再生中';timer=setTimeout(()=>{timer=null;a.currentTime=0;start()},seconds*1000)});
loop.addEventListener('change',()=>{if(!loop.checked){cancel();status.textContent=a.paused?'停止中':'音声を再生中'}});
window.addEventListener('pagehide',cancel);
</script></body></html>""".replace('AUDIOBASE64', b64)
components.html(html, height=350, scrolling=False)

