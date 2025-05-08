const tg = window.Telegram.WebApp;
tg.expand();

const userId = tg.initDataUnsafe.user.id;
const backendUrl = 'http://localhost:5000';

const balanceElement = document.getElementById('balance');
const levelElement = document.getElementById('level');
const clicksElement = document.getElementById('clicks');
const comboCountElement = document.getElementById('comboCount');
const coinElement = document.getElementById('coin');
const clickButton = document.getElementById('clickButton');
const boostTimerElement = document.getElementById('boostTimer');
const levelProgress = document.getElementById('levelProgress');
const coinSound = document.getElementById('coinSound');

// Area elements
const gameArea = document.getElementById('gameArea');
const statsArea = document.getElementById('statsArea');
const topPlayersArea = document.getElementById('topPlayersArea');
const bonusesArea = document.getElementById('bonusesArea');
const settingsArea = document.getElementById('settingsArea');
const withdrawArea = document.getElementById('withdrawArea');

// Stats area elements
const statsBalanceElement = document.getElementById('statsBalance');
const statsLevelElement = document.getElementById('statsLevel');
const nftElement = document.getElementById('nft');

// Top players area elements
const topPlayersList = document.getElementById('topPlayersList');

// Bonuses area elements
const dailyRewardButton = document.getElementById('dailyRewardButton');
const referralLinkElement = document.getElementById('referralLink');

// Settings area elements
const nicknameInput = document.getElementById('nickname');
const languageSelect = document.getElementById('language');
const saveSettingsButton = document.getElementById('saveSettingsButton');

// Buttons to navigate back
const backToGameFromStats = document.getElementById('backToGameFromStats');
const backToGameFromTopPlayers = document.getElementById('backToGameFromTopPlayers');
const backToGameFromBonuses = document.getElementById('backToGameFromBonuses');
const backToGameFromSettings = document.getElementById('backToGameFromSettings');
const backToGameFromWithdraw = document.getElementById('backToGameFromWithdraw');

// Navigation buttons
const statsButton = document.getElementById('statsButton');
const topPlayersButton = document.getElementById('topPlayersButton');
const bonusesButton = document.getElementById('bonusesButton');
const settingsButton = document.getElementById('settingsButton');

let balance = 0;
let level = 1;
let clicks = 0;
let comboCount = 0;
let levelProgressValue = 0;
let boostMultiplier = 1;
let boostTimerInterval;

// Function to play sound
function playCoinSound() {
    coinSound.currentTime = 0; // Reset sound to the beginning
    coinSound.play();
}

// Function to update boost timer display
function updateBoostTimer(duration) {
    boostTimerElement.textContent = `Буст: x${boostMultiplier} (${duration} сек)`;
    if (duration <= 0) {
        clearInterval(boostTimerInterval);
        boostTimerElement.textContent = "Буст: Нет";
        boostMultiplier = 1;
    }
}

// Function to start boost timer
function startBoostTimer(duration) {
    let timeLeft = duration;
    updateBoostTimer(timeLeft);
    boostTimerInterval = setInterval(() => {
        timeLeft--;
        updateBoostTimer(timeLeft);
        if (timeLeft <= 0) {
            clearInterval(boostTimerInterval);
        }
    }, 1000);
}

async function getUserData() {
    try {
        const response = await fetch(`${backendUrl}/api/user/${userId}`);
        const data = await response.json();
        balance = data.balance;
        level = data.level;
        clicks = data.clicks;

        balanceElement.textContent = balance;
        levelElement.textContent = level;
        clicksElement.textContent = clicks;
        levelProgressValue = clicks % 100;
        levelProgress.value = levelProgressValue;

        statsBalanceElement.textContent = balance;
        statsLevelElement.textContent = level;

    } catch (error) {
        console.error('Ошибка при получении данных пользователя:', error);
    }
}

async function handleClick() {
    try {
        const response = await fetch(`${backendUrl}/api/click/${userId}`, {
            method: 'POST',
        });
        const data = await response.json();
        balance = data.balance;
        clicks = data.clicks;
        reward = data.reward;
        level = data.level;

        balanceElement.textContent = balance;
        clicksElement.textContent = clicks;
        levelElement.textContent = level;
        statsBalanceElement.textContent = balance;
        statsLevelElement.textContent = level;

        playCoinSound();

        // Check if combo
        comboCount++;
        comboCountElement.textContent = comboCount;
        if (comboCount % 10 === 0) {
            reward += 5; // Combo bonus
        }

        levelProgressValue = clicks % 100;
        levelProgress.value = levelProgressValue;


        coinElement.classList.add('clicked');
        setTimeout(() => {
            coinElement.classList.remove('clicked');
        }, 100);

        const boostRoll = Math.random();

    } catch (error) {
        console.error('Ошибка при клике:', error);
    }
}

async function getTopPlayers() {
    try {
        const response = await fetch(`${backendUrl}/api/top-players`);
        const data = await response.json();
        topPlayersList.innerHTML = '';
        data.forEach((player, index) => {
            const listItem = document.createElement('li');
            listItem.textContent = `${index + 1}. ${player.username} - ${player.balance} SCREAM`;
            topPlayersList.appendChild(listItem);
        });
    } catch (error) {
        console.error('Ошибка при получении топ игроков:', error);
    }
}

// Function to generate referral link
function generateReferralLink() {
    const referralCode = localStorage.getItem('referralCode') || generateRandomCode();
    localStorage.setItem('referralCode', referralCode);
    referralLinkElement.textContent = `Реферальная ссылка: t.me/${tg.WebApp.botName}?start=${referralCode}`;
}

// Function to generate random code
function generateRandomCode() {
    return Math.random().toString(36).substring(2, 15);
}

// Hide all areas except the one to show
function showArea(areaId) {
    gameArea.style.display = (areaId === 'gameArea') ? 'flex' : 'none';
    statsArea.style.display = (areaId === 'statsArea') ? 'block' : 'none';
    topPlayersArea.style.display = (areaId === 'topPlayersArea') ? 'block' : 'none';
    bonusesArea.style.display = (areaId === 'bonusesArea') ? 'block' : 'none';
    settingsArea.style.display = (areaId === 'settingsArea') ? 'block' : 'none';
    withdrawArea.style.display = (areaId === 'withdrawArea') ? 'block' : 'none';
}

// Event listeners for navigation buttons
statsButton.addEventListener('click', () => {
    showArea('statsArea');
});

topPlayersButton.addEventListener('click', () => {
    getTopPlayers();
    showArea('topPlayersArea');
});

bonusesButton.addEventListener('click', () => {
    generateReferralLink();
    showArea('bonusesArea');
});

settingsButton.addEventListener('click', () => {
    showArea('settingsArea');
});

// Event listeners for back buttons
backToGameFromStats.addEventListener('click', () => {
    showArea('gameArea');
});

backToGameFromTopPlayers.addEventListener('click', () => {
    showArea('gameArea');
});

backToGameFromBonuses.addEventListener('click', () => {
    showArea('gameArea');
});

backToGameFromSettings.addEventListener('click', () => {
    showArea('gameArea');
});

backToGameFromWithdraw.addEventListener('click', () => {
    showArea('gameArea');
});

// Daily Reward
dailyRewardButton.addEventListener('click', async () => {
    try {
        const response = await fetch(`${backendUrl}/api/daily-reward/${userId}`, {
            method: 'POST',
        });
        const data = await response.json();
        balance = data.balance;
        balanceElement.textContent = balance;
        statsBalanceElement.textContent = balance;
        alert('Ежедневная награда получена!');
    } catch (error) {
        console.error('Ошибка при получении ежедневной награды:', error);
    }
});

// Settings save
saveSettingsButton.addEventListener('click', async () => {
    const nickname = nicknameInput.value;
    const language = languageSelect.value;

    try {
        const response = await fetch(`${backendUrl}/api/settings/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nickname: nickname,
                language: language
            })
        });
        const data = await response.json();
        alert('Настройки сохранены!');
    } catch (error) {
        console.error('Ошибка при сохранении настроек:', error);
    }
});

coinElement.addEventListener('click', handleClick);

getUserData();
