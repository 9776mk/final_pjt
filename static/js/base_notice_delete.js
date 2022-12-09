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