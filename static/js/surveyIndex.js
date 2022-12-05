'use strict';
let sStatus = document.querySelectorAll('.sStatus');
sStatus.forEach(item => {
    // console.log(item)
    SnumAnimation(item);
});
function SnumAnimation(item) {
    let initialRate = 0;
    let bar_frame = item.querySelector('.bar_frame');
    let targetRate = item.getAttribute('data-num');
    let progressBar = item.querySelector('.bar');
    let progressRate = item.querySelector('span');
    startNumberAnimation()
    function startNumberAnimation() {
        let numAni = setInterval(() => {
            if (targetRate != 0) {

                initialRate++;
                if (initialRate == targetRate) {
                    // 멈추는 조건
                    clearInterval(numAni)
                }
                bar_frame.style.width = `${initialRate}%`;
                progressBar.style.width = `${initialRate}%`;
                progressRate.innerText = `${initialRate}%`;
            }
        }, 20);
    }
}

// dData
let dStatus1 = document.querySelectorAll('.dStatus');
dStatus1.forEach(item => {
    // console.log(item)
    numAnimation(item);
});
function numAnimation(item) {
    let initialRate = 0;
    let bar_frame = item.querySelector('.bar_frame');
    let targetRate = item.getAttribute('data-num');
    let progressBar = item.querySelector('.bar');
    let progressRate = item.querySelector('span');
    let triggerPoint = item.offsetTop - 600;
    let excuted = false;
    window.addEventListener('scroll', function () {
        let scrollAmt = this.scrollY;
        // console.log(initialRate, targetRate)
        //console.log(triggerPoint, scrollAmt)

        if (scrollAmt > triggerPoint) {
            if (!excuted) {
                startNumberAnimation();
                excuted = true;
            }
        }
    })
    function startNumberAnimation() {
        let numAni = setInterval(() => {
            if (targetRate != 0) {

                initialRate++;
                if (initialRate == targetRate) {
                    // 멈추는 조건
                    clearInterval(numAni)
                }
                bar_frame.style.width = `${initialRate}%`;
                progressBar.style.width = `${initialRate}%`;
                progressRate.innerText = `${initialRate}%`;
            }
        }, 20);
    }
}

// enddata


// dData
let eStatus = document.querySelectorAll('.eStatus');
eStatus.forEach(item => {
    // console.log(item)
    numAnimation(item);
});
function numAnimation(item) {
    let initialRate = 0;
    let bar_frame = item.querySelector('.bar_frame');
    let targetRate = item.getAttribute('data-num');
    let progressBar = item.querySelector('.bar');
    let progressRate = item.querySelector('span');
    let triggerPoint = item.offsetTop - 800;
    let excuted = false;
    window.addEventListener('scroll', function () {
        let scrollAmt = this.scrollY;
        // console.log(initialRate, targetRate)
        console.log(triggerPoint, scrollAmt)

        if (scrollAmt > triggerPoint) {
            if (!excuted) {
                startNumberAnimation();
                excuted = true;
            }
        }
    })
    function startNumberAnimation() {
        let numAni = setInterval(() => {
            if (targetRate != 0) {

                initialRate++;
                if (initialRate == targetRate) {
                    // 멈추는 조건
                    clearInterval(numAni)
                }
                bar_frame.style.width = `${initialRate}%`;
                progressBar.style.width = `${initialRate}%`;
                progressRate.innerText = `${initialRate}%`;
            }
        }, 20);
    }
}
