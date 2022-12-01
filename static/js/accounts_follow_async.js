// 팔로우 비동기
const followForm = document.querySelector('#follow-form')
const followForm1 = document.querySelector('#follow-form1')
const followForm2 = document.querySelector('#follow-form1')
const followBtn = document.querySelector('#follow-btn')
const followBtn1 = document.querySelector('#follow-btn1')
const followBtn2 = document.querySelector('#follow-btn2')

if (followForm) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
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


if (followForm1) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    followForm1.addEventListener('submit', event => {
        event.preventDefault()
        
        const userId = event.target.dataset.userId
    
        axios({
            method: 'post',
            url: `/accounts/${userId}/follow/`,
            headers: {'X-CSRFToken': csrftoken},
        }).then(response => {
            const isFollowing = response.data.is_following
            const followBtn1 = document.querySelector('#follow-btn1') // #follow-form > input[type=submit]
            if (isFollowing === true) {
                followBtn1.value = '언팔로우'
                followBtn1.classList.add('btn-danger')
                followBtn1.classList.remove('btn-primary')
            } else {
                followBtn1.value = '팔로우'
                followBtn1.classList.add('btn-primary')
                followBtn1.classList.remove('btn-danger')
            }
            
        })
    })
}


if (followForm2) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    followForm2.addEventListener('submit', event => {
        event.preventDefault()
        
        const userId = event.target.dataset.userId
    
        axios({
            method: 'post',
            url: `/accounts/${userId}/follow/`,
            headers: {'X-CSRFToken': csrftoken},
        }).then(response => {
            const isFollowing = response.data.is_following
            const followBtn2 = document.querySelector('#follow-btn2') // #follow-form > input[type=submit]
            if (isFollowing === true) {
                followBtn2.value = '언팔로우'
                followBtn2.classList.add('btn-danger')
                followBtn2.classList.remove('btn-primary')
            } else {
                followBtn2.value = '팔로우'
                followBtn2.classList.add('btn-primary')
                followBtn2.classList.remove('btn-danger')
            }
            
        })
    })
}