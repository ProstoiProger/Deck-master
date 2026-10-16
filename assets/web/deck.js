/* deck-master web presentation runtime: adaptive view (slides or reading), navigation, overview, notes, presenter window.
   No dependencies, no network. */
(() => {
  const W = 1333.333, H = 750;
  const doc = document, root = doc.documentElement, body = doc.body;
  const slides = [...doc.querySelectorAll('.slide')];
  const n = slides.length;
  const params = new URLSearchParams(location.search);
  const presenter = params.has('presenter');
  const planned = parseFloat(body.dataset.minutes || '0') * 60;
  const $ = (id) => doc.getElementById(id);
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let cur = 0, started = 0, tick = null, idleT = null, sessionView = null, fromScroll = false, io = null;
  let chan = null;
  try { if ('BroadcastChannel' in window) chan = new BroadcastChannel('deck-master:' + doc.title); } catch (e) { chan = null; }
  const isReader = () => body.classList.contains('reader');

  /* ---- which view: slides (the stage, scaled) or reading (reflowing text) -------------------------------------------- */
  const viewPref = () => {
    const q = params.get('view');
    if (q === 'slides' || q === 'reader') return q;
    if (sessionView) return sessionView;
    try { const v = localStorage.getItem('deck-master:view'); if (v === 'slides' || v === 'reader') return v; } catch (e) { /* storage blocked */ }
    return 'auto';
  };
  // auto: the reading view on portrait screens and wherever the slide would be scaled below about half size
  const wantReader = () => {
    const p = viewPref();
    if (presenter) return false;
    if (p !== 'auto') return p === 'reader';
    return innerHeight > innerWidth * 1.1 || Math.min(innerWidth / W, innerHeight / H) < 0.55;
  };

  const fit = () => {
    if (!isReader()) {
      const room = body.classList.contains('notes-open') ? innerHeight * 0.66 : innerHeight;   // leave room for the notes panel
      root.style.setProperty('--k', Math.min(innerWidth / W, room / H));
    }
    if (body.classList.contains('ov')) {
      const first = slides[0];
      if (first) root.style.setProperty('--ko', first.clientWidth / W);
    }
    if (presenter) mountPresenter();
  };

  const applyView = () => {
    const r = wantReader();
    if (r !== isReader()) {
      body.classList.toggle('reader', r);
      root.classList.toggle('reader', r);
      if (r) { buildReader(); body.classList.remove('ov', 'notes-open'); }
      fit();
      if (r) showCard(cur, true);
    } else fit();
  };
  const toggleView = () => {
    sessionView = isReader() ? 'slides' : 'reader';
    try { localStorage.setItem('deck-master:view', sessionView); } catch (e) { /* storage blocked */ }
    params.delete('view');
    applyView();
  };

  /* ---- the reading view: built from the slides' text and pictures, in reading order --------------------------------- */
  const strong = (s) => s.split('**').map((part, i) => (i % 2 ? '<strong>' + part + '</strong>' : part)).join('');
  const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const buildReader = () => {
    const reader = $('reader');
    if (reader.dataset.built) return;
    reader.dataset.built = '1';
    const head = doc.createElement('header');
    head.className = 'rhead';
    head.innerHTML = '<span class="rtitle"></span><span id="rcount" aria-hidden="true"></span><button id="rview" aria-label="Show slides" title="Slides (V)">&#9635;</button>';
    head.querySelector('.rtitle').textContent = doc.title;
    reader.appendChild(head);
    head.querySelector('#rview').onclick = toggleView;
    slides.forEach((s, i) => {
      const stage = s.querySelector('.stage');
      const bg = stage.style.background;
      const card = doc.createElement('article');
      card.className = 'card';
      card.id = 'r-' + (i + 1);
      card.dataset.i = i;
      card.style.background = bg;
      card.setAttribute('aria-label', s.getAttribute('aria-label'));
      const norm = (x) => x.toLowerCase().replace(/\s+/g, ' ').trim();
      const els = [...stage.querySelectorAll('.t:not([data-chrome]), img')]
        .map((el) => ({ el, x: +el.dataset.x || 0, y: +el.dataset.y || 0, img: el.tagName === 'IMG', g: el.dataset.g || '' }));
      const texts = els.filter((e) => !e.img);
      const sizes = texts.map((e) => +e.el.dataset.s).sort((a, b) => a - b);
      const median = sizes.length ? sizes[Math.floor(sizes.length / 2)] : 16;
      const want = norm(s.dataset.title || '');
      let top = texts.find((e) => norm(e.el.dataset.text || '') === want);
      if (!top) top = texts.filter((e) => +e.el.dataset.s >= median * 1.3).sort((a, b) => a.y - b.y)[0] || texts[0] || null;
      // reading order: cards (groups) by position, each card's texts top to bottom; the title first
      const rowOf = (y) => Math.round(y / 38);
      const gpos = (g) => { const [gy, gx] = g.split(':').map(Number); return { y: gy, x: gx }; };
      const groups = new Map();
      els.forEach((e) => {
        const key = e.g || 'free:' + rowOf(e.y) + ':' + e.x;
        if (!groups.has(key)) groups.set(key, { key, y: e.g ? gpos(e.g).y : e.y, x: e.g ? gpos(e.g).x : e.x, members: [], card: !!e.g });
        groups.get(key).members.push(e);
      });
      const ordered = [...groups.values()].sort((a, b) => (rowOf(a.y) - rowOf(b.y)) || (a.x - b.x));
      if (top) { const gi = ordered.findIndex((g) => g.members.includes(top)); if (gi > 0) ordered.unshift(ordered.splice(gi, 1)[0]); }
      ordered.forEach((grp) => {
        grp.members.sort((a, b) => (a === top ? -1 : b === top ? 1 : 0) || (a.y - b.y) || (a.x - b.x));
        let host = card;
        if (grp.card) {
          host = doc.createElement('div');
          const fill = (grp.members.find((m) => m.el.dataset.gbg) || { el: { dataset: {} } }).el.dataset.gbg;
          host.className = fill ? 'grp fill' : 'grp line';
          if (fill) host.style.background = fill;
          card.appendChild(host);
          host.dataset.fill = fill || '';
        }
        grp.members.forEach(({ el, img }) => {
          if (img) {
            if (el.hasAttribute('data-full')) { card.style.backgroundImage = 'url("' + el.src + '")'; card.classList.add('pic'); return; }
            const fig = doc.createElement('figure');
            const im = doc.createElement('img');
            im.src = el.src; im.alt = el.alt || 'Figure'; im.loading = 'lazy';
            fig.appendChild(im); host.appendChild(fig);
            return;
          }
          const raw = el.dataset.text || '';
          const size = +el.dataset.s;
          const words = raw.split(/\s+/).length;
          const node = doc.createElement(top && el === top.el ? 'h2' : 'p');
          let kind = 'p';
          if (node.tagName === 'H2') kind = 'h';
          else if (size >= median * 1.45 && words <= 8) kind = 'big';
          else if (el.dataset.r === 'mono' && size <= 14) kind = 'lbl';
          node.className = 'r-' + kind;
          const link = el.querySelector('a');
          const html = strong(esc(raw)).replace(/\n/g, '<br>');
          if (link && !raw.includes('\n')) { const a = doc.createElement('a'); a.href = link.href; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.innerHTML = html; node.appendChild(a); }
          else node.innerHTML = html;
          node.style.color = el.style.color;
          node.style.fontFamily = el.style.fontFamily;
          if (el.dataset.bg && el.dataset.bg.toLowerCase() !== (host.dataset.fill || '').toLowerCase()) { node.classList.add('chip'); node.style.background = el.dataset.bg; }
          host.appendChild(node);
        });
      });
      const foot = doc.createElement('footer');
      foot.innerHTML = '<span>' + (i + 1) + ' / ' + n + '</span>';
      const note = (s.querySelector('.notes') || {}).textContent;
      if (note) { const d = doc.createElement('details'); d.innerHTML = '<summary>Speaker notes</summary><p></p>'; d.querySelector('p').textContent = note; foot.appendChild(d); }
      card.appendChild(foot);
      reader.appendChild(card);
    });
    // keep the current slide in step with what is on screen
    io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting && e.intersectionRatio >= 0.55) { fromScroll = true; go(+e.target.dataset.i, false, true); fromScroll = false; } });
    }, { threshold: [0.55, 0.8] });
    reader.querySelectorAll('.card').forEach((c) => io.observe(c));
  };
  const showCard = (i, instant) => {
    const c = $('r-' + (i + 1));
    if (c) c.scrollIntoView({ block: 'start', behavior: instant || reduced ? 'auto' : 'smooth' });
  };

  /* ---- timer, presenter ---------------------------------------------------------------------------------------------- */
  const fmt = (s) => { s = Math.max(0, Math.floor(s)); return String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0'); };
  const noteOf = (i) => (slides[i].querySelector('.notes') || {}).textContent || '';
  const timerText = () => {
    if (!started) return '00:00' + (planned ? ' / ' + fmt(planned) : '');
    const e = (Date.now() - started) / 1000;
    return fmt(e) + (planned ? ' / ' + fmt(planned) : '');
  };
  const startTimer = () => { if (started) return; started = Date.now(); tick = setInterval(renderTimers, 1000); };
  const resetTimer = () => { started = 0; clearInterval(tick); renderTimers(); };
  const renderTimers = () => {
    const t = timerText();
    const a = $('ntimer'); if (a) a.textContent = t;
    const b = $('ptimer');
    if (b) { b.textContent = t; b.classList.toggle('over', !!planned && started && (Date.now() - started) / 1000 > planned); }
  };
  const mountPresenter = () => {
    const cb = $('pcur'), nb = $('pnext');
    if (!cb) return;
    const put = (box, idx) => {
      box.innerHTML = '';
      if (idx < 0 || idx >= n) return;
      box.style.setProperty('--pk', box.clientWidth / W);
      box.appendChild(slides[idx].querySelector('.stage').cloneNode(true));
    };
    put(cb, cur);
    put(nb, cur + 1);
    $('pnotes').textContent = noteOf(cur);
    $('pcount').textContent = (cur + 1) + ' / ' + n;
  };

  /* ---- navigation ---------------------------------------------------------------------------------------------------- */
  const go = (i, remote, scrolled) => {
    i = Math.max(0, Math.min(n - 1, i));
    if (!remote && !scrolled && i !== cur) startTimer();
    slides[cur].classList.remove('active');
    slides[cur].removeAttribute('aria-current');
    cur = i;
    slides[cur].classList.add('active');
    slides[cur].setAttribute('aria-current', 'true');
    $('count').textContent = (cur + 1) + ' / ' + n;
    const rc = $('rcount'); if (rc) rc.textContent = (cur + 1) + ' / ' + n;
    $('progress').style.width = (n > 1 ? cur / (n - 1) * 100 : 100) + '%';
    $('live').textContent = slides[cur].getAttribute('aria-label');
    $('ntext').textContent = noteOf(cur) || '(no notes for this slide)';
    try { history.replaceState(null, '', location.search + '#' + (cur + 1)); } catch (e) { /* file:// in some browsers */ }
    if (presenter) mountPresenter();
    if (isReader() && !scrolled) showCard(cur);
    if (!remote && !scrolled) {
      if (chan) chan.postMessage({ i: cur });
      try { localStorage.setItem('deck-master:' + doc.title, JSON.stringify({ i: cur, t: Date.now() })); } catch (e) { /* storage blocked */ }
    }
  };
  const next = () => go(cur + 1), prev = () => go(cur - 1);
  const toggle = (cls, on) => { body.classList.toggle(cls, on); fit(); };
  const overview = (on) => {
    on = on === undefined ? !body.classList.contains('ov') : on;
    toggle('ov', on);
    if (on) slides[cur].scrollIntoView({ block: 'center' });
  };
  const fullscreen = () => {
    if (doc.fullscreenElement) doc.exitFullscreen();
    else if (root.requestFullscreen) root.requestFullscreen().catch(() => {});
  };
  const openPresenter = () => {
    const url = location.href.split('#')[0].split('?')[0] + '?presenter=1#' + (cur + 1);
    window.open(url, 'deck-presenter', 'width=1180,height=720');
  };

  doc.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    const k = e.key;
    if (k === 'v' || k === 'V') { toggleView(); return; }
    if (k === '?' || k === 'h' || k === 'H') { $('help').classList.toggle('open'); return; }
    if (k === 'Escape' && $('help').classList.contains('open')) { $('help').classList.remove('open'); return; }
    if (isReader()) {                                     // the page scrolls natively; j and k jump a slide
      if (k === 'j') { next(); e.preventDefault(); } else if (k === 'k') { prev(); e.preventDefault(); }
      return;
    }
    if (k === 'ArrowRight' || k === 'ArrowDown' || k === 'PageDown' || k === ' ' || k === 'Enter') { if (body.classList.contains('ov') && k === 'Enter') overview(false); else next(); e.preventDefault(); }
    else if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp' || k === 'Backspace') { prev(); e.preventDefault(); }
    else if (k === 'Home') { go(0); e.preventDefault(); }
    else if (k === 'End') { go(n - 1); e.preventDefault(); }
    else if (k === 'f' || k === 'F') fullscreen();
    else if (k === 'o' || k === 'O') overview();
    else if (k === 'Escape') { if (body.classList.contains('ov')) overview(false); }
    else if (k === 'n' || k === 'N') toggle('notes-open');
    else if (k === 'p' || k === 'P') openPresenter();
    else if (k === 'r' || k === 'R') resetTimer();
  });

  // pointer: click zones and swipe (slides view only)
  let down = null;
  $('deck').addEventListener('pointerdown', (e) => { down = { x: e.clientX, y: e.clientY }; });
  $('deck').addEventListener('pointerup', (e) => {
    if (!down) return;
    const dx = e.clientX - down.x, dy = e.clientY - down.y;
    down = null;
    if (e.target.closest('a')) return;
    if (body.classList.contains('ov')) {
      const s = e.target.closest('.slide');
      if (s) { go(slides.indexOf(s)); overview(false); }
      return;
    }
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) { dx < 0 ? next() : prev(); return; }
    if (Math.abs(dx) < 8 && Math.abs(dy) < 8) { e.clientX < innerWidth * 0.3 ? prev() : next(); }
  });

  $('b-prev').onclick = prev; $('b-next').onclick = next; $('b-ov').onclick = () => overview();
  $('b-notes').onclick = () => toggle('notes-open'); $('b-full').onclick = fullscreen; $('b-pres').onclick = openPresenter;
  $('b-view').onclick = toggleView;
  $('b-help').onclick = () => $('help').classList.toggle('open');
  $('help').onclick = () => $('help').classList.remove('open');
  if (!root.requestFullscreen) $('b-full').hidden = true;                    // iPhone Safari has no page fullscreen
  if (matchMedia('(pointer: coarse)').matches) $('b-pres').hidden = true;    // a second window makes no sense on a phone

  // hide the controls when the pointer rests
  const wake = () => { body.classList.remove('idle'); clearTimeout(idleT); idleT = setTimeout(() => { if (!body.classList.contains('ov')) body.classList.add('idle'); }, 2600); };
  doc.addEventListener('mousemove', wake); doc.addEventListener('touchstart', wake, { passive: true }); wake();

  if (chan) chan.onmessage = (m) => { if (m.data && typeof m.data.i === 'number') go(m.data.i, true); };
  addEventListener('storage', (e) => {
    if (e.key === 'deck-master:' + doc.title && e.newValue) { try { go(JSON.parse(e.newValue).i, true); } catch (x) { /* ignore */ } }
  });
  addEventListener('hashchange', () => { const v = parseInt(location.hash.slice(1), 10); if (v && v - 1 !== cur) go(v - 1, true); if (v && isReader()) showCard(v - 1); });
  addEventListener('resize', applyView);
  addEventListener('orientationchange', () => setTimeout(applyView, 200));

  if (presenter) {
    body.classList.add('presenter');
    $('pv').innerHTML = '<div class="left"><h2>Now</h2><div class="box" id="pcur"></div><div class="meta"><span id="pcount"></span><span class="timer" id="ptimer">00:00</span></div></div>' +
      '<div class="right"><div><h2>Next</h2><div class="box" id="pnext"></div></div><div style="display:flex;flex-direction:column;flex:1;min-height:0"><h2>Notes</h2><div class="pn" id="pnotes"></div></div>' +
      '<div><button id="pp">&larr; Previous</button><button id="pn">Next &rarr;</button><button id="pr">Reset timer</button></div></div>';
    $('pp').onclick = prev; $('pn').onclick = next; $('pr').onclick = resetTimer;
  }
  const h0 = parseInt(location.hash.slice(1), 10);
  go(h0 ? h0 - 1 : 0, true);
  applyView();
  renderTimers();
  body.classList.add('ready');
})();
