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


            var salonName = document.createElement("p");
            salonName.classList.add("name-salon");
            salonName.textContent = salon.name;
            salonContainer.appendChild(salonName);

            var salonImageContainer = document.createElement("div");
            salonImageContainer.classList.add("salon-image-container"); // Додайте клас для стилізації за допомогою CSS
            salonContainer.appendChild(salonImageContainer);

            var salonImage = document.createElement("img");
            salonImage.src = "photos/clipart-map-location.png"; // Шлях до фото відносно кореня сайту
            salonImage.classList.add("salon-image"); // Додайте клас для стилізації за допомогою CSS
            salonImageContainer.appendChild(salonImage);


            var salonDistrict = document.createElement("p");
            salonDistrict.classList.add("location-salon");
            salonDistrict.textContent = salon.district;
            salonContainer.appendChild(salonDistrict);

            var salonRating = document.createElement("p");
            salonRating.classList.add("rating-salon");
            salonRating.textContent = salon.rating;
            salonContainer.appendChild(salonRating);

            // var salonDetailsButton = document.createElement("button");
            // salonDetailsButton.classList.add("button-details");
            // salonDetailsButton.textContent = "Деталі";
            
            // salonDetailsButton.addEventListener("click", function() {
            //     window.location.href = "http://127.0.0.1:5000/salon_details/{{ salon.id }}";

            // });
            // salonContainer.appendChild(salonDetailsButton);

            var salonDetailsButton = document.createElement("button");
            salonDetailsButton.classList.add("button-details");
            salonDetailsButton.textContent = "Деталі";
            
            salonDetailsButton.addEventListener("click", function() {
                var salonId = salon.id;
                sessionStorage.setItem('salon', salonId);
                    window.location.href = "ChooseSalon.html";
            });
            salonDetailsButton.setAttribute("data-salon-id", "{{ salon.id }}"); // Додайте атрибут data-salon-id зі значенням ID салону
            salonContainer.appendChild(salonDetailsButton);



            salonListContainer.appendChild(salonContainer);
          });
        } else {
          console.error("Error:", xhr.status);
        }
      }
    };

    xhr.send();
  }

  // Викликати функцію для отримання доступних салонів
  getAvailableSalons();