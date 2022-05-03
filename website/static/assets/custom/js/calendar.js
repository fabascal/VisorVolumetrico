document.addEventListener('DOMContentLoaded', function() {
var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    aspectRatio : 2,
    locale : 'es',
    select : true,
    events : events,
    headerToolbar: {
        left :'',
        center: 'title'
      },
      buttonText: { today: "Hoy" },
      views:{
        titleFormat: 'MMMM YYYY' 
      },
      dateClick: function(info) {
        alert('clicked ' + info.dateStr);
      },
      customButtons: {
        prev: {
          text: 'Prev',
          click: function() {
            // so something before
            alert(calendar.getDate().getMonth() + 1)
            // do the original command
            calendar.prev();
            // do something after
            alert(calendar.getDate().getMonth() + 1)
          }
        },
        next: {
          text: 'Next',
          click: function() {
            // so something before
            alert(calendar.getDate().getMonth() + 1)
            // do the original command
            calendar.next();
            // do something after
            alert(calendar.getDate().getMonth() + 1)
          }
        },
      }
});
calendar.render();
});



