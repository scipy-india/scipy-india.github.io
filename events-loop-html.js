fetch('event_details.json')
  .then(response => response.json())
  .then(events => {
    const main = document.querySelector('main');
    
    const upcomingEventsSection = main.querySelector('#upcoming_events');
    const pastEventsSection = main.querySelector('#past_events');
    

    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = today.toLocaleString('en-US', { month: 'short' });
    const year = today.getFullYear();
    const todayStr = `${day}-${month}-${year}`;
    // Output: "17-Sep-2025"


    let pastEventsString = "";
    let upcomingEventsString = "";

    events.forEach(event => {
      
      const eventDate = new Date(event.date);
      
      if (today > eventDate) { // Past events:
        pastEventsString += `
          <div class="meetup-card">
            <h3><a href="#">${event.title}</a></h3>
            <p><strong>Date: </strong> ${event.date} (${event.day})<br>
            <strong>Time: </strong>${event.time}<br>
            <strong>Place: </strong>${event.location}</p>
            <p>
              <a href="${event.cfp_link}" target="_blank">Submit a talk here</a> | 
              <a href="${event.rsvp_link}" target="_blank">RSVP now!</a>
            </p>
          </div>
          <br>
        `;
      } else { // Upcoming events:
        upcomingEventsString += `
          <div class="meetup-card">
            <h3><a href="#">${event.title}</a></h3>
            <p><strong>Date: </strong> ${event.date} (${event.day})<br>
            <strong>Time: </strong>${event.time}<br>
            <strong>Place: </strong>${event.location}</p>
            <p>
              <a href="${event.cfp_link}" target="_blank">Submit a talk here</a> | 
              <a href="${event.rsvp_link}" target="_blank">RSVP now!</a>
            </p>
          </div>
          <br>
        `;
      }
    });

    pastEventsSection.innerHTML = pastEventsString;
    upcomingEventsSection.innerHTML = upcomingEventsString;
  });
