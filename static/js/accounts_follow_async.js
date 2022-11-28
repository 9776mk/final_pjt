// 팔로우 비동기
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
const followForm = document.querySelector('#follow-form')

if (followForm) {
    followForm.addEventListener('submit', event => {
        event.preventDefault()
        
        const userId = event.target.dataset.userId
    
        axios({
            method: 'post',
            url: `/accounts/${userId}/follow/`,
            headers: {'X-CSRFToken': csrftoken},
        }).then(response => {
            const isFollowing = response.data.is_following
            const followBtn = document.querySelector('#follow-btn') // #follow-form > input[type=submit]
            if (isFollowing === true) {
                followBtn.value = '언팔로우'
                followBtn.classList.add('btn-danger')
                followBtn.classList.remove('btn-primary')
            } else {
                followBtn.value = '팔로우'
                followBtn.classList.add('btn-primary')
                followBtn.classList.remove('btn-danger')
            }
            
            const followersCount = document.querySelector('#followers-count')
            followersCount.innerText = response.data.followers_count
        })
    })
}