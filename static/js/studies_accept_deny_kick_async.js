// 1. 가입 신청 수락 (방장)
function accept(form, study_pk, user_pk) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    axios({
        method: 'post',
        url: `/studies/${study_pk}/user/${user_pk}/accept/`,
        headers: {'X-CSRFToken': csrftoken},
    }).then(response => {
        // 스터디 인원 수 변경
        const acceptedCnt = document.querySelector('#accepted-cnt')
        acceptedCnt.innerText = response.data.accepted_cnt

        // 대기 목록에서 삭제
        const waitingUser = document.querySelector(`#waiting-user-${user_pk}`)
        const waitingCnt = response.data.waiting_cnt
        const waitingBox = document.querySelector('#waiting-box')
        
        waitingUser.remove()
        if (waitingCnt === 0) {
            waitingBox.insertAdjacentHTML('beforeend', '<p id="no-waitings" class="py-5 text-center text-muted">아직 신청 인원이 없어요</p>')
        }

        // 스터디 인원 목록에 추가
        const acceptedBox = document.querySelector('#accepted-box')
        const userImage = response.data.user_image
        const userNickname = response.data.user_nickname
        const userUsername = response.data.user_username

        acceptedBox.insertAdjacentHTML('beforeend', `
            <div class="d-flex justify-content-between align-items-center" id="accepted-user-${user_pk}">
              <div class="d-flex align-items-center my-3" >
                <div class="mx-3">
                  <a href="/accounts/${user_pk}/">
                    <img src="${userImage}" class="modal-profile-img" alt="">
                  </a>
                </div>
                <div>
                  <a href="/accounts/${user_pk}/">
                    <p class="mb-0"><b>${userNickname}</b></p>
                    <p class="mb-0" style="font-size: 13px;">${userUsername}</p>
                  </a>
                </div>
              </div>
              <div class="me-3">
                <form onsubmit="event.preventDefault(); kick(this, ${study_pk}, ${user_pk})">
                  <input type="submit" value="추방" class="btn btn-danger">
                </form>            
              </div>
            </div>
        `)
    })
}


// 2. 가입 신청 거절 (방장)
function deny(form, study_pk, user_pk) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    axios({
        method: 'post',
        url: `/studies/${study_pk}/user/${user_pk}/deny/`,
        headers: {'X-CSRFToken': csrftoken},
    }).then(response => {
        // 대기 목록에서 삭제
        const waitingUser = document.querySelector(`#waiting-user-${user_pk}`)
        const waitingCnt = response.data.waiting_cnt
        const waitingBox = document.querySelector('#waiting-box')
        
        waitingUser.remove()
        if (waitingCnt === 0) {
            waitingBox.insertAdjacentHTML('beforeend', '<p id="no-waitings" class="py-5 text-center text-muted">아직 신청 인원이 없어요</p>')
        }
    })
}


// 3. 스터디 추방 (방장)
function kick(form, study_pk, user_pk) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  axios({
      method: 'post',
      url: `/studies/${study_pk}/user/${user_pk}/kick/`,
      headers: {'X-CSRFToken': csrftoken},
  }).then(response => {
      // 스터디 인원 수 변경
      const acceptedCnt = document.querySelector('#accepted-cnt')
      acceptedCnt.innerText = response.data.accepted_cnt

      // 스터디원 목록에서 삭제
      const acceptedUser = document.querySelector(`#accepted-user-${user_pk}`)
      acceptedUser.remove()
  })
}