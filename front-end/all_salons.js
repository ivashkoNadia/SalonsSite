// Функція для отримання доступних салонів
function fetchAvailableSalons(callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "http://127.0.0.1:5000/available_salons");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                var salons = response.salons;
                sessionStorage.setItem('salons_list', JSON.stringify(salons));
                callback(salons); // Передаємо отримані дані у функцію відображення
            } else {
                console.error("Error:", xhr.status);
            }
        }
    };

    xhr.send();
}

// Функція для відображення салонів на сторінці
function displaySalons(salons) {
    var salonListContainer = document.getElementById("salonList");
    salonListContainer.innerHTML = '';

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
            img.style.width = "100%";
            img.style.height = "100%";
            photoPlace.appendChild(img);
        }

        var salonContainer1 = document.createElement('div');
        salonContainer1.classList.add('salon1-container');
        var nameInfo = document.createElement('p');
        var districtInfo = document.createElement('p');
        nameInfo.textContent = 'Назва: ' + salon.name;
        nameInfo.classList.add("name-salon");
        districtInfo.textContent = 'Район: ' + salon.district;
        salonContainer1.appendChild(nameInfo);
        salonContainer1.appendChild(districtInfo);
        salonContainer.appendChild(salonContainer1);

        var salonContainer2 = document.createElement('div');
        salonContainer2.classList.add('salon2-container');
        var ratingInfo = document.createElement('p');
        ratingInfo.textContent = 'Рейтинг: ' + salon.rating.toFixed(1) + "☆";
        salonContainer2.appendChild(ratingInfo);
        salonContainer.appendChild(salonContainer2);

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

        salonDetailsButton.setAttribute("data-salon-id", salon.id);
        buttonContainer.appendChild(salonDetailsButton);

        var userId = JSON.parse(sessionStorage.getItem('user'));

      // Перевірка наявності користувача в sessionStorage
      if (userId) {
        if (salon.owner_id == userId.user_id) {
          var editButton = createEditButton(salon.id);
          buttonContainer.appendChild(editButton);
        }
      }

      salonContainer.appendChild(buttonContainer);
      salonListContainer.appendChild(salonContainer);

    });
}

// Викликаємо функцію для отримання доступних салонів та їх відображення
fetchAvailableSalons(displaySalons);



  function createEditButton(id) {
    var editButton = document.createElement('button');
    editButton.classList.add('button-details');
    editButton.textContent = 'Редагувати';

    editButton.addEventListener("click", function() {
        var salonId = id;
        sessionStorage.setItem('salon', salonId);
        window.location.href = "EditSalon.html";
    });

    return editButton;
}

function searchByName() {
    var searchInput = document.getElementById("searchInput").value.toLowerCase(); // Отримуємо значення введеного тексту і конвертуємо його до нижнього регістру
    var salons = JSON.parse(sessionStorage.getItem('salons_list')); // Отримуємо список салонів з sessionStorage

    if (salons) { // Перевіряємо, чи є дані в sessionStorage
        var filteredSalons = salons.filter(function(salon) {
            return salon.name.toLowerCase().includes(searchInput); // Фільтруємо салони за назвою
        });
        displaySalons(filteredSalons); // Викликаємо функцію для відображення відфільтрованих салонів
    } else {
        console.error("No salon data found in sessionStorage");
    }
}


function advancedSearch() {
    var salons = JSON.parse(sessionStorage.getItem('salons_list')); // Отримання списку салонів зі sessionStorage

    // Створення форми для фільтрації салонів
    var filtersContainer = document.getElementById("filters-container");
    filtersContainer.innerHTML = ''; // Очищення контейнера перед додаванням нової форми

    // Створення рамки для форми
    var formFrame = document.createElement("div");
    formFrame.classList.add("form-frame");

    // Додавання випадаючого списку для вибору району
var districtLabel = document.createElement("label");
districtLabel.textContent = "Виберіть район:  ";
var districtSelect = document.createElement("select");
districtSelect.classList.add("district-select");
districtSelect.id = "districtSelect"; // Додайте ідентифікатор для випадаючого списку районів

// Додавання пустого елемента в початок списку
var emptyOption = document.createElement("option");
emptyOption.value = "";
emptyOption.textContent = "Всі";
districtSelect.appendChild(emptyOption);

// Отримання унікальних районів зі списку салонів
var uniqueDistricts = [...new Set(salons.map(salon => salon.district))];
uniqueDistricts.forEach(function(district) {
    var option = document.createElement("option");
    option.value = district;
    option.textContent = district;
    districtSelect.appendChild(option);
});

// Додавання випадаючого списку до форми
formFrame.appendChild(districtLabel);
formFrame.appendChild(districtSelect);


    // Додавання полів для вказання діапазону оцінок
   var ratingLabel = document.createElement("label");
ratingLabel.textContent = "Виберіть діапазон оцінок (від 1 до 5):  ";
ratingLabel.classList.add("rating-filt");

var ratingInputMin = document.createElement("input");
ratingInputMin.type = "number";
ratingInputMin.id = "minRating"; // Додайте ідентифікатор для мінімального значення оцінки
ratingInputMin.min = 1;
ratingInputMin.max = 5;

var ratingInputMax = document.createElement("input");
ratingInputMax.type = "number";
ratingInputMax.id = "maxRating"; // Додайте ідентифікатор для максимального значення оцінки
ratingInputMax.min = 1;
ratingInputMax.max = 5;


    // Додавання полів для вказання діапазону оцінок до форми
    formFrame.appendChild(ratingLabel);
    formFrame.appendChild(ratingInputMin);
    formFrame.appendChild(ratingInputMax);

    // Додавання кнопки для застосування фільтрів
    var applyButton = document.createElement("button");
    applyButton.textContent = "Застосувати";
    applyButton.classList.add("applyfilter-but");
    applyButton.addEventListener("click", applyFilters); // Додаємо обробник події для кнопки
    formFrame.appendChild(applyButton);

    var cancelButton = document.createElement("button");
    cancelButton.classList.add("cancel-but");
    cancelButton.textContent = "Скасувати";
    cancelButton.addEventListener("click", cancelFilters); // Додаємо обробник події для кнопки
    formFrame.appendChild(cancelButton);

    // Додавання рамки з формою до контейнера
    filtersContainer.appendChild(formFrame);
}

// Функція, яка буде викликатися при натисканні кнопки "Застосувати фільтри"
function applyFilters() {
    var salons = JSON.parse(sessionStorage.getItem('salons_list'));

    var districtSelect = document.getElementById("districtSelect");
    var minRatingInput = document.getElementById("minRating");
    var maxRatingInput = document.getElementById("maxRating");

    if (!districtSelect || !minRatingInput || !maxRatingInput) {
        console.error("One or more form elements are missing");
        return;
    }

    // Отримання значень з випадаючого списку району і полів вводу оцінки
var selectedDistrict = districtSelect.value;
var minRating = parseFloat(minRatingInput.value);
var maxRating = parseFloat(maxRatingInput.value);

// Перевірка, чи вказані значення для фільтрації по району
var isDistrictFilterEnabled = !!selectedDistrict;

// Перевірка, чи вказані значення для фільтрації по оцінці
var isRatingFilterEnabled = !isNaN(minRating) && !isNaN(maxRating);

// Фільтрація салонів згідно з вибраними параметрами
var filteredSalons = salons.filter(function(salon) {
    var districtMatch = !isDistrictFilterEnabled || salon.district === selectedDistrict;

    var ratingMatch = true;
    if (isRatingFilterEnabled) {
        var salonRating = salon.rating || 0;
        var minRatingValue = isNaN(minRating) ? 0 : minRating;
        var maxRatingValue = isNaN(maxRating) ? 5 : maxRating;
        ratingMatch = salonRating >= minRatingValue && salonRating <= maxRatingValue;
    }

    return districtMatch && ratingMatch;
});

// Відображення відфільтрованих салонів
displaySalons(filteredSalons);


    // // Отримання значень з випадаючого списку району і поля вводу оцінки
    // var selectedDistrict = districtSelect.value;
    // var minRating = parseFloat(minRatingInput.value);
    // var maxRating = parseFloat(maxRatingInput.value);

    

    // // Фільтрація салонів згідно з вибраними параметрами
    // var filteredSalons = salons.filter(function(salon) {
    //     var districtMatch = !selectedDistrict || salon.district === selectedDistrict;
    //     var ratingMatch = salon.rating >= minRating && salon.rating <= maxRating;
    //     return districtMatch && ratingMatch;
    // });

    // // Відображення відфільтрованих салонів
    // displaySalons(filteredSalons);
}



// Очищення контейнера з формою
function cancelFilters() {
    var filtersContainer = document.getElementById("filters-container");
    filtersContainer.innerHTML = ''; 
}


