// 팔로우 비동기
const followForm = document.querySelector('#follow-form')
const followBtn = document.querySelector('#follow-btn')

// 1. 유저 팔로우 버튼
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

                const noFollowers = document.querySelector('#no-followers')
                if (noFollowers) {
                    noFollowers.remove()
                }

                // 유저의 팔로워 목록에 나의 정보를 비동기로 추가
                const myUserId = response.data.my_user_pk
                const myImage = response.data.my_image
                const myUsername = response.data.my_username
                const myNickname = response.data.my_nickname
                const followersBox = document.querySelector('#followers-box')
                followersBox.insertAdjacentHTML('beforeend', `
                    <div class="d-flex justify-content-between align-items-center" id="user-${myUserId}">
                      <div class="d-flex align-items-center my-3">
                        <div class="mx-3">
                          <a href="/accounts/${myUserId}/">
                            <img src="${myImage}" class="modal-profile-img" alt="">
                          </a>
                        </div>
                        <div>
                          <a href="/accounts/${myUserId}/">
                            <p class="mb-0"><b>${myNickname}</b></p>
                            <p class="mb-0" style="font-size: 13px;">${myUsername}</p>
                          </a>
                        </div>
                      </div>
                    </div>
                `)
            } else {
                followBtn.value = '팔로우'

                const myUserId = response.data.my_user_pk
                const myInfo = document.querySelector(`#user-${myUserId}`)
                if (myInfo) {
                  myInfo.remove()
                }
            }
            
            const followersCount = document.querySelector(`#followers-count-${userId}`)
            followersCount.innerText = response.data.followers_count
            const followingsCount = document.querySelector(`#followings-count-${userId}`)
            followingsCount.innerText = response.data.followings_count

            if (response.data.followers_count === 0) {
                const followersBox = document.querySelector('#followers-box')
                followersBox.insertAdjacentHTML('beforeend', `
                    <p id="no-followers" class="text-muted my-3">현재 나를 팔로우하는 유저가 없습니다.</p>
                `)
            }
        })
    })
}


// 2. 팔로워 목록에서 팔로우/언팔로우
const followForms1 = document.querySelectorAll('.follow-forms-1')
if (followForms1) {
    followForms1.forEach(form => {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
        form.addEventListener('submit', event => {
            event.preventDefault()
            
            const userId = event.target.dataset.userId
            console.log(userId)
        
            axios({
                method: 'post',
                url: `/accounts/${userId}/follow/`,
                headers: {'X-CSRFToken': csrftoken},
            }).then(response => {
                const isFollowing = response.data.is_following
                const followBtn1 = document.querySelector(`#follow-btn-1-${userId}`) // #follow-form > input[type=submit]
                if (isFollowing === true) {
                    followBtn1.value = '언팔로우'

                    const userImage = response.data.user_image
                    const userUsername = response.data.user_username
                    const userNickname = response.data.user_nickname
                    
                    const followingsBox = document.querySelector('#followings-box')

                    // '나'의 팔로잉 목록에 '내가' 팔로우한 유저 추가
                    if (response.data.my_user_pk === Number(followingsBox.getAttribute('data-followings-box-id'))) {
                        const noFollowings = document.querySelector('#no-followings')
                        if (noFollowings) {
                            noFollowings.remove()
                        }
                        
                        followingsBox.insertAdjacentHTML('beforeend', `
                            <div class="d-flex justify-content-between align-items-center" id="user-${userId}">
                            <div class="d-flex align-items-center my-3">
                                <div class="mx-3">
                                <a href="/accounts/${userId}/">
                                    <img src="${userImage}" class="modal-profile-img" alt="">
                                </a>
                                </div>
                                <div>
                                <a href="/accounts/${userId}/">
                                    <p class="mb-0"><b>${userNickname}</b></p>
                                    <p class="mb-0" style="font-size: 13px;">${userUsername}</p>
                                </a>
                                </div>
                            </div>

                            <!-- 비동기로 생긴 건 3 -->
                            <div class="me-3">
                                <form class="follow-forms-3" data-user-id="${userId}">
                                <input id="follow-btn-3-${userId}" type="submit" class="btn px-3 bbtn" value="언팔로우">
                                </form>
                            </div>
                            </div>
                        `)
                    }

                    // 3. 팔로잉 목록에서 팔로우/언팔로우 (목록은 새로고침 후 변경)
                    const followForms3 = document.querySelectorAll('.follow-forms-3')
                    if (followForms3) {
                        followForms3.forEach(form => {
                            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
                            form.addEventListener('submit', event => {
                                event.preventDefault()
                                
                                const userId = event.target.dataset.userId
                                console.log(userId)
                            
                                axios({
                                    method: 'post',
                                    url: `/accounts/${userId}/follow/`,
                                    headers: {'X-CSRFToken': csrftoken},
                                }).then(response => {
                                    const isFollowing = response.data.is_following
                                    const followBtn2 = document.querySelector(`#follow-btn-3-${userId}`) // #follow-form > input[type=submit]
                                    console.log(followBtn2)
                                    if (isFollowing === true) {
                                        followBtn2.value = '언팔로우'
                                    } else {
                                        followBtn2.value = '팔로우'
                                    }
                        
                                    // 내 페이지에서 나의 팔로잉 유저의 수를 변경
                                    const myUserId = response.data.my_user_pk
                                    const followingsCount = document.querySelector(`#followings-count-${myUserId}`)
                                    if (followingsCount) {
                                        followingsCount.innerText = response.data.my_followings_count
                                    }
                                })
                            })
                        })
                    }
                } else {
                    followBtn1.value = '팔로우'

                    // 팔로워 목록에서 여러 번 팔/언팔 시
                    // 팔로잉 목록에 계속 유저가 추가되는 것을 방지
                    const user = document.querySelector(`#followings-box > #user-${userId}`)
                    if (user) {
                        user.remove()
                    }
                }

                // 내 페이지에서 나의 팔로잉 유저의 수를 변경
                const myUserId = response.data.my_user_pk
                const followingsCount = document.querySelector(`#followings-count-${myUserId}`)
                if (followingsCount) {
                    followingsCount.innerText = response.data.my_followings_count
                }
            })
        })
    })
}


// 3. 팔로잉 목록에서 팔로우/언팔로우 (목록은 새로고침 후 변경)
const followForms2 = document.querySelectorAll('.follow-forms-2')
if (followForms2) {
    followForms2.forEach(form => {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
        form.addEventListener('submit', event => {
            event.preventDefault()
            
            const userId = event.target.dataset.userId
            console.log(userId)
        
            axios({
                method: 'post',
                url: `/accounts/${userId}/follow/`,
                headers: {'X-CSRFToken': csrftoken},
            }).then(response => {
                const isFollowing = response.data.is_following
                const followBtn2 = document.querySelector(`#follow-btn-2-${userId}`) // #follow-form > input[type=submit]
                console.log(followBtn2)
                if (isFollowing === true) {
                    followBtn2.value = '언팔로우'
                } else {
                    followBtn2.value = '팔로우'
                }
    
                // 내 페이지에서 나의 팔로잉 유저의 수를 변경
                const myUserId = response.data.my_user_pk
                const followingsCount = document.querySelector(`#followings-count-${myUserId}`)
                if (followingsCount) {
                    followingsCount.innerText = response.data.my_followings_count
                }
            })
        })
    })
}