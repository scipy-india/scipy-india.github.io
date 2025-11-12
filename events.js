class EventManager {
  constructor() {
    this.upcomingContainer = document.getElementById("upcoming-events");
    this.pastContainer = document.getElementById("past-events");

    // Only load events if containers exist
    if (this.upcomingContainer && this.pastContainer) {
      this.loadEvents();
    }
  }

  async loadEvents() {
    try {
      const response = await fetch("event_details.json");
      if (!response.ok) throw new Error("Failed to load events");
      const events = await response.json();
      this.renderEvents(events);
    } catch (error) {
      console.error("Error loading events:", error);
      this.renderError();
    }
  }

  renderEvents(events) {
    const today = new Date();
    const upcomingEvents = [];
    const pastEvents = [];

    events.forEach((event) => {
      if (event.date === "Coming soon!") {
        upcomingEvents.push(event);
      } else {
        const eventDate = new Date(event.date);
        if (eventDate > today) {
          upcomingEvents.push(event);
        } else {
          pastEvents.push(event);
        }
      }
    });

    this.renderEventList(this.upcomingContainer, upcomingEvents);
    this.renderEventList(this.pastContainer, pastEvents);

    // Show message if no events
    if (upcomingEvents.length === 0) {
      this.renderNoEvents(
        this.upcomingContainer,
        "No upcoming events at the moment."
      );
    }
    if (pastEvents.length === 0) {
      this.renderNoEvents(this.pastContainer, "No past events yet.");
    }
  }

  renderEventList(container, events) {
    while (container.firstChild) {
      container.removeChild(container.firstChild);
    }

    events.forEach((event) => {
      const eventCard = this.createEventCard(event);
      container.appendChild(eventCard);
    });
  }

  createEventCard(event) {
    const card = document.createElement("div");
    card.className = "event-card";

    const title = document.createElement("h3");
    title.className = "event-title";
    title.textContent = event.title;
    card.appendChild(title);

    const details = document.createElement("div");
    details.className = "event-details";

    // Date details
    const dateDetail = document.createElement("div");
    dateDetail.className = "event-detail";
    const dateIcon = document.createElement("span");
    dateIcon.className = "icon icon-calendar";
    const dateText = document.createElement("span");
    dateText.textContent = `${event.date}${event.day ? ` (${event.day})` : ""}`;
    dateDetail.appendChild(dateIcon);
    dateDetail.appendChild(dateText);
    details.appendChild(dateDetail);

    // Time details
    if (event.time && event.time !== "Coming soon!") {
      const timeDetail = document.createElement("div");
      timeDetail.className = "event-detail";
      const timeIcon = document.createElement("span");
      timeIcon.className = "icon icon-clock";
      const timeText = document.createElement("span");
      timeText.textContent = event.time;
      timeDetail.appendChild(timeIcon);
      timeDetail.appendChild(timeText);
      details.appendChild(timeDetail);
    }

    // Location details
    const locationDetail = document.createElement("div");
    locationDetail.className = "event-detail";
    const locationIcon = document.createElement("span");
    locationIcon.className = "icon icon-location";
    const locationText = document.createElement("span");
    locationText.textContent = event.location;
    locationDetail.appendChild(locationIcon);
    locationDetail.appendChild(locationText);
    details.appendChild(locationDetail);

    card.appendChild(details);

    // Actions
    const today = new Date();
    const eventDate =
      event.date === "Coming soon!"
        ? new Date(9999, 11, 31)
        : new Date(event.date);
    const isPastEvent = eventDate < today;

    const hasActions = this.shouldShowActions(event, isPastEvent);

    if (hasActions) {
      const actions = document.createElement("div");
      actions.className = "event-actions";

      // For past events, we show a livestream if a link to it is available.
      if (isPastEvent) {
        if (event.livestream_link && event.livestream_link.trim() !== "") {
          const livestreamLink = document.createElement("a");
          livestreamLink.href = event.livestream_link;
          livestreamLink.className = "btn btn-primary";
          livestreamLink.textContent = "Watch livestream";
          livestreamLink.target = "_blank";
          livestreamLink.rel = "noopener";
          actions.appendChild(livestreamLink);
        }
      } else {
        if (event.cfp_link && event.cfp_link.trim() !== "") {
          const cfpLink = document.createElement("a");
          cfpLink.href = event.cfp_link;
          cfpLink.className = "btn btn-primary";
          cfpLink.textContent = "Submit a proposal";
          cfpLink.target = "_blank";
          cfpLink.rel = "noopener";
          actions.appendChild(cfpLink);
        }

        if (event.rsvp_link && event.rsvp_link.trim() !== "") {
          const rsvpLink = document.createElement("a");
          rsvpLink.href = event.rsvp_link;
          rsvpLink.className = "btn btn-secondary";
          rsvpLink.textContent = "RSVP now";
          rsvpLink.target = "_blank";
          rsvpLink.rel = "noopener";
          actions.appendChild(rsvpLink);
        }
      }

      if (actions.children.length > 0) {
        card.appendChild(actions);
      }
    }

    return card;
  }

  shouldShowActions(event, isPastEvent) {
    if (isPastEvent) {
      return event.livestream_link && event.livestream_link.trim() !== "";
    } else {
      return (
        (event.cfp_link && event.cfp_link.trim() !== "") ||
        (event.rsvp_link && event.rsvp_link.trim() !== "")
      );
    }
  }

  renderNoEvents(container, message) {
    while (container.firstChild) {
      container.removeChild(container.firstChild);
    }
    const messageDiv = document.createElement("div");
    messageDiv.className = "no-events";

    const icon = document.createElement("div");
    icon.className = "no-events-icon";
    icon.textContent = "📅";

    const text = document.createElement("div");
    text.textContent = message;

    messageDiv.appendChild(icon);
    messageDiv.appendChild(text);
    container.appendChild(messageDiv);
  }

  renderError() {
    const errorMessage = "Unable to load events. Please try again later.";
    this.renderNoEvents(this.upcomingContainer, errorMessage);
    this.renderNoEvents(this.pastContainer, errorMessage);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  new EventManager();
});
