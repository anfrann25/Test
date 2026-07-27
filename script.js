(() => {
'use strict';

const KEYS = {
  theme: 'htb-theme-v5',
  language: 'htb-language-v5',
  font: 'htb-font-v5',
  width: 'htb-width-v5'
};
const root = document.documentElement;
const body = document.body;
const q = (selector, scope=document) => scope.querySelector(selector);
const qa = (selector, scope=document) => [...scope.querySelectorAll(selector)];
const isGreek = () => (body.dataset.language || root.lang) === 'el';

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
  if (themeMeta) themeMeta.content=next==='dark'?'#06152e':'#f4f8ff';
}
function initTheme() {
  const preferred=window.matchMedia?.('(prefers-color-scheme: light)').matches?'light':'dark';
  applyTheme(storageGet(KEYS.theme,preferred));
  qa('[data-theme-toggle]').forEach(button=>button.addEventListener('click',()=>applyTheme(root.dataset.theme==='dark'?'light':'dark')));
}

function initCourseMenu() {
  const open=q('[data-menu-toggle]');
  if (!open) return;
  const setOpen=state=>{
    body.classList.toggle('menu-open',state);
    open.setAttribute('aria-expanded',String(state));
    q('.sidebar')?.setAttribute('aria-hidden',String(!state));
    if (state) q('.sidebar .nav-module-toggle, .sidebar a, .sidebar button')?.focus();
  };
  open.addEventListener('click',()=>setOpen(!body.classList.contains('menu-open')));
  qa('[data-menu-close]').forEach(node=>node.addEventListener('click',()=>setOpen(false)));
  qa('.sidebar a').forEach(link=>link.addEventListener('click',()=>setOpen(false)));
  document.addEventListener('keydown',event=>{ if(event.key==='Escape') setOpen(false); });
}

function initMainMenu() {
  const drawer=q('[data-main-menu]');
  const trigger=q('[data-main-menu-toggle]');
  if (!drawer||!trigger) return;
  let lastFocus=null;
  const setOpen=state=>{
    body.classList.toggle('main-menu-open',state);
    trigger.setAttribute('aria-expanded',String(state));
    drawer.setAttribute('aria-hidden',String(!state));
    if (state) {
      lastFocus=document.activeElement;
      q('[data-main-menu-close]',drawer)?.focus();
    } else if (lastFocus instanceof HTMLElement) lastFocus.focus({preventScroll:true});
  };
  trigger.addEventListener('click',()=>setOpen(!body.classList.contains('main-menu-open')));
  qa('[data-main-menu-close]').forEach(node=>node.addEventListener('click',()=>setOpen(false)));
  qa('a',drawer).forEach(link=>link.addEventListener('click',()=>setOpen(false)));
  document.addEventListener('keydown',event=>{
    if(event.key==='Escape'&&body.classList.contains('main-menu-open')) setOpen(false);
    if(event.key==='Tab'&&body.classList.contains('main-menu-open')) {
      const focusable=qa('a,button:not([disabled])',drawer).filter(node=>!node.hidden);
      if(!focusable.length) return;
      const first=focusable[0], last=focusable[focusable.length-1];
      if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
      else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
    }
  });
}

function initSidebarQuickLinks() {
  const sidebar=q('.sidebar');
  if(!sidebar||q('.sidebar-quick-links',sidebar)) return;
  const lang=body.dataset.language==='el'?'el':'en';
  const base=body.dataset.root||'.';
  const labels=lang==='el'
    ? [['⌂','Αρχική','home.html'],['▣','Ρύθμιση','pages/el/device-setup/index.html'],['›_','Τοπική πρακτική','pages/el/device-setup/command-lab.html'],['≡','Αναφορά','pages/el/reference/index.html']]
    : [['⌂','Home','home.html'],['▣','Setup','pages/en/device-setup/index.html'],['›_','Local practice','pages/en/device-setup/command-lab.html'],['≡','Reference','pages/en/reference/index.html']];
  const nav=document.createElement('nav');
  nav.className='sidebar-quick-links';
  nav.setAttribute('aria-label',lang==='el'?'Κύριοι σύνδεσμοι':'Main links');
  nav.innerHTML=labels.map(([icon,label,path])=>`<a href="${base}/${path}"><span>${icon}</span>${label}</a>`).join('');
  q('.sidebar-head',sidebar)?.insertAdjacentElement('afterend',nav);
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
}

function initCodeCopy() {
  qa('.lesson-content pre').forEach(pre=>{
    if (q('.copy-code',pre)) return;
    const code=q('code',pre);
    if (!code) return;
    const button=document.createElement('button');
    button.type='button';
    button.className='copy-code';
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
  root.lang=lang;
  storageSet(KEYS.language,lang);
  qa('[data-en][data-el]').forEach(node=>{
    const value=node.dataset[lang];
    if (value!==undefined) node.textContent=value;
  });
  qa('[data-language-toggle]').forEach(button=>button.textContent=lang==='en'?'Ελληνικά':'English');
  qa('[data-link-en][data-link-el]').forEach(link=>link.href=lang==='en'?link.dataset.linkEn:link.dataset.linkEl);
  qa('[data-start-course]').forEach(link=>link.href=`pages/${lang}/device-setup/index.html`);
  const safety=q('[data-home-safety]');
  if (safety) safety.href=`pages/${lang}/safety/index.html`;
  qa('[data-label-en][data-label-el]').forEach(node=>node.setAttribute('aria-label',lang==='en'?node.dataset.labelEn:node.dataset.labelEl));
  qa('[data-search-input]').forEach(input=>input.placeholder=lang==='en'?input.dataset.placeholderEn:input.dataset.placeholderEl);
  qa('[data-search-results]').forEach(results=>{results.hidden=true;results.innerHTML='';});
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
  document.addEventListener('click',event=>{
    if(panel&&!panel.hidden&&!panel.contains(event.target)&&event.target!==toggle){panel.hidden=true;toggle?.setAttribute('aria-expanded','false');}
  });
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

function normalized(value) {
  return value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase();
}
function linkFromRoot(path) {
  const base=(body.dataset.root||'.').replace(/\/$/,'');
  return `${base}/${path}`.replace(/^\.\/\.\//,'./');
}
function initSiteSearch() {
  const index=Array.isArray(window.HTB_COURSE_INDEX)?window.HTB_COURSE_INDEX:[];
  qa('[data-site-search]').forEach(component=>{
    const input=q('[data-search-input]',component);
    const results=q('[data-search-results]',component);
    if(!input||!results) return;
    let active=-1;
    const close=()=>{
      results.hidden=true;
      results.innerHTML='';
      input.setAttribute('aria-expanded','false');
      active=-1;
    };
    const chooseLanguage=()=>body.dataset.language||root.lang||'en';
    const render=()=>{
      const query=normalized(input.value.trim());
      if(query.length<2){close();return;}
      const language=chooseLanguage()==='el'?'el':'en';
      const matches=index.filter(item=>item.lang===language&&normalized(`${item.title} ${item.module} ${item.summary}`).includes(query)).slice(0,8);
      results.innerHTML='';
      active=-1;
      if(!matches.length){
        const empty=document.createElement('p');
        empty.className='search-empty';
        empty.textContent=language==='el'?'Δεν βρέθηκαν μαθήματα.':'No lessons found.';
        results.appendChild(empty);
      } else {
        matches.forEach((item,position)=>{
          const link=document.createElement('a');
          link.href=linkFromRoot(item.path);
          link.role='option';
          link.dataset.searchOption=String(position);
          const title=document.createElement('strong'); title.textContent=item.title;
          const module=document.createElement('span'); module.textContent=item.module;
          link.append(title,module);
          results.appendChild(link);
        });
      }
      results.hidden=false;
      input.setAttribute('aria-expanded','true');
    };
    const setActive=next=>{
      const options=qa('[data-search-option]',results);
      if(!options.length) return;
      active=(next+options.length)%options.length;
      options.forEach((option,index)=>option.classList.toggle('is-active',index===active));
      options[active].scrollIntoView({block:'nearest'});
    };
    input.addEventListener('input',render);
    input.addEventListener('focus',()=>{if(input.value.trim().length>=2)render();});
    input.addEventListener('keydown',event=>{
      const options=qa('[data-search-option]',results);
      if(event.key==='ArrowDown'){event.preventDefault();setActive(active+1);}
      else if(event.key==='ArrowUp'){event.preventDefault();setActive(active-1);}
      else if(event.key==='Enter'&&active>=0&&options[active]){event.preventDefault();options[active].click();}
      else if(event.key==='Escape') close();
    });
    document.addEventListener('click',event=>{if(!component.contains(event.target))close();});
  });
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
function initServiceWorker() {
  if('serviceWorker' in navigator && location.protocol.startsWith('http')) {
    navigator.serviceWorker.register(`${body.dataset.root||'.'}/service-worker.js`).catch(()=>{});
  }
}

initTheme();
initLanguage();
initCourseMenu();
initMainMenu();
initSidebarQuickLinks();
initNavigation();
initCodeCopy();
initReader();
initPlatformTabs();
initSiteSearch();
initBackToTop();
initExternalLinks();
initServiceWorker();
})();
