// 가입 신청 (방장 X)
function studyApply(form, study_pk) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    axios({
        method: 'post',
        url: `/studies/${study_pk}/apply/`,
        headers: {'X-CSRFToken': csrftoken},
    }).then(response => {
        const studyApplyBtn = document.querySelector(`#study-apply-btn-${study_pk}`)
        const isClosed = response.data.is_closed
        const isApplied = response.data.is_applied
        const statusBadges = document.querySelectorAll('.status-badges')
        const warningMessage = document.querySelector('.alert-warning')

        warningMessage.classList.add('d-none')
        warningMessage.classList.remove('d-block')

        if (studyApplyBtn) {
            if (isClosed === false) {
                if (isApplied === true) {
                    studyApplyBtn.value = '가입신청 취소'
                    studyApplyBtn.classList.add('btn-secondary')
                    studyApplyBtn.classList.remove('btn-success')
                } else {
                    studyApplyBtn.value = '가입신청'
                    studyApplyBtn.classList.add('btn-success')
                    studyApplyBtn.classList.remove('btn-secondary')
                }
            } else {
                studyApplyBtn.value = '가입불가'
                studyApplyBtn.classList.add('btn-danger')
                studyApplyBtn.classList.remove('btn-success')
                studyApplyBtn.disabled = true

                statusBadges.forEach(badge => {
                    badge.innerText = '모집 종료'
                    badge.classList.add('text-bg-danger')
                    badge.classList.remove('text-bg-success')
                })

                warningMessage.classList.add('d-block')
                warningMessage.classList.remove('d-none')
            }
        }
    })
}