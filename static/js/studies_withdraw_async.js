// 가입 신청 (방장 X)
function withdraw(form, study_pk) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    axios({
        method: 'post',
        url: `/studies/${study_pk}/withdraw/`,
        headers: {'X-CSRFToken': csrftoken},
    }).then(response => {
        // 스터디 인원 수 변경
        const acceptedCnt = document.querySelector('#accepted-cnt')
        acceptedCnt.innerText = response.data.accepted_cnt

        // 가입 신청 버튼 생성
        const userBtnsBox = document.querySelector('#user-btns-box')
        userBtnsBox.insertAdjacentHTML('beforeend', `
            <form style="padding: 40px 80px;" onsubmit="event.preventDefault(); studyApply(this, ${study_pk})">
              <!-- 신청을 안 한 상태 -->
              <input id="study-apply-btn-${study_pk}" type="submit" value="가입신청" class="btn btn-success">
            </form>
        `)

        // 스터디 탈퇴 버튼 삭제
        form.remove()
    })
}