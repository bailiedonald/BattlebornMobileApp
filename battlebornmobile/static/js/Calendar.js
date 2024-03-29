// Team Memebers Contributiing to this page: 
// Grant Kite -


var cal = {
    
    mon : false, 
    events : null, 
    sMth : 0, 
    sYear : 0, 
    sDIM : 0, 
    sF : 0, 
    sL : 0, 
    sFD : 0, 
    sLD : 0, 
    ready : 0, 
    
    hMth : null, hYear : null, 
    hCD : null, hCB : null, 
    hFormWrap : null, hForm : null,
    hfID : null, hfStart : null, 
    hfEnd : null, hfTxt : null,
    hfColor : null, hfBG : null,
    hfDel : null,
  
    
    ajax : (req, data, onload) => {
      // (B1) FORM DATA
      let form = new FormData();
      for (let [k,v] of Object.entries(data)) { form.append(k,v); }
  
      // (B2) FETCH
      fetch(req + "/", { method:"POST", body:form })
      .then(res => res.text())
      .then(txt => onload(txt))
      .catch(err => console.error(err));
    },
  
    // (C) INIT CALENDAR
    init : () => {
      // (C1) GET HTML ELEMENTS
      cal.hMth = document.getElementById("calMonth");
      cal.hYear = document.getElementById("calYear");
      cal.hCD = document.getElementById("calDays");
      cal.hCB = document.getElementById("calBody");
      cal.hFormWrap = document.getElementById("calForm");
      cal.hForm = cal.hFormWrap.querySelector("form");
      cal.hfID = document.getElementById("evtID");
      cal.hfStart = document.getElementById("evtStart");
      cal.hfEnd = document.getElementById("evtEnd");
      cal.hfTxt = document.getElementById("evtTxt");
      cal.hfColor = document.getElementById("evtColor");
      cal.hfBG = document.getElementById("evtBG");
      cal.hfDel = document.getElementById("evtDel");
  
      // (C2) MONTH & YEAR SELECTOR
      let now = new Date(), nowMth = now.getMonth() + 1;
      for (let [i,n] of Object.entries({
        1 : "January", 2 : "Febuary", 3 : "March", 4 : "April",
        5 : "May", 6 : "June", 7 : "July", 8 : "August",
        9 : "September", 10 : "October", 11 : "November", 12 : "December"
      })) {
        let opt = document.createElement("option");
        opt.value = i;
        opt.innerHTML = n;
        if (i==nowMth) { opt.selected = true; }
        cal.hMth.appendChild(opt);
      }
      cal.hYear.value = parseInt(now.getFullYear());
  
      // (C3) ATTACH CONTROLS
      cal.hMth.onchange = cal.load;
      cal.hYear.onchange = cal.load;
      document.getElementById("calAdd").onclick = () => cal.show();
      cal.hForm.onsubmit = () => cal.save();
      document.getElementById("evtCX").onclick = () => cal.hFormWrap.open = false;
      cal.hfDel.onclick = cal.del;
  
      // (C4) DRAW DAY NAMES
      let days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
      if (cal.mon) { days.push("Sun"); } else { days.unshift("Sun"); }
      for (let d of days) { 

        let cell = document.createElement("div");
        cell.className = "calCell";
        cell.innerHTML = d;
        cal.hCD.appendChild(cell);
      }
  
      // (C5) LOAD & DRAW CALENDAR
      cal.load();
    },
  
    // (D) LOAD EVENTS
    load : () => {
      // (D1) SET SELECTED PERIOD
      cal.sMth = parseInt(cal.hMth.value);
      cal.sYear = parseInt(cal.hYear.value);
      cal.sDIM = new Date(cal.sYear, cal.sMth, 0).getDate();
      cal.sFD = new Date(cal.sYear, cal.sMth-1, 1).getDay();
      cal.sLD = new Date(cal.sYear, cal.sMth-1, cal.sDIM).getDay();
      let m = cal.sMth;
      if (m < 10) { m = "0" + m; }
      cal.sF = parseInt(String(cal.sYear) + String(m) + "010000");
      cal.sL = parseInt(String(cal.sYear) + String(m) + String(cal.sDIM) + "2359");
  
      // (D2) AJAX GET EVENTS
      cal.ajax("get", { month : cal.sMth, year : cal.sYear }, evt => {
        cal.events = JSON.parse(evt);
        cal.draw();
      });
    },
  
    // (E) DRAW CALENDAR
    draw : () => {
      // (E1) CALCULATE DAY MONTH YEAR
      // note - jan is 0 & dec is 11 in js
      // note - sun is 0 & sat is 6 in js
      let now = new Date(), // current date
          nowMth = now.getMonth()+1, // current month
          nowYear = parseInt(now.getFullYear()), // current year
          nowDay = cal.sMth==nowMth && cal.sYear==nowYear ? now.getDate() : null ;
  
      // (E2) DRAW CALENDAR ROWS & CELLS
      // (E2-1) INIT + HELPER FUNCTIONS
      let rowA, rowB, rowC, rowMap = {}, rowNum = 1,
          cell, cellNum = 1,
      rower = () => {
        rowA = document.createElement("div");
        rowB = document.createElement("div");
        rowC = document.createElement("div");
        rowA.className = "calRow";
        rowA.id = "calRow" + rowNum;
        rowB.className = "calRowHead";
        rowC.className = "calRowBack";
        cal.hCB.appendChild(rowA);
        rowA.appendChild(rowB);
        rowA.appendChild(rowC);
      },
      celler = day => {
        cell = document.createElement("div");
        cell.className = "calCell";
        if (day) { cell.innerHTML = day; }
        rowB.appendChild(cell);
        cell = document.createElement("div");
        cell.className = "calCell";
        if (day===undefined) { cell.classList.add("calBlank"); }
        if (day!==undefined && day==nowDay) { cell.classList.add("calToday"); }
        rowC.appendChild(cell);
      };
      cal.hCB.innerHTML = ""; rower();
  
      // (E2-2) BLANK CELLS BEFORE START OF MONTH
      if (cal.mon && cal.sFD != 1) {
        let blanks = cal.sFD==0 ? 7 : cal.sFD ;
        for (let i=1; i<blanks; i++) { celler(); cellNum++; }
      }
      if (!cal.mon && cal.sFD != 0) {
        for (let i=0; i<cal.sFD; i++) { celler(); cellNum++; }
      }
  
      // (E2-3) DAYS OF THE MONTH
      for (let i=1; i<=cal.sDIM; i++) {
        rowMap[i] = { r : rowNum, c : cellNum };
        celler(i);
        if (cellNum%7==0) { rowNum++; rower(); }
        cellNum++;
      }
      
      // (E2-4) BLANK CELLS AFTER END OF MONTH
      if (cal.mon && cal.sLD != 0) {
        let blanks = cal.sLD==6 ? 1 : 7-cal.sLD;
        for (let i=0; i<blanks; i++) { celler(); cellNum++; }
      }
      if (!cal.mon && cal.sLD != 6) {
        let blanks = cal.sLD==0 ? 6 : 6-cal.sLD;
        for (let i=0; i<blanks; i++) { celler(); cellNum++; }
      }
  
      // (E3) DRAW EVENTS
      if (Object.keys(cal.events).length > 0) { for (let [id,evt] of Object.entries(cal.events)) {
        // (E3-1) EVENT START & END DAY
        let sd = new Date(evt.s), ed = new Date(evt.e);
        sd = sd.getMonth()+1 < cal.sMth ? 1 : sd.getDate();
        ed = ed.getMonth()+1 > cal.sMth ? cal.sDIM : ed.getDate();
  
        // (E3-2) "MAP" ONTO HTML CALENDAR
        cell = {}; rowNum = 0;
        for (let i=sd; i<=ed; i++) {
          if (rowNum!=rowMap[i]["r"]) {
            cell[rowMap[i]["r"]] = { s:rowMap[i]["c"], e:0 };
            rowNum = rowMap[i]["r"];
          }
          if (cell[rowNum]) { cell[rowNum]["e"] = rowMap[i]["c"]; }
        }
  
        // (E3-3) DRAW HTML EVENT ROW
        for (let [r,c] of Object.entries(cell)) {
          let o = c.s - 1 - ((r-1) * 7), // event cell offset
              w = c.e - c.s + 1; // event cell width
          rowA = document.getElementById("calRow"+r);
          rowB = document.createElement("div");
          rowB.className = "calRowEvt";
          rowB.innerHTML = cal.events[id]["t"];
          rowB.style.color = cal.events[id]["c"];
          rowB.style.backgroundColor  = cal.events[id]["b"];
          rowB.classList.add("w"+w);
          if (o!=0) { rowB.classList.add("o"+o); }
          rowB.onclick = () => cal.show(id);
          rowA.appendChild(rowB);
        }
      }}
    },
  
    // (F) SHOW EVENT FORM
    show : id => {
      if (id) {
        cal.hfID.value = id;
        cal.hfStart.value = cal.events[id]["s"];
        cal.hfEnd.value = cal.events[id]["e"];
        cal.hfTxt.value = cal.events[id]["t"];
        cal.hfColor.value = cal.events[id]["c"];
        cal.hfBG.value = cal.events[id]["b"];
        cal.hfDel.style.display = "inline-block";
      } else {
        cal.hForm.reset();
        cal.hfID.value = "";
        cal.hfDel.style.display = "none";
      }
      cal.hFormWrap.open = true;
    },
  
    // (G) SAVE EVENT
    save : () => {

      var data = {
        s : cal.hfStart.value.replace("T", " "),
        e : cal.hfEnd.value.replace("T", " "),
        t : cal.hfTxt.value,
        c : cal.hfColor.value,
        b : cal.hfBG.value
      };
      if (cal.hfID.value != "") { data.id = parseInt(cal.hfID.value); }
  
      // (G2) DATE CHECK
      if (new Date(data.s) > new Date(data.e)) {
        alert("Start date cannot be later than end date!");
        return false;
      }
  
      // (G3) SAVE
      cal.ajax("save", data, res => {
        if (res=="OK") {
          cal.hFormWrap.open = false;
          cal.load();
        } else { alert(res); }
      });
      return false;
    },
  
    // (H) DELETE EVENT
    del : () => { if (confirm("Delete Event?")) {
      cal.ajax("delete", { id : parseInt(cal.hfID.value) }, res => {
        if (res=="OK") {
          cal.hFormWrap.open = false;
          cal.load();
        } else { alert(res); }
      });
    }}
  };
  window.onload = cal.init;