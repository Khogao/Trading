const hourTens = document.querySelector('[data-hour-tens]');
const hourOnes = document.querySelector('[data-hour-ones]');
const minuteTens = document.querySelector('[data-minute-tens]');
const minuteOnes = document.querySelector('[data-minute-ones]');
const secondTens = document.querySelector('[data-second-tens]');
const secondOnes = document.querySelector('[data-second-ones]');

let lastTime = null;

function updateClock() {
    const now = new Date();
    const seconds = now.getSeconds().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const hours = now.getHours().toString().padStart(2, '0');

    const currentTime = `${hours}${minutes}${seconds}`;
    if (lastTime === currentTime) {
        requestAnimationFrame(updateClock);
        return;
    }

    flip(secondOnes, seconds[1]);
    flip(secondTens, seconds[0]);
    flip(minuteOnes, minutes[1]);
    flip(minuteTens, minutes[0]);
    flip(hourOnes, hours[1]);
    flip(hourTens, hours[0]);

    lastTime = currentTime;

    requestAnimationFrame(updateClock);
}

function flip(flipCard, newNumber) {
    const topHalf = flipCard.querySelector('.top');
    const bottomHalf = flipCard.querySelector('.bottom');
    const startNumber = topHalf.textContent;

    if (newNumber === startNumber) return;

    const topFlip = document.createElement('div');
    topFlip.classList.add('top-flip');
    const bottomFlip = document.createElement('div');
    bottomFlip.classList.add('bottom-flip');

    topHalf.textContent = newNumber;
    bottomHalf.textContent = newNumber;
    topFlip.textContent = startNumber;
    bottomFlip.textContent = newNumber;

    topFlip.addEventListener('animationstart', e => {
        topHalf.textContent = newNumber;
    });
    topFlip.addEventListener('animationend', e => {
        topFlip.remove();
    });
    bottomFlip.addEventListener('animationend', e => {
        bottomHalf.textContent = newNumber;
        bottomFlip.remove();
    });

    flipCard.append(topFlip, bottomFlip);
    
    // A more robust way to handle the flip animation
    const currentTop = flipCard.querySelector('.top');
    const currentBottom = flipCard.querySelector('.bottom');
    const nextNumber = newNumber;
    const currentNumber = startNumber;

    if (currentNumber !== nextNumber) {
        currentTop.setAttribute('data-before', currentNumber);
        currentBottom.setAttribute('data-after', nextNumber);
        flipCard.classList.add('flip');

        flipCard.addEventListener('animationend', () => {
            currentTop.setAttribute('data-before', nextNumber);
            currentBottom.setAttribute('data-after', nextNumber);
            currentTop.textContent = nextNumber;
            currentBottom.textContent = nextNumber;
            flipCard.classList.remove('flip');
        }, { once: true });
    }
}

requestAnimationFrame(updateClock);
