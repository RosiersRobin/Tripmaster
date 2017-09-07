/**
 * Created by Robin on 2/06/2017.
 */

//Clock script
function clock() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('clock_nav').innerHTML = h + ":" + m + ":" + s;
    var t = setTimeout(clock, 500);
}


function checkTime(i) {
    if (i < 10) {
        i = "0" + i;
    }  // add zero in front of numbers < 10
    return i;
}


/*
* Shut down the system
*/
function shutdownSystem() {
    console.log("System is going down...");
    $.post("/ajax/shutdown-system-safe");
}


/*
* reboot the system
*/
function rebootSystem() {
    console.log("System is going down for a reboot...");
    $.post("/ajax/reboot-system-safe");
}


/*
* Toggle the start/stop trip
 */
$(document).ready(function(){
    $("#start-stop-trip").click(function(){
        $(this).toggleClass("menu-item-red");
        $(this).toggleClass("menu-item-green");
        toggleTrip();
        $(this).text(function(i, v){
               return v === 'start trip' ? 'stop trip' : 'start trip'
            })
    });
});


/*
* THIS IS THE AJAX PART
*/

// MAKE THE POSTS
//This function will contain the post option to post data to the database
function toggleTrip() {
    $.ajax({
       url: "/ajax/update-trip-state",
       type: "POST",
       success: function(data)
       {
            console.log("Gelukt");
       },
       error: function(XMLHttpRequest, textStatus, errorThrown) {
           console.log("mislukt");
       }
    });
}


//Get the current speed dynamically
function getSpeed() {
    $.ajax({
        url: '/ajax/get-current-speed',
        type: 'GET',
        contentType: 'application/json',
        success: function (speed){
            document.getElementById('cur_speed_nav').innerHTML = speed + " km/u";
        }
    });
    var t = setTimeout(getSpeed, 1000);
}


//Get the total distance dynamically
function getDistance() {
    $.ajax({
        url: '/ajax/get-total-distance',
        type: 'GET',
        contentType: 'application/json',
        success: function (speed){
            document.getElementById('total_distance_nav').innerHTML = speed + " km";
        }
    });
    var t = setTimeout(getDistance, 1000);
}


//Get the average distance dynamically
function getAvgSpeed() {
    $.ajax({
        url: '/ajax/get-average-speed',
        type: 'GET',
        contentType: 'application/json',
        success: function (avg_speed){
            document.getElementById('avg_speed_nav').innerHTML = avg_speed;
        }
    });
    var t = setTimeout(getAvgSpeed, 1000);
}


//Get the time to clock in dynamically
function getIdealStopTime() {
    $.ajax({
        url: '/ajax/get-trip-ideal-stop-time',
        type: 'GET',
        contentType: 'application/json',
        success: function (ideal_stop_time){
            document.getElementById('ideal_stop_time').innerHTML = ideal_stop_time;
        }
    });
    var t = setTimeout(getIdealStopTime, 1000);
}


//Get the time to clock in dynamically
function getWrongDistance() {
    $.ajax({
        url: '/ajax/get-total-drove-wrong-distance',
        type: 'GET',
        contentType: 'application/json',
        success: function (total_dist_wrong){
            document.getElementById('total_dist_wrong').innerHTML = total_dist_wrong+" km";
        }
    });
    var t = setTimeout(getWrongDistance, 1000);
}


//Get the time to clock in dynamically
function getTimeBeforeClockIn() {
    $.ajax({
        url: '/ajax/get-trip-ideal-stop-time',
        type: 'GET',
        contentType: 'application/json',
        success: function (ideal_stop_time){
            var stopTime = ideal_stop_time.split(":");
            var date1 = new Date(); // now
            var date2 = new Date(date1.getFullYear(), date1.getMonth(), date1.getDate(), stopTime[0], stopTime[1], stopTime[2]);
            // console.log("Date 1:" + date1);
            // console.log("Date 2:" + date2);
            var diff = Math.abs(date1 - date2);
            // console.log(msToTime(diff));
            if(date1 > date2) {
                document.getElementById('ideal_time_for_stop').innerHTML = "+ " + msToTime(diff);
                document.getElementById('ideal_time_for_stop').parentElement.style.backgroundColor = "#B71C1C";
                document.getElementById('ideal_time_for_stop').parentElement.style.color = "#ffffff";
            }
            if(date1.getMinutes() === date2.getMinutes()){
                document.getElementById('ideal_time_for_stop').innerHTML = msToTime(diff);
                document.getElementById('ideal_time_for_stop').parentElement.style.backgroundColor = "#1B5E20";
                document.getElementById('ideal_time_for_stop').parentElement.style.color = "#ffffff";
            }
            if(date1 < date2){
                document.getElementById('ideal_time_for_stop').innerHTML = "- " + msToTime(diff);
                document.getElementById('ideal_time_for_stop').parentElement.style.backgroundColor = "#E65100";
                document.getElementById('ideal_time_for_stop').parentElement.style.color = "#ffffff";
            }
        }
    });

    var t = setTimeout(getTimeBeforeClockIn, 500);
}


function msToTime(duration) {
    var milliseconds = parseInt((duration%1000)/100)
        , seconds = parseInt((duration/1000)%60)
        , minutes = parseInt((duration/(1000*60))%60)
        , hours = parseInt((duration/(1000*60*60))%24);

    hours = (hours < 10) ? "0" + hours : hours;
    minutes = (minutes < 10) ? "0" + minutes : minutes;
    seconds = (seconds < 10) ? "0" + seconds : seconds;

    return hours + ":" + minutes + ":" + seconds;
}


// Get the current state of the tripmaster
function getTripState() {
    $.ajax({
        url: '/ajax/get-trip-state',
        type: 'GET',
        contentType: 'application/json',
        success: function (trip_state){
            return trip_state;
        }
    });
}


// Post the tripmaster setting
// and update the current setting with the new given value.
function updateAverageSpeed() {
    var average_speed = $("input[name='pref_speed']").val();
    console.log(average_speed);
    $.post("/ajax/update-trip-pref-avg-speed", {pref_speed: average_speed});
    /* Now we want to set the value of the pref_speed input to the new value dynamically */
    $("strong#cur_pref_avg_speed").html(average_speed + " km/u");
}


function update_pref_start_time() {
    var ideal_time = $("input[name='time']").val();
    console.log(ideal_time);
    $.post("/ajax/update-trip-ideal-start-time", {ideal_time: ideal_time});
    /* Now we want to set the value of the ideal start time input to the new value dynamically */
    $("strong#ideal_starting_time").html(ideal_time + ":00");
}


function update_pref_brightness() {
    var brightness = $("input[name='brightness']").val();
    console.log(brightness);
    $.post("/ajax/update-pref-brightness", {brightness: brightness});
}


function reset_database() {
    $.ajax({
        url: '/ajax/reset-database',
        type: 'POST',
        contentType: 'application/json',
        success: function (answer){
            console.log(answer);
        }
    });
}


/*
* In here, we will make the toggle for the driving wrong feature;
* It will contain a toggle function to start and stop the action
* but it will also contain a function to handle a blinking div.
*/
$("#wrong_traject_info").on("click", function(){

    if($(this).data("ison") === '0') {
        $(this).data("ison", '1');
        // Here make a call to the software to tell that it needs to activate the driving wrong thing
        $("#wrong_traject_info").toggleClass("orange-btn");
        Interval = setInterval(function(){$("#wrong_traject_info").toggleClass("orange-btn");}, 500);
        // Going to the correct function
        $.ajax({
            url: '/ajax/update-wrong-traject-state',
            type: 'POST',
            contentType: 'application/json',
            success: console.log("OK, started")
        });
    } else {
        $(this).data("ison", '0');
        // Here make a call to the software to tell that it needs to deactivate the driving wrong thing
        $.ajax({
            url: '/ajax/update-wrong-traject-state',
            type: 'POST',
            contentType: 'application/json',
            success: console.log("OK, stopped")
        });
        clearInterval(Interval);
        $("#wrong_traject_info").toggleClass("orange-btn");

        if($("#wrong_traject_info").hasClass('orange-btn')){
            $("#wrong_traject_info").removeClass("orange-btn");
        }
    }
    return false;
});


$('#timepicker').timepicker({
    maxHours:24,
    showSeconds: false,
    showMeridian: false,
    icons:{
        up: 'mdi mdi-chevron-up',
        down: 'mdi mdi-chevron-down'
    },
    showInputs: false,
    minuteStep: 1
});


/*
* This will contain the toggle trip js
* which means, every time you start a toggle trip,
* there will be data inserted in the database,
* when you stop the trip, it will keep displaying the information.
* when you restart the trip, it will first clear the database tables
* from the trip and then it will start counting again.
*/
$("#toggleTripA").on("click", function(){
    // console.log($(this).data());
    if($(this).data("running") === 0){
        $(this).data("running", 1);
        $(this).addClass("active_toggle_trip");
        if($(this).data("needsreset") === 1){
            // reset the trip here.
            $.post("/ajax/reset-toggle-trip", {trip: "A"});
            // alert("Trip A has been reset.");
            console.log("Trip has been reset.");
            $(this).data("needsreset", 0);
        }

        //start running the thing
        $.post("/ajax/update-toggle-trip-state", {trip:"A", state:"1"});
        // get data
        getToggleTripDistance('A', "start");
        console.log("Trip started");

        // alert("Trip A is running.");
    }else {
        $(this).data("running", 0);
        $(this).data("needsreset", 1);
        // alert("Trip A is stopped.");
        // Stop the trip
        $.post("/ajax/update-toggle-trip-state", {trip:"A", state:"0"});
        // stop the loading of the js
        getToggleTripDistance('A', "stop");
        console.log("Trip stopped");
        $(this).removeClass("active_toggle_trip");
    }
    return false;
});

function getToggleTripDistance(trip, type) {
    $.ajax({
        url: '/ajax/get-toggle-trip-distance/' + trip,
        type: 'GET',
        contentType: 'application/json',
        success: function (trip_dist){
            if(type === "start" && trip === "A"){
                Interval = setInterval(function(){$("#toggle_trip_a_info").html(trip_dist+" km");}, 500);
            }else if(type === "start" && trip === "B")  {
                Interval = setInterval(function(){$("#toggle_trip_b_info").html(trip_dist+" km");}, 500);
            }else {
                clearInterval(Interval);
            }
        }
    });
}


$("#toggleTripB").on("click", function(){
    // console.log($(this).data());
    if($(this).data("running") === 0){
        $(this).data("running", 1);
        $(this).addClass("active_toggle_trip");
        if($(this).data("needsreset") === 1){
            // reset the trip here.
            $.post("/ajax/reset-toggle-trip", {trip: "B"});
            // alert("Trip A has been reset.");
            console.log("Trip has been reset.");
            $(this).data("needsreset", 0);
        }

        //start running the thing
        $.post("/ajax/update-toggle-trip-state", {trip:"B", state:"1"});
        // get data
        getToggleTripDistance('B', "start");
        console.log("Trip started");

        // alert("Trip A is running.");
    }else {
        $(this).data("running", 0);
        $(this).data("needsreset", 1);
        // alert("Trip A is stopped.");
        // Stop the trip
        $.post("/ajax/update-toggle-trip-state", {trip:"B", state:"0"});
        // stop the loading of the js
        getToggleTripDistance('B', "stop");
        $(this).removeClass("active_toggle_trip");
        console.log("Trip stopped");
    }
    return false;
});


/*
* Here we start all the functions, on every page. Not every pages
* uses the functions, but it is to be sure everything works just fine.
 */
// Start the timer :D
clock();
// Get the speed every 1 second.
getSpeed();
// Get the total distance every 1 second.
getDistance();
// Get the average speed every 1 second.
getAvgSpeed();
// Get the ideal stop time every 0.5 seconds.
getIdealStopTime();
// Get the time before you have to clock in every one second.
getTimeBeforeClockIn();
// Get the total distance you drove wrong
getWrongDistance();