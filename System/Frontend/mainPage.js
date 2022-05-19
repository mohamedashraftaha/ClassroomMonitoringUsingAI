var header = document.querySelector(".btns");
var head = document.querySelector("#head");
var sel = document.querySelector("#sel");
var img = document.querySelector("#case");
let flg;

// document.getElementById("rep").onclick = function () {
//    // header.remove();
//    // sel.remove();
//    // img.remove();
//    head.innerHTML="Case has been reported";
// };

// document.getElementById("dis").onclick = function () {
//    // header.remove();
//    // sel.remove();
//    // img.remove();
//    head.innerHTML="Case has been dismissed";
// };

// current time
let ltime;
var current = new Date();
ltime = current.toLocaleTimeString();
let tm = document.getElementById("time");
tm.innerText = "Current Time: " + ltime;
const button = document.querySelector("button"),
  toast = document.querySelector(".toast"),
  closeIcon = document.querySelector(".close"),
  progress = document.querySelector(".progress");

let timer1, timer2;

//    timer1 = setTimeout(() => {
//    toast.classList.add("active");

//    }, 1000); //1s = 1000 milliseconds
// close notification when close button is clicked
closeIcon.addEventListener("click", () => {
  toast.classList.remove("active");

  // setTimeout(() => {
  //   progress.classList.remove("active");
  // }, 3000);

  // clearTimeout(timer1);
  // clearTimeout(timer2);
});
// let jsondata = "";
// let case_id_glob="";
// let apiurl='http://classroommonitoring.herokuapp.com/api/user/get_recent_case';
// async function getJson(url) {
//    let response = await fetch(url);
//    let data = await response.json()
//    return data.caseID;
// }
// jsondata= await getJson(apiurl);
// case_id_glob=jsondata.data.case_details[0].case_id;

// var link=image.getAttribute('src');
// get exam instacne id from local storage
let inst_id = localStorage.getItem("instance");

let caseid;
let stuNum;
let loadFlag = true;
function fetchRep() { //fetch rep function to get recent case every 8 seconds
  loadFlag = false;
  console.log(inst_id);
  // get recent case API 
  fetch(
    "http://classroommonitoring.herokuapp.com/api/user/get_recent_case/" +
      inst_id
  )
    .then((res) => res.json())
    .then((out) => {
      console.log(out);
      // push notification when new case arrives
      if (out.msg == "Recent Case Retreived successfully") {
        toast.classList.add("active");
      } else if (out == undefined) {
        console.log("else");
        loadFlag = true;
        // return;
      } else {
        console.log("else");
        loadFlag = true;
      }
      
      console.log("out2");
      caseid = out.data.case_details[0].case_id;
      stuNum = out.data.case_details[0].student_number;

      console.log("caseid ", caseid);
      console.log("stuNum ", stuNum);

      document.getElementById("cid").innerText = "New Case, Case ID: " + caseid;
      // get case frame by case id , instance id and student number
      return fetch(
        "http://classroommonitoring.herokuapp.com/api/user/get_frames_links/" +
          caseid +
          "/" +
          inst_id +
          "/" +
          stuNum
      );
    })
    .then((response) => response.json())
    .then((json) => {
      console.log("json");
      console.log(json);
      let cnt = json.data;
      let i = 0;
      // console.log(json.urls[1]);
      // document.getElementById("case").src=json.data[0];
      document.getElementById("case").src = json.data[i];
      // document.getElementById("case").onclick = function () {
      //   document.getElementById("case").src = json.data[i++];
      //   if (i == cnt.length) {
      //     document.getElementById("case").alt =
      //       "No more detected frames in this case";
      //   }
      // };
    })
    // reprot and dimiss button that call reprot and dismiss case APIs
    .then((resu) => {
      console.log(resu);
      console.log("buttons");
      document.getElementById("rep").onclick = function () {
        console.log("rep clicked");
        return fetch(
          "http://classroommonitoring.herokuapp.com/api/user/report_case",
          {
            method: "POST",
            headers: {
              Accept: "application/json, text/plain, */*",
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              caseID: caseid,
              exam_instance_id: inst_id,
            }),
          }
        ).then((res) => toast.classList.remove("active"));
      };

      document.getElementById("dis").onclick = function () {
        console.log("1");
        // return fetch('http://classroommonitoring.herokuapp.com/api/user/dismiss_case', {
        //     method: "POST",
        //     mode: 'no-cors',
        //     headers: {
        //        "Accept": "application/json, text/plain, */*",
        //         "Content-Type": "application/json",
        //       },
        //       body: JSON.stringify({
        //           caseID: caseid,

        //       })
        //     })

        return fetch(
          "http://classroommonitoring.herokuapp.com/api/user/dismiss_case",
          {
            method: "POST",
            headers: {
              Accept: "application/json, text/plain, */*",
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              caseID: caseid,
              exam_instance_id: inst_id,
            }),
          }
        ).then((res) => {
          console.log("2");

          toast.classList.remove("active");
          // console.log("2");
          // console.log(document.getElementById("check"));
          // document.getElementById("check").checked = false;
          // console.log(document.getElementById("check").checked);
          // console.log("3");
        });
      };

      loadFlag = true;
    });
}

//    document.getElementById("dis").onclick = function () {

//    document.getElementById("rep").onclick = function () {

//        fetch('http://classroommonitoring.herokuapp.com/api/user/report_case/', {
//            method: "POST",
//           headers: {
//              Accept: "application/json, text/plain, */*",
//              "Content-Type": "application/json",
//            },
//            body: JSON.stringify({
//                caseID: case_id_glob,

//            }),
//          });
//    }

// fetch the fetchRep function every 8 seconds
window.addEventListener("load", function () {
  // Your document is loaded.
  var fetchInterval = 8000; // 5 seconds.

  // Invoke the request every 5 seconds.
  setInterval(fetchRep, fetchInterval);
});

document.getElementById("closeNot").onclick = function () {
  console.log("2");
  console.log(document.getElementById("check"));
  console.log(document.getElementById("check").checked);

  document.getElementById("check").checked = true;
  console.log(document.getElementById("check").checked);
  console.log("3");
  console.log("close clicked");
  // document.querySelector(".alert_box").style.display = "none";
};
// if end session button is clocked end session and redirect user to end of exam report page
document.getElementById("endSession").addEventListener("click", function () {
  fetch(
    "http://classroommonitoring.herokuapp.com/api/user/end_exam/" + inst_id
  )
    .then((response) => response.json()) // pass the data as promise to next then block
    .then((dout) => {
      // if(dout.msg=="exam has ended")
      // {
      window.location.href = "examRep.html";

      // }
    });
});
//  document.getElementById('toast').addEventListener("click",function(){

//     document.querySelector(".alert_box").style.display="flex";
//  })
