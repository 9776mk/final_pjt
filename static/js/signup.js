const signupBtn = document.querySelector('#signup-btn')

function isValidId() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const userID = document.querySelector('#id_username').value
    const modalBody = document.querySelector('#modal-body')

    axios({
        method: 'post',
        url: '/accounts/is_valid_id/',
        headers: { 'X-CSRFToken': csrfToken },
        data: { 'username': userID }
    }).then(response => {
        if (userID.length > 16) {
            modalBody.innerText = "16자 이하의 문자만 가능합니다."
            signupBtn.disabled = true
        } else if (response.data.is_valid === false) {
            modalBody.innerText = "사용 불가능한 아이디입니다."
            signupBtn.disabled = true
        } else if (response.data.is_valid === 'null') {
            modalBody.innerText = "아이디를 입력하세요."
            signupBtn.disabled = true
        } else {
            modalBody.innerText = "사용 가능한 아이디입니다."
            signupBtn.disabled = false  // 회원가입 버튼 활성화
            // 비번창 나옴
            const box = document.querySelector('#passwordBox')
            box.style.display = 'block';
            // 아이디 변경을 막음
            const id_username = document.querySelector('#id_username')
            id_username.setAttribute('readonly', true);

        }
    })
}


function checkPass() {
    const pass1 = document.getElementById('id_password1').value
    const pass2 = document.getElementById('id_password2').value
    const status = document.getElementById('statusP')
    if (pass1 === pass2) {
        status.innerHTML = "Valid";
        status.style.color = "#00ff00";
    } else {
        status.innerHTML = "Invalid";
        status.style.color = "#ff0000";
    }
}

