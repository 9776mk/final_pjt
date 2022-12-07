let langCategoryDict = {}
const lang_btns = document.querySelectorAll('input[name=language-btns]')
const allUsers = document.querySelectorAll('.all-users')

lang_btns.forEach(btn => {
    btn.addEventListener('click', event => {
        // 체크된 버튼의 id값(= 언어정보)을 딕셔너리에 저장
        if (btn.checked) {
            langCategoryDict[btn.attributes.id.value] = 1
        } 
        // 체크 해제 시 딕셔너리에서 키와 값 삭제
        else {
            delete langCategoryDict[btn.attributes.id.value]
        }

        langCategoryArr = Object.keys(langCategoryDict)
        mbtiCategoryArr = Object.keys(mbtiCategoryDict)

        // 0. 사용 언어를 클릭할 때마다 모든 유저를 d-none으로
        for (let i = 0; i < allUsers.length; i++) {
            allUsers[i].classList.add('d-none')
            allUsers[i].classList.remove('d-block')
        }
        
        // 1. 선택된 언어가 있을 때
        if (langCategoryArr.length >= 1) {
            for (let i = 0; i < allUsers.length; i++) {
                for (let j = 0; j < langCategoryArr.length; j++) {
                    // (1) 선택된 MBTI가 없을 때
                    if (mbtiCategoryArr.length === 0) {
                        if (allUsers[i].classList.contains(langCategoryArr[j])) {
                            allUsers[i].classList.add('d-block')
                            allUsers[i].classList.remove('d-none')
                        }
                    }

                    // (2) 선택된 MBTI가 있을 때
                    else {
                        for (let k = 0; k < mbtiCategoryArr.length; k++) {
                            if (allUsers[i].classList.contains(langCategoryArr[j]) && allUsers[i].classList.contains(mbtiCategoryArr[k])) {
                                allUsers[i].classList.add('d-block')
                                allUsers[i].classList.remove('d-none')
                            }
                        }
                    }
                }
            }
        }

        // 2. 선택된 언어가 없을 때
        else {
            for (let i = 0; i < allUsers.length; i++) {
                // (1) 선택된 MBTI가 없을 때 → 빈 화면
                if (mbtiCategoryArr.length === 0) {
                    allUsers[i].classList.add('d-none')
                    allUsers[i].classList.remove('d-block')
                }

                // (2) 선택된 MBTI가 있을 때 → MBTI 검색
                else {
                    for (let k = 0; k < mbtiCategoryArr.length; k++) {
                        if (allUsers[i].classList.contains(mbtiCategoryArr[k])) {
                            allUsers[i].classList.add('d-block')
                            allUsers[i].classList.remove('d-none')
                        }
                    }
                }
            }
        }
    })
})


let mbtiCategoryDict = {}
const mbti_btns = document.querySelectorAll('input[name=mbti-btns]')
mbti_btns.forEach(btn => {
    btn.addEventListener('click', event => {
        // 체크된 버튼의 id값(= MBTI 정보)을 딕셔너리에 저장
        if (btn.checked) {
            mbtiCategoryDict[btn.attributes.id.value] = 1
        }
        // 체크 해제 시 딕셔너리에서 키와 값 삭제
        else {
            delete mbtiCategoryDict[btn.attributes.id.value]
        }

        langCategoryArr = Object.keys(langCategoryDict)
        mbtiCategoryArr = Object.keys(mbtiCategoryDict)

        // 0. MBTI를 클릭할 때마다 모든 유저를 d-none으로
        for (let i = 0; i < allUsers.length; i++) {
            allUsers[i].classList.add('d-none')
            allUsers[i].classList.remove('d-block')
        }
        
        // 1. 선택된 MBTI가 있을 때
        if (mbtiCategoryArr.length >= 1) {
            for (let i = 0; i < allUsers.length; i++) {
                for (let j = 0; j < mbtiCategoryArr.length; j++) {
                    // (1) 선택된 언어가 없을 때
                    if (langCategoryArr.length === 0) {
                        if (allUsers[i].classList.contains(mbtiCategoryArr[j])) {
                            allUsers[i].classList.add('d-block')
                            allUsers[i].classList.remove('d-none')
                        }
                    }

                    // (2) 선택된 언어가 있을 때
                    else {
                        for (let k = 0; k < langCategoryArr.length; k++) {
                            if (allUsers[i].classList.contains(mbtiCategoryArr[j]) && allUsers[i].classList.contains(langCategoryArr[k])) {
                                allUsers[i].classList.add('d-block')
                                allUsers[i].classList.remove('d-none')
                            }
                        }
                    }
                }
            }
        }

        // 2. 선택된 MBTI가 없을 때
        else {
            for (let i = 0; i < allUsers.length; i++) {
                // (1) 선택된 언어가 없을 때 → 빈 화면
                if (langCategoryArr.length === 0) {
                    allUsers[i].classList.add('d-none')
                    allUsers[i].classList.remove('d-block')
                }

                // (2) 선택된 언어가 있을 때 → 언어 검색
                else {
                    for (let k = 0; k < langCategoryArr.length; k++) {
                        if (allUsers[i].classList.contains(langCategoryArr[k])) {
                            allUsers[i].classList.add('d-block')
                            allUsers[i].classList.remove('d-none')
                        }
                    }
                }
            }
        }
    })
})