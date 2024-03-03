const store = {
  user: {
    "id": "",
    "name": "",
    "email": "",
    "phone": "",
    "type": "", 
  },
  salons: {},
  records: {}  
}

// Функція, яка перевіряє, чи "email" та "password" порожні
function areCredentialsEmpty() {
    return store.user.email === "";
}

// Функція, яка обробляє клік по кнопці "Мій акаунт"
function handleMyAccountClick() {
    if (areCredentialsEmpty()) {
        window.location.href = "login.html";
    } else {
        window.location.href = "MyPage.html";
    }
}

// Додаємо обробник подій до кнопки "Мій акаунт"
document.getElementById("myAccountButton").addEventListener("click", handleMyAccountClick);


function registerUser() {
    var userName = document.getElementById("user_name").value;
    var userEmail = document.getElementById("user_email").value;
    var userPassword = document.getElementById("user_password").value;
    var userPhone = document.getElementById("user_phone").value;
    var checkBox = document.getElementById('business-checkbox');
    var userAccountType = checkBox.checked ? 1 : 2;

    var data = {
        user_name: userName,
        user_email: userEmail,
        user_password: userPassword,
        user_phone: userPhone,
        user_account_type: userAccountType
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/add_user");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.message) {
                    document.getElementById("message").innerText = response.message;
                } else if (response.errors) {
                    // Очищення повідомлень про помилки перед відображенням нових
                    clearErrorMessages(".error-message");
                    // Показ повідомлень про помилки під відповідними інпутами
                    displayErrorMessages(response.errors);
                }
            } else {
                document.getElementById("message").innerText = "An error occurred while processing your request.";
            }
        }
    };

    xhr.send(JSON.stringify(data));
}

// Функція для відображення повідомлень про помилки під відповідними інпутами
function displayErrorMessages(errors) {
    for (var fieldName in errors) {
        var elementId = fieldName === "message" ? "message-after" : fieldName + "-error";
        var errorMessage = errors[fieldName];
        var errorElement = document.getElementById(elementId);
        if (errorElement) {
            errorElement.innerText = errorMessage;
        }
    }
}


// Функція для очищення повідомлень про помилки
// function clearErrorMessages() {
//     var errorMessages = document.querySelectorAll(".error-message");
//     errorMessages.forEach(function(element) {
//         element.innerText = "";
//     });
// }

function clearErrorMessages(id) {
    var errorMessages = document.querySelectorAll(id);
    errorMessages.forEach(function(element) {
        element.innerText = "";
    });
}


function loginUser() {
    var userEmail = document.getElementById("login_email").value;
    var userPassword = document.getElementById("login_password").value;

    var data = {
        user_email: userEmail,
        user_password: userPassword
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/login");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                // if (response.message ) {
                //     document.getElementById("message2").innerText = response.message;
                // } 
                if (response.error) {
                    document.getElementById("message2").innerText = response.error;
                }
                else{
                    store.user.id = response.user_id;
                    store.user.name = response.name;
                    store.user.email = response.email;
                    store.user.phone = response.phone;
                    store.user.type = response.type_user;

                    // store.user.id = "";
                    // store.user.name = "";
                    // store.user.email = "";
                    // store.user.phone = "";
                    // store.user.type = "";
                    document.getElementById("message2").innerText = store.user.id;
                }

            }
        }
    };

    xhr.send(JSON.stringify(data));
}




// function registerUser() {
//             var userName = document.getElementById("user_name").value;
//             var userEmail = document.getElementById("user_email").value;
//             var userPassword = document.getElementById("user_password").value;
//             var userPhone = document.getElementById("user_phone").value
//             var checkBox = document.getElementById('business-checkbox');
//             var userAcountType = checkBox.checked ? 1 : 2;

//             var data = {
//                 user_name: userName,
//                 user_email: userEmail,
//                 user_password: userPassword,
//                 user_phone: userPhone,
//                 user_account_type: userAcountType
//             };

//             var xhr = new XMLHttpRequest();
//             xhr.open("POST", "http://127.0.0.1:5000/add_user");
//             xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
//             xhr.send(JSON.stringify(data));
//         }