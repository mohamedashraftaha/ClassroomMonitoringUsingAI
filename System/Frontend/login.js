let input = document.getElementById("submit");
let loading = false;
document.getElementById("loader").style.display = "none";
document.getElementById("submit").style.display = "block";
// Submit button when login is ok
let button = input.addEventListener("click", (e) => {
  console.log("here");
  let form = {
    email: document.querySelector("#userID"),
    password: document.querySelector("#password"),
    submit: document.querySelector("#submit"),
  };
  var usID = document.getElementById("userID").value;
  console.log(document.getElementById("userID").value);
  console.log(form);
  // ser in local storage for future use in other pages
  localStorage.setItem("val", usID);
// fetch login proctor API POST API with national id and password
  e.preventDefault();
  const login =
    " https://classroommonitoring.herokuapp.com/api/user/login_proctor";
  loading = true;
  document.getElementById("loader").style.display = "block";
  document.getElementById("submit").style.display = "none";
  fetch(login, {
    method: "POST",
    headers: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      national_id: form.email.value,
      password: form.password.value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      // loading spinner
      document.getElementById("loader").style.display = "none";
      document.getElementById("submit").style.display = "block";
// check if credentials are correct to redirect user
      loading = false;
      console.log(data.status);
      if (data.status == "success") {
        window.location.href = "confirm.html";
      } else {
        alert("Invalid User ID or Password"); /*displays error message*/
      }
    })
    .catch((err) => {
      console.log(err);
    });
});
