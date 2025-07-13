//TREND
document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const tab = params.get("tab");

    const tabMap = {
      "north-america": "#1a",
      "south-america": "#2a",
      "europe": "#3a",
      "asia": "#4a",
      "africa": "#5a",
      "australia": "#6a",
      "antartica": "#7a"
    };

    if (tab && tabMap[tab]) {
      const targetTabLink = document.querySelector(`a[href="${tabMap[tab]}"]`);
      if (targetTabLink) {
        $(targetTabLink).tab('show');
      }
    }
  });