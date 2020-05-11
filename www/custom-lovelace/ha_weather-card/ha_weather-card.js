class HAWeatherCard extends Polymer.Element {

  static get template() {
    return Polymer.html`
      <style>
        :root {
          --main-bg-color: linear-gradient(to bottom,#03a9f4,#68d0ff);
          --main-title-color: white;
          --ch-highlight-color: #03a9f4;
          --cell-title-color: #515151;
          --cell-date-color: #aaa;
        }
        .card {
          padding: 0 18px 18px 18px;
        }
        .header div {
          display: flex;
        }        
        .container {
          background: var(--main-bg-color);
        }
        .title {
          color: var(--main-title-color);
          font-size: 30px;
          text-align: center;
          padding-top: 50px;
          padding-bottom: 8px;
        }
        .sub_title {
          color: var(--main-title-color);
          font-size: 14px;
          text-align: center;
          padding-bottom: 30px;
        }

        .temperature {
          color: var(--main-title-color);
          font-size: 60px;
          text-align: center;
          padding-bottom: 50px;
        }
        .hourly {
          white-space: nowrap;
          overflow-x: scroll;
        }
        .hourly_item {
          color: var(--main-title-color);          
          text-align: center;
          display: inline-block;
          padding-left: 10px;
        }
        .daily {
          white-space: nowrap;
          overflow-x: scroll;
        }
        .daily_item {
          color: var(--main-title-color);          
          text-align: center;
          display: inline-block;
          padding-left: 10px;
        }        
      </style>
      <ha-card>
        <div class="container">
          <div style="align-items: baseline;">
            <div class="title">北京市朝阳区</div>
            <div class="sub_title">{{condition}}</div>
            <div class="temperature">{{temperature}}</div>

            <div class="hourly">
              <template is="dom-repeat" items="{{hourlyList}}">
                  <div class="hourly_item">
                    <div>{{item.date}}</div>
                    <div>{{item.condition}}</div>
                    <div>{{item.temperature}}</div>
                    <div>降水概率{{item.probability}}</div>
                  </div>
              </template>            
            </div>
            <div class="daily">
              <template is="dom-repeat" items="{{dailyList}}">
                  <div class="daily_item">
                    <div>{{item.date}}</div>
                    <div>{{item.max}}</div>
                    <div>{{item.min}}</div>
                    <div>{{item.day}}</div>
                    <div>{{item.night}}</div>
                  </div>
              </template>            
            </div> 

          </div>
        </div>

      </ha-card>
    `;
  }

  static get properties() {

    return {
      config: Object,
      calendarEntity: {
        type: Object,
        observer: 'dataChanged',
      },
    };
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('Please define "calendar" entity in the card config');
    }
    this.config = config;
   }

  constructor() {
    super();

  }

  set hass(hass) {
    this._hass = hass;
    // this.lang = this._hass.selectedLanguage || this._hass.language;
    this.weatherEntity = this.config.entity in hass.states ? hass.states[this.config.entity] : null;

    var attributes = this.weatherEntity.attributes;

    this.temperature = attributes['now']['temperature'];
    this.condition = attributes['now']['condition'];
    this.hourlyList = attributes['hourlys'];
    this.dailyList = attributes['dailys'];
  }

  dataChanged() {
    // this.HourlyForecastChartData = this.drawChart('hourly', this.hourlyForecast);
    // this.DailyForecastChartData = this.drawChart('daily', this.dailyForecast);
  }


  getIcon(index) {
    return `${
      this.config.icons
    }${
      index
    }.png`;
  }

}


customElements.define('ha_weather-card', HAWeatherCard);
