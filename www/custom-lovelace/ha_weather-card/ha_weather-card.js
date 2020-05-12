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
        ha-icon {
          color: var(--main-title-color);
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
        .attributes {
          width: 50%;
          cursor: pointer;
          justify-content: space-between;
          align-items: center;
          color: var(--main-title-color);          
          margin: 5px 0px 5px 0px;
        }
        .attributes div{
          display: flex;
        }
        .attributes div div{
          width: 50%;
          margin: 5px 5px 0px 5px;
          align-items: center;
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
            <div class="sub_title"> aqi:{{aqi}} pm25:{{pm25}} {{condition}}</div>
            <div class="temperature">{{temperature}}</div>

            <div> {{minutely_description}} <br> {{hourly_description}} </div>

            <div class="attributes">
              <div on-click="_weatherAttr">
                <div>
                  <ha-icon icon="hass:water-percent"></ha-icon>&nbsp;[[humidity]] %
                </div>
                <div>
                  <ha-icon icon="hass:gauge"></ha-icon>&nbsp;[[pressure]] hPa
                </div>
              </div>
              <div on-click="_weatherAttr">
                <div>
                  <ha-icon icon="hass:[[getWindDirIcon(wind_degree)]]"></ha-icon>&nbsp;[[wind_direction]]
                </div>
                <div>
                  <ha-icon icon="hass:weather-windy"></ha-icon>&nbsp;[[wind_speed]] km/h
                </div>
              </div>
            </div>


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
      weatherEntity: {
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
    this.cardinalDirectionsIcon = [
      'mdi:arrow-down', 'mdi:arrow-bottom-left', 'mdi:arrow-left',
      'mdi:arrow-top-left', 'mdi:arrow-up', 'mdi:arrow-top-right',
      'mdi:arrow-right', 'mdi:arrow-bottom-right', 'mdi:arrow-down'
    ];
  }

  set hass(hass) {
    this._hass = hass;
    // this.lang = this._hass.selectedLanguage || this._hass.language;
    this.weatherEntity = this.config.entity in hass.states ? hass.states[this.config.entity] : null;
  }

  dataChanged() {
    var attributes = this.weatherEntity.attributes;
    
    this.aqi = attributes['now']['aqi'];
    this.pm25 = attributes['now']['pm25'];

    this.description = attributes['description'];
    this.minutely_description = attributes['minutely_description'];
    this.hourly_description = attributes['hourly_description'];
    this.humidity = Math.round(attributes['now']['humidity']);
    this.pressure = Math.round(attributes['now']['pressure']);
    this.wind_speed = Math.round(attributes['now']['wind_speed']);
    this.wind_degree = attributes['now']['wind_degree'];
    this.wind_direction = attributes['now']['wind_direction'];

    this.temperature = attributes['now']['temperature'];
    this.condition = attributes['now']['condition'];
    this.hourlyList = attributes['hourlys'];
    this.dailyList = attributes['dailys'];
  }


  getIcon(index) {
    return `${
      this.config.icons
    }${
      index
    }.png`;
  }

  getWindDirIcon(degree) {
    return this.cardinalDirectionsIcon[parseInt((degree + 22.5) / 45.0)];
  }
  
  _fire(type, detail, options) {
    const node = this.shadowRoot;
    options = options || {};
    detail = (detail === null || detail === undefined) ? {} : detail;
    const e = new Event(type, {
      bubbles: options.bubbles === undefined ? true : options.bubbles,
      cancelable: Boolean(options.cancelable),
      composed: options.composed === undefined ? true : options.composed
    });
    e.detail = detail;
    node.dispatchEvent(e);
    return e;
  }
  _weatherAttr() {
    this._fire('hass-more-info', { entityId: this.config.entity });
  }
}


customElements.define('ha_weather-card', HAWeatherCard);
