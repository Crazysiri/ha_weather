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
          margin: 0px 0px 0px 25px;
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
          font-size: 15px;          
          color: var(--main-title-color);          
          padding: 20px 0px 10px;
          text-align: center;          
        } 
        .detail {
          font-size: 15px;          
          color: var(--main-title-color);          
          padding: 7px 20px 8px;
        }             
        .daily_hourly {
          white-space: nowrap;
          overflow-x: scroll;
          display: flex;
          justify-content: space-between;  
          padding-top: 10px;                        
        }
        .daily_hourly::-webkit-scrollbar {
          display: none;
        }
        .hourly_item {
          color: var(--main-title-color);          
          text-align: center;
          padding-left: 15px;
          padding-right: 5px;
          display: flex;
          justify-content: space-between;                
          flex-direction: column;
        }

        .daily_item {
          color: var(--main-title-color);          
          text-align: center;
          padding-left: 15px;
          padding-right: 5px;
          display: flex;
          justify-content: space-between;                
          flex-direction: column;
        }    

        .line {
          background-color:rgba(255,255,255,0.3);
          height: 0.5px;
          margin: 0px 10px 0px 10px;
        } 

        .icon {
          width: 70px;
          height: 70px;
          margin-left: -20px;
        } 
        .icon_small {
          width: 55px;
          height: 55px;
          margin-left: 0px;
        }                   
      </style>
      <ha-card>
        <div class="container">
          <div style="align-items: baseline;">
            <div class="title">{{city}}市{{area}}区</div>
            <div class='header'>
              <div style="align-items: center;">
                <div class$ = "aqi [[aqiLevel(aqi)]]">[[aqi]]</div>
                <i class="icon" style="background: none, url([[getWeatherIcon(condition)]]) no-repeat; background-size: contain;"></i>              
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
            <div style='margin-top:30px;' class='line'></div>
            <div class="daily_hourly">
              <template is="dom-repeat" items="{{hourlyList}}">
                  <div class="hourly_item">
                    <div style='font-size: 15px;margin:0px 0px 12px 0px'>{{item.time}}</div>
                    <i class="icon_small" style="background: none, url([[getWeatherIcon(item.condition)]]) no-repeat; background-size: contain;"></i>                                  
                    <template is="dom-if" if="[[item.is_probability]]">
                      <div style='font-size: 10px;margin:0px 0px 10px 0px'>降水概率{{item.probability}}%</div>
                    </template>  
                    <div style='font-size: 17px;margin:0px 0px 10px 0px'>{{item.temperature}}</div>                                        
                  </div>
              </template>            
            </div>
            <div style='margin-top:30px;'></div>  
            <div class='description'> {{hourly_description}}</div>                                            
            <div class="daily_hourly">
              <template is="dom-repeat" items="{{dailyList}}">
                  <div class="daily_item">
                    <div style='font-size: 15px;margin:0px 0px 8px 0px'>{{item.week_description}}</div>                  
                    <div style='font-size: 15px;margin:0px 0px 12px 0px'>{{item.date_description}}</div>
                    <template is="dom-if" if="[[condition_is_equal(item.day,item.night)]]">
                      <i class="icon_small" style="background: none, url([[getWeatherIcon(item.day)]]) no-repeat; background-size: contain;"></i>                                  
                    </template>
                    <template is="dom-if" if="[[!condition_is_equal(item.day,item.night)]]">
                      <i class="icon_small" style="background: none, url([[getWeatherIcon(item.day)]]) no-repeat; background-size: contain;"></i>                                  
                      <i class="icon_small" style="background: none, url([[getWeatherIcon(item.night)]]) no-repeat; background-size: contain;"></i>                                  
                    </template>                    
                    <div style='font-size: 17px;margin:0px 0px 10px 0px'>{{temperature_round(item.min,item.max)}}</div>
                  </div>
              </template>            
            </div> 
            <div class='line'></div>      
            <div class='detail'><div style='font-size: 12px;'>pm2.5</div><br><div style='font-size: 25px;margin-top:-15px;'>[[pm25]]</div></div>                  
            <div class='line'></div>      
            <div class='line'></div>
            <div class='detail'><div style='font-size: 12px;'>pm10</div><br><div style='font-size: 25px;margin-top:-15px;'>[[pm10]]</div></div>                  
            <div class='line'></div>  
            <div class='line'></div>
            <div class='detail'><div style='font-size: 12px;'>舒适指数</div><br><div style='font-size: 25px;margin-top:-15px;'>[[index]]</div></div>                  
            <div class='line'></div>  
            <div class='line'></div>
            <div class='detail'><div style='font-size: 12px;'>舒适度</div><br><div style='font-size: 25px;margin-top:-15px;'>[[comfort]]</div></div>                  
            <div class='line'></div>              
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
    this.weatherIcons = {
      'sunny': 'day',
      'sunny_night': 'night',
      'cloudy': 'cloudy',
      'fog': 'cloudy',
      'hail': 'rainy-7',
      'lightning': 'thunder',
      'lightning-rainy': 'thunder',
      'partlycloudy': 'cloudy-day-3',
      'partlycloudy_night': 'cloudy-night-3',
      'pouring': 'rainy-6',
      'rainy': 'rainy-5',
      'snowy': 'snowy-6',
      'snowy-rainy': 'rainy-7',
      'sunny': 'day',
      'windy': 'cloudy',
      'windy-variant': 'cloudy-day-3',
      exceptional: '!!'
    };  
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
    this.pm10 = attributes['now']['pm10'];
    this.city = attributes['now']['city'];
    this.area = attributes['now']['area'];
    this.index = attributes['now']['index'];
    this.comfort = attributes['now']['comfort'];
    this.update_time = attributes['update_time'];

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


  getWeatherIcon(condition) {
    return `${
      this.config.icons
        ? this.config.icons
        : "https://cdn.jsdelivr.net/gh/bramkragten/custom-ui@master/weather-card/icons/animated/"
    }${
        this.weatherIcons[condition]
    }.svg`;
  }

  getWindDirIcon(degree) {
    return this.cardinalDirectionsIcon[parseInt((degree + 22.5) / 45.0)];
  }

  aqiLevel(aqi) {
    return 'aqi_level_'+parseInt(aqi / 50.0)+'_bg';
  }  

  //结合早晚的天气 如果一样的话
  condition_is_equal(day,night) {

    if (day == night) {
      return true;
    }
    return false;
  }

  //最低最高气温
  temperature_round(min,max) {

    return Math.round(min) + '/' + Math.round(max);
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
