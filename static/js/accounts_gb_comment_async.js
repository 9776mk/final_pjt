// 1. 방명록 댓글 삭제 비동기
function delete_gb_comment(form, user_pk, article_pk, comment_pk) {
  // preventDafault를 onsubmit에다 해줌
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  axios({
      method: 'post',
      url: `/accounts/${user_pk}/guestbook/article/${article_pk}/comment/${comment_pk}/delete/`,
      headers: {'X-CSRFToken': csrftoken},
  }).then(response => {
      const comment = document.querySelector(`#comment-${comment_pk}`)
      comment.remove()

      if (response.data.total_comment_cnt === 0) {
        const commentsBox = document.querySelector(`#gb-comments-box-${article_pk}`)

        if (commentsBox.classList.contains('comment-bg')) {
          commentsBox.classList.remove('comment-bg')
        } else if (commentsBox.classList.contains('comment-bg-secret')) {
          commentsBox.classList.remove('comment-bg-secret')
        }
      }
  })
}


// 2. 방명록 댓글 생성 비동기(★)
function create_gb_comment(form, user_pk, article_pk) {
    // preventDafault를 onsubmit에다 해줌
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    let formData = new FormData(form)

    const commentSecretBtn = document.querySelector(`#comment-secret-btn-${article_pk}`)
    let isSecret = false
    if (commentSecretBtn) {
        isSecret = commentSecretBtn.getAttribute('data-is-secret')
    }
    formData.append('is_secret', isSecret)  // key - value 쌍

    axios({
        method: 'post',
        url: `/accounts/${user_pk}/guestbook/article/${article_pk}/comment_create/`,
        headers: {'X-CSRFToken': csrftoken},
        data: formData
    }).then(response => {
        const commentPk = response.data.comment_pk
        const commentUser = response.data.comment_user
        const commentContent = response.data.comment_content
        const commentCreatedAt = response.data.comment_created_at
        const commentUserImage = response.data.comment_user_image
        const articleIsSecret = response.data.article_is_secret // 방명록 글이 비밀글이면, 댓글도 비밀댓글
        const commentIsSecret = response.data.comment_is_secret

        const commentsBox = document.querySelector(`#gb-comments-box-${article_pk}`)
        
        if (articleIsSecret === true || commentIsSecret === true) {
            commentsBox.classList.add('comment-bg-secret')
            commentsBox.insertAdjacentHTML('beforeend', `
              <div id="comment-${commentPk}" class="mb-2">
                <div class="d-flex flex-column justify-content-between">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <div style="font-weight: bold; font-size: 15px;">
                      <!-- 프로필 사진 3 -->
                      <div class="d-flex align-items-center">
                        <a href="/accounts/${user_pk}/"><img src="${commentUserImage}" style="border-radius: 70%; width: 25px;" alt=""></a>
                        <a href="/accounts/${user_pk}/"><p class="ms-2 mb-0">${commentUser}</p></a>
                      </div>
                    </div>
                    <p class="mb-0" style="font-size: 12px;">${commentCreatedAt}</p>
                  </div>
                </div>
                <div class="d-flex justify-content-between">
                  <p class="mb-0 text-break">
                    <span>${commentContent}</span>
                    <span class="bi bi-lock"></span>
                  </p>
                  <div class="d-flex align-items-end">
                    <!-- 답글 삭제 Form -->
                    <form id="gb-comment-delete-form-${commentPk}" onsubmit="event.preventDefault(); delete_gb_comment(this, '${user_pk}', '${article_pk}', '${commentPk}')">
                      <input type="submit" class="btn-close" style="color:transparent; font-size: 12px;" onclick="return confirm('삭제하시겠습니까?');">
                    </form>
                  </div>
                </div>
              </div>
            `)
        } else {
            commentsBox.classList.add('comment-bg')
            commentsBox.insertAdjacentHTML('beforeend', `
              <div id="comment-${commentPk}" class="mb-2">
                <div class="d-flex flex-column justify-content-between">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <div style="font-weight: bold; font-size: 15px;">
                      <!-- 프로필 사진 3 -->
                      <div class="d-flex align-items-center">
                        <a href="/accounts/${user_pk}/"><img src="${commentUserImage}" style="border-radius: 70%; width: 25px;" alt=""></a>
                        <a href="/accounts/${user_pk}/"><p class="ms-2 mb-0">${commentUser}</p></a>
                      </div>
                    </div>
                    <p class="mb-0" style="font-size: 12px;">${commentCreatedAt}</p>
                  </div>
                </div>
                <div class="d-flex justify-content-between">
                  <p class="mb-0 text-break">
                    <span>${commentContent}</span>
                  </p>
                  <div class="d-flex align-items-end">
                    <!-- 답글 삭제 Form -->
                    <form id="gb-comment-delete-form-${commentPk}" onsubmit="event.preventDefault(); delete_gb_comment(this, '${user_pk}', '${article_pk}', '${commentPk}')">
                      <input type="submit" class="btn-close" style="color:transparent; font-size: 12px;" onclick="return confirm('삭제하시겠습니까?');">
                    </form>
                  </div>
                </div>
              </div>
            `)
        }
        
        

        const noComments = document.querySelector(`#article-${article_pk}-no-comments`)
        if (noComments) {
            noComments.remove()
        }
        form.reset()
    })
}


// 3. 비공개 선택 버튼
// const commentSecretBtns = document.querySelectorAll('.comment-secret-btn')
// commentSecretBtns.forEach(btn => {
//     btn.addEventListener('click', event => {
//         const articleId = Number(btn.getAttribute('data-article-id'))
//         // console.log(event.target.dataset.articleId) // 왜 undefined

//         // 아이콘 이미지 변경
//         const icon = document.querySelector(`#comment-secret-btn-icon-${articleId}`)
//         icon.classList.toggle('bi-unlock')
//         icon.classList.toggle('bi-lock-fill')
    
//         // data-is-secret 값 변경
//         let isSecret = btn.getAttribute('data-is-secret')
//         if (isSecret === 'true') {
//             btn.setAttribute('data-is-secret', 'false')
//         } else {
//             btn.setAttribute('data-is-secret', 'true')
//         }
//     })
// })

function secretComment(btn, article_pk) {
    // 아이콘 이미지 변경
    const icon = document.querySelector(`#comment-secret-btn-icon-${article_pk}`)
    icon.classList.toggle('bi-unlock')
    icon.classList.toggle('bi-lock-fill')

    // data-is-secret 값 변경
    let isSecret = btn.getAttribute('data-is-secret')
    if (isSecret === 'true') {
        btn.setAttribute('data-is-secret', 'false')
    } else {
        btn.setAttribute('data-is-secret', 'true')
    }
}