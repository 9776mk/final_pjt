let langCategoryDict = {}
const lang_btns = document.querySelectorAll('input[name=language-btns]')
const allUsers = document.querySelectorAll('.all-users')

lang_btns.forEach(btn => {
    btn.addEventListener('click', event => {
        if (btn.checked) {
            langCategoryDict[btn.attributes.id.value] = 1
        } else {
            delete langCategoryDict[btn.attributes.id.value]
        }

        langCategoryArr = Object.keys(langCategoryDict)
        mbtiCategoryArr = Object.keys(mbtiCategoryDict)
        console.log(langCategoryArr)
        console.log(mbtiCategoryArr)

        for (let i = 0; i < allUsers.length; i++) {
            allUsers[i].classList.add('d-none')
            allUsers[i].classList.remove('d-block')
        }
        
        // 선택된 언어가 있을 때
        if (langCategoryArr.length >= 1) {
            for (let i = 0; i < allUsers.length; i++) {
                for (let j = 0; j < langCategoryArr.length; j++ ) {
                    if (allUsers[i].classList.contains(langCategoryArr[j])) {
                        allUsers[i].classList.add('d-block')
                        allUsers[i].classList.remove('d-none')
                    }
                    // 선택된 MBTI가 있을 때
                    // if (mbtiCategoryArr.length === 0) {
                        
                    // }

                    // else {
                        
                    // }
                }
            }
        }
        // 선택된 언어가 없을 때 → 빈 화면 or MBTI 검색
        else {
            for (let i = 0; i < allUsers.length; i++) {
                allUsers[i].classList.add('d-none')
                allUsers[i].classList.remove('d-block')
            }
        }

        if (Object.keys(mbtiCategoryDict).length >= 1) {
            console.log(';sjdflaksj')
        }
    })
})


let mbtiCategoryDict = {}
const mbti_btns = document.querySelectorAll('input[name=mbti-btns]')
mbti_btns.forEach(btn => {
    btn.addEventListener('click', event => {
        if (btn.checked) {
            mbtiCategoryDict[btn.attributes.id.value] = 1
        } else {
            delete mbtiCategoryDict[btn.attributes.id.value]
        }

        console.log(mbtiCategoryDict)
    })
})

if (langCategoryDict.length >= 1) {
    console.log('asdlkf;jasdjfkla;sjdflaksj')
}