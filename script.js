const CACHE_KEY = 'productImageCache';
const CACHE_TIME_KEY = 'productImageCacheTime';
const CACHE_LIFETIME = 3 * 60 * 60 * 1000; // 3 часа в мс

let allCards = [];      // данные из wb_cards_all.json (с фото, брендом и т.п.)
let allPrices = {};     // объект с nmID -> данные с ценами
let imageCache = {};

function saveCacheToStorage() {
  localStorage.setItem(CACHE_KEY, JSON.stringify(imageCache));
  localStorage.setItem(CACHE_TIME_KEY, Date.now().toString());
}

function loadCacheFromStorage() {
  const cachedTime = parseInt(localStorage.getItem(CACHE_TIME_KEY));
  if (!cachedTime || Date.now() - cachedTime > CACHE_LIFETIME) {
    localStorage.removeItem(CACHE_KEY);
    localStorage.removeItem(CACHE_TIME_KEY);
    imageCache = {};
    return;
  }
  const cachedData = localStorage.getItem(CACHE_KEY);
  if (cachedData) {
    imageCache = JSON.parse(cachedData);
  }
}

async function loadProducts() {
  loadCacheFromStorage();

  // Загружаем карточки товаров
  const cardsResponse = await fetch('wb_cards_all.json');
  allCards = await cardsResponse.json();

  // Загружаем цены
  const pricesResponse = await fetch('wildberries_all_products.json');
  const pricesArray = await pricesResponse.json();

  // Преобразуем массив с ценами в объект для быстрого доступа
  allPrices = {};
  for (const p of pricesArray) {
    allPrices[p.nmID] = p;
  }

  // Фильтруем карточки по бренду CuteShop
  const filteredCards = allCards.filter(c => c.brand === 'CuteShop');

  await renderProducts(filteredCards);

  document.getElementById('loader').classList.add('hidden');

  setTimeout(() => {
    document.getElementById('catalog').classList.remove('hidden-opacity');
    document.getElementById('catalog').classList.add('visible-opacity');

    setTimeout(() => {
      document.getElementById('search-css').classList.remove('hidden-opacity');
      document.getElementById('search-css').classList.add('visible-opacity');

      setTimeout(() => {
        document.getElementById('product-list').classList.remove('hidden-opacity');
        document.getElementById('product-list').classList.add('visible-opacity');
      }, 1000);
    }, 1500);
  }, 2000);
}

async function renderProducts(productArray) {
  const container = document.getElementById('product-list');
  container.innerHTML = '';

  const filteredProducts = productArray.filter(product => {
    const vc = product.vendorCode || '';
    if (vc.startsWith('RIR')) return false;
    if (/^\d/.test(vc)) return false;
    return true;
  });

  const cardsData = filteredProducts.map(product => {
    const nmID = product.nmID;
    const imageUrl = product.photos && product.photos.length > 0 ? product.photos[0].big : 'https://via.placeholder.com/300x200?text=Нет+фото';

    const priceData = allPrices[nmID] || {};
    const sizes = priceData.sizes || [];
    const price = sizes.length > 0 ? sizes[0].price : '—';
    const discountedPrice = sizes.length > 0 ? sizes[0].discountedPrice : '—';

    return { product, imageUrl, price, discountedPrice };
  });

  for (const { product, imageUrl, price, discountedPrice } of cardsData) {
    const vendorCode = product.vendorCode || product.nmID || 'Без артикула';
    const name = product.title || vendorCode;

    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <img src="${imageUrl}" alt="${name}">
      <h2>${name}</h2>
      <p>Цена: ${price} ₽<br>
         <strong style="color:red">Цена со скидкой: ${discountedPrice} ₽</strong></p>
      <button class="buy-button" data-nmid="${product.nmID}">Купить</button>
    `;
    container.appendChild(card);
  }

  container.querySelectorAll('.buy-button').forEach(button => {
    button.addEventListener('click', (e) => {
      const nmID = e.target.dataset.nmid;
      if (nmID) {
        window.open(`https://www.wildberries.ru/catalog/${nmID}/detail.aspx`, '_blank');
      }
    });
  });
}

function search() {
  const query = document.getElementById('site-search').value.trim().toLowerCase();

  const filtered = allCards.filter(product =>
    (product.title || product.vendorCode || '').toLowerCase().includes(query)
    && product.brand === 'CuteShop'
  );
  renderProducts(filtered);
}

// Изначально скрываем элементы UI
document.getElementById('catalog').classList.add('hidden-opacity');
document.getElementById('search-css').classList.add('hidden-opacity');
document.getElementById('product-list').classList.add('hidden-opacity');

loadProducts();
