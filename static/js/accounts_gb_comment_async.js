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
        commentsBox.classList.remove('comment-bg')
      }
  })
}


// 2. 방명록 댓글 생성 비동기(★)
function create_gb_comment(form, user_pk, article_pk) {
  // preventDafault를 onsubmit에다 해줌
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  axios({
      method: 'post',
      url: `/accounts/${user_pk}/guestbook/article/${article_pk}/comment_create/`,
      headers: {'X-CSRFToken': csrftoken},
      data: new FormData(form)
  }).then(response => {
      const commentPk = response.data.comment_pk
      const commentUser = response.data.comment_user
      const commentContent = response.data.comment_content
      const commentCreatedAt = response.data.comment_created_at
      const commentUserImage = response.data.comment_user_image

      const commentsBox = document.querySelector(`#gb-comments-box-${article_pk}`)
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
            <p class="mb-0">${commentContent}</p>
            <div class="d-flex align-items-end">
              <!-- 답글 삭제 Form -->
              <form id="gb-comment-delete-form-${commentPk}" onsubmit="event.preventDefault(); delete_gb_comment(this, '${user_pk}', '${article_pk}', '${commentPk}')">
                <input type="submit" class="btn-close" style="color:transparent; font-size: 12px;" onclick="return confirm('삭제하시겠습니까?');">
              </form>
            </div>
          </div>
        </div>
      `)

      const noComments = document.querySelector(`#article-${article_pk}-no-comments`)
      if (noComments) {
          noComments.remove()
      }
      form.reset()
  })
}