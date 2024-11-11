async function getWeather() {
    const city = document.getElementById("city-input").value;
    if (!city) {
        alert("Please enter a city name.");
        return;
    }

    const response = await fetch(`http://192.168.31.16:8000/weather/api/weather?city_str=${city}`);
    if (!response.ok) {
        document.getElementById("weather-now").innerHTML = "<p>City not found or API error.</p>";
        document.getElementById("forecast").innerHTML = "";
        return;
    }

    const data = await response.json();

    // Отображение текущей погоды
    const weatherNow = data.weather_now[0];
    const mainNow = data.weather_now_main;
    const windNow = data.weather_now_wind;

    document.getElementById("weather-now").innerHTML = `
        <h3>Current Weather in ${city}</h3>
        <p><strong>Temperature:</strong> ${mainNow.temp} °C</p>
        <p><strong>Feels Like:</strong> ${mainNow.feels_like} °C</p>
        <p><strong>Condition:</strong> ${weatherNow.description}</p>
        <p><strong>Wind Speed:</strong> ${windNow.speed} m/s</p>
    `;

    // Отображение прогноза на 5 дней
    const forecastContainer = document.getElementById("forecast");
    forecastContainer.innerHTML = "";  // Очистка предыдущих данных

    for (let i = 1; i <= 5; i++) {
        const day = data.day_list[`${i}_day`];
        const dayWeather = day.weather[0];
        const dayMain = day.main;
        const dayWind = day.wind;

        const forecastCard = document.createElement("div");
        forecastCard.className = "weather-card";
        forecastCard.innerHTML = `
            <h3>Day ${i}</h3>
            <p><strong>Temperature:</strong> ${dayMain.temp} °C</p>
            <p><strong>Feels Like:</strong> ${dayMain.feels_like} °C</p>
            <p><strong>Condition:</strong> ${dayWeather.description}</p>
            <p><strong>Wind Speed:</strong> ${dayWind.speed} m/s</p>
        `;
        forecastContainer.appendChild(forecastCard);
    }
}
