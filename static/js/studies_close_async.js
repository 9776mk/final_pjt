// 모집 시작 & 모집 마감
function studyClose(form, study_pk) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    axios({
        method: 'post',
        url: `/studies/${study_pk}/close/`,
        headers: {'X-CSRFToken': csrftoken},
    }).then(response => {
        const studyCloseBtn = document.querySelector(`#study-close-btn-${study_pk}`)
        const isClosed = response.data.is_closed
        const isFull = response.data.is_full
        const statusBadges = document.querySelectorAll('.status-badges')

        if (isClosed === false) {
            studyCloseBtn.value = '모집마감'
            studyCloseBtn.classList.add('btn-danger')
            studyCloseBtn.classList.remove('btn-success')
            studyCloseBtn.disabled = false

            statusBadges.forEach(badge => {
                badge.innerText = '모집중'
                badge.classList.add('text-bg-success')
                badge.classList.remove('text-bg-danger')
            })
        } else if (isFull == true) {
            // 이 부분이 좀 걸린다
            studyCloseBtn.value = '모집완료'
            studyCloseBtn.classList.add('btn-success')
            studyCloseBtn.classList.remove('btn-danger')
            studyCloseBtn.disabled = true

            statusBadges.forEach(badge => {
                badge.innerText = '모집 종료'
                badge.classList.add('text-bg-danger')
                badge.classList.remove('text-bg-success')
            })
        } else {
            studyCloseBtn.value = '모집시작'
            studyCloseBtn.classList.add('btn-success')
            studyCloseBtn.classList.remove('btn-danger')
            studyCloseBtn.disabled = false

            statusBadges.forEach(badge => {
                badge.innerText = '모집 종료'
                badge.classList.add('text-bg-danger')
                badge.classList.remove('text-bg-success')
            })
        }
    })
}