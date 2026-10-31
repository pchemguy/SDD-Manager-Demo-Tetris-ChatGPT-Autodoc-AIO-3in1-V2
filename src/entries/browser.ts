/** Browser-only host selection. */
import {startWeb} from './web.js';
import {BrowserSettings} from '../platform/browser/settings.js';
startWeb(new BrowserSettings());
