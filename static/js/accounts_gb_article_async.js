// 1. 방명록 글 삭제 비동기
function delete_gb_article(form, user_pk, article_pk) {
    // preventDafault를 onsubmit에다 해줌
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    axios({
        method: 'post',
        url: `/accounts/${user_pk}/guestbook/article/${article_pk}/delete/`,
        headers: {'X-CSRFToken': csrftoken},
    }).then(response => {
        const article = document.querySelector(`#article-${article_pk}`)
        article.remove()
    })
}


// 2. 방명록 글 생성 비동기
function create_gb_article(form, user_pk) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    axios({
        method: 'post',
        url: `/accounts/${user_pk}/guestbook/article_create/`,
        headers: {'X-CSRFToken': csrftoken},
        data: new FormData(form)
    }).then(response => {
        const articlePk = response.data.article_pk
        const articleUser = response.data.article_user
        const articleContent = response.data.article_content
        const articleCreatedAt = response.data.article_created_at
        const articleUserImage = response.data.article_user_image

        const articlesBox = document.querySelector('#gb-articles-box')
        articlesBox.insertAdjacentHTML('afterbegin', `
          <div id="article-${articlePk}" class="mb-3">
            <div class="d-flex justify-content-between align-items-center">
              <!-- 프로필 사진 2 -->
              <div class="d-flex flex-column align-items-center">
                <a href="/accounts/${user_pk}/"><img src="${articleUserImage}" style="border-radius: 70%; width: 50px;" alt=""></a>
                <a href="/accounts/${user_pk}/"><p class="mt-2 mb-0">${articleUser}</p></a>
              </div>

              <!-- 방명록 말풍선 -->
              <div class="speech-bubble w-100 ms-3">
                <!-- 내용 & 날짜 -->
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <div class="me-3">${articleContent}</div>
                  <div style="font-size: 12px;">${articleCreatedAt}</div>
                </div>

                <!-- 답글 달기 토글 & 방명록 글 삭제 Form -->
                <div class="d-flex justify-content-between align-items-center" style="font-size: 12px;">
                  <a data-bs-toggle="collapse" href="#collapse-gb-comment-form-${articlePk}" style="font-size: 15px;" class="text-center">답글 달기</a>
                  
                  <form id="gb-article-delete-form-${articlePk}" onsubmit="event.preventDefault(); delete_gb_article(this, '${user_pk}', '${articlePk}')">
                    <input type="submit" class="btn-close" style="color:transparent; font:16px" onclick="return confirm('삭제하시겠습니까?');">
                  </form>
                </div>

                <div class="collapse" id="collapse-gb-comment-form-${articlePk}">
                  <!-- 답글 생성 Form -->
                  <form onsubmit="event.preventDefault(); create_gb_comment(this, '${user_pk}', '${articlePk}')">
                    <div class="d-flex align-items-center my-2">
                      <textarea name="content" cols="40" rows="1" class="form-control me-2" placeholder="답글을 남겨주세요" required id="id_content"></textarea>
                      <input type="submit" value="작성" name="gb_comment_create" class="btn ms-1" style="width: 50px; height: 40px; background-color: #f37c2c; color: white;">
                    </div>
                  </form>

                  <!-- 답글 -->
                  <div id="gb-comments-box-${articlePk}">
                  </div>
                </div>
              </div>
            </div>
          </div>
        `)

        form.reset()
    }).catch(error => {
        console.log(error)
    })
}