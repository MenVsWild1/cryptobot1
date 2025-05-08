const coin = document.getElementById('coin');
const clickCounter = document.getElementById('click-counter');
const levelProgress = document.getElementById('level-progress');
const boostTimer = document.getElementById('boost-timer');

let clicks = 0;
let level = 1;
const clicksPerLevel = 100;

coin.addEventListener('click', () => {
    clicks++;
    clickCounter.textContent = `Кликов: ${clicks}`;
    // Анимация взрыва (пока простая смена класса)
    coin.classList.add('explode');
    setTimeout(() => {
        coin.classList.remove('explode');
    }, 100);

    // Проверка на повышение уровня
    if (clicks >= level * clicksPerLevel) {
        level++;
        levelProgress.textContent = `Уровень: ${level} (${clicks}/${level * clicksPerLevel})`;
        // Здесь можно добавить логику получения NFT, бустов и т.д.
        console.log(`Новый уровень: ${level}!`);
    }
});

// Пример анимации взрыва (добавьте этот стиль в style.css)
/*
.coin.explode {
    transform: scale(1.1);
    opacity: 0.8;
}
*/