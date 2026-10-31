/** Electron supplies a persistent secure app origin; renderer uses standard web ports. */
import {BrowserSettings,browserSettingsHost} from '../browser/settings.js';
export function createDesktopSettings():BrowserSettings{return new BrowserSettings(browserSettingsHost);}
