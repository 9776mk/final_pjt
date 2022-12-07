'use strict';
let progressWap = document.querySelectorAll('.progress_wap');
progressWap.forEach(item => {
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


var btt = document.getElementById('back-to-top'),
    docElem = document.documentElement,
    offset,
    scrollPos,
    docHeight;

docHeight = Math.max(docElem.offsetHeight, docElem.scrollHeight); //둘중에 높은 값을 가져온다.
// console.log(docHeight);

scrollPos = docElem.scrollTop // 스크롤 양을 알 수 있음...

if (docHeight != '') {
    offset = docHeight / 4;
}
// 스크롤 이벤트 추가
window.addEventListener('scroll', function () { // 스크롤 양을 실시간으로 보여줌...
    scrollPos = docElem.scrollTop;

    btt.className = (scrollPos > offset) ? 'visible' : '';

});
btt.addEventListener('click', function (e) {
    e.preventDefault() // 링크의 본연의 기능을 막는다.
    docElem.scrollTop = 0
})

//algo

const ti = document.querySelectorAll('.ch')
// console.log(ti)
ti.forEach(form => {
    form.addEventListener('click', e => {
        var targetTi = e.target.value

        axios({
            method: 'get',
            url: '',
            params: { 'targetTi': targetTi }
        })
            .then(response => {
                // console.log(response.data.num)
                // console.log(response.data.title)
                // console.log(response.data.tags)
                const D = document.getElementById('ddd')
                if (D) {
                    D.remove()
                }
                const recom = document.querySelector('.recom')
                const tags = response.data.tags
                if (response.data.tags == '[]') {
                    tags = '없음'
                }
                recom.insertAdjacentHTML('beforeend', `
                <div id='ddd'>
                <a  href="https://www.acmicpc.net/problem/${response.data.num}" target="_blank">
                <span>제목: ${response.data.title}</span>
                </a>
                <p style="margin-bottom:0; margin-top:20px;"> 문제 유형</p>
                <p>${tags}</p>
                </div>
                `)
            })
    })
})


