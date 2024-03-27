function getAvailableSalons() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "http://127.0.0.1:5000/available_salons");

    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          var salons = response.salons;

          var salonListContainer = document.getElementById("salonList");

          salons.forEach(function(salon) {
    var salonContainer = document.createElement("div");
    salonContainer.classList.add("salon-container");

    var photoPlace = document.createElement("div");
    photoPlace.classList.add("photo-place");
    salonContainer.appendChild(photoPlace);

    // Додавання фото, якщо воно є
    if (salon.photo) {
        var img = document.createElement('img');
        img.src = "data:image/jpeg;base64," + salon.photo;
        img.style.width = "100%"; // Зробити фото квадратним
        img.style.height = "100%"; // Зробити фото квадратним
        photoPlace.appendChild(img);
    }

    var salonContainer1 = document.createElement('div'); // Замінено змінну з "salonContainer" на "salonContainer1"
    salonContainer1.classList.add('salon1-container');
    var nameInfo = document.createElement('p');
    var districtInfo = document.createElement('p');
    nameInfo.textContent = 'Назва: ' + salon.name;
    nameInfo.classList.add("name-salon");
    districtInfo.textContent = 'Район: ' + salon.district;
    salonContainer1.appendChild(nameInfo);
    salonContainer1.appendChild(districtInfo);
    salonContainer.appendChild(salonContainer1); // Додано до контейнера салону

    var salonContainer2 = document.createElement('div');
    salonContainer2.classList.add('salon2-container');
    var ratingInfo = document.createElement('p');
    ratingInfo.textContent = 'Рейтинг: ' + salon.rating.toFixed(1) + "☆"; // Виправлено присвоєння тексту рейтингу
    salonContainer2.appendChild(ratingInfo);
    salonContainer.appendChild(salonContainer2); // Додано до контейнера салону




    var buttonContainer = document.createElement('div');
    buttonContainer.classList.add("button_container");
    var salonDetailsButton = document.createElement('button');
    salonDetailsButton.classList.add('button-details');
    salonDetailsButton.textContent = 'Деталі';

    salonDetailsButton.addEventListener("click", function() {
        var salonId = salon.id;
        sessionStorage.setItem('salon', salonId);
        window.location.href = "ChooseSalon.html";
    });

    salonDetailsButton.setAttribute("data-salon-id", "{{ salon.id }}"); // Додайте атрибут data-salon-id зі значенням ID салону
    buttonContainer.appendChild(salonDetailsButton);


    // var userId = JSON.parse(sessionStorage.getItem('user'));
    // if (salon.owner_id == userId.user_id) {
    //     var editButton = createEditButton(salon.id);
    //     var deleteButton = createDeleteButton();
    //     buttonContainer.appendChild(editButton);
    //      buttonContainer.appendChild(deleteButton);
    // }
    


    salonContainer.appendChild(buttonContainer);
    salonListContainer.appendChild(salonContainer);
});
        } else {
          console.error("Error:", xhr.status);
        }
      }
    };

    xhr.send();
  }


//   function createEditButton(id) {
//     var editButton = document.createElement('button');
//     editButton.classList.add('button-details');
//     editButton.textContent = 'Редагувати';

//     editButton.addEventListener("click", function() {
//         var salonId = id;
//         sessionStorage.setItem('salon', salonId);
//         window.location.href = "EditSalon.html";
//     });

//     return editButton;
// }

// function createDeleteButton() {
//     var deleteButton = document.createElement('button');
//     deleteButton.classList.add('button-details');
//     deleteButton.textContent = 'Видалити';

//     deleteButton.addEventListener("click", function() {
//         // Додаткова логіка для редагування
//     });

//     return deleteButton;
// }

// Викликати функцію для отримання доступних салонів
  getAvailableSalons();


