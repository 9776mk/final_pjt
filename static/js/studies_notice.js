// 1. 스터디 알림 읽음 처리
function noticeRead() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    axios({
        method: 'post',
        url: '/studies/notice_read/',
        headers: {'X-CSRFToken': csrftoken},
    }).then(response => {
        const isRead = response.data.is_read

        if (isRead) {
            const studyNoticeCnt = document.querySelector('#study-notice-cnt')
            
            if (studyNoticeCnt) {
                studyNoticeCnt.remove()
            }
        }
    })
}


// 2. 스터디 알림 삭제
function noticeDelete(form, notice_pk) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    axios({
        method: 'post',
        url: `/studies/${notice_pk}/notice_delete/`,
        headers: {'X-CSRFToken': csrftoken},
    }).then(response => {
        const notice = document.querySelector(`#notice-${notice_pk}`)
        notice.remove()
    })
}


// 3. 알림 모두 삭제
function noticeDeleteAll() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    axios({
        method: 'post',
        url: `/studies/notice_delete/all/`,
        headers: {'X-CSRFToken': csrftoken},
    }).then(response => {
        const noticeBox = document.querySelector(`#notice-box`)
        const deleteBtn = document.querySelector('#notice-delete-all-btn')
        noticeBox.remove()
        deleteBtn.remove()

        const modalBody = document.querySelector('.modal-body')
        modalBody.insertAdjacentHTML('beforeend', '<p id="no-notices" class="py-5 text-center text-muted">아직 알림이 없어요</p>')
    })
}