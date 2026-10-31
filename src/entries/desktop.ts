/** Desktop host selection shares the full application and UI. */
import {startWeb} from './web.js';
import {createDesktopSettings} from '../platform/desktop/host.js';
startWeb(createDesktopSettings());
