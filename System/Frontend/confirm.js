let li = document.createElement("li");
let li2 = document.createElement("li");
let li3 = document.createElement("li");
let li4 = document.createElement("li");
li.style.listStyleImage = "url('inst.png')";
li.style.display = "list-item";
li.style.listStylePosition = "inside";

// const {form} = require('./login.js');
let det = document.querySelector("#details");
// let read_message;

//    fetch(" https://classroommonitoring.herokuapp.com/api/user/get_assigned_exams/"+nat_id)
//      .then((response) => response.json())
//      .then((dataOut)=>{
//          read_message=dataOut.data;
//         //  console.log(read_message);
//         //  det.innerText = read_message;
//         //  document.body.appendChild(det);
//  return read_message;
//  })
// console.log(read_message);
let det2 = document.querySelector("#details2");

let examSubCode;
let schoolName;
let cameraIP;
//      fetch("http://classroommonitoring.herokuapp.com/api/user/get_exam_instance_details/"+read_message)
//      .then((res) => res.json())
//      .then((output)=>{

//         examSubCode=output.data.Exam_Details[0].Exam_Subject_code;
//         schoolName=output.data.Exam_Details[0].School;
//         cameraIP=output.data.Exam_Details[0].Assigned_Camera_IP;

//      })

let welcome = document.getElementById("welc");
let det3 = document.querySelector("#details3");
let det4 = document.querySelector("#details4");

// const nat_id = require('/login');
var nat_id;
nat_id = localStorage.getItem("val");
console.log(nat_id);
// Fetching get assigned exams api to get all exam details on the confirmation page to pass the assigned exam instance to the rest of APIs 
const result = fetch(
  " https://classroommonitoring.herokuapp.com/api/user/get_assigned_exams/" +
    nat_id
)
  .then((response) => response.json()) // pass the data as promise to next then block
  .then((dataOut) => {
    let inst = dataOut.data;
    localStorage.setItem("instance", inst);

    det.innerText = inst;
    document.body.appendChild(det);
    // Get exam instance details api to display exam details on confirmation
    return fetch(
      "http://classroommonitoring.herokuapp.com/api/user/get_exam_instance_details/" +
        inst
    ); // make a 2nd request and return a promise
  })
  .then((response) => response.json())
  .then((output) => {
  
    if (output.status == "failed") {
      //if no assigned exam display the below messgae and ask the user to logout
      li1.innerText = "No Assigned Exam Subject Code";
      // document.body.appendChild(det2);
      let Det1 = document.getElementById("li1");
      let Det2 = document.getElementById("li2");
      let Det3 = document.getElementById("li3");
      Det1.remove();
      Det2.remove();
      Det3.remove();
      let noexm = document.getElementById("noExam");
      noexm.innerHTML =
        "No Assigned Exam on Your Account, Please Contact Your Adminstrator";
      noexm.style.color = "red";
      let noImg = document.getElementById("noimg");
      noImg.src = "close.png";
      let bord = document.getElementById("details4");
      bord.style.boxShadow = "none";
 // Add a logout button
      let butOut = document.getElementById("confirm_but");
      butOut.innerText = "Log Out";
      // redirect user to logout page 
      document.getElementById("confirm_but").onclick = function () {
        location.href = "login.html";
      };
      // li2.innerText = "No Assigned Exam Subject Code";
      // // document.body.appendChild(det3);

      // li3.innerText = "No Assigned Exam Subject Code";
      // document.body.appendChild(det4);
    } else {
      //append exam informaion to the divs to display on screen  
      examSubCode = output.data.Exam_Details[0].Exam_Subject_code;
      schoolName = output.data.Exam_Details[0].School;
      cameraIP = output.data.Exam_Details[0].Assigned_Camera_IP;

      det2.innerText = examSubCode;

      document.body.appendChild(det2);

      det3.innerText = examSubCode;
      document.body.appendChild(det3);

      det4.innerText = cameraIP;
      document.body.appendChild(det4);
    }
  });
  // redirect the user to select the sensitivity when the exam info is confirmed

document.getElementById("confirm_but").onclick = function () {
  location.href = "sense.html";
  // location.href = "examRep.html";
};
