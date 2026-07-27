(() => {
'use strict';

const KEYS = {
  theme: 'htb-theme-v4',
  language: 'htb-language-v4',
  completed: 'htb-completed-v4',
  font: 'htb-font-v4',
  width: 'htb-width-v4'
};
const root = document.documentElement;
const body = document.body;
const isGreek = () => (body.dataset.language || root.lang) === 'el';
const q = (selector, scope=document) => scope.querySelector(selector);
const qa = (selector, scope=document) => [...scope.querySelectorAll(selector)];

function storageGet(key, fallback=null) {
  try { return localStorage.getItem(key) ?? fallback; } catch (_) { return fallback; }
}
function storageSet(key, value) {
  try { localStorage.setItem(key, value); } catch (_) {}
}
function showToast(en, el=en) {
  const toast=q('[data-toast]');
  if (!toast) return;
  toast.textContent=isGreek()?el:en;
  toast.classList.add('is-visible');
  clearTimeout(showToast.timer);
  showToast.timer=setTimeout(()=>toast.classList.remove('is-visible'),2200);
}

function readCompleted() {
  try {
    const value=JSON.parse(storageGet(KEYS.completed,'[]'));
    return new Set(Array.isArray(value)?value:[]);
  } catch (_) { return new Set(); }
}
function saveCompleted(items) { storageSet(KEYS.completed,JSON.stringify([...items])); }

function applyTheme(theme) {
  const next=theme==='light'?'light':'dark';
  root.dataset.theme=next;
  storageSet(KEYS.theme,next);
  qa('[data-theme-toggle]').forEach(button=>{
    button.textContent=next==='dark'?'☀':'☾';
    button.setAttribute('aria-label',next==='dark'?(isGreek()?'Χρήση φωτεινού θέματος':'Use light theme'):(isGreek()?'Χρήση σκοτεινού θέματος':'Use dark theme'));
    button.setAttribute('aria-pressed',String(next==='light'));
  });
  const themeMeta=q('meta[name="theme-color"]');
  if (themeMeta) themeMeta.content=next==='dark'?'#07110f':'#f4f8f6';
}
function initTheme() {
  const preferred=window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';
  applyTheme(storageGet(KEYS.theme,preferred));
  qa('[data-theme-toggle]').forEach(button=>button.addEventListener('click',()=>applyTheme(root.dataset.theme==='dark'?'light':'dark')));
}

function updateProgress() {
  const completed=readCompleted();
  const total=Number(body.dataset.totalLessons||36);
  const listed=new Set(qa('[data-lesson-id]').map(node=>node.dataset.lessonId).filter(Boolean));
  const count=[...completed].filter(id=>listed.size===0||listed.has(id)).length;
  const safe=Math.min(count,total);
  const percent=Math.round((safe/total)*100);
  qa('[data-progress-fill]').forEach(node=>node.style.width=`${percent}%`);
  qa('[data-progress-text]').forEach(node=>node.textContent=`${percent}%`);
  qa('[data-progress-count]').forEach(node=>node.textContent=`${safe}/${total}`);
  qa('[data-lesson-id]').forEach(link=>link.classList.toggle('is-complete',completed.has(link.dataset.lessonId)));
}
function initCompletion() {
  const pageId=body.dataset.pageId;
  const button=q('.complete-button');
  const refresh=()=>{
    if (!button||!pageId) return;
    const done=readCompleted().has(pageId);
    button.classList.toggle('is-complete',done);
    button.textContent=done?`✓ ${button.dataset.completedLabel}`:button.dataset.completeLabel;
    button.setAttribute('aria-pressed',String(done));
  };
  button?.addEventListener('click',()=>{
    const completed=readCompleted();
    completed.has(pageId)?completed.delete(pageId):completed.add(pageId);
    saveCompleted(completed);
    refresh(); updateProgress();
    showToast(completed.has(pageId)?'Lesson completed':'Lesson reopened',completed.has(pageId)?'Το μάθημα ολοκληρώθηκε':'Το μάθημα άνοιξε ξανά');
  });
  refresh(); updateProgress();
}

function initMenu() {
  const open=q('[data-menu-toggle]');
  const setOpen=state=>{
    body.classList.toggle('menu-open',state);
    open?.setAttribute('aria-expanded',String(state));
    if (state) q('.sidebar input')?.focus();
  };
  open?.addEventListener('click',()=>setOpen(!body.classList.contains('menu-open')));
  qa('[data-menu-close]').forEach(node=>node.addEventListener('click',()=>setOpen(false)));
  document.addEventListener('keydown',event=>{ if(event.key==='Escape') setOpen(false); });
}
function initNavigation() {
  qa('.nav-module').forEach(module=>{
    const button=q('.nav-module-toggle',module);
    const active=module.classList.contains('is-current');
    module.classList.toggle('is-collapsed',!active);
    button?.setAttribute('aria-expanded',String(active));
  });
  qa('.nav-module-toggle').forEach(button=>button.addEventListener('click',()=>{
    const module=button.closest('.nav-module');
    const collapsed=module.classList.toggle('is-collapsed');
    button.setAttribute('aria-expanded',String(!collapsed));
  }));
  const input=q('#lesson-search');
  input?.addEventListener('input',()=>{
    const query=input.value.trim().toLocaleLowerCase();
    qa('.nav-lesson').forEach(link=>{
      link.hidden=query.length>0&&!(link.dataset.search||link.textContent.toLowerCase()).includes(query);
    });
    qa('.nav-module').forEach(module=>{
      const any=qa('.nav-lesson',module).some(link=>!link.hidden);
      module.hidden=query.length>0&&!any;
      if (query&&any) {
        module.classList.remove('is-collapsed');
        q('.nav-module-toggle',module)?.setAttribute('aria-expanded','true');
      }
    });
  });
}

function initCodeCopy() {
  qa('.lesson-content pre').forEach(pre=>{
    if (q('.copy-code',pre)) return;
    const code=q('code',pre);
    if (!code) return;
    const button=document.createElement('button');
    button.type='button'; button.className='copy-code';
    button.textContent=isGreek()?'Αντιγραφή':'Copy';
    button.addEventListener('click',async()=>{
      try {
        await navigator.clipboard.writeText(code.innerText);
        button.textContent=isGreek()?'Αντιγράφηκε':'Copied';
        setTimeout(()=>button.textContent=isGreek()?'Αντιγραφή':'Copy',1300);
      } catch (_) { showToast('Copy failed','Η αντιγραφή απέτυχε'); }
    });
    pre.appendChild(button);
  });
}

function setHomeLanguage(language) {
  const lang=language==='el'?'el':'en';
  root.lang=lang; storageSet(KEYS.language,lang);
  qa('[data-en][data-el]').forEach(node=>{
    const value=node.dataset[lang];
    if (value!==undefined) node.textContent=value;
  });
  qa('[data-language-toggle]').forEach(button=>button.textContent=lang==='en'?'Ελληνικά':'English');
  qa('[data-module-link],[data-device-link]').forEach(link=>link.href=lang==='en'?link.dataset.linkEn:link.dataset.linkEl);
  qa('[data-start-course]').forEach(link=>link.href=`pages/${lang}/device-setup/index.html`);
  const safety=q('[data-home-safety]');
  if (safety) safety.href=`pages/${lang}/safety/index.html`;
  applyTheme(root.dataset.theme);
}
function initLanguage() {
  if (body.classList.contains('home-page')) {
    const browserGreek=(navigator.language||'').toLowerCase().startsWith('el');
    setHomeLanguage(storageGet(KEYS.language,browserGreek?'el':'en'));
    qa('[data-language-toggle]').forEach(button=>button.addEventListener('click',()=>setHomeLanguage(root.lang==='en'?'el':'en')));
  } else if (body.dataset.language) {
    storageSet(KEYS.language,body.dataset.language);
    q('[data-language-switch]')?.addEventListener('click',()=>{
      const url=body.dataset.altLanguageUrl;
      if (url) window.location.href=url;
    });
  }
}

function applyReader() {
  const size=Math.max(0,Math.min(3,Number(storageGet(KEYS.font,'0'))));
  body.dataset.fontSize=String(size);
  body.classList.toggle('narrow-reading',storageGet(KEYS.width,'normal')==='narrow');
}
function initReader() {
  applyReader();
  const panel=q('[data-reader-panel]');
  const toggle=q('[data-reader-toggle]');
  toggle?.addEventListener('click',()=>{
    const opening=panel?.hidden;
    if(panel) panel.hidden=!opening;
    toggle.setAttribute('aria-expanded',String(opening));
  });
  q('[data-font-minus]')?.addEventListener('click',()=>{storageSet(KEYS.font,String(Math.max(0,Number(storageGet(KEYS.font,'0'))-1)));applyReader();});
  q('[data-font-plus]')?.addEventListener('click',()=>{storageSet(KEYS.font,String(Math.min(3,Number(storageGet(KEYS.font,'0'))+1)));applyReader();});
  q('[data-font-reset]')?.addEventListener('click',()=>{storageSet(KEYS.font,'0');applyReader();});
  q('[data-width-toggle]')?.addEventListener('click',()=>{storageSet(KEYS.width,body.classList.contains('narrow-reading')?'normal':'narrow');applyReader();});
}

function initPlatformTabs() {
  qa('.platform-tabs').forEach(group=>{
    qa('button',group).forEach(button=>button.addEventListener('click',()=>{
      const target=button.dataset.tabTarget;
      qa('button',group).forEach(b=>b.classList.toggle('is-active',b===button));
      const parent=group.parentElement;
      qa('[data-tab-panel]',parent).forEach(panel=>panel.hidden=panel.dataset.tabPanel!==target);
    }));
  });
}

function initProgressTools() {
  q('[data-export-progress]')?.addEventListener('click',()=>{
    const payload={version:1,course:'HackTheBasics.gr',exportedAt:new Date().toISOString(),completed:[...readCompleted()],theme:root.dataset.theme,language:body.dataset.language||root.lang};
    const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
    const url=URL.createObjectURL(blob);
    const a=document.createElement('a'); a.href=url; a.download='hackthebasics-progress.json'; a.click();
    URL.revokeObjectURL(url);
    showToast('Progress exported','Η πρόοδος εξήχθη');
  });
  q('[data-import-progress]')?.addEventListener('change',async event=>{
    const file=event.target.files?.[0]; if(!file) return;
    try {
      const data=JSON.parse(await file.text());
      if(!Array.isArray(data.completed)) throw new Error('invalid');
      saveCompleted(new Set(data.completed.filter(x=>typeof x==='string')));
      if(data.theme) applyTheme(data.theme);
      updateProgress();
      showToast('Progress imported','Η πρόοδος εισήχθη');
    } catch(_) { showToast('Invalid progress file','Μη έγκυρο αρχείο προόδου'); }
    event.target.value='';
  });
  q('[data-reset-progress]')?.addEventListener('click',()=>{
    const message=isGreek()?'Να μηδενιστεί όλη η πρόοδος;':'Reset all course progress?';
    if(window.confirm(message)){saveCompleted(new Set());updateProgress();showToast('Progress reset','Η πρόοδος μηδενίστηκε');}
  });
}

function initCommandLab() {
  const lab=q('[data-command-lab]'); if(!lab) return;
  const output=q('[data-lab-output]',lab), form=q('[data-lab-form]',lab), input=q('[data-lab-input]',lab);
  const fs={
    '/home/student':{type:'dir',children:['notes','welcome.txt','.flag']},
    '/home/student/welcome.txt':{type:'file',content:'Welcome. Explore the notes directory and inspect hidden files.'},
    '/home/student/.flag':{type:'file',content:'HTB{browser_shell_basics}'},
    '/home/student/notes':{type:'dir',children:['networking.txt','safety.txt']},
    '/home/student/notes/networking.txt':{type:'file',content:'DNS maps names to addresses. Ports identify network services.'},
    '/home/student/notes/safety.txt':{type:'file',content:'Only test systems you own or have explicit permission to assess.'}
  };
  let cwd='/home/student';
  const clean=path=>{
    if(!path||path==='~') return '/home/student';
    const base=path.startsWith('/')?[]:cwd.split('/').filter(Boolean);
    path.split('/').forEach(part=>{if(!part||part==='.')return;if(part==='..')base.pop();else base.push(part);});
    return '/'+base.join('/');
  };
  const print=(text,klass='')=>{
    const p=document.createElement('p'); if(klass)p.className=klass;
    p.textContent=text; output.appendChild(p); output.scrollTop=output.scrollHeight;
  };
  form.addEventListener('submit',event=>{
    event.preventDefault();
    const raw=input.value.trim(); if(!raw)return;
    print(`student@hackthebasics:${cwd.replace('/home/student','~')}$ ${raw}`,'lab-command');
    input.value='';
    const parts=raw.split(/\s+/), cmd=parts[0], args=parts.slice(1);
    if(cmd==='clear'){output.innerHTML='';return;}
    if(cmd==='help') print('help, pwd, ls [-la], cd <dir>, cat <file>, whoami, python --version, clear');
    else if(cmd==='pwd') print(cwd);
    else if(cmd==='whoami') print('student');
    else if(cmd==='python'&&args[0]==='--version') print('Python 3.12.0 (simulated)');
    else if(cmd==='ls'){
      const node=fs[cwd];
      if(!node||node.type!=='dir') print('Not a directory','lab-error');
      else {
        let names=[...node.children];
        const all=args.includes('-la')||args.includes('-a');
        if(!all) names=names.filter(name=>!name.startsWith('.'));
        print(names.join('  ')||'(empty)');
      }
    } else if(cmd==='cd'){
      const target=clean(args[0]||'~'), node=fs[target];
      if(node?.type==='dir') cwd=target; else print(`cd: ${args[0]||''}: no such directory`,'lab-error');
    } else if(cmd==='cat'){
      const target=clean(args[0]), node=fs[target];
      if(node?.type==='file') print(node.content);
      else print(`cat: ${args[0]||''}: no such file`,'lab-error');
    } else print(`${cmd}: command not found. Type help.`,'lab-error');
  });
  input.focus();
}

function initBackToTop() {
  const button=q('[data-back-to-top]');
  if(!button)return;
  const refresh=()=>button.classList.toggle('is-visible',window.scrollY>500);
  window.addEventListener('scroll',refresh,{passive:true}); refresh();
  button.addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));
}
function initExternalLinks() {
  qa('.lesson-content a[href^="http"]').forEach(link=>{link.target='_blank';link.rel='noopener noreferrer';});
}
function initPWA() {
  if('serviceWorker' in navigator && location.protocol.startsWith('http')) navigator.serviceWorker.register(`${body.dataset.root||'.'}/service-worker.js`).catch(()=>{});
  let deferred;
  window.addEventListener('beforeinstallprompt',event=>{
    event.preventDefault(); deferred=event;
    const button=q('[data-install-app]');
    if(button){button.hidden=false;button.addEventListener('click',async()=>{button.hidden=true;await deferred.prompt();deferred=null;},{once:true});}
  });
}
initTheme();
initLanguage();
initMenu();
initNavigation();
initCompletion();
initCodeCopy();
initReader();
initPlatformTabs();
initProgressTools();
initCommandLab();
initBackToTop();
initExternalLinks();
initPWA();
})();