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
            salonName.textContent = "Name: " + salon.name;
            salonContainer.appendChild(salonName);

            var salonRating = document.createElement("p");
            salonRating.textContent = "Rating: " + salon.rating;
            salonContainer.appendChild(salonRating);

            var salonDistrict = document.createElement("p");
            salonDistrict.textContent = "Location: " + salon.district;
            salonContainer.appendChild(salonDistrict);

            // if (salon.photo) {
            //     var img = document.createElement('img');
            //     img.src = "data:image/jpeg;base64," + salon.photo;
            //     salonContainer.appendChild(img);
            // }

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