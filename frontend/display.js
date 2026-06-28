 fetch('navbar.html')
      .then(response => response.text())
      .then(data => {
        document.getElementById('navbar').innerHTML = data;
        let storedname = localStorage.getItem("firstname");
        if (!storedname || storedname === "undefined" || storedname === "null") {
            storedname = "there friend";
        }
        let nameElement = document.getElementById('nav-firstname');
        if (nameElement) nameElement.textContent = storedname;
      });
