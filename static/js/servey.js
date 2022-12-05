// 질문 1
let dropdown1 = document.querySelector('.dropdown1')
let option1 = document.querySelector('.option1')
dropdown1.onclick = function () {
    dropdown1.classList.toggle('active');
}
function show1(a) {
    document.querySelector('.text01').value = a;

}
option1.addEventListener('click', function () {
    const text1 = document.querySelector('.text01').value
    if (text1) {
        const check1 = document.querySelector('.check1');
        check1.className = ' val';
    }
})

// 질문 2
let dropdown2 = document.querySelector('.dropdown2')
let option2 = document.querySelector('.option2')

dropdown2.onclick = function () {
    dropdown2.classList.toggle('active');
}
function show2(a) {
    document.querySelector('.text02').value = a;
}
option2.addEventListener('click', function () {
    const text2 = document.querySelector('.text02').value
    if (text2) {
        const check2 = document.querySelector('.check2');
        check2.className = ' val';
    }
})
// 질문 3
let dropdown3 = document.querySelector('.dropdown3')
let option3 = document.querySelector('.option3')

dropdown3.onclick = function () {
    dropdown3.classList.toggle('active');
}
function show3(a) {
    document.querySelector('.text03').value = a;
}
option3.addEventListener('click', function () {
    const text3 = document.querySelector('.text03').value
    if (text3) {
        const check3 = document.querySelector('.check3');
        check3.className = ' val';
    }
})
// 질문 4
let dropdown4 = document.querySelector('.dropdown4')
let option4 = document.querySelector('.option4')

dropdown4.onclick = function () {
    dropdown4.classList.toggle('active');
}
function show4(a) {
    document.querySelector('.text04').value = a;
}
option4.addEventListener('click', function () {
    const text4 = document.querySelector('.text04').value
    if (text4) {
        const check4 = document.querySelector('.check4');
        check4.className = ' val';
    }
})
// 질문 5
let dropdown5 = document.querySelector('.dropdown5')
let option5 = document.querySelector('.option5')

dropdown5.onclick = function () {
    dropdown5.classList.toggle('active');
}
function show5(a) {
    document.querySelector('.text05').value = a;
}
option5.addEventListener('click', function () {
    const text5 = document.querySelector('.text05').value
    if (text5) {
        const check5 = document.querySelector('.check5');
        check5.className = ' val';
    }
})
// 질문 6
// 질문 7
// 질문 8
// 질문 9
// 질문 10
// 질문 11