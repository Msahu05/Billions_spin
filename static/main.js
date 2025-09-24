document.addEventListener('DOMContentLoaded', () => {
  const wheel = document.getElementById('wheel');
  const spinBtn = document.getElementById('spinBtn');
  const overlay = document.getElementById('overlay');
  const popupVideo = document.getElementById('popupVideo');
  const popupTitle = document.getElementById('popupTitle');
  const popupDesc = document.getElementById('popupDesc');

  let items = [];
  let currentRotation = 0; // degrees
  let spinning = false;

  // load your data.json (keeps your internal paths like "media/images/img1.png")
  fetch('/static/data.json')
    .then(r => r.json())
    .then(json => {
      items = json;
      buildWheel();
      window.addEventListener('resize', rebuildOnResize);
    })
    .catch(err => {
      console.error('Failed to load data.json', err);
      wheel.innerHTML = '<div style="padding:20px">Failed to load data.json</div>';
      spinBtn.disabled = true;
    });

  function rebuildOnResize() {
    // small debounce
    clearTimeout(window._wheelResizeTimer);
    window._wheelResizeTimer = setTimeout(buildWheel, 120);
  }

  function buildWheel() {
    wheel.innerHTML = '';
    if (!items || !items.length) return;

    const N = items.length;
    const angleStep = 360 / N;

    // compute radius and image size dynamically to avoid overlap
    const rect = wheel.getBoundingClientRect();
    const wheelRadius = Math.min(rect.width, rect.height) / 2;
    // leave some padding so images don't touch border
    const padding = Math.max(40, Math.round(wheelRadius * 0.12));
    const radius = Math.max( (wheelRadius - padding), 60 );

    // angular arc length approx (r * angle)
    const angleRad = (2 * Math.PI) / N;
    const arcLen = radius * angleRad;
    // image size should be somewhat less than arc length
    let imgSize = Math.floor(Math.min(110, Math.max(36, arcLen * 0.85)));
    // safety cap for small N
    if (N <= 8) imgSize = Math.min(imgSize, 110);

    items.forEach((it, i) => {
      const slice = document.createElement('div');
      slice.className = 'slice';
      slice.style.width = `${imgSize}px`;
      slice.style.height = `${imgSize}px`;
      // position center and push out by radius (rotate, then translate up)
      const angle = i * angleStep;
      slice.style.transform = `rotate(${angle}deg) translateY(-${radius}px)`;
      slice.style.top = '50%';
      slice.style.left = '50%';

      const img = document.createElement('img');
      // if user already wrote absolute path with leading /, keep it; else prepend /static/
      img.src = (it.image && it.image.startsWith('/')) ? it.image : `/static/${it.image}`;
      img.alt = it.title || `item-${i}`;
      // keep image upright by counter-rotating it
      img.style.transform = `rotate(${-angle}deg)`;

      // click on image: quick spin to that index (optional)
      img.addEventListener('click', (e) => {
        e.stopPropagation();
        if (!spinning) spinToIndex(i);
      });

      slice.appendChild(img);
      wheel.appendChild(slice);
    });
  }

  // Easing
  function easeOutCubic(t){ return 1 - Math.pow(1 - t, 3); }

  function spinToIndex(targetIndex) {
    if (spinning || !items.length) return;
    spinning = true;
    spinBtn.disabled = true;

    const N = items.length;
    const angleStep = 360 / N;

    // ensure final rotation is greater than currentRotation
    const extraSpins = 4 + Math.floor(Math.random() * 3); // 4..6 full spins
    let baseSpins = Math.floor(currentRotation / 360);
    let finalRotation = (baseSpins + extraSpins) * 360 - targetIndex * angleStep;

    if (finalRotation <= currentRotation) {
      finalRotation += 360; // ensure forward
    }

    // animate from currentRotation -> finalRotation with requestAnimationFrame
    const duration = 3800 + Math.floor(Math.random() * 900); // ms
    const start = performance.now();
    const startRotation = currentRotation;
    function frame(now) {
      const elapsed = now - start;
      const t = Math.min(1, elapsed / duration);
      const eased = easeOutCubic(t);
      const rot = startRotation + (finalRotation - startRotation) * eased;
      wheel.style.transform = `rotate(${rot}deg)`;

      if (t < 1) {
        requestAnimationFrame(frame);
      } else {
        // finish exactly
        currentRotation = finalRotation;
        wheel.style.transform = `rotate(${currentRotation}deg)`;

        // small delay to let user see final pose
        setTimeout(() => {
          spinning = false;
          spinBtn.disabled = false;
          showPopup(items[targetIndex]);
        }, 220);
      }
    }
    requestAnimationFrame(frame);
  }

  spinBtn.addEventListener('click', () => {
    if (!items.length || spinning) return;
    const target = Math.floor(Math.random() * items.length);
    spinToIndex(target);
  });

  function showPopup(item) {
    popupVideo.src = (item.video && item.video.startsWith('/')) ? item.video : `/static/${item.video || ''}`;
    popupTitle.textContent = item.title || '';
    popupDesc.textContent = item.description || '';
    overlay.classList.remove('hidden');
    // autoplay (muted) is optional, usually browsers restrict autoplay with sound
    // popupVideo.play().catch(()=>{/* ignore */});
  }

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      overlay.classList.add('hidden');
      try { popupVideo.pause(); popupVideo.currentTime = 0; } catch(e){/*ignore*/ }
    }
  });
});
