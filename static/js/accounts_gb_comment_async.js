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

      const commentsBox = document.querySelector(`#gb-comments-box-${article_pk}`)
      commentsBox.insertAdjacentHTML('beforeend', `
          <div id="comment-${commentPk}">
              <p>${commentUser} | ${commentContent} | ${commentCreatedAt}</p>
          
              <!-- 답글 삭제 Form -->
              <form id="gb-comment-delete-form-${article_pk}" onsubmit="event.preventDefault(); delete_gb_comment(this, '${user_pk}', '${article_pk}', '${commentPk}')">
                  <input type="submit" class="btn-close" style="color:transparent;">
              </form>
          </div>
      `)

      const noComments = document.querySelector(`#article-${article_pk}-no-comments`)
      if (noComments) {
          noComments.remove()
      }
      form.reset()
  })
}