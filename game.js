class MeatClicker {
    constructor() {
        this.meat = 0;
        this.prestigePoints = 0;
        this.clickPower = 1;
        this.autoClickerRate = 0;
        this.prestigeMultiplier = 1;
        this.lastUpdate = Date.now();
        
        this.upgrades = [
            { id: 'couteau', name: 'Couteau Tranchant', baseCost: 10, count: 0, production: 0.1, costMultiplier: 1.15 },
            { id: 'boucher', name: 'Boucher Expert', baseCost: 50, count: 0, production: 0.5, costMultiplier: 1.15 },
            { id: 'abattoir', name: 'Mini Abattoir', baseCost: 250, count: 0, production: 2, costMultiplier: 1.15 },
            { id: 'ferme', name: 'Ferme d\'Élevage', baseCost: 1000, count: 0, production: 10, costMultiplier: 1.15 },
            { id: 'usine', name: 'Usine de Transformation', baseCost: 5000, count: 0, production: 50, costMultiplier: 1.15 },
            { id: 'corporation', name: 'Corporation Carnée', baseCost: 25000, count: 0, production: 250, costMultiplier: 1.15 },
            { id: 'labo', name: 'Laboratoire de Viande', baseCost: 100000, count: 0, production: 1000, costMultiplier: 1.15 },
            { id: 'dimension', name: 'Dimension Carnivore', baseCost: 500000, count: 0, production: 5000, costMultiplier: 1.15 }
        ];

        this.prestigeUpgrades = [
            { id: 'clickBoost', name: 'Lame Affûtée', cost: 1, purchased: false, effect: () => this.clickPower *= 2 },
            { id: 'productionBoost', name: 'Efficacité Maximale', cost: 2, purchased: false, effect: () => this.prestigeMultiplier *= 1.5 },
            { id: 'autoClickBoost', name: 'Automation Avancée', cost: 3, purchased: false, effect: () => this.autoClickerRate += 1 },
            { id: 'megaBoost', name: 'Viande Quantique', cost: 5, purchased: false, effect: () => { this.clickPower *= 3; this.prestigeMultiplier *= 2; } }
        ];

        this.setupEventListeners();
        this.loadGame();
        this.startGameLoop();
    }

    setupEventListeners() {
        document.getElementById('meatClicker').addEventListener('click', () => this.clickMeat());
        document.getElementById('prestigeButton').addEventListener('click', () => this.prestige());
        this.renderUpgrades();
        this.updateDisplay();
    }

    clickMeat() {
        const gain = this.clickPower * this.prestigeMultiplier;
        this.meat += gain;
        this.createFloatingNumber(gain);
        this.updateDisplay();
    }

    createFloatingNumber(number) {
        const clicker = document.getElementById('meatClicker');
        const popup = document.createElement('div');
        popup.className = 'number-popup';
        popup.textContent = `+${number.toFixed(1)}`;
        
        const rect = clicker.getBoundingClientRect();
        popup.style.left = `${rect.left + Math.random() * rect.width}px`;
        popup.style.top = `${rect.top + Math.random() * rect.height}px`;
        
        document.body.appendChild(popup);
        setTimeout(() => popup.remove(), 1000);
    }

    buyUpgrade(upgradeId) {
        const upgrade = this.upgrades.find(u => u.id === upgradeId);
        if (!upgrade) return;

        const cost = this.calculateUpgradeCost(upgrade);
        if (this.meat >= cost) {
            this.meat -= cost;
            upgrade.count++;
            this.updateDisplay();
            this.renderUpgrades();
        }
    }

    calculateUpgradeCost(upgrade) {
        return Math.floor(upgrade.baseCost * Math.pow(upgrade.costMultiplier, upgrade.count));
    }

    buyPrestigeUpgrade(upgradeId) {
        const upgrade = this.prestigeUpgrades.find(u => u.id === upgradeId);
        if (!upgrade || upgrade.purchased || this.prestigePoints < upgrade.cost) return;

        this.prestigePoints -= upgrade.cost;
        upgrade.purchased = true;
        upgrade.effect();
        this.updateDisplay();
        this.renderUpgrades();
    }

    prestige() {
        if (this.meat < 1000000) return;
        
        const prestigePointsGained = Math.floor(Math.log10(this.meat) - 5);
        this.prestigePoints += prestigePointsGained;
        
        // Reset game but keep prestige upgrades
        this.meat = 0;
        this.upgrades.forEach(upgrade => upgrade.count = 0);
        
        this.updateDisplay();
        this.renderUpgrades();
        this.saveGame();
    }

    calculateMeatPerSecond() {
        return this.upgrades.reduce((total, upgrade) => {
            return total + (upgrade.production * upgrade.count * this.prestigeMultiplier);
        }, this.autoClickerRate * this.clickPower * this.prestigeMultiplier);
    }

    renderUpgrades() {
        const upgradesList = document.getElementById('upgradesList');
        upgradesList.innerHTML = '';

        // Regular upgrades
        this.upgrades.forEach(upgrade => {
            const cost = this.calculateUpgradeCost(upgrade);
            const element = document.createElement('div');
            element.className = `upgrade-item ${this.meat >= cost ? '' : 'disabled'}`;
            element.innerHTML = `
                <h3>${upgrade.name}</h3>
                <p>Coût: ${cost.toFixed(0)} kg</p>
                <p>Production: ${(upgrade.production * this.prestigeMultiplier).toFixed(1)} kg/s</p>
                <p>Possédés: ${upgrade.count}</p>
            `;
            element.onclick = () => this.buyUpgrade(upgrade.id);
            upgradesList.appendChild(element);
        });

        // Prestige upgrades
        this.prestigeUpgrades.forEach(upgrade => {
            if (!upgrade.purchased) {
                const element = document.createElement('div');
                element.className = `upgrade-item ${this.prestigePoints >= upgrade.cost ? '' : 'disabled'}`;
                element.innerHTML = `
                    <h3>${upgrade.name} (Prestige)</h3>
                    <p>Coût: ${upgrade.cost} points de prestige</p>
                `;
                element.onclick = () => this.buyPrestigeUpgrade(upgrade.id);
                upgradesList.appendChild(element);
            }
        });
    }

    updateDisplay() {
        document.getElementById('meatCount').textContent = Math.floor(this.meat).toLocaleString();
        document.getElementById('meatPerSecond').textContent = this.calculateMeatPerSecond().toFixed(1);
        document.getElementById('prestigePoints').textContent = this.prestigePoints;
        
        const prestigeButton = document.getElementById('prestigeButton');
        prestigeButton.disabled = this.meat < 1000000;
        prestigeButton.textContent = `Prestige (Nécessite 1M de viande) - Gain: ${Math.max(0, Math.floor(Math.log10(this.meat) - 5))} points`;
    }

    startGameLoop() {
        setInterval(() => {
            const now = Date.now();
            const delta = (now - this.lastUpdate) / 1000;
            this.lastUpdate = now;

            this.meat += this.calculateMeatPerSecond() * delta;
            this.updateDisplay();
        }, 50);

        // Sauvegarde automatique toutes les 30 secondes
        setInterval(() => this.saveGame(), 30000);
    }

    saveGame() {
        const saveData = {
            meat: this.meat,
            prestigePoints: this.prestigePoints,
            clickPower: this.clickPower,
            autoClickerRate: this.autoClickerRate,
            prestigeMultiplier: this.prestigeMultiplier,
            upgrades: this.upgrades,
            prestigeUpgrades: this.prestigeUpgrades
        };
        localStorage.setItem('meatClickerSave', JSON.stringify(saveData));
    }

    loadGame() {
        const savedGame = localStorage.getItem('meatClickerSave');
        if (savedGame) {
            const saveData = JSON.parse(savedGame);
            Object.assign(this, saveData);
        }
    }
}

// Démarrer le jeu
window.onload = () => new MeatClicker(); 