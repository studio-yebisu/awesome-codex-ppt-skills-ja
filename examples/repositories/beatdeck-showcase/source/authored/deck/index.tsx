import {defineDeck} from 'beatdeck';
import '../themes/neutral.css';
import '../themes/light.css';
import './theme-brand.css';
import {config} from './deck.config';
import {SCENES} from './scenes';
import {initialLive,timeline,type Live} from './timeline';
import {World} from './World';
import {Opening,Materials,DoughScene,Baking,Shop,Handoff} from './SceneLayers';
import {CatalogBridge} from './CatalogBridge';
function Stage(){return <><World/><Opening/><Materials/><DoughScene/><Baking/><Shop/><Handoff/><CatalogBridge/></>;}
export default defineDeck<Live>({id:'bread-stage',title:config.title,lang:'ja',scenes:SCENES,Stage,initialLive,timeline,
 fonts:['400 140px "BreadDisplay"','400 34px "BreadBody"','700 34px "BreadBody"','500 32px "BreadNumber"']});
