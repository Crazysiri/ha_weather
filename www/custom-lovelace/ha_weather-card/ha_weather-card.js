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
        .header {
          color: var(--main-title-color);          
          font-family: var(--paper-font-headline_-_font-family);
          -webkit-font-smoothing: var(
            --paper-font-headline_-_-webkit-font-smoothing
          );
          font-size: 15px;
          font-weight: var(--paper-font-headline_-_font-weight);
          letter-spacing: var(--paper-font-headline_-_letter-spacing);
          line-height: var(--paper-font-headline_-_line-height);
          text-rendering: var(
            --paper-font-common-expensive-kerning_-_text-rendering
          );
          opacity: var(--dark-primary-opacity);
          display: flex;
          justify-content: center;
          align-content: center;
        }
        .header div {
          display: flex;
          margin-right: 10px;
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
        .temperature {
          color: var(--main-title-color);
          font-size: 60px;
          text-align: center;
          padding-bottom: 50px;
          padding-top: 30px;

        }
        .aqi,
        .alarm {
          font-size: 16px;
          border-radius: 3px;
          color: #fff;
          line-height: 20px;
          padding: 2px 5px 2px 5px;
          margin: 0px 0px 0px 10px;
          height: 20px;
        }        
        .aqi_level_0_bg {
          background-color: #40c057;
        }
        .aqi_level_1_bg{
          background-color: #82c91e;
        }
        .aqi_level_2_bg {
          background-color: #f76707;
        }
        .aqi_level_3_bg {
          background-color: #e03131;
        }
        .aqi_level_4_bg {
          background-color: #841c3c;
        }
        .aqi_level_5_bg{
          background-color: #540822;
        }        
        .attributes {
          cursor: pointer;
          justify-content: center;
          align-items: center;
          color: var(--main-title-color);          
          display: flex;
          margin-left: 15px;  
        }
        .attributes div{
          width: 30%;  
        }
        .attributes div div{
          width: 90%;
          align-items: center;
        }

        .description {
          font-size: 17px;          
          color: var(--main-title-color);          
          padding: 75px 0px 15px;
          text-align: center;          
        }     
        .daily_hourly {
          white-space: nowrap;
          overflow-x: scroll;
          margin:10px 0x;
        }
        .daily_hourly::-webkit-scrollbar {
          display: none;
        }
        .hourly_item {
          color: var(--main-title-color);          
          text-align: center;
          display: inline-block;
          padding-left: 15px;
          padding-right: 5px;

        }

        .daily_item {
          color: var(--main-title-color);          
          text-align: center;
          display: inline-block;
          padding-left: 20px;
        }        
      </style>
      <ha-card>
        <div class="container">
          <div style="align-items: baseline;">

            <div class="title">北京市朝阳区</div>
            <div class='header'>
              <div style="align-items: center;">
                <div class$ = "aqi [[aqiLevel(aqi)]]">[[aqi]]</div>
                [[condition]]
              </div>
            </div>
            <div class="temperature">{{temperature}}</div>

            <div class='attributes'>          
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

            <div class='description'> {{minutely_description}}</div>
            <div class="daily_hourly">
              <template is="dom-repeat" items="{{hourlyList}}">
                  <div class="hourly_item">
                    <div style='font-size: 15px;margin:0px 0px 12px 0px'>{{item.time}}</div>
                    <div style='font-size: 15px;margin:0px 0px 8px 0px'>{{item.condition}}</div>
                    <div style='font-size: 17px;margin:0px 0px 10px 0px'>{{item.temperature}}</div>
                    <template is="dom-if" if="[[item.is_probability]]">
                      <div style='font-size: 10px;margin:0px 0px 6px 0px'>降水概率{{item.probability}}%</div>
                    </template>                      
                  </div>
              </template>            
            </div>
            <div class='description'> {{hourly_description}}</div>                            
            <div class="daily_hourly">
              <template is="dom-repeat" items="{{dailyList}}">
                  <div class="daily_item">
                    <div style='font-size: 15px;margin:0px 0px 12px 0px'>{{item.week_description}}</div>                  
                    <div style='font-size: 15px;margin:0px 0px 8px 0px'>{{item.date_description}}</div>
                    <div style='font-size: 17px;margin:0px 0px 10px 0px'>{{item.min}}/{{item.max}}</div>
                    <div style='font-size: 15px;margin:0px 0px 6px 0px'>{{item.day}}</div>
                    <div style='font-size: 10px;margin:0px 0px 6px 0px'>{{item.night}}</div>
                  </div>
              </template>            
            </div> 
            <div>
              <div>
                pm2.5: [[pm25]]
              </div>
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

  aqiLevel(aqi) {
    return 'aqi_level_'+parseInt(aqi / 50.0)+'_bg';
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
