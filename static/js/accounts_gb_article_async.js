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

        const articlesBox = document.querySelector('#gb-articles-box')
        articlesBox.insertAdjacentHTML('beforeend', `
            <div id="article-${articlePk}">
                <p>${articleUser} | ${articleContent} | ${articleCreatedAt}</p>
            
            <!-- 방명록 글 삭제 Form -->
            <form id="gb-article-delete-form-${articlePk}" onsubmit="event.preventDefault(); delete_gb_article(this, '${user_pk}', '${articlePk}')">
                <input type="submit" class="btn-close" style="color:transparent;">
            </form>
        </div>
        `)

        form.reset()
    }).catch(error => {
        console.log(error)
    })
}